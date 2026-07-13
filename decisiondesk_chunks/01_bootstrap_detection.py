import json
import os
import re
import shutil
import zipfile
from datetime import datetime
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None

try:
    from sqlalchemy import create_engine, text
    from sqlalchemy.pool import NullPool
except Exception:
    create_engine = None
    text = None
    NullPool = None

if load_dotenv is not None:
    load_dotenv()

from core.sql_query_engine import run_sql_query
from agents.query_agent import ask_query_agent
from core.data_loader import load_all_data


@st.cache_data(ttl=600, show_spinner="Loading company Excel data...")
def load_cached_company_data():
    """Load static Excel company data once per session window.

    This avoids re-reading every Excel sheet on each Streamlit rerun.
    Proposal/client/delivery workflow data still comes from Supabase.
    """
    return load_all_data()
# from core.calculations import calculate_lop
from core.calculations import calculate_lop, calculate_salary_after_lop
# from core.receptionist import receptionist_route
from core.receptionist import receptionist_understand
from agents.workflow import (
    run_new_project_proposal_workflow,
    run_company_health_workflow,
)
from core.report_generator import generate_proposal_report
from llm_client import ask_llm

DB_PATH = "db/virtual_company_db_final.xlsx"
# For hosted product reliability, proposal workflow writes should go to Supabase/PostgreSQL.
# Excel remains the seed database for static company data such as users, employees, payroll, etc.
REQUIRE_SUPABASE_FOR_PROPOSALS = True

# Lightweight operating mode: Excel is used for static company data. Supabase is used
# only for dynamic workflow inserts/updates. Expensive schema repair and long LLM
# generations are opt-in so normal clicks stay fast.
LIGHTWEIGHT_FAST_MODE = os.getenv("DD_LIGHTWEIGHT_FAST_MODE", "1").strip().lower() not in ["0", "false", "no"]
AUTO_SCHEMA_CHECK = os.getenv("DD_AUTO_SCHEMA_CHECK", "0").strip().lower() in ["1", "true", "yes"]
USE_LLM_FOR_LONG_DOCUMENTS = os.getenv("DD_USE_LLM_LONG_OUTPUTS", "0").strip().lower() in ["1", "true", "yes"]
POSTGRES_CONNECT_TIMEOUT_SECONDS = int(os.getenv("DD_POSTGRES_CONNECT_TIMEOUT", "2"))
POSTGRES_READ_CACHE_TTL_SECONDS = int(os.getenv("DD_POSTGRES_READ_CACHE_TTL", "240"))
POSTGRES_STATEMENT_TIMEOUT_MS = int(os.getenv("DD_POSTGRES_STATEMENT_TIMEOUT_MS", "9000"))

# Keep dashboard reads small and cached so product actions stay responsive.
# Increase with DD_DASHBOARD_ROW_LIMIT only if you need older history.
DASHBOARD_ROW_LIMIT = int(os.getenv("DD_DASHBOARD_ROW_LIMIT", "12"))
DYNAMIC_CAPACITY_CACHE_TTL_SECONDS = int(os.getenv("DD_DYNAMIC_CAPACITY_CACHE_TTL", "90"))


# ---------------- LOGIN ----------------

@st.cache_data(ttl=600, show_spinner=False)
def load_cached_users_sheet():
    """Login uses the Excel seed DB, cached for speed."""
    return pd.read_excel(DB_PATH, sheet_name="Users")


def login(user_id: str, secret_key: str):
    users = load_cached_users_sheet()

    match = users[
        (users["user_id"].astype(str).str.upper() == str(user_id).upper())
        & (users["secret_key"].astype(str) == str(secret_key))
    ]

    if match.empty:
        return None

    return match.iloc[0].to_dict()


# ---------------- DETECTION HELPERS ----------------

def detect_lead_id(query):
    q = query.upper()

    for lead_id in ["L001", "L002", "L003"]:
        if lead_id in q:
            return lead_id

    q_lower = query.lower()

    if "retailmax" in q_lower or "retail" in q_lower:
        return "L001"
    if "insurepro" in q_lower or "insurance" in q_lower:
        return "L002"
    if "edusmart" in q_lower or "education" in q_lower:
        return "L003"

    return None


def is_project_proposal_query(query):
    q = query.lower()

    keywords = [
        "lead",
        "project proposal",
        "new project",
        "new client",
        "proposal",
        "deal",
        "should we accept",
        "accept it",
        "reject it",
        "quote",
        "pricing",
        "client wants",
        "chatbot",
        "ai assistant",
        "virtual assistant",
        "employee assistant",
        "assistant for internal employees",
        "internal employees",
        "automation",
        "data pipeline",
        "pipeline",
        "data engineering",
        "etl",
        "data platform",
    ]

    return any(k in q for k in keywords)




def is_company_performance_query(query):
    """Detect internal company performance/report requests so they are never treated as client proposals."""
    q = query.lower().strip()
    patterns = [
        "company performance",
        "company report",
        "performance report",
        "company health",
        "business performance",
        "business report",
        "company status",
        "company summary",
        "internal report",
        "management report",
    ]
    return any(pattern in q for pattern in patterns)


def is_complete_client_proposal(query):
    """A client proposal is complete only when requirement, budget, timeline, company, and contact are present."""
    return not is_company_performance_query(query) and len(missing_client_proposal_fields(query)) == 0

def extract_budget(query):
    q = query.lower()

    match = re.search(r"(\d+)\s*(lakh|lakhs|l)", q)
    if match:
        return int(match.group(1)) * 100000

    match = re.search(r"(\d+)\s*(crore|crores|cr)", q)
    if match:
        return int(match.group(1)) * 10000000

    match = re.search(r"budget\s*(is|of)?\s*(\d+)", q)
    if match:
        return int(match.group(2))

    return 3000000


def extract_timeline_months(query):
    q = query.lower()

    match = re.search(r"(\d+)\s*months?", q)
    if match:
        return int(match.group(1))

    match = re.search(r"(\d+)\s*weeks?", q)
    if match:
        weeks = int(match.group(1))
        return max(1, round(weeks / 4))

    return 3


def detect_project_type_from_query(query):
    """Return a known project type only when the message actually contains one."""
    q = query.lower()

    if any(k in q for k in ["data engineering", "data pipeline", "pipeline", "etl", "data platform"]):
        return "Data Platform"

    if any(k in q for k in [
        "chatbot", "ai bot", "customer support bot", "virtual assistant",
        "ai assistant", "employee assistant", "internal assistant",
        "assistant for internal employees", "internal employees",
        "copilot", "ai chatbot", "ai based software", "ai-based software", "ai software",
        "ai based", "ai solution", "ai application", "genai assistant",
        "bank assistant", "assistant for employees"
    ]):
        return "AI Chatbot"

    # If the sentence clearly asks us to build/create/provide an AI assistant
    # but does not use the exact word chatbot, still map to the AI Chatbot
    # delivery template. This prevents valid client messages like
    # "we need an AI assistant for internal employees" from being treated
    # as missing project type.
    if re.search(r"\b(?:need|want|build|create|develop|require)\b.*\bai\b.*\bassistant\b", q):
        return "AI Chatbot"

    # Product reliability: if the client clearly gives a software/project proposal but
    # not an exact supported project type, map it to the nearest available template.
    if "software" in q and any(k in q for k in ["proposal", "project", "client", "requirement"]):
        return "AI Chatbot"

    return None


def has_budget_in_query(query):
    q = query.lower()
    return bool(
        re.search(r"\d+\s*(lakh|lakhs|lac|lacs|l|crore|crores|cr)\b", q)
        or re.search(r"budget\s*(is|of|:)?\s*₹?\s*\d+", q)
        or re.search(r"₹\s*\d+", q)
    )


def has_timeline_in_query(query):
    q = query.lower()
    return bool(re.search(r"\d+\s*(month|months|week|weeks)\b", q))


def has_company_name_in_query(query):
    """Detect whether the client has shared an identifiable company/organization name.

    Fix: "we are from AR Bank" must count as a company name. Earlier logic
    accepted only company/firm/startup-style phrases, so banks were missed.
    """
    q = query.lower().strip()

    org_suffixes = (
        "company|firm|startup|school|college|enterprise|organization|organisation|"
        "institute|bank|finance|financial|insurance|hospital|clinic|retail|"
        "technologies|technology|tech|labs|solutions|services|pvt|ltd|llp"
    )

    explicit_patterns = [
        r"company\s*(name)?\s*(is|:|-)\s*[a-z0-9 &._-]{2,}",
        rf"we\s+are\s+(?:an?\s+)?[a-z0-9 &._-]{{2,}}\s+(?:{org_suffixes})\b",
        rf"from\s+[a-z0-9 &._-]{{2,}}\s+(?:{org_suffixes})\b",
        r"\bwe\s*(?:are|'re)\s+from\s+[a-z0-9 &._-]{2,}",
        r"\b[a-z0-9][a-z0-9 &._-]{1,}\s+bank\b",
    ]
    if any(re.search(pattern, q, flags=re.IGNORECASE) for pattern in explicit_patterns):
        return True

    org_words = [
        "educational based company", "education company", "educational company",
        "school", "college", "institute", "startup", "firm", "organization",
        "organisation", "enterprise", "bank", "financial services", "insurance",
        "hospital", "clinic", "retail company", "tech company"
    ]
    return any(word in q for word in org_words)

def extract_client_contact_from_text(query):
    """Extract a usable client contact from natural language.

    Accepts normal email/phone formats and business phrasing such as
    "contact us at", "connect us at", "reach us at", or a company website/domain.
    """
    text = safe_text(query) if 'safe_text' in globals() else str(query or '')

    email = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    if email:
        return email.group(0)

    phone = re.search(r"(?:\+91[-\s]?)?[6-9]\d{9}", text)
    if phone:
        return phone.group(0)

    contact_phrase = re.search(
        r"(?:contact|connect|reach|get\s+back\s+to|write\s+to|mail|email)\s+(?:us\s+)?(?:at|on|via|is|:)\s*([A-Za-z0-9._%+:/-]+\.[A-Za-z]{2,})",
        text,
        flags=re.IGNORECASE,
    )
    if contact_phrase:
        return contact_phrase.group(1).strip(" .,")

    website = re.search(r"\b(?:https?://)?(?:www\.)?[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+\b", text)
    if website:
        candidate = website.group(0).strip(" .,")
        if len(candidate) <= 80 and "@" not in candidate:
            return candidate

    return ""


def has_contact_in_query(query):
    """Detect whether email, phone, or a usable web/contact handle is present."""
    return bool(extract_client_contact_from_text(query))


def missing_client_proposal_fields(query):
    missing = []
    if not detect_project_type_from_query(query):
        missing.append("project requirement / project type")
    if not has_budget_in_query(query):
        missing.append("expected budget")
    if not has_timeline_in_query(query):
        missing.append("timeline")
    if not has_company_name_in_query(query):
        missing.append("company name")
    if not has_contact_in_query(query):
        missing.append("contact email or phone number")
    return missing


def format_missing_client_fields_message(missing):
    if not missing:
        return ""
    return (
        "AI Front Desk: I can start the internal LifecycleDesk AI meeting after I have all client details. "
        "Please share: " + ", ".join(missing) + ". "
        "Example: 'Company name is EduSmart, contact edu@example.com, we need an AI chatbot, budget 40 lakhs, timeline 8 months.'"
    )


def is_salary_related_query(query):
    q = query.lower()
    return any(
        k in q
        for k in [
            "salary", "inhand", "in-hand", "pay", "ctc", "payroll",
            "credited", "deduction", "deductions", "compensation"
        ]
    )


def detect_salary_role(query):
    q = query.lower()

    role_aliases = {
        "Data Engineer": ["data engineer", "data engineering"],
        "AI/ML Engineer": ["ai/ml", "ai engineer", "ml engineer", "machine learning engineer"],
        "Backend Developer": ["backend", "backend developer"],
        "Frontend Developer": ["frontend", "frontend developer"],
        "Full Stack Developer": ["full stack", "fullstack"],
        "DevOps Engineer": ["devops", "devops engineer"],
        "QA Engineer": ["qa engineer", "tester", "quality analyst"],
        "Project Manager": ["project manager", "pm salary"],
    }

    for canonical_role, aliases in role_aliases.items():
        if any(alias in q for alias in aliases):
            return canonical_role

    return None


def is_role_salary_query(query):
    return is_salary_related_query(query) and detect_salary_role(query) is not None


def can_view_salary_by_role(user):
    if not user:
        return False

    role = str(user.get("role", "")).lower()
    designation = str(user.get("designation", "")).lower()
    department = str(user.get("department", "")).lower()

    return role == "founder" or "finance" in designation or department == "finance"


def answer_salary_by_role(query, user, data):
    if user is None:
        return "Finance Agent: Please login first so I can verify your access."

    if not can_view_salary_by_role(user):
        return "Finance Agent: Role-wise salary data is restricted to Founder/CEO and Finance Executive access."

    role = detect_salary_role(query)
    if role is None:
        return get_employee_salary_info(user, data)

    employees = data["employees"]
    people = employees[
        employees["designation"].astype(str).str.lower() == role.lower()
    ].copy()

    if people.empty:
        # Fall back to contains matching because some sheets may store titles slightly differently.
        role_words = role.lower().replace("/", " ").split()
        mask = employees["designation"].astype(str).str.lower().apply(
            lambda value: all(word in value for word in role_words if word not in ["engineer", "developer"])
        )
        people = employees[mask].copy()

    if people.empty:
        return f"Finance Agent: I could not find any employee records for {role}."

    avg_ctc = float(people["monthly_ctc"].mean())
    avg_inhand = float(people["monthly_inhand"].mean())
    total_ctc = float(people["monthly_ctc"].sum())

    lines = []
    for _, row in people.iterrows():
        lines.append(
            f"{row['employee_name']} - {row['designation']} - "
            f"Monthly CTC ₹{float(row['monthly_ctc']):,.0f}, "
            f"In-hand ₹{float(row['monthly_inhand']):,.0f}"
        )

    return (
        f"Finance Agent: Salary analysis for {role}:\n\n"
        f"Count: {len(people)}\n"
        f"Average monthly CTC: ₹{avg_ctc:,.0f}\n"
        f"Average in-hand salary: ₹{avg_inhand:,.0f}\n"
        f"Total monthly CTC: ₹{total_ctc:,.0f}\n\n"
        "Employee details:\n- " + "\n- ".join(lines)
    )
