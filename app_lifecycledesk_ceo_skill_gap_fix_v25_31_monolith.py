"""LifecycleDesk AI v25.31 backup monolith.
Generated from app.py + decisiondesk_chunks. Prefer running modular app.py with decisiondesk_chunks/.
"""

# ==== 01_bootstrap_detection.py ====
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
# For hosted/demo reliability, proposal workflow writes should go to Supabase/PostgreSQL.
# Excel remains the seed database for static company data such as users, employees, payroll, etc.
REQUIRE_SUPABASE_FOR_PROPOSALS = True

# Lightweight demo mode: Excel is used for static company data. Supabase is used
# only for dynamic workflow inserts/updates. Expensive schema repair and long LLM
# generations are opt-in so normal clicks stay fast.
LIGHTWEIGHT_FAST_MODE = os.getenv("DD_LIGHTWEIGHT_FAST_MODE", "1").strip().lower() not in ["0", "false", "no"]
AUTO_SCHEMA_CHECK = os.getenv("DD_AUTO_SCHEMA_CHECK", "0").strip().lower() in ["1", "true", "yes"]
USE_LLM_FOR_LONG_DOCUMENTS = os.getenv("DD_USE_LLM_LONG_OUTPUTS", "0").strip().lower() in ["1", "true", "yes"]
POSTGRES_CONNECT_TIMEOUT_SECONDS = int(os.getenv("DD_POSTGRES_CONNECT_TIMEOUT", "2"))
POSTGRES_READ_CACHE_TTL_SECONDS = int(os.getenv("DD_POSTGRES_READ_CACHE_TTL", "150"))
POSTGRES_STATEMENT_TIMEOUT_MS = int(os.getenv("DD_POSTGRES_STATEMENT_TIMEOUT_MS", "9000"))


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

    # Demo reliability: if the client clearly gives a software/project proposal but
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
        "Receptionist: I can start the internal DecisionDesk AI meeting after I have all client details. "
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


# ==== 02_employee_receptionist.py ====
# ---------------- EMPLOYEE SELF-SERVICE ----------------

def get_employee_salary_info(user, data):
    emp_id = str(user["user_id"]).upper()

    payroll = data["payroll"]
    employees = data["employees"]

    pay = payroll[payroll["employee_id"].astype(str).str.upper() == emp_id]
    emp = employees[employees["employee_id"].astype(str).str.upper() == emp_id]

    if pay.empty and emp.empty:
        return "Finance Agent: I could not find your salary details."

    if not pay.empty:
        net_salary = pay.iloc[0]["net_salary"]
        gross_salary = pay.iloc[0]["gross_salary"]
    else:
        net_salary = emp.iloc[0]["monthly_inhand"]
        gross_salary = emp.iloc[0]["monthly_ctc"]

    return (
        f"Finance Agent: Your gross monthly salary is ₹{gross_salary:,.0f}. "
        f"Your expected in-hand salary is ₹{net_salary:,.0f}. "
        f"Salary is credited on the month's last working day."
    )


def get_employee_personal_updates(user, data):
    updates = []
    emp_id = str(user["user_id"]).upper()

    if user["role"] == "new_joinee":
        onboarding = data["onboarding"]
        row = onboarding[onboarding["employee_id"].astype(str).str.upper() == emp_id]

        if not row.empty:
            r = row.iloc[0]

            if r["forms_submitted"] != "Yes":
                updates.append("HR Update: Your onboarding forms are still pending.")
            if r["virtual_id_created"] != "Yes":
                updates.append("HR Update: Your virtual ID card is not created yet.")
            if r["laptop_issued"] != "Yes":
                updates.append("HR Update: Laptop is not yet issued.")
            if r["email_created"] != "Yes":
                updates.append("HR Update: Official email creation is pending.")

    assignments = data["assignments"]
    projects = data["projects"]

    my_assignments = assignments[
        assignments["employee_id"].astype(str).str.upper() == emp_id
    ]

    for _, a in my_assignments.iterrows():
        project_id = a["project_id"]
        project = projects[projects["project_id"] == project_id]

        if not project.empty:
            p = project.iloc[0]
            updates.append(
                f"Operations Update: You are assigned to {p['project_name']} "
                f"with {a['allocation_percent']}% bandwidth."
            )

            if p["actual_progress"] < p["expected_progress"]:
                updates.append(
                    f"Project Alert: {p['project_name']} is behind schedule. "
                    f"Expected progress is {p['expected_progress']}%, actual is {p['actual_progress']}%."
                )

    if not updates:
        updates.append("No pending HR or operational updates. Have a good day.")

    return updates


# ---------------- EXTERNAL CLIENT MULTI-AGENT ANALYSIS ----------------

# 

def adjust_employee_availability_with_dynamic_allocations(employees):
    """Return employees with availability reduced by live Supabase project allocations.

    Excel remains the fast static source for employee master data. Supabase stores
    the dynamic project allocations created after client acceptance. When a new
    external proposal is analysed, the Operations/HR capacity calculation should
    use Excel availability minus active Supabase allocation percent so the skill
    gap changes as new projects are assigned.
    """
    adjusted = employees.copy()
    if "employee_id" not in adjusted.columns or "availability_percent" not in adjusted.columns:
        return adjusted

    try:
        allocations = read_simple_table("project_allocations", PROJECT_ALLOCATION_COLUMNS)
    except Exception:
        return adjusted

    if allocations is None or allocations.empty:
        return adjusted

    active = allocations.copy()
    if "allocation_status" in active.columns:
        active = active[active["allocation_status"].fillna("Active").astype(str).str.lower() == "active"]
    if active.empty:
        return adjusted

    active["allocation_percent_num"] = pd.to_numeric(active.get("allocation_percent", 0), errors="coerce").fillna(0)
    dynamic_used = active.groupby(active["employee_id"].astype(str).str.upper())["allocation_percent_num"].sum().to_dict()

    def remaining_availability(row):
        emp_id = str(row.get("employee_id", "")).upper()
        static_available = safe_number(row.get("availability_percent"), 0)
        used_now = float(dynamic_used.get(emp_id, 0))
        return max(0, static_available - used_now)

    adjusted["availability_percent"] = adjusted.apply(remaining_availability, axis=1)
    return adjusted

#     budget = extract_budget(query)
#     timeline_months = extract_timeline_months(query)
#     project_type = detect_project_type_from_query(query)

#     requirements = data["requirements"]
#     employees = data["employees"]

#     req = requirements[requirements["project_type"] == project_type]

#     if req.empty:
#         project_type = "AI Chatbot"
#         req = requirements[requirements["project_type"] == project_type]

#     employee_cost = 0

#     for _, row in req.iterrows():
#         role = row["required_role"]
#         count = row["required_people"]

#         matching = employees[employees["designation"] == role]

#         if matching.empty:
#             avg_salary = 120000
#         else:
#             avg_salary = matching["monthly_ctc"].mean()

#         employee_cost += avg_salary * count * timeline_months

#     overhead = employee_cost * 0.20
#     cloud_cost = employee_cost * 0.10
#     total_cost = employee_cost + overhead + cloud_cost

#     target_margin = 0.40
#     recommended_quote = total_cost / (1 - target_margin)

#     profit_at_client_budget = budget - total_cost
#     margin_at_client_budget = profit_at_client_budget / budget if budget else 0

#     skill_gap = []

#     for _, row in req.iterrows():
#         role = row["required_role"]
#         needed = row["required_people"]

#         available = employees[
#             (employees["designation"] == role)
#             & (employees["availability_percent"] >= 40)
#         ]

#         available_capacity = available["availability_percent"].sum() / 100
#         gap = max(0, needed - available_capacity)

#         skill_gap.append({
#             "role": role,
#             "needed": needed,
#             "available_capacity": round(available_capacity, 2),
#             "gap": round(gap, 2),
#         })

#     if budget < total_cost:
#         decision = "Reject or Renegotiate"
#         reason = "Client budget is below estimated delivery cost."
#     elif budget < recommended_quote:
#         decision = "Accept only with conditions"
#         reason = "Client budget covers delivery cost, but is below our target-margin quote."
#     elif timeline_months < 2:
#         decision = "Accept only with conditions"
#         reason = "Timeline is aggressive and needs delivery approval."
#     else:
#         decision = "Accept"
#         reason = "Budget and timeline are feasible."

#     return {
#         "client_message": query,
#         "client_budget": budget,
#         "project_type": project_type,
#         "timeline_months": timeline_months,
#         "employee_cost": round(employee_cost, 2),
#         "overhead": round(overhead, 2),
#         "cloud_cost": round(cloud_cost, 2),
#         "estimated_cost": round(total_cost, 2),
#         "recommended_quote": round(recommended_quote, 2),
#         "expected_profit_at_client_budget": round(profit_at_client_budget, 2),
#         "profit_margin_at_client_budget": round(margin_at_client_budget * 100, 2),
#         "skill_gap": skill_gap,
#         "decision": decision,
#         "reason": reason,
#     }

def answer_with_sql_agent(query, user, data, agent_name):
    if user is None:
        return f"{agent_name}: Please login first so I can verify your access."

    result = run_sql_query(query, user, data)

    if not result["success"]:
        return result["answer"]

    return result




def _to_datetime_or_none(value):
    """Small, safe datetime parser for Supabase text dates."""
    try:
        if value is None or pd.isna(value):
            return None
    except Exception:
        pass
    value_text = str(value).strip()
    if not value_text:
        return None
    try:
        parsed = pd.to_datetime(value_text, errors="coerce")
        if pd.isna(parsed):
            return None
        return parsed.to_pydatetime()
    except Exception:
        return None


def _months_between(start_dt, end_dt):
    if not start_dt or not end_dt:
        return 0.0
    return max(0.0, (end_dt - start_dt).days / 30.0)


def _latest_employee_update_map(employee_updates):
    """Return {(project_id, employee_id): latest_update_dict}."""
    result = {}
    if employee_updates is None or employee_updates.empty:
        return result

    updates = employee_updates.copy()
    if "created_at" in updates.columns:
        updates["_created_at_dt"] = pd.to_datetime(updates["created_at"], errors="coerce")
        updates = updates.sort_values("_created_at_dt")

    for _, row in updates.iterrows():
        project_id = safe_text(row.get("project_id")).upper()
        employee_id = safe_text(row.get("employee_id")).upper()
        if project_id and employee_id:
            result[(project_id, employee_id)] = row.to_dict()
    return result


def _proposal_timeline_map():
    """Map proposal_id -> quoted/original timeline months from live proposal store."""
    try:
        proposals = read_proposal_store(create_if_missing=False)
    except Exception:
        return {}
    if proposals is None or proposals.empty:
        return {}

    timeline_by_proposal = {}
    for _, row in proposals.iterrows():
        proposal_id = safe_text(row.get("proposal_id")).upper()
        timeline = (
            safe_int(row.get("ceo_final_timeline_months"))
            or safe_int(row.get("timeline_months"))
            or 0
        )
        if proposal_id and timeline:
            timeline_by_proposal[proposal_id] = timeline
    return timeline_by_proposal


def read_dynamic_capacity_sources():
    """Read live Supabase workload tables for HR/Operations capacity analysis.

    Excel remains the source for employee master data and salary. Supabase is the
    source for live project workload, employee allocations, project progress,
    hurdles, and estimated release timing.
    """
    sources = {
        "projects": pd.DataFrame(),
        "allocations": pd.DataFrame(),
        "delivery_plans": pd.DataFrame(),
        "employee_updates": pd.DataFrame(),
        "timeline_by_proposal": {},
    }

    try:
        sources["projects"] = read_simple_table("projects", PROJECT_COLUMNS)
    except Exception:
        pass
    try:
        sources["allocations"] = read_simple_table("project_allocations", PROJECT_ALLOCATION_COLUMNS)
    except Exception:
        pass
    try:
        sources["delivery_plans"] = read_simple_table("delivery_plans", DELIVERY_PLAN_COLUMNS)
    except Exception:
        pass
    try:
        sources["employee_updates"] = read_simple_table("employee_project_updates", EMPLOYEE_PROJECT_UPDATE_COLUMNS)
    except Exception:
        pass
    try:
        sources["timeline_by_proposal"] = _proposal_timeline_map()
    except Exception:
        pass

    return sources


def build_dynamic_employee_capacity(employees, new_project_timeline_months=0):
    """Build employee-level live availability using Supabase workload state.

    The output keeps Excel employee columns but adds:
    - live_allocated_percent: allocation currently reserved by accepted Supabase projects
    - availability_percent: current immediately usable capacity
    - projected_available_percent: capacity expected to be usable during the new proposal timeline
    - avg_project_progress_percent: latest progress from employee weekly updates
    - active_project_count, hurdle_count, next_release_date, capacity_notes
    """
    adjusted = employees.copy()
    if "employee_id" not in adjusted.columns:
        return adjusted

    if "availability_percent" not in adjusted.columns:
        adjusted["availability_percent"] = 100

    adjusted["base_availability_percent"] = pd.to_numeric(
        adjusted.get("availability_percent", 100), errors="coerce"
    ).fillna(100).clip(lower=0, upper=100)
    adjusted["live_allocated_percent"] = 0.0
    adjusted["projected_release_percent"] = 0.0
    adjusted["projected_available_percent"] = adjusted["base_availability_percent"].astype(float)
    adjusted["avg_project_progress_percent"] = 0.0
    adjusted["active_project_count"] = 0
    adjusted["hurdle_count"] = 0
    adjusted["next_release_date"] = ""
    adjusted["capacity_notes"] = "No active Supabase project allocation."

    sources = read_dynamic_capacity_sources()
    allocations = sources["allocations"]
    if allocations is None or allocations.empty:
        return adjusted

    active = allocations.copy()
    if "allocation_status" in active.columns:
        active = active[active["allocation_status"].fillna("Active").astype(str).str.lower().isin(["active", "assigned", "in progress", "approved"])]
    if active.empty:
        return adjusted

    latest_updates = _latest_employee_update_map(sources["employee_updates"])
    timeline_by_proposal = sources["timeline_by_proposal"]
    now_dt = datetime.now()
    new_timeline = max(0, safe_number(new_project_timeline_months, 0))
    try:
        new_end_dt = (pd.Timestamp(now_dt) + pd.DateOffset(months=int(max(1, round(new_timeline or 1))))).to_pydatetime()
    except Exception:
        new_end_dt = now_dt + pd.Timedelta(days=int(max(30, new_timeline * 30))).to_pytimedelta()

    project_meta = {}
    projects = sources["projects"]
    if projects is not None and not projects.empty:
        for _, project in projects.iterrows():
            project_id = safe_text(project.get("project_id")).upper()
            if project_id:
                project_meta[project_id] = project.to_dict()

    per_employee = {}
    for _, alloc in active.iterrows():
        emp_id = safe_text(alloc.get("employee_id")).upper()
        project_id = safe_text(alloc.get("project_id")).upper()
        proposal_id = safe_text(alloc.get("proposal_id")).upper()
        if not emp_id:
            continue

        allocation_percent = safe_number(alloc.get("allocation_percent"), 0)
        update = latest_updates.get((project_id, emp_id), {})
        progress = safe_number(update.get("progress_percent"), 0)
        progress = min(max(progress, 0), 100)

        hurdle_text = " ".join([
            safe_text(update.get("hurdles")),
            safe_text(update.get("support_needed")),
            safe_text(update.get("notes")),
        ]).strip()
        has_hurdle = bool(hurdle_text)

        start_dt = _to_datetime_or_none(alloc.get("start_date"))
        end_dt = _to_datetime_or_none(alloc.get("end_date"))
        project = project_meta.get(project_id, {})
        if not start_dt:
            start_dt = _to_datetime_or_none(project.get("kickoff_date")) or _to_datetime_or_none(project.get("created_at")) or now_dt
        if not end_dt:
            timeline = timeline_by_proposal.get(proposal_id, 0)
            if timeline:
                try:
                    end_dt = (pd.Timestamp(start_dt) + pd.DateOffset(months=int(timeline))).to_pydatetime()
                except Exception:
                    end_dt = None

        months_left = _months_between(now_dt, end_dt) if end_dt else 0.0
        remaining_work_fraction = max(0.0, min(1.0, (100.0 - progress) / 100.0)) if progress else 1.0

        # Current reservation should reflect both official allocation and live progress.
        # Keep a minimum reservation while the assignment is still active, because even
        # an 85-90% complete project still needs support, review, and handover.
        if progress >= 100 or (end_dt and end_dt < now_dt and not has_hurdle):
            current_reserved = 0.0
        else:
            current_reserved = allocation_percent * max(0.20, remaining_work_fraction)
            if has_hurdle:
                current_reserved = min(allocation_percent, current_reserved * 1.15)

        release_within_new_project = bool(end_dt and end_dt <= new_end_dt)
        projected_release = allocation_percent if (progress >= 100 or release_within_new_project) else max(0.0, allocation_percent - current_reserved)

        bucket = per_employee.setdefault(emp_id, {
            "live_allocated_percent": 0.0,
            "projected_release_percent": 0.0,
            "progress_values": [],
            "active_project_count": 0,
            "hurdle_count": 0,
            "release_dates": [],
            "notes": [],
        })
        bucket["live_allocated_percent"] += current_reserved
        bucket["projected_release_percent"] += projected_release
        bucket["active_project_count"] += 1
        if progress:
            bucket["progress_values"].append(progress)
        if has_hurdle:
            bucket["hurdle_count"] += 1
        if end_dt:
            bucket["release_dates"].append(end_dt)
        project_label = safe_text(project.get("project_name")) or safe_text(alloc.get("project_role")) or project_id
        note_parts = [project_label, f"{allocation_percent:.0f}% allocated"]
        if progress:
            note_parts.append(f"{progress:.0f}% complete")
        if months_left:
            note_parts.append(f"~{months_left:.1f} months left")
        if has_hurdle:
            note_parts.append("hurdle/support request present")
        bucket["notes"].append("; ".join(note_parts))

    def apply_capacity(row):
        emp_id = safe_text(row.get("employee_id")).upper()
        base_available = safe_number(row.get("base_availability_percent"), 100)
        live = per_employee.get(emp_id)
        if not live:
            row["availability_percent"] = min(100, max(0, base_available))
            row["projected_available_percent"] = min(100, max(0, base_available))
            return row

        live_used = min(100, max(0, live["live_allocated_percent"]))
        projected_release = min(100, max(0, live["projected_release_percent"]))
        current_available = max(0, base_available - live_used)
        projected_available = min(100, max(current_available, base_available - max(0, live_used - projected_release)))
        avg_progress = sum(live["progress_values"]) / len(live["progress_values"]) if live["progress_values"] else 0
        next_release = min(live["release_dates"]).strftime("%Y-%m-%d") if live["release_dates"] else ""

        row["live_allocated_percent"] = round(live_used, 2)
        row["availability_percent"] = round(current_available, 2)
        row["projected_release_percent"] = round(projected_release, 2)
        row["projected_available_percent"] = round(projected_available, 2)
        row["avg_project_progress_percent"] = round(avg_progress, 2)
        row["active_project_count"] = int(live["active_project_count"])
        row["hurdle_count"] = int(live["hurdle_count"])
        row["next_release_date"] = next_release
        row["capacity_notes"] = " | ".join(live["notes"][:3])
        return row

    adjusted = adjusted.apply(apply_capacity, axis=1)
    return adjusted


def adjust_employee_availability_with_dynamic_allocations(employees, new_project_timeline_months=0):
    """Backward-compatible wrapper used by older code paths."""
    return build_dynamic_employee_capacity(employees, new_project_timeline_months)


def build_dynamic_role_capacity(required_roles, employees, new_project_timeline_months=0):
    """Summarise live/projected capacity by role for HR and Operations."""
    dynamic_employees = build_dynamic_employee_capacity(employees, new_project_timeline_months)
    rows = []

    for _, req_row in required_roles.iterrows():
        role = safe_text(req_row.get("required_role"))
        needed = safe_number(req_row.get("required_people"), 0)
        matching = dynamic_employees[dynamic_employees["designation"].astype(str).str.lower() == role.lower()] if "designation" in dynamic_employees.columns else pd.DataFrame()

        if matching.empty:
            avg_salary = 90000
            available_now_fte = 0.0
            projected_available_fte = 0.0
            active_allocated_fte = 0.0
            avg_progress = 0.0
            blockers = 0
            nearest_release = ""
            capacity_notes = "No employee found for this role."
        else:
            avg_salary = safe_number(pd.to_numeric(matching.get("monthly_ctc"), errors="coerce").dropna().mean(), 90000)
            available_now_fte = pd.to_numeric(matching.get("availability_percent", 0), errors="coerce").fillna(0).clip(lower=0).sum() / 100
            projected_available_fte = pd.to_numeric(matching.get("projected_available_percent", 0), errors="coerce").fillna(0).clip(lower=0).sum() / 100
            active_allocated_fte = pd.to_numeric(matching.get("live_allocated_percent", 0), errors="coerce").fillna(0).clip(lower=0).sum() / 100
            progress_values = pd.to_numeric(matching.get("avg_project_progress_percent", 0), errors="coerce").fillna(0)
            progress_values = progress_values[progress_values > 0]
            avg_progress = float(progress_values.mean()) if len(progress_values) else 0.0
            blockers = int(pd.to_numeric(matching.get("hurdle_count", 0), errors="coerce").fillna(0).sum())
            release_dates = [safe_text(v) for v in matching.get("next_release_date", []) if safe_text(v)]
            nearest_release = min(release_dates) if release_dates else ""
            note_values = [safe_text(v) for v in matching.get("capacity_notes", []) if safe_text(v) and safe_text(v) != "No active Supabase project allocation."]
            capacity_notes = " | ".join(note_values[:2]) or "No active Supabase project pressure for this role."

        rows.append({
            "role": role,
            "needed": round(needed, 2),
            "available_capacity": round(available_now_fte, 2),
            "available_now_fte": round(available_now_fte, 2),
            "projected_available_fte": round(projected_available_fte, 2),
            "active_allocated_fte": round(active_allocated_fte, 2),
            "gap": round(max(0, needed - projected_available_fte), 2),
            "immediate_gap": round(max(0, needed - available_now_fte), 2),
            "avg_current_project_progress_percent": round(avg_progress, 2),
            "hurdle_or_support_request_count": blockers,
            "nearest_release_date": nearest_release,
            "capacity_notes": capacity_notes,
            "avg_monthly_salary": round(avg_salary, 2),
        })

    return rows


def run_external_client_decision(query, data):
    budget = extract_budget(query)
    timeline_months = extract_timeline_months(query)
    project_type = detect_project_type_from_query(query) or "AI Chatbot"

    requirements = data["requirements"]
    employees = data["employees"]

    req = requirements[requirements["project_type"] == project_type]

    if req.empty:
        project_type = "AI Chatbot"
        req = requirements[requirements["project_type"] == project_type]

    default_allocation = {
        "AI/ML Engineer": 0.40,
        "Backend Developer": 0.40,
        "Frontend Developer": 0.30,
        "DevOps Engineer": 0.20,
        "QA Engineer": 0.30,
        "Data Engineer": 0.45,
        "Project Manager": 0.20,
        "Full Stack Developer": 0.40,
    }

    capacity_rows = build_dynamic_role_capacity(req, employees, timeline_months)
    capacity_by_role = {item["role"]: item for item in capacity_rows}

    employee_cost = 0
    role_cost_breakdown = []
    skill_gap = []

    for _, row in req.iterrows():
        role = row["required_role"]
        needed = float(row["required_people"])
        capacity = capacity_by_role.get(role, {})
        avg_salary = safe_number(capacity.get("avg_monthly_salary"), 90000)
        allocation = default_allocation.get(role, 0.35)
        role_cost = avg_salary * needed * allocation * timeline_months
        employee_cost += role_cost

        role_cost_breakdown.append({
            "role": role,
            "people_required": needed,
            "avg_monthly_salary": round(avg_salary, 2),
            "allocation_used": allocation,
            "timeline_months": timeline_months,
            "role_cost": round(role_cost, 2),
            "dynamic_capacity_basis": capacity.get("capacity_notes", ""),
            "available_now_fte": capacity.get("available_now_fte", 0),
            "projected_available_fte": capacity.get("projected_available_fte", 0),
            "active_allocated_fte": capacity.get("active_allocated_fte", 0),
            "avg_current_project_progress_percent": capacity.get("avg_current_project_progress_percent", 0),
            "nearest_release_date": capacity.get("nearest_release_date", ""),
        })

        skill_gap.append({
            "role": role,
            "needed": needed,
            "available_capacity": capacity.get("projected_available_fte", 0),
            "available_now_fte": capacity.get("available_now_fte", 0),
            "projected_available_fte": capacity.get("projected_available_fte", 0),
            "active_allocated_fte": capacity.get("active_allocated_fte", 0),
            "immediate_gap": capacity.get("immediate_gap", needed),
            "gap": capacity.get("gap", needed),
            "avg_current_project_progress_percent": capacity.get("avg_current_project_progress_percent", 0),
            "hurdle_or_support_request_count": capacity.get("hurdle_or_support_request_count", 0),
            "nearest_release_date": capacity.get("nearest_release_date", ""),
            "capacity_notes": capacity.get("capacity_notes", ""),
        })

    overhead = employee_cost * 0.10
    cloud_cost = employee_cost * 0.05
    software_cost = employee_cost * 0.03
    contingency = employee_cost * 0.05

    total_cost = employee_cost + overhead + cloud_cost + software_cost + contingency

    target_margin = 0.30
    recommended_quote = total_cost / (1 - target_margin) if target_margin < 1 else total_cost

    profit_at_client_budget = budget - total_cost
    margin_at_client_budget = profit_at_client_budget / budget if budget else 0

    total_skill_gap = sum(safe_number(item.get("gap"), 0) for item in skill_gap)
    immediate_skill_gap = sum(safe_number(item.get("immediate_gap"), 0) for item in skill_gap)
    total_active_allocated_fte = sum(safe_number(item.get("active_allocated_fte"), 0) for item in skill_gap)
    total_hurdles = sum(safe_int(item.get("hurdle_or_support_request_count"), 0) for item in skill_gap)

    if timeline_months < 2:
        timeline_risk = "High"
    elif timeline_months < 3 or total_hurdles > 0:
        timeline_risk = "Medium"
    else:
        timeline_risk = "Low"

    if budget < total_cost:
        decision = "Reject or Renegotiate"
        reason = "Client budget is below estimated delivery cost."
    elif budget < recommended_quote:
        decision = "Accept only with conditions"
        reason = "Client budget covers delivery cost, but is below our target-margin quote."
    elif total_skill_gap > 1:
        decision = "Accept only with conditions"
        reason = "Budget is feasible, but dynamic Supabase workload shows a resource gap during the proposed timeline."
    elif immediate_skill_gap > 0.5:
        decision = "Accept only with conditions"
        reason = "Immediate capacity is tight, but employees are expected to become available during the project timeline."
    elif timeline_risk == "High":
        decision = "Accept only with conditions"
        reason = "Timeline is aggressive and needs delivery approval."
    else:
        decision = "Accept"
        reason = "Budget, timeline, and live employee capacity are feasible based on current Supabase allocations and updates."

    return {
        "client_message": query,
        "client_budget": round(budget, 2),
        "project_type": project_type,
        "timeline_months": timeline_months,

        "employee_cost": round(employee_cost, 2),
        "overhead": round(overhead, 2),
        "cloud_cost": round(cloud_cost, 2),
        "software_cost": round(software_cost, 2),
        "contingency": round(contingency, 2),
        "estimated_cost": round(total_cost, 2),

        "target_margin_percent": round(target_margin * 100, 2),
        "recommended_quote": round(recommended_quote, 2),
        "expected_profit_at_client_budget": round(profit_at_client_budget, 2),
        "profit_margin_at_client_budget": round(margin_at_client_budget * 100, 2),

        "role_cost_breakdown": role_cost_breakdown,
        "skill_gap": skill_gap,
        "total_skill_gap": round(total_skill_gap, 2),
        "immediate_skill_gap": round(immediate_skill_gap, 2),
        "total_active_allocated_fte": round(total_active_allocated_fte, 2),
        "dynamic_hurdle_count": int(total_hurdles),
        "timeline_risk": timeline_risk,
        "capacity_basis": "Excel employee master/payroll + Supabase projects, project_allocations, delivery_plans, and employee_project_updates.",

        "decision": decision,
        "reason": reason,
    }

def handle_hr_agent_query(query, user, data):
    q = query.lower()

    if user is None:
        return "HR Agent: Please login first so I can verify your identity."

    emp_id = str(user["user_id"]).upper()

    employees = data["employees"]
    users = data["users"]
    attendance = data["attendance"]
    onboarding = data["onboarding"]

    emp = employees[employees["employee_id"].astype(str).str.upper() == emp_id]

    if "manager" in q or "reporting" in q:
        current_user = users[users["user_id"].astype(str).str.upper() == emp_id]

        if current_user.empty:
            return "HR Agent: I could not find your reporting manager details."

        manager_id = current_user.iloc[0].get("manager_id")

        if pd.isna(manager_id) or str(manager_id).strip() == "":
            return "HR Agent: You do not have a reporting manager assigned."

        manager = users[users["user_id"].astype(str).str.upper() == str(manager_id).upper()]

        if manager.empty:
            return f"HR Agent: Your reporting manager ID is {manager_id}, but manager details are missing."

        m = manager.iloc[0]

        return (
            f"HR Agent: Your reporting manager is {m['employee_name']} "
            f"({m['designation']}) from {m['department']} department."
        )

    if "attendance" in q:
        my_attendance = attendance[
            attendance["employee_id"].astype(str).str.upper() == emp_id
        ]

        if my_attendance.empty:
            return "HR Agent: I could not find your attendance records."

        avg_attendance = my_attendance["attendance_percent"].mean()
        total_leave = my_attendance["leave_days"].sum()

        return (
            f"HR Agent: Your average attendance is {avg_attendance:.2f}%. "
            f"You have taken {total_leave} leave day(s) in the available records."
        )

    if "lop" in q or "loss of pay" in q:
        lop_df = calculate_lop(attendance)
        my_lop = lop_df[lop_df["employee_id"].astype(str).str.upper() == emp_id]

        total_lop = my_lop["lop_days"].sum()

        if total_lop == 0:
            return "HR Agent: You currently have no LOP days."

        return f"HR Agent: You have {total_lop} LOP day(s). Please check with HR for regularization."

    if "form" in q or "id card" in q or "onboarding" in q:
        row = onboarding[onboarding["employee_id"].astype(str).str.upper() == emp_id]

        if row.empty:
            return "HR Agent: No onboarding record found for you."

        r = row.iloc[0]

        return (
            "HR Agent: Here is your onboarding status:\n\n"
            f"- Forms Submitted: {r['forms_submitted']}\n"
            f"- Virtual ID Created: {r['virtual_id_created']}\n"
            f"- Laptop Issued: {r['laptop_issued']}\n"
            f"- Email Created: {r['email_created']}\n"
            f"- Onboarding Status: {r['onboarding_status']}"
        )

    if emp.empty:
        return "HR Agent: I could not find your employee profile."

    e = emp.iloc[0]

    return (
        "HR Agent: Here are your employee details:\n\n"
        f"- Name: {e['employee_name']}\n"
        f"- Designation: {e['designation']}\n"
        f"- Primary Skill: {e['primary_skill']}\n"
        f"- Domain: {e['domain']}\n"
        f"- Availability: {e['availability_percent']}%"
    )

# ---------------- RECEPTIONIST ----------------

# 
def is_simple_greeting_query(query):
    """Return True for plain greetings so the receptionist does not over-route.

    This keeps "hi" from being sent to CEO/company-performance or any other agent.
    Longer messages like "hi, show company performance" still continue to normal routing.
    """
    text_value = safe_text(query).strip().lower()
    text_value = re.sub(r"[^a-z\s]", "", text_value).strip()
    greetings = {
        "hi", "hello", "hey", "hai", "hii", "good morning", "good afternoon",
        "good evening", "namaste", "thanks", "thank you"
    }
    return text_value in greetings or (len(text_value.split()) <= 3 and any(g == text_value for g in greetings))

# def handle_receptionist_query(query, user, data):
#     q = query.lower()

#     if user is None and st.session_state.external_enquiry_mode:
#         st.session_state.external_enquiry_mode = False

#         return {
#             "type": "external_client_details_received",
#             "message": (
#                 "Receptionist: Thank you for sharing the project details. "
#                 "I am calling Sales, HR, Operations, Finance, and CEO Agents for an internal feasibility check."
#             ),
#         }

#     if user is None:
#         if is_project_proposal_query(query) or any(
#             k in q for k in ["client", "budget", "startup", "contact", "company", "solution"]
#         ):
#             st.session_state.external_enquiry_mode = True

#             return {
#                 "type": "external_client",
#                 "message": (
#                     "Receptionist: Welcome to VirtualTech Solutions. "
#                     "I can help with your project enquiry. Please share your company name, industry, "
#                     "project requirement, expected budget, urgency, and contact details."
#                 ),
#             }

#         return {
#             "type": "general",
#             "message": (
#                 "Receptionist: Welcome to VirtualTech Solutions. "
#                 "You can login as an employee, executive, or founder. "
#                 "If you are a client, you can tell me about your project requirement."
#             ),
#         }

#     if any(k in q for k in ["salary", "inhand", "in-hand", "pay", "credited", "salary date"]):
#         return {
#             "type": "text",
#             "message": "Receptionist: Connecting you to Finance Agent.\n\n"
#             + get_employee_salary_info(user, data),
#         }

#     if is_project_proposal_query(query):
#         lead_id = detect_lead_id(query)

#         if lead_id is None:
#             return {
#                 "type": "text",
#                 "message": (
#                     "Receptionist: I understand this is a project proposal request. "
#                     "Please mention the lead ID, for example L001, L002, or L003."
#                 ),
#             }

#         return {
#             "type": "proposal_workflow",
#             "lead_id": lead_id,
#             "message": (
#                 f"Receptionist: Lead {lead_id} detected. "
#                 "Starting internal AI decision meeting with Sales, HR, Operations, Finance, and CEO Agents."
#             ),
#         }

#     if any(k in q for k in ["company health", "business performance", "company performance"]):
#         if user["role"] == "founder":
#             return {
#                 "type": "company_health",
#                 "message": "Receptionist: Connecting you to CEO Agent for company performance analysis.",
#             }

#         return {
#             "type": "text",
#             "message": "Receptionist: Company performance reports require Founder/CEO access.",
#         }

#     agent = receptionist_route(query)

#     return {
#         "type": "route_agent",
#         "agent": agent,
#         "message": f"Receptionist: Connecting you to {agent}.",
#     }

def explain_salary_difference(user, data):
    if user is None:
        return "Finance Agent: Please login first so I can verify your payroll details."

    emp_id = str(user["user_id"]).upper()

    payroll = data["payroll"]
    attendance = data["attendance"]

    pay = payroll[payroll["employee_id"].astype(str).str.upper() == emp_id]

    if pay.empty:
        return "Finance Agent: I could not find your payroll record."

    pay = pay.iloc[0]

    gross_salary = float(pay["gross_salary"])
    normal_net_salary = float(pay["net_salary"])

    my_attendance = attendance[
        attendance["employee_id"].astype(str).str.upper() == emp_id
    ]

    if my_attendance.empty:
        return (
            f"Finance Agent: Your expected in-hand salary is ₹{normal_net_salary:,.0f}. "
            "I could not find attendance records to explain the difference."
        )

    lop_records = []

    for _, row in my_attendance.iterrows():
        is_lop = str(row.get("is_lop", "No")).strip().lower()
        status = str(row.get("status", "")).strip().lower()
        leave_status = str(row.get("leave_status", "")).strip().lower()
        remarks = str(row.get("remarks", "")).strip()

        lop_flag = (
            is_lop == "yes"
            or "lop" in remarks.lower()
            or "unapproved" in leave_status
            or "absent" in status and "not applied" in leave_status
        )

        if lop_flag:
            lop_records.append({
                "date": row.get("date", row.get("attendance_date", "")),
                "month": row.get("month", ""),
                "status": row.get("status", ""),
                "leave_status": row.get("leave_status", ""),
                "remarks": remarks if remarks else "Marked as LOP"
            })

    total_lop_days = len(lop_records)

    per_day_salary = gross_salary / 30
    lop_deduction = per_day_salary * total_lop_days
    estimated_final_salary = normal_net_salary - lop_deduction

    if total_lop_days == 0:
        return (
            "Finance Agent: I checked your payroll and attendance records.\n\n"
            f"Expected in-hand salary: ₹{normal_net_salary:,.0f}\n"
            "LOP days found: 0\n\n"
            "I do not see any LOP-based deduction. If your credited amount is still lower, "
            "it may be due to tax, PF adjustment, or manual payroll correction. Please raise this to Finance Executive."
        )

    lop_lines = []
    for r in lop_records:
        lop_lines.append(
            f"{r['date']} - {r['remarks']}"
        )

    return (
        "Finance Agent: I checked your payroll and attendance records.\n\n"
        f"Gross salary: ₹{gross_salary:,.0f}\n"
        f"Expected in-hand salary: ₹{normal_net_salary:,.0f}\n"
        f"LOP days found: {total_lop_days}\n"
        f"Per-day salary: ₹{per_day_salary:,.0f}\n"
        f"LOP deduction: ₹{lop_deduction:,.0f}\n"
        f"Estimated salary after LOP: ₹{estimated_final_salary:,.0f}\n\n"
        "Reason:\n- " + "\n- ".join(lop_lines)
    )

# def explain_salary_difference(user, data):
#     if user is None:
#         return "Finance Agent: Please login first so I can verify your payroll details."

#     emp_id = str(user["user_id"]).upper()

#     payroll = data["payroll"]
#     attendance = data["attendance"]

#     pay = payroll[payroll["employee_id"].astype(str).str.upper() == emp_id]

#     if pay.empty:
#         return "Finance Agent: I could not find your payroll record."

#     pay = pay.iloc[0]

#     gross_salary = float(pay["gross_salary"])
#     normal_net_salary = float(pay["net_salary"])

#     my_attendance = attendance[
#         attendance["employee_id"].astype(str).str.upper() == emp_id
#     ]

#     if my_attendance.empty:
#         return (
#             f"Finance Agent: Your expected in-hand salary is ₹{normal_net_salary:,.0f}. "
#             "I could not find attendance or LOP records to explain the difference."
#         )

#     total_lop_days = 0
#     lop_reasons = []

#     for _, row in my_attendance.iterrows():
#         leave_days = float(row.get("leave_days", 0))
#         leave_applied = str(row.get("leave_applied", "No"))
#         leave_approved = str(row.get("leave_approved", "No"))

#         if leave_days > 0 and leave_applied == "No":
#             total_lop_days += leave_days
#             lop_reasons.append(f"{row['month']}: {leave_days} day(s) LOP because leave was not applied.")
#         elif leave_days > 0 and leave_applied == "Yes" and leave_approved == "No":
#             total_lop_days += leave_days
#             lop_reasons.append(f"{row['month']}: {leave_days} day(s) LOP because leave was not approved.")

#     per_day_salary = gross_salary / 30
#     lop_deduction = per_day_salary * total_lop_days
#     estimated_final_salary = normal_net_salary - lop_deduction

#     if total_lop_days == 0:
#         return (
#             f"Finance Agent: I checked your payroll and attendance records.\n\n"
#             f"Expected in-hand salary: ₹{normal_net_salary:,.0f}\n"
#             f"LOP days found: 0\n\n"
#             "I do not see any LOP-based deduction. If your credited amount is still lower, "
#             "it may be due to tax, PF adjustment, or manual payroll correction. Please raise this to Finance Executive."
#         )

#     return (
#         "Finance Agent: I checked your payroll and attendance records.\n\n"
#         f"Gross salary: ₹{gross_salary:,.0f}\n"
#         f"Expected in-hand salary: ₹{normal_net_salary:,.0f}\n"
#         f"LOP days found: {total_lop_days}\n"
#         f"Per-day salary: ₹{per_day_salary:,.0f}\n"
#         f"LOP deduction: ₹{lop_deduction:,.0f}\n"
#         f"Estimated final salary after LOP: ₹{estimated_final_salary:,.0f}\n\n"
#         "Reason:\n- " + "\n- ".join(lop_reasons)
#     )


def is_simple_greeting_query(query):
    """Return True for plain greetings so the receptionist does not over-route.

    This keeps "hi" from being sent to CEO/company-performance or any other agent.
    Longer messages like "hi, show company performance" still continue to normal routing.
    """
    text_value = safe_text(query).strip().lower()
    text_value = re.sub(r"[^a-z\s]", "", text_value).strip()
    greetings = {
        "hi", "hello", "hey", "hai", "hii", "good morning", "good afternoon",
        "good evening", "namaste", "thanks", "thank you"
    }
    return text_value in greetings or (len(text_value.split()) <= 3 and any(g == text_value for g in greetings))

def handle_receptionist_query(query, user, data):
    """
    Receptionist routes the user to the right agent.

    Important hackathon reliability rule:
    Use deterministic routing for high-value demo flows first, then use the LLM
    receptionist as a fallback. This prevents simple asks like
    "salary of the data engineer" from dying in the generic receptionist fallback.
    """

    q = query.lower().strip()

    if is_simple_greeting_query(query):
        name = actor_name(user) if user else "there"
        return {
            "type": "general",
            "agent": "Receptionist",
            "intent": "greeting",
            "confidence": 1.0,
            "message": f"Receptionist: Hello {name}. Hope you are doing good today. How can I help you?",
        }

    # 1. If the user asks for company performance/report, never treat it as a client proposal.
    # This is an internal CEO-level report, so it must require login and proper access.
    if is_company_performance_query(query):
        st.session_state.external_enquiry_mode = False
        if user is None:
            return {
                "type": "login_required",
                "agent": "CEO Agent",
                "intent": "company_performance",
                "message": (
                    "Receptionist: Company performance reports are internal company data. "
                    "Please login first so I can verify your access."
                ),
            }
        if user.get("role") == "founder":
            return {
                "type": "company_health",
                "agent": "CEO Agent",
                "intent": "company_performance",
                "message": "Receptionist: Connecting you to CEO Agent for company performance analysis.",
            }
        return {
            "type": "text",
            "agent": "CEO Agent",
            "intent": "company_performance",
            "message": "Receptionist: Company performance reports require Founder/CEO access.",
        }

    # 2. If an external client was already asked for details, only trigger the workflow
    # when the follow-up actually contains a complete proposal. This prevents random
    # messages like 'company performance report' from being saved as fake proposals.
    if user is None and st.session_state.external_enquiry_mode:
        previous_details = safe_text(st.session_state.get("pending_client_proposal_text", ""))
        combined_query = (previous_details + "\n" + query).strip() if previous_details else query

        if is_complete_client_proposal(combined_query):
            st.session_state.external_enquiry_mode = False
            st.session_state.pending_client_proposal_text = combined_query
            return {
                "type": "external_client_details_received",
                "agent": "Sales Agent",
                "intent": "external_client_details_received",
                "client_query": combined_query,
                "message": (
                    "Receptionist: Thank you for sharing the complete project details. "
                    "I am calling Sales, HR, Operations, Finance, and CEO Agents "
                    "for an internal feasibility check."
                ),
            }

        st.session_state.pending_client_proposal_text = combined_query
        missing = missing_client_proposal_fields(combined_query)
        return {
            "type": "external_client",
            "agent": "Sales Agent",
            "intent": "external_client_enquiry_incomplete",
            "message": format_missing_client_fields_message(missing),
        }

    # 3. Do not use old lead-ID routing for the hackathon demo.
    # Any proposal-like message, even if it mentions L001/L002/L003, should be treated
    # as a new client enquiry and processed through the external-client decision room.

    # 4. Salary/payroll is a core demo path, so do not leave it only to the LLM router.
    if user is not None and is_salary_related_query(query):
        return {
            "type": "route_agent",
            "agent": "Finance Agent",
            "intent": "role_salary_lookup" if is_role_salary_query(query) else "salary_info",
            "confidence": 1.0,
            "message": "Receptionist: Connecting you to Finance Agent.",
        }

    # 5. External/new client enquiry can work without login.
    looks_like_external_project = (
        not is_company_performance_query(query)
        and (
            is_project_proposal_query(query)
            or any(k in q for k in ["client", "budget", "startup", "company", "solution", "requirement", "software"])
        )
    )

    if user is None and looks_like_external_project:
        if is_complete_client_proposal(query):
            st.session_state.pending_client_proposal_text = query
            return {
                "type": "external_client_details_received",
                "agent": "Sales Agent",
                "intent": "external_client_details_received",
                "client_query": query,
                "message": (
                    "Receptionist: Thank you. I found the company details, contact, project requirement, budget, and timeline. "
                    "I am calling Sales, HR, Operations, Finance, and CEO Agents for feasibility analysis."
                ),
            }

        st.session_state.external_enquiry_mode = True
        st.session_state.pending_client_proposal_text = query
        missing = missing_client_proposal_fields(query)
        return {
            "type": "external_client",
            "agent": "Sales Agent",
            "intent": "external_client_enquiry",
            "message": format_missing_client_fields_message(missing),
        }

    # 6. Logged-in sales/CEO users may also enter a brand-new client requirement during demo.
    if user is not None and looks_like_external_project:
        if is_complete_client_proposal(query):
            return {
                "type": "external_client_details_received",
                "agent": "Sales Agent",
                "intent": "external_client_details_received",
                "client_query": query,
                "message": (
                    "Receptionist: New client requirement detected with company/contact details. "
                    "Calling Sales, HR, Operations, Finance, and CEO Agents for feasibility analysis."
                ),
            }
        if has_budget_in_query(query) or has_timeline_in_query(query) or detect_project_type_from_query(query):
            missing = missing_client_proposal_fields(query)
            return {
                "type": "text",
                "agent": "Sales Agent",
                "intent": "external_client_enquiry_incomplete",
                "message": format_missing_client_fields_message(missing),
            }

    # 7. Ask the LLM receptionist after deterministic hackathon-critical routes.
    try:
        understood = receptionist_understand(query, user)
    except Exception as e:
        understood = {
            "agent": "Receptionist",
            "intent": "unknown",
            "confidence": 0.0,
            "reason": f"Receptionist understanding failed: {e}",
        }

    agent = understood.get("agent", "Receptionist")
    intent = understood.get("intent", "unknown")
    confidence = float(understood.get("confidence", 0.0) or 0.0)

    # 8. If not logged in and this is not a client enquiry, ask for login for internal data.
    if user is None:
        if agent == "Sales Agent" and intent in [
            "external_client_enquiry",
            "new_project_enquiry",
            "project_proposal",
            "lead_qualification",
        ]:
            st.session_state.external_enquiry_mode = True
            return {
                "type": "external_client",
                "agent": "Sales Agent",
                "intent": intent,
                "message": (
                    "Receptionist: Welcome to VirtualTech Solutions. "
                    "I understand you have a project requirement. Please share company name, industry, budget, timeline, urgency, and contact details."
                ),
            }

        if agent in ["HR Agent", "Finance Agent", "Operations Agent", "CEO Agent"] or is_salary_related_query(query):
            return {
                "type": "login_required",
                "agent": agent if agent != "Receptionist" else "Finance Agent",
                "intent": intent,
                "message": (
                    "Receptionist: This is an internal company-data request. "
                    "Please login first so I can verify your access."
                ),
            }

        return {
            "type": "general",
            "agent": "Receptionist",
            "intent": intent,
            "confidence": confidence,
            "message": (
                "Receptionist: Welcome to VirtualTech Solutions. You can login as an employee, executive, or founder. "
                "If you are a client, describe your project requirement."
            ),
        }

    # 9. Logged-in project enquiry without full details.
    if agent == "Sales Agent" and intent in [
        "external_client_enquiry",
        "new_project_enquiry",
        "project_proposal",
        "lead_qualification",
    ]:
        return {
            "type": "text",
            "agent": "Sales Agent",
            "intent": intent,
            "message": (
                "Receptionist: This looks like a new client project enquiry. "
                "Please provide the full new-client details with project type, budget, and timeline so I can start the multi-agent decision room."
            ),
        }

    # 10. Company performance / CEO report.
    if agent == "CEO Agent" and intent in [
        "company_health",
        "business_performance",
        "company_performance",
        "strategy_report",
    ]:
        if user.get("role") == "founder":
            return {
                "type": "company_health",
                "agent": "CEO Agent",
                "intent": intent,
                "message": "Receptionist: Connecting you to CEO Agent for company performance analysis.",
            }

        return {
            "type": "text",
            "agent": "CEO Agent",
            "intent": intent,
            "message": "Receptionist: Company performance reports require Founder/CEO access.",
        }

    # 11. Internal project decision without a lead ID.
    if agent == "CEO Agent" and intent in [
        "internal_project_decision",
        "approve_reject_project",
        "project_decision",
    ]:
        return {
            "type": "text",
            "agent": "CEO Agent",
            "intent": intent,
            "message": (
                "Receptionist: I understand this is a project decision request. "
                "Please provide the full new-client requirement with project type, budget, and timeline so I can start the multi-agent decision room."
            ),
        }

    # 12. Normal agent route.
    if agent in ["HR Agent", "Finance Agent", "Operations Agent", "Sales Agent", "CEO Agent"]:
        return {
            "type": "route_agent",
            "agent": agent,
            "intent": intent,
            "confidence": confidence,
            "message": f"Receptionist: Connecting you to {agent}.",
        }

    # 13. Last-resort deterministic fallback.
    if is_salary_related_query(query):
        return {
            "type": "route_agent",
            "agent": "Finance Agent",
            "intent": "role_salary_lookup" if is_role_salary_query(query) else "salary_info",
            "confidence": 1.0,
            "message": "Receptionist: Connecting you to Finance Agent.",
        }

    return {
        "type": "general",
        "agent": "Receptionist",
        "intent": intent,
        "confidence": confidence,
        "message": (
            "Receptionist: I can help route you to HR, Finance, Operations, Sales, "
            "or CEO Agent. Please tell me what you need."
        ),
    }


# ==== 03_storage_client_delivery.py ====
# ---------------- WORKSPACE / REPORT HELPERS ----------------

PROPOSAL_DECISIONS_SHEET = "Proposal_Decisions"
PROPOSAL_HISTORY_SHEET = "Proposal_Decision_History"

PROPOSAL_NOTIFICATION_COLUMNS = {
    "sales": "sales_seen",
    "finance": "finance_seen",
    "hr": "hr_seen",
    "operations": "operations_seen",
    "ceo": "ceo_seen",
}

PROPOSAL_DEPARTMENT_LABELS = {
    "sales": "Sales Executive",
    "finance": "Finance Executive",
    "hr": "HR Executive",
    "operations": "Operations Executive",
    "ceo": "CEO",
}

PROPOSAL_SEEN_AT_COLUMNS = {
    "sales": "sales_seen_at",
    "finance": "finance_seen_at",
    "hr": "hr_seen_at",
    "operations": "operations_seen_at",
    "ceo": "ceo_seen_at",
}

PROPOSAL_DECISION_COLUMNS = [
    "proposal_id",
    "created_at",
    "source",
    "client_name",
    "client_contact",
    "raw_client_message",
    "project_type",
    "client_budget",
    "timeline_months",
    "employee_cost",
    "overhead",
    "cloud_cost",
    "software_cost",
    "contingency",
    "estimated_cost",
    "target_margin_percent",
    "recommended_quote",
    "expected_profit_at_client_budget",
    "profit_margin_at_client_budget",
    "total_skill_gap",
    "timeline_risk",
    "initial_agent_decision",
    "initial_agent_reason",
    "decision",
    "reason",
    "workflow_status",
    "current_owner",
    "decision_version",
    "sales_agent_summary",
    "hr_agent_summary",
    "operations_agent_summary",
    "finance_agent_summary",
    "ceo_agent_summary",
    "skill_gap_json",
    "role_cost_breakdown_json",
    "sales_decision",
    "sales_comment",
    "sales_recommended_quote",
    "sales_recommended_timeline_months",
    "sales_decided_by",
    "sales_decided_at",
    "finance_decision",
    "finance_comment",
    "finance_recommended_quote",
    "finance_recommended_timeline_months",
    "finance_decided_by",
    "finance_decided_at",
    "hr_decision",
    "hr_comment",
    "hr_recommended_quote",
    "hr_recommended_timeline_months",
    "hr_decided_by",
    "hr_decided_at",
    "operations_decision",
    "operations_comment",
    "operations_recommended_quote",
    "operations_recommended_timeline_months",
    "operations_decided_by",
    "operations_decided_at",
    "ceo_final_decision",
    "ceo_comment",
    "ceo_final_quote",
    "ceo_final_timeline_months",
    "ceo_decided_by",
    "ceo_decided_at",
    "client_quotation",
    "quotation_generated_at",
    "quotation_sent",
    "quotation_sent_at",
    "client_id",
    "client_user_id",
    "client_password",
    "client_response",
    "client_response_comment",
    "client_response_at",
    "project_id",
    "project_created",
    "project_created_at",
    "sales_seen",
    "finance_seen",
    "hr_seen",
    "operations_seen",
    "ceo_seen",
    "sales_seen_at",
    "finance_seen_at",
    "hr_seen_at",
    "operations_seen_at",
    "ceo_seen_at",
    "last_updated_by",
    "last_updated_role",
    "last_updated_at",
    "last_update_summary",
]

PROPOSAL_HISTORY_COLUMNS = [
    "event_id",
    "proposal_id",
    "event_at",
    "actor_id",
    "actor_name",
    "actor_role",
    "action_type",
    "decision",
    "comment",
    "recommended_quote",
    "recommended_timeline_months",
    "summary",
]

CLIENT_ACCOUNT_COLUMNS = [
    "client_id",
    "proposal_id",
    "client_name",
    "client_contact",
    "client_user_id",
    "client_password",
    "created_at",
    "last_login_at",
    "account_status",
]

CLIENT_RESPONSE_COLUMNS = [
    "response_id",
    "proposal_id",
    "client_id",
    "response",
    "comment",
    "responded_at",
]

PROJECT_COLUMNS = [
    "project_id",
    "proposal_id",
    "client_id",
    "project_name",
    "project_status",
    "operations_owner_id",
    "operations_owner_name",
    "kickoff_date",
    "created_at",
    "updated_at",
]

DELIVERY_PLAN_COLUMNS = [
    "delivery_plan_id",
    "project_id",
    "proposal_id",
    "client_id",
    "requirement_source",
    "uploaded_file_name",
    "raw_requirement_text",
    "operations_agent_plan",
    "operations_manager_plan",
    "suggested_tools",
    "cloud_plan",
    "security_plan",
    "module_breakdown",
    "risks_and_blockers",
    "client_clarifications_needed",
    "approval_status",
    "approved_by",
    "approved_at",
    "created_at",
    "updated_at",
]

PROJECT_ALLOCATION_COLUMNS = [
    "allocation_id",
    "project_id",
    "proposal_id",
    "client_id",
    "employee_id",
    "employee_name",
    "employee_department",
    "employee_designation",
    "project_role",
    "assigned_module",
    "responsibility_summary",
    "allocation_percent",
    "start_date",
    "end_date",
    "assigned_by",
    "assigned_at",
    "allocation_status",
]

EMPLOYEE_NOTIFICATION_COLUMNS = [
    "notification_id",
    "employee_id",
    "project_id",
    "proposal_id",
    "notification_type",
    "message",
    "seen",
    "created_at",
    "seen_at",
]

EMPLOYEE_PROJECT_UPDATE_COLUMNS = [
    "employee_update_id",
    "project_id",
    "proposal_id",
    "client_id",
    "employee_id",
    "employee_name",
    "project_role",
    "assigned_module",
    "week_label",
    "progress_status",
    "progress_percent",
    "hurdles",
    "support_needed",
    "notes",
    "created_at",
    "operations_status",
    "operations_done_by",
    "operations_done_at",
    "operations_resolution_note",
]

WEEKLY_UPDATE_COLUMNS = [
    "update_id",
    "project_id",
    "proposal_id",
    "client_id",
    "week_label",
    "update_text",
    "blockers",
    "client_action_needed",
    "generated_by",
    "generated_at",
    "published_by",
    "visible_to_client",
]

CLIENT_RESPONSE_OPTIONS = ["Accept Proposal", "Decline Proposal", "Request Reconsideration"]

EXECUTIVE_DECISION_OPTIONS = [
    "Support / Accept",
    "Support with Conditions",
    "Need Negotiation",
    "Reject / Not Feasible",
    "Need More Info",
]

CEO_DECISION_OPTIONS = [
    "Approve",
    "Approve with Conditions",
    "Negotiate with Client",
    "Reject",
    "Hold / Need More Review",
]


def current_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def safe_text(value, default=""):
    if value is None:
        return default
    if isinstance(value, float) and pd.isna(value):
        return default
    try:
        if pd.isna(value):
            return default
    except Exception:
        pass
    return str(value)


def safe_number(value, default=0.0):
    if value is None:
        return default
    try:
        if pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def safe_int(value, default=0):
    try:
        return int(round(safe_number(value, default)))
    except Exception:
        return default


def encode_json(value):
    return json.dumps(value if value is not None else [], ensure_ascii=False)


def decode_json(value, default=None):
    if default is None:
        default = []
    if value is None:
        return default
    if isinstance(value, (list, dict)):
        return value
    if isinstance(value, float) and pd.isna(value):
        return default
    text_value = str(value).strip()
    if not text_value:
        return default
    try:
        return json.loads(text_value)
    except Exception:
        return default


def money_text(value):
    return f"₹{safe_number(value):,.0f}"


def make_event_id():
    return "E-" + datetime.now().strftime("%Y%m%d%H%M%S%f")


def make_response_id():
    return "CR-" + datetime.now().strftime("%Y%m%d%H%M%S%f")


def make_project_id():
    return "PRJ-" + datetime.now().strftime("%Y%m%d%H%M%S%f")


def make_delivery_plan_id():
    return "DP-" + datetime.now().strftime("%Y%m%d%H%M%S%f")


def make_allocation_id():
    return "AL-" + datetime.now().strftime("%Y%m%d%H%M%S%f")


def make_notification_id():
    return "NT-" + datetime.now().strftime("%Y%m%d%H%M%S%f")


def make_employee_update_id():
    return "EU-" + datetime.now().strftime("%Y%m%d%H%M%S%f")


def make_weekly_update_id():
    return "WU-" + datetime.now().strftime("%Y%m%d%H%M%S%f")


def make_client_id():
    return "C-" + datetime.now().strftime("%Y%m%d%H%M%S%f")


def make_client_password():
    """Create a short demo-friendly temporary password.

    Production version should hash passwords and enforce reset on first login.
    """
    return "DD-" + datetime.now().strftime("%S%f")[-4:]


def make_client_user_id(client_id):
    """Create a short demo-friendly client login ID instead of a long timestamp."""
    digits = re.sub(r"\D", "", safe_text(client_id))
    suffix = digits[-4:] if len(digits) >= 4 else datetime.now().strftime("%S%f")[-4:]
    return f"CLIENT-{suffix}"


def make_proposal_id():
    return "P-" + datetime.now().strftime("%Y%m%d%H%M%S%f")


def maybe_extract_client_name(raw_client_message):
    """Extract client/company name from natural project messages.

    Supports banking-style phrasing such as "we are from AR Bank".
    """
    text = safe_text(raw_client_message)
    org_suffixes = (
        "company|firm|startup|school|college|enterprise|organization|organisation|"
        "institute|bank|finance|financial|insurance|hospital|clinic|retail|"
        "technologies|technology|tech|labs|solutions|services|pvt|ltd|llp"
    )
    patterns = [
        r"company\s*(?:name)?\s*(?:is|:)\s*([^.,\n]+)",
        rf"we\s+are\s+from\s+([^.,\n]+?(?:{org_suffixes})?)\b",
        rf"from\s+([^.,\n]+?\s+(?:{org_suffixes}))\b",
        rf"we\s+are\s+(?:an?\s+)?([^.,\n]+?\s+(?:{org_suffixes}))\b",
        rf"\b([^.,\n]+?\s+bank)\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            candidate = match.group(1).strip(" .,-")
            candidate = re.split(
                r"\b(?:we\s+need|need|our\s+budget|budget|time\s*line|timeline|contact|phone|email)\b",
                candidate,
                maxsplit=1,
                flags=re.IGNORECASE,
            )[0].strip(" .,-")
            if len(candidate) >= 2:
                return re.sub(r"\s+", " ", candidate)[:80]
    return "External Client"

def maybe_extract_client_contact(raw_client_message):
    return extract_client_contact_from_text(raw_client_message)


def normalise_proposal_store(df):
    """Add all required decision, notification, and quote columns without breaking older rows."""
    if df is None or df.empty:
        df = pd.DataFrame(columns=PROPOSAL_DECISION_COLUMNS)

    for column in PROPOSAL_DECISION_COLUMNS:
        if column not in df.columns:
            if column in PROPOSAL_NOTIFICATION_COLUMNS.values():
                df[column] = "No"
            elif column == "quotation_sent":
                df[column] = "No"
            elif column == "decision_version":
                df[column] = 0
            else:
                df[column] = ""

    for role_key, column in PROPOSAL_NOTIFICATION_COLUMNS.items():
        df[column] = df[column].fillna("No").replace("", "No")

    if "quotation_sent" in df.columns:
        df["quotation_sent"] = df["quotation_sent"].fillna("No").replace("", "No")

    # Backward compatibility with the earlier one-step sheet.
    if "initial_agent_decision" in df.columns and "decision" in df.columns:
        missing = df["initial_agent_decision"].fillna("").astype(str).str.strip() == ""
        df.loc[missing, "initial_agent_decision"] = df.loc[missing, "decision"]
    if "initial_agent_reason" in df.columns and "reason" in df.columns:
        missing = df["initial_agent_reason"].fillna("").astype(str).str.strip() == ""
        df.loc[missing, "initial_agent_reason"] = df.loc[missing, "reason"]
    if "workflow_status" in df.columns:
        df["workflow_status"] = df["workflow_status"].fillna("").replace("", "Awaiting Executive Decisions")
    if "current_owner" in df.columns:
        df["current_owner"] = df["current_owner"].fillna("").replace("", "Sales, Finance, HR, Operations, CEO")

    ordered_columns = PROPOSAL_DECISION_COLUMNS + [
        col for col in df.columns if col not in PROPOSAL_DECISION_COLUMNS
    ]
    return df[ordered_columns]


def normalise_history_store(df):
    if df is None or df.empty:
        return pd.DataFrame(columns=PROPOSAL_HISTORY_COLUMNS)
    for column in PROPOSAL_HISTORY_COLUMNS:
        if column not in df.columns:
            df[column] = ""
    ordered_columns = PROPOSAL_HISTORY_COLUMNS + [
        col for col in df.columns if col not in PROPOSAL_HISTORY_COLUMNS
    ]
    return df[ordered_columns]


def make_excel_backup(db_file):
    """Create a timestamped backup before any workbook write.

    Excel .xlsx files are zip archives. If Streamlit is stopped mid-write or the
    workbook is open in Excel, the file can become corrupted. Keeping backups
    makes recovery quick during demos.
    """
    db_file = Path(db_file)
    backup_dir = db_file.parent / "backups"
    backup_dir.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    backup_file = backup_dir / f"{db_file.stem}_backup_{stamp}{db_file.suffix}"
    shutil.copy2(db_file, backup_file)
    return backup_file


def write_excel_sheet(sheet_name, df):
    """Replace one sheet while preserving the rest of the workbook.

    Excel is still used for static company data and as a local fallback.
    Proposal workflow writes use PostgreSQL/Supabase when the Streamlit secret
    [connections.postgresql] is configured.

    A backup is created before every Excel fallback write. If the write fails,
    the previous file is restored automatically.
    """
    db_file = Path(DB_PATH)
    if not db_file.exists():
        raise FileNotFoundError(f"Excel DB not found at: {db_file}")

    backup_file = make_excel_backup(db_file)
    try:
        with pd.ExcelWriter(
            db_file,
            engine="openpyxl",
            mode="a",
            if_sheet_exists="replace",
        ) as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    except Exception:
        try:
            shutil.copy2(backup_file, db_file)
        except Exception:
            pass
        raise


def _secret_value(path, default=""):
    """Safely read nested Streamlit secrets without crashing when secrets are absent."""
    try:
        value = st.secrets
        for key in path:
            value = value[key]
        return str(value).strip()
    except Exception:
        return default


def get_postgres_url():
    """Return the database URL used for proposal storage.

    Priority is intentionally: Streamlit/Supabase pooler URL first, then direct URL.
    Direct Supabase hosts like db.<project-ref>.supabase.co may fail on some
    networks because of DNS/IPv6 restrictions. The pooler URL is safer for
    Streamlit and hosted demos.
    """
    candidates = [
        _secret_value(["SUPABASE_POOLER_DB_URL"]),
        os.getenv("SUPABASE_POOLER_DB_URL", "").strip(),
        _secret_value(["connections", "postgresql", "url"]),
        _secret_value(["SUPABASE_DB_URL"]),
        os.getenv("SUPABASE_DB_URL", "").strip(),
    ]
    for url in candidates:
        if url:
            if url.startswith("postgres://"):
                url = "postgresql://" + url[len("postgres://"):]
            return url
    return ""


def mask_db_url(url):
    if not url:
        return ""
    return re.sub(r"://([^:/@]+):([^@]+)@", r"://\1:****@", url)


def postgres_config_available():
    """Return True when a PostgreSQL URL is configured."""
    return bool(get_postgres_url())


def proposal_storage_backend_label():
    return "Supabase PostgreSQL" if postgres_config_available() else "Excel fallback / Supabase not connected"


def explain_postgres_connection_error(exc):
    message = str(exc)
    configured = mask_db_url(get_postgres_url())
    extra = ""
    if "could not translate host name" in message or "Name or service not known" in message:
        extra = (
            "\n\nMost likely fix: use the Supabase POOLER connection string instead of the direct "
            "db.<project-ref>.supabase.co string. In Supabase open Connect / Database settings, "
            "copy Transaction pooler or Session pooler URI, then set it as SUPABASE_POOLER_DB_URL "
            "or as [connections.postgresql].url. Also make sure the project is not paused/deleted."
        )
    return f"Configured database: {configured}\n\n{message}{extra}"


def is_transient_postgres_error(exc):
    """Return True for network/pooler errors that should not crash the UI."""
    message = str(exc).lower()
    patterns = [
        "could not translate host name",
        "name or service not known",
        "server closed the connection unexpectedly",
        "ssl syscall error",
        "connection reset",
        "timeout expired",
        "connection timed out",
        "temporary failure in name resolution",
    ]
    return any(pattern in message for pattern in patterns)


def remember_postgres_error(exc):
    try:
        st.session_state["proposal_storage_last_error"] = explain_postgres_connection_error(exc)
    except Exception:
        pass


def require_postgres_or_raise():
    if postgres_config_available():
        return
    raise RuntimeError(
        "Supabase PostgreSQL is not connected. Add either .streamlit/secrets.toml or .env and restart.\n\n"
        "Recommended Streamlit secret format:\n"
        "SUPABASE_POOLER_DB_URL = \"postgresql://postgres.PROJECT_REF:YOUR_PASSWORD@POOLER_HOST:6543/postgres\"\n\n"
        "Or direct format if your network supports it:\n"
        "[connections.postgresql]\n"
        "url = \"postgresql://postgres:YOUR_PASSWORD@db.PROJECT_REF.supabase.co:5432/postgres\"\n\n"
        "Proposal data was not saved to Excel to avoid workbook corruption."
    )


class PgConnectionAdapter:
    def __init__(self, engine):
        self.engine = engine

    def query(self, sql, ttl=0):
        sql_text = str(sql).strip()
        if sql_text.lower().startswith("select"):
            return cached_postgres_select(get_postgres_url(), sql_text)
        return pd.read_sql_query(sql_text, self.engine)


@st.cache_resource(show_spinner=False)
def get_pg_engine_cached(db_url):
    """Create one cached SQLAlchemy engine for the configured Supabase URL."""
    connect_args = {
        "sslmode": "require",
        "connect_timeout": POSTGRES_CONNECT_TIMEOUT_SECONDS,
        "application_name": "decisiondesk_ai",
        "options": f"-c statement_timeout={POSTGRES_STATEMENT_TIMEOUT_MS}",
    }
    engine_kwargs = {
        "pool_pre_ping": True,
        "connect_args": connect_args,
    }
    # For speed, keep SQLAlchemy's normal lightweight pool. Supabase already pools
    # on the server side; keeping a local engine avoids reconnecting on every rerun.
    if (not LIGHTWEIGHT_FAST_MODE) and NullPool is not None:
        engine_kwargs["poolclass"] = NullPool
    return create_engine(db_url, **engine_kwargs)


@st.cache_data(ttl=POSTGRES_READ_CACHE_TTL_SECONDS, show_spinner=False)
def cached_postgres_select(db_url, sql):
    """Cache short-lived read queries during Streamlit reruns.

    Workflow writes clear this cache, so dashboards stay responsive without
    repeatedly hitting Supabase for the same SELECT on every click.
    """
    engine = get_pg_engine_cached(db_url)
    return pd.read_sql_query(sql, engine)


def clear_workflow_read_cache():
    """Clear cached Supabase read queries after any workflow write."""
    try:
        cached_postgres_select.clear()
    except Exception:
        pass


def get_pg_conn():
    if text is None or create_engine is None:
        raise RuntimeError("SQLAlchemy is not installed. Add sqlalchemy and psycopg2-binary to requirements.txt.")
    db_url = get_postgres_url()
    if not db_url:
        require_postgres_or_raise()
    engine = get_pg_engine_cached(db_url)
    return PgConnectionAdapter(engine)


def test_postgres_connection():
    if not postgres_config_available():
        return False, "No PostgreSQL URL configured."
    try:
        conn = get_pg_conn()
        with conn.engine.connect() as db:
            db.execute(text("SELECT 1"))
        return True, "Connected"
    except Exception as exc:
        return False, explain_postgres_connection_error(exc)


def ensure_postgres_tables():
    """Create/upgrade workflow tables once per Streamlit session.

    The old app ran CREATE/ALTER checks repeatedly while rendering dashboards.
    This is safe but slow on Supabase. The schema is now verified once per
    session; write paths still call this function, but it returns immediately
    after the first successful run.
    """
    if st.session_state.get("_dd_pg_schema_ready"):
        return
    # Fast demo mode assumes tables already exist and avoids repeated CREATE/ALTER
    # checks during normal page loads. Use the sidebar button to repair schema.
    if LIGHTWEIGHT_FAST_MODE and not AUTO_SCHEMA_CHECK and not st.session_state.pop("_dd_run_schema_repair_now", False):
        return
    conn = get_pg_conn()
    engine = conn.engine

    proposal_columns_sql = ",\n                ".join([
        f"{col} TEXT" for col in PROPOSAL_DECISION_COLUMNS if col != "proposal_id"
    ])
    history_columns_sql = ",\n                ".join([
        f"{col} TEXT" for col in PROPOSAL_HISTORY_COLUMNS if col != "event_id"
    ])

    with engine.begin() as db:
        db.execute(text(f"""
            CREATE TABLE IF NOT EXISTS proposal_decisions (
                proposal_id TEXT PRIMARY KEY,
                {proposal_columns_sql}
            )
        """))
        db.execute(text(f"""
            CREATE TABLE IF NOT EXISTS proposal_decision_history (
                event_id TEXT PRIMARY KEY,
                {history_columns_sql}
            )
        """))

        # v21 client portal tables. These are dynamic workflow tables in Supabase.
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS client_accounts (
                client_id TEXT PRIMARY KEY,
                proposal_id TEXT,
                client_name TEXT,
                client_contact TEXT,
                client_user_id TEXT UNIQUE,
                client_password TEXT,
                created_at TEXT,
                last_login_at TEXT,
                account_status TEXT DEFAULT 'Active'
            )
        """))
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS client_responses (
                response_id TEXT PRIMARY KEY,
                proposal_id TEXT,
                client_id TEXT,
                response TEXT,
                comment TEXT,
                responded_at TEXT
            )
        """))

        db.execute(text("""
            CREATE TABLE IF NOT EXISTS projects (
                project_id TEXT PRIMARY KEY,
                proposal_id TEXT,
                client_id TEXT,
                project_name TEXT,
                project_status TEXT,
                operations_owner_id TEXT,
                operations_owner_name TEXT,
                kickoff_date TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        """))
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS delivery_plans (
                delivery_plan_id TEXT PRIMARY KEY,
                project_id TEXT,
                proposal_id TEXT,
                client_id TEXT,
                requirement_source TEXT,
                uploaded_file_name TEXT,
                raw_requirement_text TEXT,
                operations_agent_plan TEXT,
                operations_manager_plan TEXT,
                suggested_tools TEXT,
                cloud_plan TEXT,
                security_plan TEXT,
                module_breakdown TEXT,
                risks_and_blockers TEXT,
                client_clarifications_needed TEXT,
                approval_status TEXT DEFAULT 'Draft',
                approved_by TEXT,
                approved_at TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        """))
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS project_allocations (
                allocation_id TEXT PRIMARY KEY,
                project_id TEXT,
                proposal_id TEXT,
                client_id TEXT,
                employee_id TEXT,
                employee_name TEXT,
                employee_department TEXT,
                employee_designation TEXT,
                project_role TEXT,
                assigned_module TEXT,
                responsibility_summary TEXT,
                allocation_percent TEXT,
                start_date TEXT,
                end_date TEXT,
                assigned_by TEXT,
                assigned_at TEXT,
                allocation_status TEXT DEFAULT 'Active'
            )
        """))
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS employee_notifications (
                notification_id TEXT PRIMARY KEY,
                employee_id TEXT,
                project_id TEXT,
                proposal_id TEXT,
                notification_type TEXT,
                message TEXT,
                seen TEXT DEFAULT 'No',
                created_at TEXT,
                seen_at TEXT
            )
        """))
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS employee_project_updates (
                employee_update_id TEXT PRIMARY KEY,
                project_id TEXT,
                proposal_id TEXT,
                client_id TEXT,
                employee_id TEXT,
                employee_name TEXT,
                project_role TEXT,
                assigned_module TEXT,
                week_label TEXT,
                progress_status TEXT,
                progress_percent TEXT,
                hurdles TEXT,
                support_needed TEXT,
                notes TEXT,
                created_at TEXT,
                operations_status TEXT DEFAULT 'Open',
                operations_done_by TEXT,
                operations_done_at TEXT,
                operations_resolution_note TEXT
            )
        """))
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS weekly_project_updates (
                update_id TEXT PRIMARY KEY,
                project_id TEXT,
                proposal_id TEXT,
                client_id TEXT,
                week_label TEXT,
                update_text TEXT,
                blockers TEXT,
                client_action_needed TEXT,
                generated_by TEXT DEFAULT 'Operations Agent',
                generated_at TEXT,
                published_by TEXT,
                visible_to_client TEXT DEFAULT 'Yes'
            )
        """))

        # CREATE TABLE IF NOT EXISTS does not add missing columns to tables that
        # already exist. Keep these ALTER statements so older Supabase tables are
        # upgraded in place instead of crashing during INSERT/UPDATE.
        for col in ["client_id", "client_user_id", "client_password", "client_response", "client_response_comment", "client_response_at"]:
            db.execute(text(f"ALTER TABLE proposal_decisions ADD COLUMN IF NOT EXISTS {col} TEXT"))

        for col in CLIENT_ACCOUNT_COLUMNS:
            if col != "client_id":
                default_sql = " DEFAULT 'Active'" if col == "account_status" else ""
                db.execute(text(f"ALTER TABLE client_accounts ADD COLUMN IF NOT EXISTS {col} TEXT{default_sql}"))

        # v21.3 schema repair: old Supabase tables may already exist with fewer columns.
        # CREATE TABLE IF NOT EXISTS will not add columns, so upgrade all workflow tables in place.
        for col in PROPOSAL_DECISION_COLUMNS:
            if col != "proposal_id":
                db.execute(text(f"ALTER TABLE proposal_decisions ADD COLUMN IF NOT EXISTS {col} TEXT"))

        for col in PROPOSAL_HISTORY_COLUMNS:
            if col != "event_id":
                db.execute(text(f"ALTER TABLE proposal_decision_history ADD COLUMN IF NOT EXISTS {col} TEXT"))

        for col in CLIENT_RESPONSE_COLUMNS:
            if col != "response_id":
                db.execute(text(f"ALTER TABLE client_responses ADD COLUMN IF NOT EXISTS {col} TEXT"))

        for table_name, columns, key_col in [
            ("projects", PROJECT_COLUMNS, "project_id"),
            ("delivery_plans", DELIVERY_PLAN_COLUMNS, "delivery_plan_id"),
            ("project_allocations", PROJECT_ALLOCATION_COLUMNS, "allocation_id"),
            ("employee_notifications", EMPLOYEE_NOTIFICATION_COLUMNS, "notification_id"),
            ("employee_project_updates", EMPLOYEE_PROJECT_UPDATE_COLUMNS, "employee_update_id"),
            ("weekly_project_updates", WEEKLY_UPDATE_COLUMNS, "update_id"),
        ]:
            for col in columns:
                if col != key_col:
                    db.execute(text(f"ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS {col} TEXT"))


    st.session_state["_dd_pg_schema_ready"] = True


def repair_proposal_workflow_text_schema():
    """Repair older Supabase schemas that used INTEGER/DOUBLE columns.

    Earlier prototype tables sometimes stored quote/budget/timeline fields as
    INTEGER. Once real proposal values grew or a legacy row had a quote in a
    timeline column, PostgreSQL raised `integer out of range`. The app reads
    values through safe_number/safe_int anyway, so keeping workflow columns as
    TEXT is the safest demo schema and avoids failed inserts from old tables.
    This repair is only run manually or after a schema-related insert failure.
    """
    if not postgres_config_available():
        return
    conn = get_pg_conn()
    with conn.engine.begin() as db:
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS proposal_decisions (
                proposal_id TEXT PRIMARY KEY
            )
        """))
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS proposal_decision_history (
                event_id TEXT PRIMARY KEY
            )
        """))
        for col in PROPOSAL_DECISION_COLUMNS:
            if col == "proposal_id":
                continue
            db.execute(text(f"ALTER TABLE proposal_decisions ADD COLUMN IF NOT EXISTS {col} TEXT"))
            db.execute(text(f"ALTER TABLE proposal_decisions ALTER COLUMN {col} TYPE TEXT USING {col}::TEXT"))
        for col in PROPOSAL_HISTORY_COLUMNS:
            if col == "event_id":
                continue
            db.execute(text(f"ALTER TABLE proposal_decision_history ADD COLUMN IF NOT EXISTS {col} TEXT"))
            db.execute(text(f"ALTER TABLE proposal_decision_history ALTER COLUMN {col} TYPE TEXT USING {col}::TEXT"))
    st.session_state["_dd_pg_schema_ready"] = True
    clear_workflow_read_cache()


def is_schema_numeric_range_error(exc):
    message = str(exc).lower()
    return (
        "integer out of range" in message
        or "numericvalueoutofrange" in message
        or "numeric value out of range" in message
        or "value out of range" in message
    )


def is_missing_column_error(exc):
    message = str(exc).lower()
    return (
        "undefinedcolumn" in message
        or "undefined column" in message
        or "does not exist" in message and "column" in message
    )


def workflow_table_columns(table_name):
    table_map = {
        "proposal_decisions": (PROPOSAL_DECISION_COLUMNS, "proposal_id"),
        "proposal_decision_history": (PROPOSAL_HISTORY_COLUMNS, "event_id"),
        "client_accounts": (CLIENT_ACCOUNT_COLUMNS, "client_id"),
        "client_responses": (CLIENT_RESPONSE_COLUMNS, "response_id"),
        "projects": (PROJECT_COLUMNS, "project_id"),
        "delivery_plans": (DELIVERY_PLAN_COLUMNS, "delivery_plan_id"),
        "project_allocations": (PROJECT_ALLOCATION_COLUMNS, "allocation_id"),
        "employee_notifications": (EMPLOYEE_NOTIFICATION_COLUMNS, "notification_id"),
        "employee_project_updates": (EMPLOYEE_PROJECT_UPDATE_COLUMNS, "employee_update_id"),
        "weekly_project_updates": (WEEKLY_UPDATE_COLUMNS, "update_id"),
    }
    return table_map.get(table_name)


def ensure_workflow_table_columns(table_name, columns=None, key_column=None, force=False):
    """Fast schema patch for one live Supabase workflow table.

    Lightweight mode intentionally avoids full schema repair on every page load.
    When a new version adds columns, old Supabase tables may be missing those
    columns until repaired. This helper upgrades only the table being written,
    so employee requests/client messages do not crash and we do not run the
    full CREATE/ALTER set on every dashboard click.
    """
    if not postgres_config_available():
        return
    if columns is None or key_column is None:
        mapped = workflow_table_columns(table_name)
        if not mapped:
            return
        columns, key_column = mapped

    cache_key = f"_dd_schema_cols_ready_{table_name}_{len(columns)}"
    if not force and st.session_state.get(cache_key):
        return

    conn = get_pg_conn()
    with conn.engine.begin() as db:
        db.execute(text(f"CREATE TABLE IF NOT EXISTS {table_name} ({key_column} TEXT PRIMARY KEY)"))
        for col in columns:
            if col != key_column:
                db.execute(text(f"ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS {col} TEXT"))

    st.session_state[cache_key] = True


def execute_with_schema_repair(sql, records, table_label="workflow"):
    """Execute insert/upsert records safely against legacy Supabase schemas.

    The old Supabase table may still have INTEGER / numeric workflow columns.
    Repairing only after failure can still leave the user seeing a crash if the
    failed transaction is surfaced by Streamlit. For proposal/history workflow
    writes, repair to TEXT once before inserting, then retry once if PostgreSQL
    still reports a numeric range/type problem.
    """
    if table_label in ["proposal_decisions", "proposal_decision_history"]:
        try:
            if not st.session_state.get("_dd_pg_text_schema_repaired", False):
                repair_proposal_workflow_text_schema()
                st.session_state["_dd_pg_text_schema_repaired"] = True
        except Exception as repair_exc:
            # Let the actual write attempt raise a useful error if repair cannot run.
            remember_postgres_error(repair_exc)

    conn = get_pg_conn()
    try:
        with conn.engine.begin() as db:
            for record in records:
                db.execute(sql, record)
        return
    except Exception as exc:
        if is_missing_column_error(exc):
            remember_postgres_error(exc)
            ensure_workflow_table_columns(table_label, force=True)
            conn = get_pg_conn()
            with conn.engine.begin() as db:
                for record in records:
                    db.execute(sql, record)
            return

        if not is_schema_numeric_range_error(exc):
            raise
        remember_postgres_error(exc)
        repair_proposal_workflow_text_schema()
        st.session_state["_dd_pg_text_schema_repaired"] = True
        conn = get_pg_conn()
        with conn.engine.begin() as db:
            for record in records:
                db.execute(sql, record)


PROPOSAL_NUMERIC_COLUMNS = [
    "client_budget",
    "employee_cost",
    "overhead",
    "cloud_cost",
    "software_cost",
    "contingency",
    "estimated_cost",
    "target_margin_percent",
    "recommended_quote",
    "expected_profit_at_client_budget",
    "profit_margin_at_client_budget",
    "total_skill_gap",
    "sales_recommended_quote",
    "finance_recommended_quote",
    "hr_recommended_quote",
    "operations_recommended_quote",
    "ceo_final_quote",
]

PROPOSAL_INTEGER_COLUMNS = [
    "timeline_months",
    "decision_version",
    "sales_recommended_timeline_months",
    "finance_recommended_timeline_months",
    "hr_recommended_timeline_months",
    "operations_recommended_timeline_months",
    "ceo_final_timeline_months",
]

HISTORY_NUMERIC_COLUMNS = ["recommended_quote"]
HISTORY_INTEGER_COLUMNS = ["recommended_timeline_months"]


def prepare_dataframe_for_postgres(df, numeric_columns=None, integer_columns=None):
    """Convert blank Excel-style cells to SQL NULL before inserting into PostgreSQL.

    The Supabase tables may have DOUBLE PRECISION / INTEGER columns. Pandas rows
    created for proposal defaults often contain empty strings for fields that are
    not decided yet, for example sales_recommended_quote = ''. PostgreSQL cannot
    insert '' into numeric columns, so those blanks must become NULL.
    """
    if numeric_columns is None:
        numeric_columns = []
    if integer_columns is None:
        integer_columns = []

    cleaned = df.copy()
    cleaned = cleaned.where(pd.notna(cleaned), None)

    for column in numeric_columns:
        if column in cleaned.columns:
            cleaned[column] = cleaned[column].replace("", None)
            cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")
            cleaned[column] = cleaned[column].where(pd.notna(cleaned[column]), None)

    for column in integer_columns:
        if column in cleaned.columns:
            cleaned[column] = cleaned[column].replace("", None)
            cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")
            cleaned[column] = cleaned[column].round()
            cleaned[column] = cleaned[column].where(pd.notna(cleaned[column]), None)

    for column in cleaned.columns:
        if column not in numeric_columns and column not in integer_columns:
            cleaned[column] = cleaned[column].where(pd.notna(cleaned[column]), None)

    return cleaned



def normalise_simple_store(df, columns):
    if df is None or df.empty:
        df = pd.DataFrame(columns=columns)
    for column in columns:
        if column not in df.columns:
            df[column] = ""
    ordered = columns + [col for col in df.columns if col not in columns]
    return df[ordered]


def read_client_accounts():
    if not postgres_config_available():
        return pd.DataFrame(columns=CLIENT_ACCOUNT_COLUMNS)
    try:
        ensure_postgres_tables()
        conn = get_pg_conn()
        df = conn.query("SELECT * FROM client_accounts", ttl=0)
        return normalise_simple_store(df, CLIENT_ACCOUNT_COLUMNS)
    except Exception as exc:
        remember_postgres_error(exc)
        return pd.DataFrame(columns=CLIENT_ACCOUNT_COLUMNS)


def write_client_account(row):
    if not postgres_config_available():
        require_postgres_or_raise()
    ensure_postgres_tables()
    clean_row = {col: safe_text(row.get(col, "")) for col in CLIENT_ACCOUNT_COLUMNS}
    conn = get_pg_conn()
    engine = conn.engine
    cols = CLIENT_ACCOUNT_COLUMNS
    values_clause = ", ".join([f":{c}" for c in cols])
    update_clause = ", ".join([f"{c}=EXCLUDED.{c}" for c in cols if c != "client_id"])
    sql = text(f"""
        INSERT INTO client_accounts ({', '.join(cols)})
        VALUES ({values_clause})
        ON CONFLICT (client_id) DO UPDATE SET {update_clause}
    """)
    with engine.begin() as db:
        db.execute(sql, clean_row)
    clear_workflow_read_cache()


def client_login(client_user_id, client_password):
    accounts = read_client_accounts()
    if accounts.empty:
        return None
    match = accounts[
        (accounts["client_user_id"].astype(str).str.strip().str.upper() == safe_text(client_user_id).strip().upper())
        & (accounts["client_password"].astype(str) == safe_text(client_password))
        & (accounts["account_status"].fillna("Active").astype(str).str.lower() == "active")
    ]
    if match.empty:
        return None
    account = match.iloc[0].to_dict()
    try:
        ensure_postgres_tables()
        conn = get_pg_conn()
        with conn.engine.begin() as db:
            db.execute(
                text("UPDATE client_accounts SET last_login_at = :now WHERE client_id = :client_id"),
                {"now": current_timestamp(), "client_id": account.get("client_id")},
            )
    except Exception:
        pass
    return account


def create_client_account_for_proposal(proposal_id, client_name, client_contact):
    client_id = make_client_id()
    client_user_id = make_client_user_id(client_id)
    client_password = make_client_password()
    row = {
        "client_id": client_id,
        "proposal_id": proposal_id,
        "client_name": client_name or "External Client",
        "client_contact": client_contact,
        "client_user_id": client_user_id,
        "client_password": client_password,
        "created_at": current_timestamp(),
        "last_login_at": "",
        "account_status": "Active",
    }
    write_client_account(row)
    return row


def build_client_credentials_text(report):
    """Generate a downloadable client-portal credential note."""
    client_name = report.get("client_name") or "Client"
    return f"""DecisionDesk AI - Client Portal Access

Dear {client_name},

Your proposal has been received and is now under internal executive review.
Use the below temporary credentials to track quotation status and future project updates.

Client User ID: {report.get('client_user_id', '')}
Temporary Password: {report.get('client_password', '')}

Login area: Client Portal
Proposal ID: {report.get('proposal_id', '')}

Security note: These are demo credentials for the hackathon prototype. In production, the client would be asked to reset the password on first login.

Regards,
VirtualTech Solutions
"""


def get_client_proposal_reports(client_account):
    proposal_id = safe_text(client_account.get("proposal_id")) if client_account else ""
    if not proposal_id:
        return []
    df = read_proposal_store(create_if_missing=True)
    if df.empty:
        return []
    matched = df[df["proposal_id"].astype(str) == proposal_id].copy()
    return [proposal_row_to_report(row) for _, row in matched.iterrows()]


def save_client_response(proposal_id, client_account, response, comment):
    response = safe_text(response)
    comment = safe_text(comment)
    client_id = safe_text(client_account.get("client_id"))
    now = current_timestamp()

    if response not in CLIENT_RESPONSE_OPTIONS:
        return False, "Please choose Accept, Decline, or Request Reconsideration."

    df = read_proposal_store(create_if_missing=True)
    if df.empty or "proposal_id" not in df.columns:
        return False, "No proposal records were found."
    mask = df["proposal_id"].astype(str) == str(proposal_id)
    if not mask.any():
        return False, "This proposal was not found."

    status_map = {
        "Accept Proposal": "Client Accepted - Delivery Readiness Pending",
        "Decline Proposal": "Client Declined - Closed",
        "Request Reconsideration": "Client Requested Reconsideration",
    }
    owner_map = {
        "Accept Proposal": "Operations / Delivery Planning",
        "Decline Proposal": "Sales / CEO Closure Review",
        "Request Reconsideration": "Sales / CEO Negotiation Review",
    }

    df.loc[mask, "client_id"] = client_id
    df.loc[mask, "client_response"] = response
    df.loc[mask, "client_response_comment"] = comment
    df.loc[mask, "client_response_at"] = now
    df.loc[mask, "workflow_status"] = status_map[response]
    df.loc[mask, "current_owner"] = owner_map[response]
    df.loc[mask, "last_updated_by"] = safe_text(client_account.get("client_name")) or "Client"
    df.loc[mask, "last_updated_role"] = "Client"
    df.loc[mask, "last_updated_at"] = now
    df.loc[mask, "last_update_summary"] = f"Client response received: {response}."
    for role_key, column in PROPOSAL_NOTIFICATION_COLUMNS.items():
        df.loc[mask, column] = "No"
        df.loc[mask, PROPOSAL_SEEN_AT_COLUMNS[role_key]] = ""
    upsert_current_proposal_from_df(df, mask)

    if postgres_config_available():
        ensure_postgres_tables()
        row = {
            "response_id": make_response_id(),
            "proposal_id": proposal_id,
            "client_id": client_id,
            "response": response,
            "comment": comment,
            "responded_at": now,
        }
        conn = get_pg_conn()
        with conn.engine.begin() as db:
            db.execute(
                text("""
                    INSERT INTO client_responses
                    (response_id, proposal_id, client_id, response, comment, responded_at)
                    VALUES (:response_id, :proposal_id, :client_id, :response, :comment, :responded_at)
                """),
                row,
            )

    if response == "Accept Proposal":
        try:
            latest_df = read_proposal_store(create_if_missing=True)
            latest_match = latest_df[latest_df["proposal_id"].astype(str) == str(proposal_id)]
            if not latest_match.empty:
                updated_report = proposal_row_to_report(latest_match.iloc[0])
                ensure_project_for_accepted_proposal(updated_report, client_account)
        except Exception:
            pass

    return True, f"Your response was saved: {response}. Our team has been notified."



# ---------------- DYNAMIC COMPANY PERFORMANCE ----------------

def get_dynamic_company_performance(data):
    """Measure company performance from Supabase dynamic project workflow.

    Excel stays the static source for employee master, salary, attendance, and fixed expenses.
    Supabase is the source for live proposals, accepted projects, allocations, and employee updates.
    """
    proposals = read_proposal_store(create_if_missing=False)
    projects = read_simple_table("projects", PROJECT_COLUMNS)
    allocations = read_simple_table("project_allocations", PROJECT_ALLOCATION_COLUMNS)
    employee_updates = read_simple_table("employee_project_updates", EMPLOYEE_PROJECT_UPDATE_COLUMNS)

    employees = data.get("employees", pd.DataFrame()).copy()
    expenses = data.get("expenses", pd.DataFrame()).copy()
    payroll = data.get("payroll", pd.DataFrame()).copy()

    total_static_expense = safe_number(expenses["monthly_cost"].sum()) if not expenses.empty and "monthly_cost" in expenses.columns else 0
    employee_count = len(employees) if not employees.empty else 0

    if projects.empty:
        adjusted_employees = adjust_employee_availability_with_dynamic_allocations(employees) if not employees.empty else employees
        available_people = 0
        if adjusted_employees is not None and not adjusted_employees.empty and "availability_percent" in adjusted_employees.columns:
            available_people = int((pd.to_numeric(adjusted_employees["availability_percent"], errors="coerce").fillna(0) >= 50).sum())
        return {
            "source": "Supabase dynamic workflow tables",
            "active_projects": 0,
            "total_projects": 0,
            "total_revenue": 0.0,
            "estimated_delivery_cost": 0.0,
            "estimated_profit": 0.0,
            "company_margin_percent": 0.0,
            "average_dynamic_allocation_percent": 0.0,
            "available_people": available_people,
            "employee_count": employee_count,
            "monthly_static_expenses": total_static_expense,
            "high_attention_projects": 0,
            "company_health": "No dynamic project data yet",
            "project_rows": [],
        }

    proposal_lookup = {}
    if proposals is not None and not proposals.empty:
        for _, row in proposals.iterrows():
            proposal_lookup[safe_text(row.get("proposal_id"))] = row.to_dict()

    project_rows = []
    total_revenue = 0.0
    total_cost = 0.0
    high_attention_projects = 0

    for _, project in projects.iterrows():
        proposal_id = safe_text(project.get("proposal_id"))
        proposal = proposal_lookup.get(proposal_id, {})
        quote = safe_number(proposal.get("ceo_final_quote")) or safe_number(proposal.get("recommended_quote"))
        cost = safe_number(proposal.get("estimated_cost"))
        profit = quote - cost
        margin = (profit / quote * 100) if quote else 0
        status = safe_text(project.get("project_status"), "Planning")

        project_allocations = allocations[allocations["project_id"].astype(str) == safe_text(project.get("project_id"))] if not allocations.empty else pd.DataFrame()
        allocated_count = 0 if project_allocations.empty else len(project_allocations)

        project_updates = employee_updates[employee_updates["project_id"].astype(str) == safe_text(project.get("project_id"))] if not employee_updates.empty else pd.DataFrame()
        latest_update_status = ""
        if not project_updates.empty:
            project_updates = project_updates.sort_values("created_at", ascending=False)
            latest_update_status = safe_text(project_updates.iloc[0].get("progress_status"))
            if latest_update_status in ["Blocked", "Minor risk"]:
                high_attention_projects += 1

        total_revenue += quote
        total_cost += cost
        project_rows.append({
            "Project ID": safe_text(project.get("project_id")),
            "Project": safe_text(project.get("project_name")),
            "Status": status,
            "Quote/Revenue": quote,
            "Estimated Cost": cost,
            "Estimated Profit": profit,
            "Margin %": round(margin, 2),
            "Allocated Employees": allocated_count,
            "Latest Team Status": latest_update_status or "No update yet",
        })

    total_profit = total_revenue - total_cost
    company_margin = (total_profit / total_revenue * 100) if total_revenue else 0

    dynamic_used_percent = 0.0
    if not allocations.empty:
        active_allocations = allocations.copy()
        if "allocation_status" in active_allocations.columns:
            active_allocations = active_allocations[active_allocations["allocation_status"].fillna("Active").astype(str).str.lower() == "active"]
        dynamic_used_percent = safe_number(pd.to_numeric(active_allocations.get("allocation_percent", 0), errors="coerce").fillna(0).sum())
    average_dynamic_allocation = (dynamic_used_percent / employee_count) if employee_count else 0

    adjusted_employees = adjust_employee_availability_with_dynamic_allocations(employees) if not employees.empty else employees
    available_people = 0
    if adjusted_employees is not None and not adjusted_employees.empty and "availability_percent" in adjusted_employees.columns:
        available_people = int((pd.to_numeric(adjusted_employees["availability_percent"], errors="coerce").fillna(0) >= 50).sum())

    active_projects = 0
    for _, project in projects.iterrows():
        status = safe_text(project.get("project_status")).lower()
        if not any(closed in status for closed in ["closed", "declined", "completed", "cancelled"]):
            active_projects += 1

    if total_revenue == 0 and active_projects == 0:
        health = "No dynamic project data yet"
    elif company_margin >= 30 and high_attention_projects == 0:
        health = "Strong"
    elif company_margin >= 20 and high_attention_projects <= 1:
        health = "Moderate"
    else:
        health = "Needs Attention"

    return {
        "source": "Supabase dynamic workflow tables + Excel static payroll/expense context",
        "active_projects": active_projects,
        "total_projects": len(projects),
        "total_revenue": round(total_revenue, 2),
        "estimated_delivery_cost": round(total_cost, 2),
        "estimated_profit": round(total_profit, 2),
        "company_margin_percent": round(company_margin, 2),
        "average_dynamic_allocation_percent": round(average_dynamic_allocation, 2),
        "available_people": available_people,
        "employee_count": employee_count,
        "monthly_static_expenses": round(total_static_expense, 2),
        "high_attention_projects": high_attention_projects,
        "company_health": health,
        "project_rows": project_rows,
    }


def run_company_health_workflow(data):
    """CEO/company performance uses dynamic Supabase project data, not static Excel projects."""
    performance = get_dynamic_company_performance(data)
    fallback = (
        f"Company health: {performance['company_health']}. "
        f"Active dynamic projects: {performance['active_projects']}. "
        f"Revenue INR {performance['total_revenue']:,.0f}, estimated cost INR {performance['estimated_delivery_cost']:,.0f}, "
        f"estimated profit INR {performance['estimated_profit']:,.0f}, margin {performance['company_margin_percent']}%. "
        f"Available people after live allocations: {performance['available_people']}/{performance['employee_count']}."
    )
    if not USE_LLM_FOR_LONG_DOCUMENTS:
        return {"performance": performance, "llm_response": fallback}

    prompt = f"""
You are the CEO Agent. Analyze company performance using only this data.
This performance is based on Supabase dynamic projects/proposals/allocations and Excel static payroll/expense context.
Do not use static Excel projects as the source of live project performance.

{json.dumps(performance, ensure_ascii=False)}

Give:
1. Company health summary
2. Dynamic project/revenue interpretation
3. Operations capacity interpretation
4. Hiring/resource concern
5. CEO recommendation
"""
    return {"performance": performance, "llm_response": ask_llm(prompt, fallback=fallback)}


def render_company_performance_dashboard(data):
    health = run_company_health_workflow(data)
    perf = health.get("performance", {})
    st.markdown("### Dynamic company performance")
    # st.caption("Measured from Supabase dynamic workflow tables. Excel is used only for static employee/payroll/expense context.")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Active Projects", perf.get("active_projects", 0))
    c2.metric("Revenue", money_text(perf.get("total_revenue", 0)))
    c3.metric("Estimated Profit", money_text(perf.get("estimated_profit", 0)))
    c4.metric("Margin", f"{perf.get('company_margin_percent', 0)}%")
    c5, c6, c7 = st.columns(3)
    c5.metric("Available People", f"{perf.get('available_people', 0)} / {perf.get('employee_count', 0)}")
    c6.metric("Avg Live Allocation", f"{perf.get('average_dynamic_allocation_percent', 0)}%")
    c7.metric("Health", perf.get("company_health", "Unknown"))
    st.write(health.get("llm_response", ""))
    rows = perf.get("project_rows", [])
    if rows:
        with st.expander("Dynamic project performance details", expanded=False):
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.info("No Supabase dynamic projects are available yet. Once clients accept proposals and projects are created, performance will populate here.")



def get_latest_quote_summary(report):
    """Return client-safe latest quotation summary for proposal/client/operations dashboards."""
    analysis = report.get("analysis", {}) if isinstance(report, dict) else {}
    final_quote = safe_number(report.get("ceo_final_quote") or analysis.get("recommended_quote"), 0)
    final_timeline = safe_int(report.get("ceo_final_timeline_months") or analysis.get("timeline_months"), 0)
    return {
        "quote_amount": final_quote,
        "timeline_months": final_timeline,
        "quotation_text": safe_text(report.get("client_quotation")),
        "quotation_generated_at": safe_text(report.get("quotation_generated_at")),
        "quotation_sent": safe_text(report.get("quotation_sent"), "No"),
        "client_response": safe_text(report.get("client_response"), "Not responded yet"),
        "client_response_at": safe_text(report.get("client_response_at")),
    }


def render_latest_quotation_panel(report, *, title="Latest quotation sent", expanded=False, key_prefix="latest_quote"):
    """Compact client-safe quotation panel.

    Used after CEO sends the quote, including CEO-bypass cases where other
    executive decisions are still blank. It shows only the latest quote status,
    client response, and an optional dropdown/expander to view the actual quote.
    """
    if not isinstance(report, dict):
        return
    summary = get_latest_quote_summary(report)
    has_quote = bool(summary["quotation_text"].strip())
    if not has_quote:
        return

    proposal_id = safe_text(report.get("proposal_id")) or "proposal"
    st.markdown(
        f"""
        <div class="dd-info-strip">
            <strong>{title}</strong>
            <span>Client response: {summary['client_response']}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    q1, q2, q3 = st.columns(3)
    q1.metric("Quotation amount", money_text(summary["quote_amount"]))
    q2.metric("Timeline", f"{summary['timeline_months']} month(s)" if summary["timeline_months"] else "Not specified")
    q3.metric("Client status", summary["client_response"])
    if summary["quotation_generated_at"]:
        st.caption(f"Latest quotation sent/updated at: {summary['quotation_generated_at']}")
    if summary["client_response_at"]:
        st.caption(f"Client responded at: {summary['client_response_at']}")

    with st.expander("View latest quotation sent", expanded=expanded):
        st.text_area(
            "Latest quotation sent to client",
            value=summary["quotation_text"],
            height=240,
            disabled=True,
            key=f"{key_prefix}_{proposal_id}",
        )


def get_proposal_report_by_id(proposal_id):
    proposal_id = safe_text(proposal_id)
    if not proposal_id:
        return None
    try:
        df = read_proposal_store(create_if_missing=True)
        if df.empty or "proposal_id" not in df.columns:
            return None
        matched = df[df["proposal_id"].astype(str) == proposal_id]
        if matched.empty:
            return None
        return proposal_row_to_report(matched.iloc[0])
    except Exception:
        return None

def is_client_delivery_kickstarted(report):
    """Return True after accepted proposal has moved into delivery execution.

    Once delivery is started/approved/team-allocated, the client portal should
    stop showing quotation/proposal-response details and show only the
    client-safe weekly delivery view.
    """
    if safe_text(report.get("client_response")) != "Accept Proposal":
        return False

    project = get_project_for_proposal(report.get("proposal_id"))
    if not project:
        return False

    project_id = safe_text(project.get("project_id"))
    project_status = safe_text(project.get("project_status")).lower()
    plan = get_delivery_plan_for_client_project(project_id)
    plan_status = safe_text(plan.get("approval_status") if plan else "").lower()

    try:
        allocations = get_project_allocations(project_id)
        has_allocation = allocations is not None and not allocations.empty
    except Exception:
        has_allocation = False

    delivery_started_words = [
        "approved",
        "allocated",
        "in progress",
        "delivery",
        "active",
        "kickoff",
    ]
    return (
        has_allocation
        or any(word in plan_status for word in delivery_started_words)
        or any(word in project_status for word in delivery_started_words)
    )


def render_client_active_delivery_only(report, client_account):
    """Client-safe delivery view after project kickoff.

    This intentionally hides proposal-stage text, quotation decision summaries,
    internal approval trail, employee names, blockers, and delivery-plan details.
    """
    st.markdown(
        """
        <div class="dd-dashboard-shell">
            <div class="dd-title-row">
                <div>
                    <div class="dd-section-title">Project delivery update</div>
                    <div class="dd-section-subtitle">Your project is active. Team work is going on.</div>
                </div>
                <div class="dd-title-badge">Client-safe view</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_client_delivery_section(report, client_account)


def render_client_dashboard(client_account):
    st.markdown(
        f"""
        <div class=\"dd-section-card\">
            <div class=\"dd-section-title\">Client Portal</div>
            <div class=\"dd-section-subtitle\">
                Welcome {safe_text(client_account.get('client_name'), 'Client')}. This portal shows only client-safe proposal status, quotation, and next steps.
            </div>
            <div class=\"dd-muted-small\">Client ID: <b>{safe_text(client_account.get('client_id'))}</b></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    reports = get_client_proposal_reports(client_account)
    if not reports:
        st.warning("No proposal is linked to this client account yet.")
        return

    for report in reports:
        analysis = report["analysis"]
        if is_client_delivery_kickstarted(report):
            render_client_active_delivery_only(report, client_account)
            continue

        st.markdown(
            """
            <div class="dd-dashboard-shell">
                <div class="dd-title-row">
                    <div>
                        <div class="dd-section-title">Proposal status</div>
                        <div class="dd-section-subtitle">Latest company quotation and response options.</div>
                    </div>
                    <div class="dd-title-badge">Recent first</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Project", analysis.get("project_type", "Project"))
        c2.metric("Status", report.get("workflow_status", "Under review"))
        c3.metric("Timeline", f"{analysis.get('timeline_months', 0)} months")
        c4.metric("Quotation Sent", report.get("quotation_sent", "No"))

        st.info(
            "Your proposal is being handled by our internal Sales, HR, Finance, Operations, and CEO team. "
            "Internal comments, cost, margin, and employee-level details are private."
        )

        quotation = report.get("client_quotation")
        if quotation:
            existing_response = safe_text(report.get("client_response"))
            quote_label = "Reconsidered quote sent by company" if existing_response == "Request Reconsideration" else "CEO-approved quotation"
            st.markdown("#### Company quotation")
            if existing_response == "Request Reconsideration":
                quote_time = safe_text(report.get("quotation_generated_at"))
                st.markdown(
                    f"""
                    <div class="dd-quote-update-card">
                        <b>Your previous response was:</b> Request Reconsideration<br/>
                        <b>The reconsidered quote from our company is given below.</b>
                        <div class="dd-small-line">You can now accept, decline, or request another reconsideration from this same panel.</div>
                        {f'<div class="dd-small-line">Latest quote updated at: {quote_time}</div>' if quote_time else ''}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            elif existing_response:
                st.success(f"Your current response: {existing_response}")
                if safe_text(report.get("client_response_comment")):
                    st.caption(f"Your note: {safe_text(report.get('client_response_comment'))}")

            already_final_response = existing_response in ["Accept Proposal", "Decline Proposal"]
            if already_final_response:
                render_latest_quotation_panel(
                    report,
                    title="Quotation and client decision summary",
                    expanded=False,
                    key_prefix="client_final_quote",
                )
            else:
                st.text_area(
                    quote_label,
                    value=quotation,
                    height=260,
                    key=f"client_quote_{report.get('proposal_id')}",
                    disabled=True,
                )

            can_respond_to_quote = not already_final_response

            if can_respond_to_quote:
                form_title = "Respond to reconsidered quote" if existing_response == "Request Reconsideration" else "Submit response"
                with st.form(f"client_response_form_{report.get('proposal_id')}_{existing_response or 'new'}"):
                    default_index = 0
                    response = st.radio("Your response", CLIENT_RESPONSE_OPTIONS, index=default_index, horizontal=True)
                    comment_label = "Optional note for the company team"
                    if existing_response == "Request Reconsideration":
                        comment_label = "Optional note about this reconsidered quotation"
                    comment = st.text_area(comment_label, height=90)
                    submitted = st.form_submit_button(form_title, type="primary")
                if submitted:
                    ok, msg = save_client_response(report.get("proposal_id"), client_account, response, comment)
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
            render_client_delivery_section(report, client_account)
        else:
            st.warning("Quotation is not ready yet. Please check this dashboard later for CEO-approved updates.")



def read_simple_table(table_name, columns):
    if not postgres_config_available():
        return pd.DataFrame(columns=columns)
    try:
        ensure_postgres_tables()
        conn = get_pg_conn()
        df = conn.query(f"SELECT * FROM {table_name}", ttl=0)
        return normalise_simple_store(df, columns)
    except Exception as exc:
        remember_postgres_error(exc)
        return pd.DataFrame(columns=columns)


def upsert_simple_row(table_name, key_column, columns, row):
    if not postgres_config_available():
        require_postgres_or_raise()
    ensure_postgres_tables()
    ensure_workflow_table_columns(table_name, columns, key_column)
    prepared = {col: safe_text(row.get(col, "")) for col in columns}
    values_clause = ", ".join([f":{c}" for c in columns])
    update_clause = ", ".join([f"{c}=EXCLUDED.{c}" for c in columns if c != key_column])
    sql = text(f"""
        INSERT INTO {table_name} ({', '.join(columns)})
        VALUES ({values_clause})
        ON CONFLICT ({key_column}) DO UPDATE SET {update_clause}
    """)
    execute_with_schema_repair(sql, [prepared], table_label=table_name)
    clear_workflow_read_cache()


def insert_simple_row(table_name, columns, row):
    if not postgres_config_available():
        require_postgres_or_raise()
    ensure_postgres_tables()
    mapped = workflow_table_columns(table_name)
    key_column = mapped[1] if mapped else columns[0]
    ensure_workflow_table_columns(table_name, columns, key_column)
    prepared = {col: safe_text(row.get(col, "")) for col in columns}
    values_clause = ", ".join([f":{c}" for c in columns])
    sql = text(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({values_clause})")
    execute_with_schema_repair(sql, [prepared], table_label=table_name)
    clear_workflow_read_cache()


def get_project_for_proposal(proposal_id):
    projects = read_simple_table("projects", PROJECT_COLUMNS)
    if projects.empty:
        return None
    matched = projects[projects["proposal_id"].astype(str) == safe_text(proposal_id)]
    if matched.empty:
        return None
    return matched.iloc[0].to_dict()


def ensure_project_for_accepted_proposal(report, client_account):
    proposal_id = safe_text(report.get("proposal_id"))
    client_id = safe_text(client_account.get("client_id"))
    existing = get_project_for_proposal(proposal_id)
    if existing:
        return existing
    project_id = make_project_id()
    project_type = safe_text(report.get("analysis", {}).get("project_type"), "Client Project")
    client_name = safe_text(client_account.get("client_name"), report.get("client_name", "Client"))
    now = current_timestamp()
    row = {
        "project_id": project_id,
        "proposal_id": proposal_id,
        "client_id": client_id,
        "project_name": f"{client_name} - {project_type}",
        "project_status": "Client Accepted - Awaiting Detailed Requirement",
        "operations_owner_id": "",
        "operations_owner_name": "Operations Executive",
        "kickoff_date": "",
        "created_at": now,
        "updated_at": now,
    }
    upsert_simple_row("projects", "project_id", PROJECT_COLUMNS, row)
    try:
        df = read_proposal_store(create_if_missing=True)
        mask = df["proposal_id"].astype(str) == proposal_id
        if mask.any():
            df.loc[mask, "project_id"] = project_id
            df.loc[mask, "project_created"] = "Yes"
            df.loc[mask, "project_created_at"] = now
            df.loc[mask, "workflow_status"] = "Project Created - Awaiting Detailed Requirement"
            df.loc[mask, "current_owner"] = "Client / Operations"
            df.loc[mask, "last_updated_at"] = now
            df.loc[mask, "last_update_summary"] = "Client accepted quotation; delivery project shell was created."
            upsert_current_proposal_from_df(df, mask)
    except Exception:
        pass
    append_proposal_history(
        proposal_id,
        {"user_id": "SYSTEM", "employee_name": "Delivery Automation", "designation": "System"},
        "Project Created",
        summary=f"Accepted proposal converted to project {project_id} for delivery readiness.",
    )
    return row


def build_operations_agent_delivery_plan(report, requirement_text):
    analysis = report.get("analysis", {})
    fallback = f"""Operations Agent Delivery Readiness Plan

1. Business Objective
Deliver {analysis.get('project_type', 'the requested solution')} for the client based on the accepted quotation and detailed requirement.

2. Functional Requirements
- User-facing workflow based on the client requirement
- Admin/operations dashboard for managing core records
- Reporting/status visibility for the client
- Role-based access for internal users and client users

3. Suggested Tools and Software
- Frontend / App: Streamlit for prototype, React or enterprise web UI for production
- Backend: Python services / FastAPI when APIs are needed
- Database: Supabase PostgreSQL
- AI Layer: OpenAI-compatible API for assistant, summarization, and automation
- Document Handling: PDF/DOCX/text extraction pipeline
- Version Control: GitHub

4. Cloud and Access Plan
- Host application on Streamlit Cloud or enterprise cloud app hosting
- Keep API keys and database URLs in secrets, not source code
- Separate client, employee, executive, and operations access
- Restrict client view to quotation, weekly updates, and approved project information

5. Security and Access Requirements
- Client can see quotation, project status, weekly updates, and operations contact only
- Employees can see assigned project requirements and their own module context
- Executives can see internal decision room based on role
- Finance/margin/salary/internal comments remain hidden from client and normal employees

6. Module Breakdown
- Client portal and authentication
- Proposal and quotation status
- Detailed requirement processing
- Operations delivery planning
- Employee allocation and notifications
- Weekly client update generation

7. Roles Needed
- Operations Manager / Project Owner
- Backend Developer
- Frontend Developer
- AI/ML Engineer
- QA Engineer
- DevOps Engineer

8. Risks / Blockers
- Requirement scope must be confirmed before kickoff
- Client dependencies and integrations must be clarified
- Cloud and security expectations need approval

9. Client Clarifications Needed
- Final feature priority
- User roles and permissions
- External integrations
- Branding/UI expectations
- Deployment preference
"""
    if LIGHTWEIGHT_FAST_MODE and not USE_LLM_FOR_LONG_DOCUMENTS:
        return fallback

    prompt = f"""
You are the Operations Agent for an IT services company.
Create a delivery-readiness plan from the accepted quotation and detailed client requirement.
Do not reveal internal margin, salary, or executive comments.

Client: {report.get('client_name')}
Project type: {analysis.get('project_type')}
Approved quotation/timeline context: quote {analysis.get('recommended_quote')}, timeline {analysis.get('timeline_months')} months
Original proposal: {report.get('raw_client_message')}
Detailed requirement: {requirement_text}

Return a professional structured plan with these sections:
1. Business objective
2. Functional requirements
3. Non-functional requirements
4. Suggested tools/software
5. Cloud/deployment/access plan
6. Security/access requirements
7. Module breakdown
8. Roles needed
9. Risks/blockers
10. Client clarifications needed
"""
    return ask_llm(prompt, fallback=fallback)


def save_client_detailed_requirement(report, client_account, requirement_text, uploaded_file_name=""):
    requirement_text = safe_text(requirement_text).strip()
    if len(requirement_text) < 20:
        return False, "Please provide a more detailed requirement before submitting."
    project = ensure_project_for_accepted_proposal(report, client_account)
    now = current_timestamp()
    plan_text = build_operations_agent_delivery_plan(report, requirement_text)
    row = {
        "delivery_plan_id": make_delivery_plan_id(),
        "project_id": project.get("project_id"),
        "proposal_id": report.get("proposal_id"),
        "client_id": client_account.get("client_id"),
        "requirement_source": "Client Portal Text/File",
        "uploaded_file_name": uploaded_file_name,
        "raw_requirement_text": requirement_text,
        "operations_agent_plan": plan_text,
        "operations_manager_plan": plan_text,
        "suggested_tools": "See Operations Agent plan",
        "cloud_plan": "See Operations Agent plan",
        "security_plan": "See Operations Agent plan",
        "module_breakdown": "See Operations Agent plan",
        "risks_and_blockers": "See Operations Agent plan",
        "client_clarifications_needed": "Please confirm final feature priorities, user roles and permissions, external integrations, branding/UI expectations, and deployment preference.",
        "approval_status": "Operations Agent Drafted - Manager Review Pending",
        "approved_by": "",
        "approved_at": "",
        "created_at": now,
        "updated_at": now,
    }
    upsert_simple_row("delivery_plans", "delivery_plan_id", DELIVERY_PLAN_COLUMNS, row)
    try:
        df = read_proposal_store(create_if_missing=True)
        mask = df["proposal_id"].astype(str) == safe_text(report.get("proposal_id"))
        if mask.any():
            df.loc[mask, "workflow_status"] = "Detailed Requirement Submitted - Operations Review Pending"
            df.loc[mask, "current_owner"] = "Operations Manager"
            df.loc[mask, "operations_seen"] = "No"
            df.loc[mask, "operations_seen_at"] = ""
            df.loc[mask, "last_updated_by"] = safe_text(client_account.get("client_name"), "Client")
            df.loc[mask, "last_updated_role"] = "Client"
            df.loc[mask, "last_updated_at"] = now
            df.loc[mask, "last_update_summary"] = "Client submitted detailed requirement. Operations Agent created delivery plan for manager review."
            upsert_current_proposal_from_df(df, mask)
    except Exception:
        pass
    append_proposal_history(
        report.get("proposal_id"),
        {"user_id": safe_text(client_account.get("client_user_id")), "employee_name": safe_text(client_account.get("client_name")), "designation": "Client"},
        "Detailed Requirement Submitted",
        summary="Client submitted detailed requirement; Operations Agent created delivery plan.",
    )
    return True, "Detailed requirement submitted. Operations Agent has created a delivery plan and notified the Operations Manager."


def get_delivery_plans_for_project(project_id):
    plans = read_simple_table("delivery_plans", DELIVERY_PLAN_COLUMNS)
    if plans.empty:
        return plans
    matched = plans[plans["project_id"].astype(str) == safe_text(project_id)].copy()
    if not matched.empty and "created_at" in matched.columns:
        matched = matched.sort_values("created_at", ascending=False)
    return matched


def get_delivery_plan_for_client_project(project_id):
    plans = get_delivery_plans_for_project(project_id)
    if plans.empty:
        return None
    return plans.iloc[0].to_dict()


def get_project_allocations(project_id):
    allocations = read_simple_table("project_allocations", PROJECT_ALLOCATION_COLUMNS)
    if allocations.empty:
        return allocations
    return allocations[allocations["project_id"].astype(str) == safe_text(project_id)].copy()


def get_employee_notifications(employee_id):
    notifications = read_simple_table("employee_notifications", EMPLOYEE_NOTIFICATION_COLUMNS)
    if notifications.empty:
        return notifications
    matched = notifications[notifications["employee_id"].astype(str).str.upper() == safe_text(employee_id).upper()].copy()
    if not matched.empty and "created_at" in matched.columns:
        matched = matched.sort_values("created_at", ascending=False)
    return matched


def get_employee_allocations(employee_id):
    allocations = read_simple_table("project_allocations", PROJECT_ALLOCATION_COLUMNS)
    if allocations.empty:
        return allocations
    return allocations[allocations["employee_id"].astype(str).str.upper() == safe_text(employee_id).upper()].copy()


def get_employee_project_updates(project_id=None, employee_id=None):
    updates = read_simple_table("employee_project_updates", EMPLOYEE_PROJECT_UPDATE_COLUMNS)
    if updates.empty:
        return updates
    matched = updates.copy()
    if project_id:
        matched = matched[matched["project_id"].astype(str) == safe_text(project_id)]
    if employee_id:
        matched = matched[matched["employee_id"].astype(str).str.upper() == safe_text(employee_id).upper()]
    if not matched.empty and "created_at" in matched.columns:
        matched = matched.sort_values("created_at", ascending=False)
    return matched




def get_open_employee_project_updates(project_id=None, employee_id=None):
    """Employee requests/updates that Operations has not marked as done."""
    updates = get_employee_project_updates(project_id=project_id, employee_id=employee_id)
    if updates.empty:
        return updates
    if "operations_status" not in updates.columns:
        updates["operations_status"] = "Open"
    status = updates["operations_status"].fillna("Open").astype(str).str.lower().str.strip()
    open_updates = updates[~status.isin(["done", "closed", "resolved", "completed"])]
    return open_updates.copy()


def mark_employee_project_update_done(employee_update_id, user, resolution_note=""):
    """Close one employee update/request so it disappears from the Operations active dashboard."""
    update_id = safe_text(employee_update_id).strip()
    if not update_id:
        return False, "No employee update selected."
    if not postgres_config_available():
        require_postgres_or_raise()
    ensure_postgres_tables()
    now = current_timestamp()
    sql = text("""
        UPDATE employee_project_updates
        SET operations_status = :status,
            operations_done_by = :done_by,
            operations_done_at = :done_at,
            operations_resolution_note = :note
        WHERE employee_update_id = :update_id
    """)
    try:
        conn = get_pg_conn()
        with conn.engine.begin() as db:
            db.execute(sql, {
                "status": "Done",
                "done_by": actor_name(user),
                "done_at": now,
                "note": safe_text(resolution_note),
                "update_id": update_id,
            })
        clear_workflow_read_cache()
        return True, "Marked as done. This request/update is removed from the active Operations dashboard."
    except Exception as exc:
        remember_postgres_error(exc)
        return False, f"Could not mark this request as done: {exc}"


def mark_employee_notification_done(notification_id, user=None):
    """Mark a project notification as reviewed/done for Operations."""
    notif_id = safe_text(notification_id).strip()
    if not notif_id:
        return False, "No notification selected."
    if not postgres_config_available():
        require_postgres_or_raise()
    ensure_postgres_tables()
    sql = text("""
        UPDATE employee_notifications
        SET seen = 'Yes', seen_at = :seen_at
        WHERE notification_id = :notification_id
    """)
    try:
        conn = get_pg_conn()
        with conn.engine.begin() as db:
            db.execute(sql, {"seen_at": current_timestamp(), "notification_id": notif_id})
        clear_workflow_read_cache()
        return True, "Notification marked as done."
    except Exception as exc:
        remember_postgres_error(exc)
        return False, f"Could not mark notification as done: {exc}"

def get_operations_notification_recipients(project_id=""):
    """Return Operations Executive user IDs that should receive delivery/update alerts."""
    recipients = []

    # Prefer the actual Operations owner for this project if it has been assigned.
    try:
        projects = read_simple_table("projects", PROJECT_COLUMNS)
        if not projects.empty and project_id:
            match = projects[projects["project_id"].astype(str) == safe_text(project_id)]
            if not match.empty:
                owner_id = safe_text(match.iloc[0].get("operations_owner_id"))
                if owner_id:
                    recipients.append(owner_id.upper())
    except Exception:
        pass

    # Also notify all Operations executives from the Users sheet as a fallback.
    try:
        users = pd.read_excel(DB_PATH, sheet_name="Users")
        for _, row in users.iterrows():
            role = safe_text(row.get("role")).lower()
            department = safe_text(row.get("department")).lower()
            designation = safe_text(row.get("designation")).lower()
            user_id = safe_text(row.get("user_id")).upper()
            if user_id and ("operation" in department or "operation" in designation) and role in ["executive", "founder"]:
                recipients.append(user_id)
    except Exception:
        pass

    # Remove blanks/duplicates while preserving order.
    clean = []
    for item in recipients:
        if item and item not in clean:
            clean.append(item)
    return clean


def analyze_employee_update_with_llm(alloc, user, progress_status, progress_percent, hurdles, support_needed, notes):
    """Use the LLM, not keyword/regex matching, to understand employee delivery updates.

    Employees may describe risk in many styles and languages. The Operations Agent
    should infer whether Operations needs to step in, what the problem is, and how
    urgent it is from the full update context. The fallback is conservative: if the
    LLM is unavailable, Operations still gets an alert for human review rather than
    silently missing a potential blocker.
    """
    context = {
        "employee_name": actor_name(user),
        "employee_id": actor_id(user),
        "project_id": safe_text(alloc.get("project_id")),
        "project_role": safe_text(alloc.get("project_role")),
        "assigned_module": safe_text(alloc.get("assigned_module")),
        "responsibility_summary": safe_text(alloc.get("responsibility_summary")),
        "selected_status": safe_text(progress_status),
        "progress_percent": safe_text(progress_percent),
        "employee_hurdles_field": safe_text(hurdles),
        "employee_support_field": safe_text(support_needed),
        "employee_notes_field": safe_text(notes),
    }

    fallback = json.dumps({
        "needs_operations_attention": True,
        "urgency": "Review",
        "problem_summary": "LLM review was unavailable, so Operations should review the employee update manually.",
        "recommended_action": "Open the employee update and decide whether follow-up, access, clarification, or backup support is needed.",
        "client_safe_summary": "Internal delivery update received from the project team.",
        "confidence": 0.5,
    })

    prompt = f"""
You are DecisionDesk AI's Operations Agent.
Read the employee's weekly project update and decide whether the Operations Executive needs to take action.
Do not use keyword matching. Understand the meaning, tone, and delivery risk.

Return only valid JSON with these keys:
- needs_operations_attention: boolean
- urgency: one of [No action, Watch, Review, Urgent]
- problem_summary: one concise sentence explaining the real issue, or say no issue reported
- recommended_action: one concise instruction for the Operations Executive
- client_safe_summary: one client-safe sentence that does not reveal internal access credentials or private employee issues
- confidence: number between 0 and 1

Project and employee context:
{json.dumps(context, ensure_ascii=False)}
"""
    try:
        raw = ask_llm(prompt, fallback=fallback)
        parsed = json.loads(safe_text(raw).strip())
        return {
            "needs_operations_attention": bool(parsed.get("needs_operations_attention", True)),
            "urgency": safe_text(parsed.get("urgency"), "Review"),
            "problem_summary": safe_text(parsed.get("problem_summary"), "Employee update needs Operations review."),
            "recommended_action": safe_text(parsed.get("recommended_action"), "Review the employee update."),
            "client_safe_summary": safe_text(parsed.get("client_safe_summary"), "Project team update received."),
            "confidence": safe_number(parsed.get("confidence"), 0.5),
        }
    except Exception:
        return json.loads(fallback)


def save_employee_project_update(alloc, user, progress_status, progress_percent, hurdles, support_needed, notes):
    now = current_timestamp()
    project_id = safe_text(alloc.get("project_id"))
    proposal_id = safe_text(alloc.get("proposal_id"))
    module = safe_text(alloc.get("assigned_module"))
    status_text = safe_text(progress_status)
    hurdles_text = safe_text(hurdles).strip()
    support_text = safe_text(support_needed).strip()
    notes_text = safe_text(notes).strip()

    agent_review = analyze_employee_update_with_llm(
        alloc, user, status_text, progress_percent, hurdles_text, support_text, notes_text
    )

    row = {column: "" for column in EMPLOYEE_PROJECT_UPDATE_COLUMNS}
    row.update({
        "employee_update_id": make_employee_update_id(),
        "project_id": project_id,
        "proposal_id": proposal_id,
        "client_id": safe_text(alloc.get("client_id")),
        "employee_id": actor_id(user),
        "employee_name": actor_name(user),
        "project_role": safe_text(alloc.get("project_role")),
        "assigned_module": module,
        "week_label": current_week_label(),
        "progress_status": status_text,
        "progress_percent": safe_text(progress_percent),
        "hurdles": hurdles_text,
        "support_needed": support_text,
        "notes": notes_text,
        "created_at": now,
        "operations_status": "Open",
        "operations_done_by": "",
        "operations_done_at": "",
        "operations_resolution_note": "",
    })
    upsert_simple_row("employee_project_updates", "employee_update_id", EMPLOYEE_PROJECT_UPDATE_COLUMNS, row)

    attention_text = "Operations attention needed" if agent_review.get("needs_operations_attention") else "No immediate action needed"
    message = (
        f"Operations Agent alert: {actor_name(user)} submitted a weekly update for project {project_id}, "
        f"module {module or 'assigned module'}. "
        f"AI assessment: {attention_text}. Urgency: {agent_review.get('urgency')}. "
        f"Problem summary: {agent_review.get('problem_summary')}. "
        f"Recommended action: {agent_review.get('recommended_action')}. "
        f"Employee update: status {status_text}, progress {safe_text(progress_percent)}%, "
        f"hurdles: {hurdles_text or 'none provided'}, support requested: {support_text or 'none provided'}, "
        f"notes: {notes_text or 'none provided'}."
    )
    recipients = get_operations_notification_recipients(project_id)
    for recipient in recipients:
        try:
            notification = {
                "notification_id": make_notification_id(),
                "employee_id": recipient,
                "project_id": project_id,
                "proposal_id": proposal_id,
                "notification_type": "Employee Weekly Update",
                "message": message,
                "seen": "No",
                "created_at": now,
                "seen_at": "",
            }
            upsert_simple_row("employee_notifications", "notification_id", EMPLOYEE_NOTIFICATION_COLUMNS, notification)
        except Exception:
            pass

    try:
        append_proposal_history(
            proposal_id,
            user,
            "Employee Weekly Update",
            comment=(
                f"{status_text}; {safe_text(progress_percent)}% complete. "
                f"Operations Agent assessment: {agent_review.get('urgency')} - {agent_review.get('problem_summary')}"
            ),
            summary=f"{actor_name(user)} shared a project update for {module or project_id}. Operations was notified with AI assessment.",
        )
    except Exception:
        pass

    if recipients:
        return True, "Thanks. Your weekly update/request was saved. The Operations Executive has been notified and will connect with you soon if follow-up is needed."
    return True, "Thanks. Your weekly update/request was saved. Operations can review it in the delivery dashboard and will connect with you soon if follow-up is needed."


def current_week_label():
    return datetime.now().strftime("%Y-W%U")


def generate_weekly_update_if_needed(project, delivery_plan, allocations):
    updates = read_simple_table("weekly_project_updates", WEEKLY_UPDATE_COLUMNS)
    project_id = safe_text(project.get("project_id"))
    week = current_week_label()
    if not updates.empty:
        matched = updates[(updates["project_id"].astype(str) == project_id) & (updates["week_label"].astype(str) == week)]
        if not matched.empty:
            return matched.iloc[0].to_dict()
    allocation_count = 0 if allocations is None or allocations.empty else len(allocations)
    plan_status = safe_text(delivery_plan.get("approval_status"), "Planning") if delivery_plan else "Planning"
    fallback = (
        "Hi, hope you are doing well. Your project is moving through delivery readiness. "
        f"Current status: {safe_text(project.get('project_status'), 'Planning')}. "
        f"Operations plan status: {plan_status}. "
        f"Allocated team members: {allocation_count}. "
        "At the moment, there are no major blockers recorded. If you have any change in priority, scope, branding, or integrations, please share it with the Operations Executive through this portal."
    )
    if LIGHTWEIGHT_FAST_MODE and not USE_LLM_FOR_LONG_DOCUMENTS:
        update_text = fallback
        row = {
            "update_id": make_weekly_update_id(),
            "project_id": project_id,
            "proposal_id": safe_text(project.get("proposal_id")),
            "client_id": safe_text(project.get("client_id")),
            "week_label": week,
            "update_text": update_text,
            "blockers": "No major blockers recorded",
            "client_action_needed": "Share changes/blockers with Operations Executive if any",
            "generated_by": "Operations Agent",
            "generated_at": current_timestamp(),
            "published_by": "Operations Agent",
            "visible_to_client": "Yes",
        }
        upsert_simple_row("weekly_project_updates", "update_id", WEEKLY_UPDATE_COLUMNS, row)
        return row

    prompt = f"""
Write a short, professional weekly project update for a client portal.
Do not reveal internal employee bandwidth, salary, margin, or private comments.

Project: {project.get('project_name')}
Project status: {project.get('project_status')}
Operations plan status: {plan_status}
Team allocation count: {allocation_count}
Approved delivery plan summary: {safe_text(delivery_plan.get('operations_manager_plan') if delivery_plan else '')[:2000]}

Tone: friendly operations agent. Start with a greeting. Mention whether we are on track and ask the client to share blockers or requirement changes if any.
"""
    update_text = ask_llm(prompt, fallback=fallback)
    row = {
        "update_id": make_weekly_update_id(),
        "project_id": project_id,
        "proposal_id": safe_text(project.get("proposal_id")),
        "client_id": safe_text(project.get("client_id")),
        "week_label": week,
        "update_text": update_text,
        "blockers": "No major blockers recorded",
        "client_action_needed": "Share changes/blockers with Operations Executive if any",
        "generated_by": "Operations Agent",
        "generated_at": current_timestamp(),
        "published_by": "Operations Agent",
        "visible_to_client": "Yes",
    }
    upsert_simple_row("weekly_project_updates", "update_id", WEEKLY_UPDATE_COLUMNS, row)
    return row


def approve_delivery_plan_and_allocate(project, plan, user, manager_plan_text, selected_rows):
    now = current_timestamp()
    plan.update({
        "operations_manager_plan": manager_plan_text,
        "approval_status": "Approved by Operations Manager",
        "approved_by": actor_name(user),
        "approved_at": now,
        "updated_at": now,
    })
    upsert_simple_row("delivery_plans", "delivery_plan_id", DELIVERY_PLAN_COLUMNS, plan)
    project.update({
        "project_status": "Delivery Plan Approved - Team Allocated",
        "operations_owner_id": actor_id(user),
        "operations_owner_name": actor_name(user),
        "kickoff_date": now[:10],
        "updated_at": now,
    })
    upsert_simple_row("projects", "project_id", PROJECT_COLUMNS, project)

    # Replace active demo allocations for the project to keep the UI clean during repeated tests.
    try:
        conn = get_pg_conn()
        with conn.engine.begin() as db:
            db.execute(text("DELETE FROM project_allocations WHERE project_id = :project_id"), {"project_id": project.get("project_id")})
    except Exception:
        pass

    for item in selected_rows:
        allocation = {
            "allocation_id": make_allocation_id(),
            "project_id": project.get("project_id"),
            "proposal_id": project.get("proposal_id"),
            "client_id": project.get("client_id"),
            "employee_id": item.get("employee_id"),
            "employee_name": item.get("employee_name"),
            "employee_department": item.get("department"),
            "employee_designation": item.get("designation"),
            "project_role": item.get("project_role"),
            "assigned_module": item.get("assigned_module"),
            "responsibility_summary": item.get("responsibility_summary"),
            "allocation_percent": item.get("allocation_percent"),
            "start_date": now[:10],
            "end_date": "",
            "assigned_by": actor_name(user),
            "assigned_at": now,
            "allocation_status": "Active",
        }
        upsert_simple_row("project_allocations", "allocation_id", PROJECT_ALLOCATION_COLUMNS, allocation)
        notification = {
            "notification_id": make_notification_id(),
            "employee_id": item.get("employee_id"),
            "project_id": project.get("project_id"),
            "proposal_id": project.get("proposal_id"),
            "notification_type": "Project Assignment",
            "message": f"You have been assigned to {project.get('project_name')} as {item.get('project_role')} for {item.get('assigned_module')}. Please review the approved requirement plan in your project workbench.",
            "seen": "No",
            "created_at": now,
            "seen_at": "",
        }
        upsert_simple_row("employee_notifications", "notification_id", EMPLOYEE_NOTIFICATION_COLUMNS, notification)

    try:
        df = read_proposal_store(create_if_missing=True)
        mask = df["proposal_id"].astype(str) == safe_text(project.get("proposal_id"))
        if mask.any():
            df.loc[mask, "workflow_status"] = "Project Kickoff Ready - Team Allocated"
            df.loc[mask, "current_owner"] = "Operations / Delivery Team"
            df.loc[mask, "last_updated_by"] = actor_name(user)
            df.loc[mask, "last_updated_role"] = actor_role_label(user)
            df.loc[mask, "last_updated_at"] = now
            df.loc[mask, "last_update_summary"] = "Operations Manager approved delivery plan and allocated project team."
            for role_key, column in PROPOSAL_NOTIFICATION_COLUMNS.items():
                df.loc[mask, column] = "No"
                df.loc[mask, PROPOSAL_SEEN_AT_COLUMNS[role_key]] = ""
            upsert_current_proposal_from_df(df, mask)
    except Exception:
        pass
    append_proposal_history(
        project.get("proposal_id"),
        user,
        "Delivery Plan Approved",
        summary=f"Operations Manager approved delivery plan and allocated {len(selected_rows)} employee(s).",
    )
    return True, "Delivery plan approved. Selected employees have been notified and the client dashboard will show weekly updates."



def get_client_safe_project_progress(project_id):
    """Return a client-safe progress summary for an accepted project.

    The client should not see employee names, blockers, internal hurdles, or
    resource requests. We expose only the latest weekly progress percentage
    and whether the company needs any information from the client.
    """
    updates = get_employee_project_updates(project_id=project_id)
    if updates is None or updates.empty:
        return {
            "weekly_progress_percent": "Not updated yet",
            "progress_percent": "Not updated yet",
            "status": "Team work is going on",
            "updated_at": "",
        }

    working = updates.copy()
    if "created_at" in working.columns:
        working = working.sort_values("created_at", ascending=False)

    # Use the latest update from each employee if employee IDs exist; otherwise
    # average the latest available percentages. This keeps the output project-
    # level, not person-level.
    if "employee_id" in working.columns:
        latest_rows = working.drop_duplicates(subset=["employee_id"], keep="first")
    else:
        latest_rows = working.head(5)

    values = []
    for _, row in latest_rows.iterrows():
        val = safe_number(row.get("progress_percent"), None)
        if val is not None:
            values.append(max(0, min(100, val)))

    if values:
        avg = round(sum(values) / len(values))
        pct = f"{avg}%"
    else:
        pct = "Not updated yet"

    latest_status = safe_text(working.iloc[0].get("progress_status"), "Team work is going on") if not working.empty else "Team work is going on"
    latest_at = safe_text(working.iloc[0].get("created_at"), "") if not working.empty else ""
    return {
        "weekly_progress_percent": pct,
        "progress_percent": pct,
        "status": latest_status,
        "updated_at": latest_at,
    }


def get_client_safe_information_needed(plan, latest_update=None):
    """Return only client-action-needed text, never internal blockers."""
    candidates = []
    if latest_update:
        candidates.append(safe_text(latest_update.get("client_action_needed")))
    if plan:
        candidates.append(safe_text(plan.get("client_clarifications_needed")))

    for item in candidates:
        clean = item.strip()
        if not clean:
            continue
        lowered = clean.lower()
        # Avoid showing internal blocker wording to the client. Keep only true
        # client action/clarification text.
        if lowered in ["none", "no", "no major blockers recorded", "not applicable", "n/a"]:
            continue
        if "see operations agent plan" in lowered or "operations agent plan" == lowered:
            continue
        if "internal" in lowered and "client" not in lowered:
            continue
        if "blocker" in lowered and "client" not in lowered and "clarification" not in lowered:
            continue
        return clean
    return "No additional information is required from your side right now."


def save_client_message_to_operations(project, report, client_account, message_text):
    """Send a client portal message to the Operations Executive inbox."""
    message_text = safe_text(message_text).strip()
    if not message_text:
        return False, "Please type a message before sending."

    project_id = safe_text(project.get("project_id"))
    proposal_id = safe_text(project.get("proposal_id") or report.get("proposal_id"))
    client_name = safe_text(client_account.get("client_name") or report.get("client_name"), "Client")
    now = current_timestamp()

    recipients = get_operations_notification_recipients(project_id)
    if not recipients:
        recipients = [safe_text(project.get("operations_owner_id"))]
    recipients = [safe_text(r).upper() for r in recipients if safe_text(r)]

    if not recipients:
        return False, "Operations Executive is not configured yet. Please try again later."

    note = (
        f"Client message from {client_name} for project {project_id}: {message_text}"
    )
    for recipient in recipients:
        notification = {
            "notification_id": make_notification_id(),
            "employee_id": recipient,
            "project_id": project_id,
            "proposal_id": proposal_id,
            "notification_type": "Client Message",
            "message": note,
            "seen": "No",
            "created_at": now,
            "seen_at": "",
        }
        upsert_simple_row("employee_notifications", "notification_id", EMPLOYEE_NOTIFICATION_COLUMNS, notification)

    try:
        append_proposal_history(
            proposal_id,
            {"user_id": safe_text(client_account.get("client_user_id")), "employee_name": client_name, "designation": "Client"},
            "Client Message to Operations",
            comment=message_text,
            summary="Client sent a message to the Operations Executive from the client portal.",
        )
    except Exception:
        pass

    return True, "Your message has been sent to the Operations Executive."

def render_client_delivery_section(report, client_account):
    response = safe_text(report.get("client_response"))
    if response != "Accept Proposal":
        return

    st.markdown("### Weekly delivery update")
    project = ensure_project_for_accepted_proposal(report, client_account)
    plan = get_delivery_plan_for_client_project(project.get("project_id"))

    if plan is None:
        st.success("Proposal accepted. Our delivery team is ready to start the next step.")
        st.info("Please share your detailed requirement so our Operations Agent can prepare the delivery plan.")
        uploaded_text = ""
        uploaded_name = ""
        upload = st.file_uploader("Optional: upload a text requirement file", type=["txt", "md"], key=f"client_req_file_{project.get('project_id')}")
        if upload is not None:
            uploaded_name = upload.name
            try:
                uploaded_text = upload.read().decode("utf-8", errors="ignore")
            except Exception:
                uploaded_text = ""
        with st.form(f"client_requirement_form_{project.get('project_id')}"):
            requirement_text = st.text_area(
                "Detailed requirement",
                value=uploaded_text,
                height=190,
                placeholder="Describe modules, user roles, integrations, cloud/access needs, reporting expectations, and priorities.",
            )
            submitted = st.form_submit_button("Submit detailed requirement to Operations Agent", type="primary")
        if submitted:
            ok, msg = save_client_detailed_requirement(report, client_account, requirement_text, uploaded_name)
            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)
        return

    status = safe_text(plan.get("approval_status"))
    if status == "Approved by Operations Manager":
        allocations = get_project_allocations(project.get("project_id"))
        latest_update = generate_weekly_update_if_needed(project, plan, allocations)
        progress = get_client_safe_project_progress(project.get("project_id"))
        info_needed = get_client_safe_information_needed(plan, latest_update)

        st.success("Your project is active. Team work is going on.")
        c1, c2, c3 = st.columns(3)
        c1.metric("Delivery status", "In progress")
        c2.metric("Latest weekly update", progress.get("weekly_progress_percent") or progress.get("progress_percent"))
        c3.metric("Team allocation", "Allocated" if not allocations.empty else "Being finalized")

        latest_line = f"Latest weekly project update: {progress['updated_at']}" if progress.get("updated_at") else "The first weekly project update is not submitted yet."
        st.markdown(
            f"""
            <div class="dd-client-progress-card">
                <b>Weekly project progress</b>
                <span>Your delivery team is working on the approved requirement. This number represents the latest weekly progress update shared internally by the team, not a final overall completion certificate.</span>
                <span>{latest_line}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.info(f"Information needed from your side: {info_needed}")

        with st.expander("Message Operations Executive", expanded=False):
            sent_key = f"client_ops_msg_sent_{safe_text(project.get('project_id'))}"
            if st.session_state.get(sent_key, False):
                st.success("Your message has been sent to the Operations Executive.")
                if st.button("Send another message", key=f"client_ops_msg_again_{project.get('project_id')}"):
                    st.session_state[sent_key] = False
                    st.rerun()
            else:
                with st.form(f"client_ops_message_form_{project.get('project_id')}"):
                    msg = st.text_area(
                        "Type your message for the Operations Executive",
                        height=110,
                        placeholder="Example: Please confirm the branch-wise rollout order / integration priority / access details.",
                    )
                    submitted_msg = st.form_submit_button("Send message to Operations Executive", type="primary")
                if submitted_msg:
                    ok, message = save_client_message_to_operations(project, report, client_account, msg)
                    if ok:
                        st.session_state[sent_key] = True
                        st.rerun()
                    else:
                        st.error(message)
    else:
        st.info("Your detailed requirement has been received. The Operations Manager is reviewing the AI-generated delivery plan.")
        st.caption("Once delivery is approved and the team is allocated, this portal will show only client-safe project progress and any information needed from your side.")




def render_operations_notification_inbox_with_done(unread_alerts, user, key_prefix="ops_alerts_done"):
    """Compact Operations notification inbox with a Done action."""
    if unread_alerts is None or unread_alerts.empty:
        return
    working = unread_alerts.copy()
    if "created_at" in working.columns:
        working = working.sort_values("created_at", ascending=False)
    labels = []
    rows = []
    for idx, (_, row) in enumerate(working.iterrows(), start=1):
        labels.append(
            f"{idx}. {safe_text(row.get('created_at'))} | {safe_text(row.get('project_id'))} | {safe_text(row.get('notification_type'))}"
        )
        rows.append(row)
    st.markdown("#### Operations request inbox")
    selected = st.selectbox("Open request / alert", labels, key=f"{key_prefix}_select")
    row = rows[labels.index(selected)]
    with st.container(border=True):
        st.write(f"**Project:** {safe_text(row.get('project_id'))}")
        st.write(f"**Type:** {safe_text(row.get('notification_type'))}")
        st.write(f"**Received:** {safe_text(row.get('created_at'))}")
        st.write(safe_text(row.get("message")))
        if st.button("Mark this alert as done", key=f"{key_prefix}_done_{safe_text(row.get('notification_id'))}", type="primary"):
            ok, msg = mark_employee_notification_done(row.get("notification_id"), user)
            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)



def render_employee_update_inbox_with_done(employee_updates, user, project_id, key_prefix="employee_update_done"):
    """Project-scoped employee request/update inbox for Operations.

    Shows every open employee request/update in a visible recent-first queue, then
    lets Operations choose one item to review and mark done. Nothing disappears
    until Operations explicitly marks it done.
    """
    if employee_updates is None or employee_updates.empty:
        st.markdown(
            """
            <div class="dd-soft-panel">
                <strong>No open employee request for this project.</strong><br>
                <span>Weekly updates, blockers, and resource requests will appear here only when an assigned employee submits them.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    working = employee_updates.copy()
    if "operations_status" not in working.columns:
        working["operations_status"] = "Open"
    open_mask = ~working["operations_status"].fillna("Open").astype(str).str.lower().str.strip().isin(
        ["done", "closed", "resolved", "completed"]
    )
    working = working[open_mask].copy()
    if working.empty:
        st.markdown(
            """
            <div class="dd-soft-panel">
                <strong>All employee requests for this project are closed.</strong><br>
                <span>New weekly updates or resource requests will appear here when employees submit them.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    if "created_at" in working.columns:
        working = working.sort_values("created_at", ascending=False)

    st.markdown("### Open employee requests / weekly updates")
    st.caption("Every unresolved request for this project is listed below. Recent requests appear first. Select one to review and close.")

    queue_rows = []
    labels = []
    row_by_label = {}
    for idx, (_, row) in enumerate(working.iterrows(), start=1):
        employee = safe_text(row.get("employee_name")) or safe_text(row.get("employee_id")) or "Employee"
        status = safe_text(row.get("progress_status")) or "Weekly update"
        progress = safe_text(row.get("progress_percent")) or "0"
        module = safe_text(row.get("assigned_module")) or "Assigned module"
        created = safe_text(row.get("created_at")) or "Time not captured"
        issue = safe_text(row.get("support_needed")).strip() or safe_text(row.get("hurdles")).strip() or safe_text(row.get("notes")).strip()
        label = f"{idx}. {created} | {employee} | {status} | {progress}% | {module}"
        labels.append(label)
        row_by_label[label] = row
        queue_rows.append({
            "#": idx,
            "Received": created,
            "Employee": employee,
            "Status": status,
            "Progress": f"{progress}%",
            "Module": module,
            "Request / issue": issue or "No blocker mentioned",
        })

    st.markdown(
        f"""
        <div class="dd-soft-panel">
            <strong>{len(queue_rows)} open request/update item(s)</strong><br>
            <span>Items stay here until Operations marks them as done.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Visible queue so the manager can see that all unresolved items exist, not only the latest selected item.
    st.dataframe(pd.DataFrame(queue_rows), width="stretch", hide_index=True)

    selected = st.selectbox(
        "Choose request/update to review",
        labels,
        key=f"{key_prefix}_{project_id}_select",
    )
    row = row_by_label[selected]
    update_id = safe_text(row.get("employee_update_id"))

    employee = safe_text(row.get("employee_name")) or safe_text(row.get("employee_id")) or "Employee"
    status = safe_text(row.get("progress_status")) or "Weekly update"
    progress = safe_text(row.get("progress_percent")) or "0"
    module = safe_text(row.get("assigned_module")) or "Assigned module"
    hurdles = safe_text(row.get("hurdles")).strip()
    support = safe_text(row.get("support_needed")).strip()
    notes = safe_text(row.get("notes")).strip()

    st.markdown(
        f"""
        <div class="dd-project-card">
            <div class="dd-card-header-row">
                <div>
                    <div class="dd-card-kicker">Selected employee request</div>
                    <div class="dd-card-title-small">{employee}</div>
                    <div class="dd-card-subtle">{safe_text(row.get('created_at')) or '-'}</div>
                </div>
                <div class="dd-status-pill">{status}</div>
            </div>
            <div class="dd-metric-grid">
                <div class="dd-mini-metric"><span>Weekly progress</span><strong>{progress}%</strong></div>
                <div class="dd-mini-metric"><span>Module</span><strong>{module}</strong></div>
                <div class="dd-mini-metric"><span>Operations status</span><strong>Open</strong></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        if hurdles:
            st.markdown(f"**Blocker / hurdle**  \n{hurdles}")
        if support:
            st.markdown(f"**Support / resource needed**  \n{support}")
        if notes:
            st.markdown(f"**Employee note**  \n{notes}")
        if not (hurdles or support or notes):
            st.info("No blocker, support request, or note was provided for this update.")

    resolution_note = st.text_area(
        "Operations closing note",
        placeholder="Example: AWS access shared, issue discussed, backup assigned, no further action needed...",
        key=f"{key_prefix}_{update_id}_note",
    )
    if st.button("Mark this request/update as done", key=f"{key_prefix}_{update_id}_done", type="primary"):
        ok, msg = mark_employee_project_update_done(update_id, user, resolution_note)
        if ok:
            st.success(msg)
            st.rerun()
        else:
            st.error(msg)


def render_operations_delivery_workspace(user, data, focus_proposal_id=None):
    """Clean Operations Manager delivery workspace.

    Keeps the v25.26 UI baseline, but removes duplicate global alert ramayan,
    repeated quotation blocks, and unnecessary proposal-stage detail. The page is
    project-first: choose project -> requirement -> agent conclusion -> employee
    requests -> allocation controls.
    """
    if role_key_for_user(user) != "operations":
        return

    st.markdown(
        """
        <div class="dd-section-card dd-dashboard-shell">
            <div class="dd-section-eyebrow">Delivery operations</div>
            <div class="dd-section-title">Project delivery workspace</div>
            <div class="dd-section-subtitle">
                Select one accepted project, review the client requirement, check the Operations Agent conclusion,
                handle employee requests, and open allocation controls only when needed.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    projects = read_simple_table("projects", PROJECT_COLUMNS)
    plans = read_simple_table("delivery_plans", DELIVERY_PLAN_COLUMNS)
    if projects.empty:
        st.info("No accepted client projects are available yet.")
        return

    if plans.empty:
        projects_only = projects.copy()
        if focus_proposal_id:
            projects_only = projects_only[projects_only["proposal_id"].astype(str) == safe_text(focus_proposal_id)]
        if projects_only.empty:
            st.info("This accepted project does not have a delivery plan yet. Ask the client to submit the detailed requirement from the client portal.")
            return
        st.info("Accepted project exists, but the client has not submitted the detailed requirement yet.")
        cols = [c for c in ["project_name", "project_status", "created_at"] if c in projects_only.columns]
        st.dataframe(projects_only[cols], width="stretch", hide_index=True)
        return

    merged = plans.merge(projects, on=["project_id", "proposal_id", "client_id"], how="left", suffixes=("", "_project"))
    if focus_proposal_id:
        merged = merged[merged["proposal_id"].astype(str) == safe_text(focus_proposal_id)]
    if merged.empty:
        st.info("No delivery plan found for this accepted project yet. Once the client submits the detailed requirement, the Operations Agent analysis and allocation controls will appear here.")
        return

    if "created_at" in merged.columns:
        merged = merged.sort_values("created_at", ascending=False)

    labels = []
    rows = []
    for idx, (_, row) in enumerate(merged.iterrows(), start=1):
        project_name = safe_text(row.get("project_name")) or safe_text(row.get("project_id")) or "Accepted client project"
        status = safe_text(row.get("approval_status")) or "Waiting for review"
        created = safe_text(row.get("created_at")) or safe_text(row.get("updated_at"))
        labels.append(f"{idx}. {project_name} - {status} - {created}")
        rows.append(row)

    selected_label = st.selectbox(
        f"Accepted projects - recent first ({len(labels)} project(s))",
        labels,
        key=f"ops_delivery_selected_project_{actor_id(user)}_{safe_text(focus_proposal_id) or 'all'}",
    )
    selected_row = rows[labels.index(selected_label)]

    project = {col: selected_row.get(col, "") for col in PROJECT_COLUMNS}
    plan = {col: selected_row.get(col, "") for col in DELIVERY_PLAN_COLUMNS}
    project_id = project.get("project_id")
    plan_id = plan.get("delivery_plan_id")

    existing_allocations = get_project_allocations(project_id)
    employee_updates = get_open_employee_project_updates(project_id=project_id)
    proposal_report = get_proposal_report_by_id(project.get("proposal_id"))
    client_response = "Accepted"
    if proposal_report:
        client_response = safe_text(proposal_report.get("client_response")) or "Accepted"

    st.markdown(
        f"""
        <div class="dd-project-card">
            <div class="dd-card-header-row">
                <div>
                    <div class="dd-card-kicker">Selected accepted project</div>
                    <div class="dd-card-title-small">{safe_text(project.get('project_name')) or safe_text(project_id)}</div>
                    <div class="dd-card-subtle">Project ID: {safe_text(project_id)}</div>
                </div>
                <div class="dd-status-pill">Client {client_response}</div>
            </div>
            <div class="dd-metric-grid">
                <div class="dd-mini-metric"><span>Delivery status</span><strong>{safe_text(plan.get('approval_status')) or 'Waiting for review'}</strong></div>
                <div class="dd-mini-metric"><span>Allocated employees</span><strong>{0 if existing_allocations.empty else len(existing_allocations)}</strong></div>
                <div class="dd-mini-metric"><span>Open employee requests</span><strong>{0 if employee_updates.empty else len(employee_updates)}</strong></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption("Proposal approval is already complete. This workspace is only for delivery readiness, allocation, and project updates.")

    st.markdown("### Client requirement")
    requirement_text = safe_text(plan.get("raw_requirement_text")).strip()
    if requirement_text:
        st.text_area(
            "Requirement provided by client",
            value=requirement_text,
            height=130,
            disabled=True,
            key=f"ops_client_req_{plan_id}",
        )
    else:
        st.info("No detailed client requirement text was captured for this project yet.")

    agent_conclusion = safe_text(plan.get("operations_agent_plan")).strip()
    with st.expander("Operations Agent conclusion", expanded=False):
        if agent_conclusion:
            st.text_area(
                "AI delivery analysis and conclusion",
                value=agent_conclusion,
                height=220,
                disabled=True,
                key=f"ops_agent_conclusion_{plan_id}",
            )
        else:
            st.info("Operations Agent analysis is not available yet. It is generated after the client submits a detailed requirement.")

    render_employee_update_inbox_with_done(
        employee_updates,
        user,
        project_id,
        key_prefix=f"ops_weekly_updates_{project_id}",
    )

    if not existing_allocations.empty:
        with st.expander("Allocated team summary", expanded=False):
            cols = [c for c in ["employee_name", "project_role", "assigned_module", "allocation_percent", "allocation_status"] if c in existing_allocations.columns]
            st.dataframe(existing_allocations[cols], width="stretch", hide_index=True)

    with st.expander("Delivery plan and team allocation", expanded=False):
        st.caption("Open only when you need to approve/update the delivery plan or add employees to the project.")
        manager_plan = st.text_area(
            "Operations Manager delivery plan",
            value=safe_text(plan.get("operations_manager_plan") or plan.get("operations_agent_plan")),
            height=220,
            key=f"manager_plan_{plan_id}",
        )

        employees = data.get("employees", pd.DataFrame()).copy() if isinstance(data, dict) else pd.DataFrame()
        if employees.empty:
            st.warning("Employee sheet is not available for allocation.")
            return

        employees["label"] = employees.apply(lambda r: f"{r.get('employee_id')} - {r.get('employee_name')} ({r.get('designation')}, availability {r.get('availability_percent', '')}%)", axis=1)
        selected = st.multiselect("Add employees to this project", employees["label"].tolist(), key=f"alloc_select_{plan_id}")
        st.caption("Employees selected here receive project assignment notifications and will see this project in their weekly update workbench.")

        selected_rows = []
        for label in selected:
            emp = employees[employees["label"] == label].iloc[0].to_dict()
            c1, c2, c3 = st.columns([1, 1, 1])
            with c1:
                module = st.text_input(f"Module for {emp.get('employee_name')}", value=safe_text(emp.get("primary_skill")) or safe_text(emp.get("designation")), key=f"module_{plan_id}_{emp.get('employee_id')}")
            with c2:
                role = st.text_input(f"Project role for {emp.get('employee_name')}", value=safe_text(emp.get("designation")), key=f"role_{plan_id}_{emp.get('employee_id')}")
            with c3:
                alloc = st.number_input(f"Allocation % for {emp.get('employee_name')}", min_value=5, max_value=100, value=40, step=5, key=f"pct_{plan_id}_{emp.get('employee_id')}")
            selected_rows.append({
                "employee_id": safe_text(emp.get("employee_id")),
                "employee_name": safe_text(emp.get("employee_name")),
                "department": safe_text(emp.get("department")),
                "designation": safe_text(emp.get("designation")),
                "project_role": role,
                "assigned_module": module,
                "responsibility_summary": f"Own {module} delivery for {project.get('project_name')}. Submit weekly progress and raise hurdles/resource needs from the employee workbench.",
                "allocation_percent": str(alloc),
            })

        button_text = "Approve delivery plan and notify selected employees" if safe_text(plan.get("approval_status")) != "Approved by Operations Manager" else "Update team allocation and notify selected employees"
        if st.button(button_text, key=f"approve_delivery_{plan_id}", type="primary"):
            if not selected_rows:
                st.error("Select at least one employee before approving/updating the delivery team.")
            elif not safe_text(manager_plan).strip():
                st.error("Please keep or edit the delivery plan before approving.")
            else:
                ok, msg = approve_delivery_plan_and_allocate(project, plan, user, manager_plan, selected_rows)
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

def render_compact_record_dropdown(title, df, label_columns=None, detail_columns=None, key_prefix="record_dropdown"):
    """Show recent records as one compact dropdown instead of a long dataframe."""
    if df is None or df.empty:
        return
    label_columns = label_columns or []
    detail_columns = detail_columns or list(df.columns)
    working = df.copy()
    if "created_at" in working.columns:
        working = working.sort_values("created_at", ascending=False)
    elif "assigned_at" in working.columns:
        working = working.sort_values("assigned_at", ascending=False)

    labels = []
    rows = []
    for idx, (_, row) in enumerate(working.iterrows(), start=1):
        parts = []
        for col in label_columns:
            val = safe_text(row.get(col)).strip()
            if val:
                parts.append(val)
        label = " | ".join(parts) if parts else f"Record {idx}"
        labels.append(f"{idx}. {label}")
        rows.append(row)

    st.markdown(f"#### {title}")
    selected = st.selectbox("Recent first", labels, key=f"{key_prefix}_select")
    selected_index = labels.index(selected)
    row = rows[selected_index]
    with st.expander("View selected update", expanded=False):
        for col in detail_columns:
            if col in row.index:
                value = safe_text(row.get(col)).strip()
                if value:
                    st.write(f"**{col.replace('_', ' ').title()}:** {value}")


def render_employee_project_workbench(user):
    """Employee project workbench driven only by live Supabase allocations.

    No static Excel project list is shown here. Employees see one live project at
    a time, the client requirement, the Operations Agent conclusion, and the
    weekly progress/blocker/resource request form.
    """
    emp_id = safe_text(user.get("user_id")).upper()
    allocations = get_employee_allocations(emp_id)
    notifications = get_employee_notifications(emp_id)

    if allocations.empty:
        st.markdown(
            """
            <div class="dd-section-card">
                <div class="dd-section-title">My live project workbench</div>
                <div class="dd-section-subtitle">
                    No live Supabase project allocation is assigned to you yet.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if not notifications.empty:
            render_compact_record_dropdown(
                "Latest Operations notification",
                notifications,
                label_columns=["created_at", "notification_type", "project_id"],
                detail_columns=["created_at", "notification_type", "project_id", "message", "seen"],
                key_prefix=f"emp_notifications_{emp_id}",
            )
        return

    working = allocations.copy()
    if "assigned_at" in working.columns:
        working = working.sort_values("assigned_at", ascending=False)

    st.markdown(
        """
        <div class="dd-section-card">
            <div class="dd-section-title">My live project workbench</div>
            <div class="dd-section-subtitle">
                Choose a live project. For each project, share weekly progress, blockers,
                hurdles, access needs, and resource requests with Operations.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    labels = []
    rows = []
    for idx, (_, alloc_row) in enumerate(working.iterrows(), start=1):
        project_id = safe_text(alloc_row.get("project_id"))
        role = safe_text(alloc_row.get("project_role")) or "Assigned"
        module = safe_text(alloc_row.get("assigned_module")) or "Project work"
        labels.append(f"{idx}. {project_id} | {role} | {module}")
        rows.append(alloc_row)

    selected_label = st.selectbox(
        f"Open live project ({len(labels)} assigned project(s))",
        labels,
        key=f"emp_live_project_selector_{emp_id}",
    )
    alloc = rows[labels.index(selected_label)]
    project_id = safe_text(alloc.get("project_id"))
    ack_key = f"emp_update_sent_ack_{safe_text(alloc.get('allocation_id'))}"

    if st.session_state.get(ack_key, False):
        st.success("Your update/request has been sent to the Operations Executive.")
        st.info("Operations Executive will connect with you soon if follow-up is needed.")
        if st.button("Send another update for this project", key=f"emp_send_another_{alloc.get('allocation_id')}"):
            st.session_state[ack_key] = False
            st.rerun()
        return

    st.info(
        "Correct path: choose project -> review customer requirement and AI conclusion -> send weekly progress, blockers, or resource needs below."
    )

    # Keep the bench clean: show only assignment context, client requirement,
    # Operations Agent conclusion, and the required weekly update form.
    c1, c2, c3 = st.columns(3)
    c1.metric("Project", project_id or "Live project")
    c2.metric("My role", safe_text(alloc.get("project_role")) or "Assigned")
    c3.metric("Module", safe_text(alloc.get("assigned_module")) or "Project work")

    responsibility = safe_text(alloc.get("responsibility_summary"))
    if responsibility:
        st.caption(responsibility)

    plan = get_delivery_plan_for_client_project(project_id)
    st.markdown("#### Project reference")
    if plan:
        requirement = safe_text(plan.get("raw_requirement_text"))
        agent_conclusion = safe_text(plan.get("operations_agent_plan"))

        if requirement:
            st.text_area(
                "Customer requirement",
                value=requirement,
                height=180,
                disabled=True,
                key=f"emp_customer_requirement_{alloc.get('allocation_id')}",
            )
        else:
            st.info("Customer requirement is not available yet.")

        if agent_conclusion:
            st.text_area(
                "Operations Agent conclusion on the requirement",
                value=agent_conclusion,
                height=220,
                disabled=True,
                key=f"emp_agent_conclusion_{alloc.get('allocation_id')}",
            )
        else:
            st.info("Operations Agent conclusion is not available yet.")
    else:
        st.info("Delivery requirement and Operations Agent conclusion are not available yet for this project.")

    updates = get_employee_project_updates(project_id=project_id, employee_id=emp_id)
    current_week = current_week_label()
    already_this_week = False
    if not updates.empty and "week_label" in updates.columns:
        already_this_week = any(updates["week_label"].astype(str) == current_week)

    st.markdown("#### Weekly progress, blocker, and resource request")
    if already_this_week:
        st.info(
            "You already shared an update this week. Submit again only if there is a new blocker, "
            "resource need, access issue, or important progress change."
        )
    else:
        st.warning(
            "Please share this week's project status before closing your workbench: completion, blockers, "
            "hurdles, access/resource needs, and how the project is doing."
        )

    with st.form(key=f"employee_weekly_update_{alloc.get('allocation_id')}"):
        u1, u2 = st.columns([1, 1])
        with u1:
            status = st.selectbox(
                "How is the project doing this week?",
                ["On track", "Minor risk", "Blocked", "Ahead of plan"],
                key=f"emp_status_{alloc.get('allocation_id')}",
            )
        with u2:
            progress = st.slider(
                "How much of your weekly target is completed?",
                min_value=0,
                max_value=100,
                value=70,
                step=5,
                key=f"emp_progress_{alloc.get('allocation_id')}",
            )
        hurdles = st.text_area(
            "Any blockers, problems, hurdles, or dependencies?",
            placeholder="Example: waiting for API access, client sample data, AWS IAM permission, review feedback...",
            key=f"emp_hurdles_{alloc.get('allocation_id')}",
        )
        support = st.text_area(
            "Any extra resource, access, backup support, or clarification needed?",
            placeholder="Example: need DevOps help, AWS access, DB access, QA support, extra engineer, client clarification...",
            key=f"emp_support_{alloc.get('allocation_id')}",
        )
        notes = st.text_area(
            "Short summary for Operations Manager",
            placeholder="Example: Completed authentication flow; integration work is pending sample data from client.",
            key=f"emp_notes_{alloc.get('allocation_id')}",
        )
        submitted = st.form_submit_button("Send weekly update / request to Operations", type="primary")

    if submitted:
        ok, msg = save_employee_project_update(alloc, user, status, progress, hurdles, support, notes)
        if ok:
            st.session_state[ack_key] = True
            st.rerun()
        else:
            st.error(msg)

    if not updates.empty:
        with st.expander("Previous updates for this project", expanded=False):
            render_compact_record_dropdown(
                "My previous weekly updates / requests",
                updates,
                label_columns=["created_at", "week_label", "progress_status"],
                detail_columns=["created_at", "week_label", "progress_status", "progress_percent", "hurdles", "support_needed", "notes"],
                key_prefix=f"emp_weekly_updates_{emp_id}_{project_id}",
            )


def clean_scalar_for_postgres(column, value, numeric_columns=None, integer_columns=None):
    """Clean one value before proposal/history PostgreSQL upsert.

    Workflow tables are intentionally stored as TEXT for hackathon reliability.
    The UI converts values back with safe_number/safe_int when calculating or
    displaying. Sending text prevents old INTEGER columns from causing range
    crashes after schema repair.
    """
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass
    return safe_text(value)


def upsert_proposal_row(row):
    """Insert/update exactly one proposal row using TEXT-safe workflow storage."""
    if not postgres_config_available():
        df = read_proposal_store(create_if_missing=True)
        row_df = pd.DataFrame([row])
        if not df.empty and "proposal_id" in df.columns:
            df = df[df["proposal_id"].astype(str) != safe_text(row.get("proposal_id"))]
        write_proposal_store(pd.concat([df, row_df], ignore_index=True))
        return

    ensure_postgres_tables()
    try:
        if not st.session_state.get("_dd_pg_text_schema_repaired", False):
            repair_proposal_workflow_text_schema()
            st.session_state["_dd_pg_text_schema_repaired"] = True
    except Exception as repair_exc:
        remember_postgres_error(repair_exc)

    cols = PROPOSAL_DECISION_COLUMNS
    prepared = {col: clean_scalar_for_postgres(col, row.get(col, "")) for col in cols}
    values_clause = ", ".join([f":{c}" for c in cols])
    update_clause = ", ".join([f"{c}=EXCLUDED.{c}" for c in cols if c != "proposal_id"])
    sql = text(f"""
        INSERT INTO proposal_decisions ({', '.join(cols)})
        VALUES ({values_clause})
        ON CONFLICT (proposal_id) DO UPDATE SET {update_clause}
    """)
    execute_with_schema_repair(sql, [prepared], table_label="proposal_decisions")
    clear_workflow_read_cache()


def upsert_current_proposal_from_df(df, mask):
    """Persist only the currently changed proposal row.

    Earlier decision actions rewrote every proposal row back to Supabase.
    That made simple actions such as approve / review / quote unnecessarily slow
    when the table had older demo records. This helper keeps UI actions light:
    one changed proposal becomes one row-level UPSERT.
    """
    try:
        if df is None or not mask.any():
            return
        row = df.loc[mask].iloc[0].to_dict()
        upsert_proposal_row(row)
    except Exception:
        raise


def insert_history_row(row):
    """Insert exactly one proposal history row without rewriting the audit table."""
    if not postgres_config_available():
        history = read_history_store(create_if_missing=True)
        history = pd.concat([history, pd.DataFrame([row])], ignore_index=True)
        write_history_store(history)
        return

    ensure_postgres_tables()
    prepared = {col: clean_scalar_for_postgres(col, row.get(col, ""), HISTORY_NUMERIC_COLUMNS, HISTORY_INTEGER_COLUMNS) for col in PROPOSAL_HISTORY_COLUMNS}
    cols = PROPOSAL_HISTORY_COLUMNS
    values_clause = ", ".join([f":{c}" for c in cols])
    update_clause = ", ".join([f"{c}=EXCLUDED.{c}" for c in cols if c != "event_id"])
    sql = text(f"""
        INSERT INTO proposal_decision_history ({', '.join(cols)})
        VALUES ({values_clause})
        ON CONFLICT (event_id) DO UPDATE SET {update_clause}
    """)
    conn = get_pg_conn()
    with conn.engine.begin() as db:
        db.execute(sql, prepared)
    clear_workflow_read_cache()

def write_proposal_store(df):
    """Save proposal_decisions safely as row-level TEXT upserts.

    This avoids old Supabase INTEGER/numeric column crashes and also avoids the
    earlier DELETE+rewrite pattern. All workflow values are stored as TEXT;
    display/calculation code converts values back with safe_number/safe_int.
    """
    df = normalise_proposal_store(df)
    df = df[PROPOSAL_DECISION_COLUMNS].copy()

    if postgres_config_available():
        ensure_postgres_tables()
        try:
            repair_proposal_workflow_text_schema()
            st.session_state["_dd_pg_text_schema_repaired"] = True
        except Exception as repair_exc:
            remember_postgres_error(repair_exc)

        cols = PROPOSAL_DECISION_COLUMNS
        values_clause = ", ".join([f":{c}" for c in cols])
        update_clause = ", ".join([f"{c}=EXCLUDED.{c}" for c in cols if c != "proposal_id"])
        sql = text(f"""
            INSERT INTO proposal_decisions ({', '.join(cols)})
            VALUES ({values_clause})
            ON CONFLICT (proposal_id) DO UPDATE SET {update_clause}
        """)
        records = [
            {col: clean_scalar_for_postgres(col, row.get(col, "")) for col in cols}
            for _, row in df.iterrows()
        ]
        execute_with_schema_repair(sql, records, table_label="proposal_decisions")
        clear_workflow_read_cache()
        return

    if REQUIRE_SUPABASE_FOR_PROPOSALS:
        require_postgres_or_raise()

    write_excel_sheet(PROPOSAL_DECISIONS_SHEET, df)


def write_history_store(df):
    """Save proposal_decision_history safely as row-level TEXT upserts."""
    df = normalise_history_store(df)
    df = df[PROPOSAL_HISTORY_COLUMNS].copy()

    if postgres_config_available():
        ensure_postgres_tables()
        try:
            repair_proposal_workflow_text_schema()
            st.session_state["_dd_pg_text_schema_repaired"] = True
        except Exception as repair_exc:
            remember_postgres_error(repair_exc)

        cols = PROPOSAL_HISTORY_COLUMNS
        values_clause = ", ".join([f":{c}" for c in cols])
        update_clause = ", ".join([f"{c}=EXCLUDED.{c}" for c in cols if c != "event_id"])
        sql = text(f"""
            INSERT INTO proposal_decision_history ({', '.join(cols)})
            VALUES ({values_clause})
            ON CONFLICT (event_id) DO UPDATE SET {update_clause}
        """)
        records = [
            {col: clean_scalar_for_postgres(col, row.get(col, "")) for col in cols}
            for _, row in df.iterrows()
        ]
        execute_with_schema_repair(sql, records, table_label="proposal_decision_history")
        clear_workflow_read_cache()
        return

    if REQUIRE_SUPABASE_FOR_PROPOSALS:
        require_postgres_or_raise()

    write_excel_sheet(PROPOSAL_HISTORY_SHEET, df)


def read_proposal_store(create_if_missing=True):
    if postgres_config_available():
        try:
            ensure_postgres_tables()
            conn = get_pg_conn()
            df = conn.query("SELECT * FROM proposal_decisions", ttl=0)
            st.session_state["proposal_storage_last_error"] = ""
        except Exception as exc:
            remember_postgres_error(exc)
            # Do not crash executive workspaces when Supabase/pooler has a transient
            # network/DNS reset. Return an empty store and show the saved error in UI.
            df = pd.DataFrame(columns=PROPOSAL_DECISION_COLUMNS)
        return normalise_proposal_store(df)

    db_file = Path(DB_PATH)
    if not db_file.exists():
        return pd.DataFrame(columns=PROPOSAL_DECISION_COLUMNS)

    try:
        xls = pd.ExcelFile(db_file)
        if PROPOSAL_DECISIONS_SHEET in xls.sheet_names:
            df = pd.read_excel(db_file, sheet_name=PROPOSAL_DECISIONS_SHEET)
        else:
            df = pd.DataFrame(columns=PROPOSAL_DECISION_COLUMNS)
            if create_if_missing:
                write_proposal_store(df)
    except ValueError:
        df = pd.DataFrame(columns=PROPOSAL_DECISION_COLUMNS)
        if create_if_missing:
            write_proposal_store(df)

    return normalise_proposal_store(df)


def read_history_store(create_if_missing=True):
    if postgres_config_available():
        try:
            ensure_postgres_tables()
            conn = get_pg_conn()
            df = conn.query("SELECT * FROM proposal_decision_history", ttl=0)
            st.session_state["proposal_storage_last_error"] = ""
        except Exception as exc:
            remember_postgres_error(exc)
            df = pd.DataFrame(columns=PROPOSAL_HISTORY_COLUMNS)
        return normalise_history_store(df)

    db_file = Path(DB_PATH)
    if not db_file.exists():
        return pd.DataFrame(columns=PROPOSAL_HISTORY_COLUMNS)

    try:
        xls = pd.ExcelFile(db_file)
        if PROPOSAL_HISTORY_SHEET in xls.sheet_names:
            df = pd.read_excel(db_file, sheet_name=PROPOSAL_HISTORY_SHEET)
        else:
            df = pd.DataFrame(columns=PROPOSAL_HISTORY_COLUMNS)
            if create_if_missing:
                write_history_store(df)
    except ValueError:
        df = pd.DataFrame(columns=PROPOSAL_HISTORY_COLUMNS)
        if create_if_missing:
            write_history_store(df)

    return normalise_history_store(df)

def role_key_for_user(user):
    if not user:
        return None

    role = str(user.get("role", "")).strip().lower()
    department = str(user.get("department", "")).strip().lower()
    designation = str(user.get("designation", "")).strip().lower()

    if role == "founder" or "ceo" in designation or "founder" in designation:
        return "ceo"
    if "sales" in department or "sales" in designation:
        return "sales"
    if "finance" in department or "finance" in designation:
        return "finance"
    if department == "hr" or "hr" in designation or "human resource" in department:
        return "hr"
    if "operation" in department or "operation" in designation:
        return "operations"
    return None


def user_notification_column(user):
    role_key = role_key_for_user(user)
    if role_key is None:
        return None
    return PROPOSAL_NOTIFICATION_COLUMNS[role_key]


def user_seen_at_column(user):
    role_key = role_key_for_user(user)
    if role_key is None:
        return None
    return PROPOSAL_SEEN_AT_COLUMNS[role_key]


def actor_name(user):
    if not user:
        return "Unknown"
    return safe_text(user.get("employee_name") or user.get("user_id") or "Unknown")


def actor_id(user):
    if not user:
        return ""
    return safe_text(user.get("user_id"))


def actor_role_label(user):
    role_key = role_key_for_user(user)
    if role_key:
        return PROPOSAL_DEPARTMENT_LABELS[role_key]
    return safe_text(user.get("designation", "Employee")) if user else "Unknown"


def re_notify_everyone_except(df, mask, role_key_to_keep_seen):
    """
    Core collaboration rule:
    whenever any executive updates a proposal, every other role must be notified again.
    The updater's seen flag becomes Yes; all others become No.
    """
    now = current_timestamp()
    for role_key, column in PROPOSAL_NOTIFICATION_COLUMNS.items():
        seen_at_column = PROPOSAL_SEEN_AT_COLUMNS[role_key]
        if role_key == role_key_to_keep_seen:
            df.loc[mask, column] = "Yes"
            df.loc[mask, seen_at_column] = now
        else:
            df.loc[mask, column] = "No"
            df.loc[mask, seen_at_column] = ""
    return df


def append_proposal_history(
    proposal_id,
    user,
    action_type,
    decision="",
    comment="",
    recommended_quote="",
    recommended_timeline_months="",
    summary="",
):
    try:
        row = {
            "event_id": make_event_id(),
            "proposal_id": proposal_id,
            "event_at": current_timestamp(),
            "actor_id": actor_id(user),
            "actor_name": actor_name(user),
            "actor_role": actor_role_label(user),
            "action_type": action_type,
            "decision": decision,
            "comment": comment,
            "recommended_quote": recommended_quote,
            "recommended_timeline_months": recommended_timeline_months,
            "summary": summary,
        }
        insert_history_row(row)
    except Exception:
        # History is useful, but the main decision update must not fail because of audit logging.
        pass

def build_agent_summaries(analysis):
    budget = safe_number(analysis.get("client_budget"))
    quote = safe_number(analysis.get("recommended_quote"))
    cost = safe_number(analysis.get("estimated_cost"))
    margin = safe_number(analysis.get("profit_margin_at_client_budget"))
    timeline = safe_int(analysis.get("timeline_months"))
    skill_gap = safe_number(analysis.get("total_skill_gap"))
    timeline_risk = safe_text(analysis.get("timeline_risk"))
    decision = safe_text(analysis.get("decision"))
    reason = safe_text(analysis.get("reason"))

    return {
        "sales_agent_summary": (
            f"Sales captured a {analysis.get('project_type', 'project')} opportunity with client budget "
            f"{money_text(budget)}. Recommended client-facing quote is {money_text(quote)}."
        ),
        "hr_agent_summary": (
            f"HR found a total projected resource gap of {skill_gap} FTE using Excel employee master data "
            "plus live Supabase project allocations, progress updates, hurdles, and release timing."
        ),
        "operations_agent_summary": (
            f"Operations reviewed a {timeline}-month timeline with live Supabase workload data. "
            f"Timeline risk is {timeline_risk}."
        ),
        "finance_agent_summary": (
            f"Finance estimated delivery cost at {money_text(cost)}, target quote at {money_text(quote)}, "
            f"and margin at client budget at {margin}%."
        ),
        "ceo_agent_summary": f"Initial CEO-style recommendation: {decision}. Reason: {reason}",
    }


def save_external_client_report_to_excel(raw_client_message, analysis):
    """Persist the agent decision packet first, then create client credentials.

    Earlier v21 created the client account before saving proposal_decisions. If the
    client_accounts table was missing a column, the whole proposal save failed and
    neither proposal_decisions nor proposal_decision_history was created. That is
    unsafe because the internal agent meeting had already completed. This version
    saves the proposal row and audit row first, then attaches client credentials.
    """
    now = current_timestamp()
    proposal_id = make_proposal_id()
    client_name = maybe_extract_client_name(raw_client_message)
    client_contact = maybe_extract_client_contact(raw_client_message)
    summaries = build_agent_summaries(analysis)

    row = {column: "" for column in PROPOSAL_DECISION_COLUMNS}
    row.update({
        "proposal_id": proposal_id,
        "created_at": now,
        "source": "External Client Chat",
        "client_name": client_name,
        "client_contact": client_contact,
        "raw_client_message": raw_client_message,
        "project_type": analysis.get("project_type", ""),
        "client_budget": analysis.get("client_budget", 0),
        "timeline_months": analysis.get("timeline_months", 0),
        "employee_cost": analysis.get("employee_cost", 0),
        "overhead": analysis.get("overhead", 0),
        "cloud_cost": analysis.get("cloud_cost", 0),
        "software_cost": analysis.get("software_cost", 0),
        "contingency": analysis.get("contingency", 0),
        "estimated_cost": analysis.get("estimated_cost", 0),
        "target_margin_percent": analysis.get("target_margin_percent", 0),
        "recommended_quote": analysis.get("recommended_quote", 0),
        "expected_profit_at_client_budget": analysis.get("expected_profit_at_client_budget", 0),
        "profit_margin_at_client_budget": analysis.get("profit_margin_at_client_budget", 0),
        "total_skill_gap": analysis.get("total_skill_gap", 0),
        "timeline_risk": analysis.get("timeline_risk", ""),
        "initial_agent_decision": analysis.get("decision", ""),
        "initial_agent_reason": analysis.get("reason", ""),
        "decision": analysis.get("decision", ""),
        "reason": analysis.get("reason", ""),
        "workflow_status": "Awaiting Executive Decisions",
        "current_owner": "Sales, Finance, HR, Operations, CEO",
        "decision_version": 1,
        "sales_agent_summary": summaries["sales_agent_summary"],
        "hr_agent_summary": summaries["hr_agent_summary"],
        "operations_agent_summary": summaries["operations_agent_summary"],
        "finance_agent_summary": summaries["finance_agent_summary"],
        "ceo_agent_summary": summaries["ceo_agent_summary"],
        "skill_gap_json": encode_json(analysis.get("skill_gap", [])),
        "role_cost_breakdown_json": encode_json(analysis.get("role_cost_breakdown", [])),
        "sales_seen": "No",
        "finance_seen": "No",
        "hr_seen": "No",
        "operations_seen": "No",
        "ceo_seen": "No",
        "quotation_sent": "No",
        "last_updated_by": "AI Receptionist",
        "last_updated_role": "System",
        "last_updated_at": now,
        "last_update_summary": "New proposal created and shared with all executives.",
    })

    # 1) Save the internal decision packet no matter what happens to client portal setup.
    upsert_proposal_row(row)

    # 2) Save audit history immediately after the proposal row.
    append_proposal_history(
        proposal_id,
        {"user_id": "SYSTEM", "employee_name": "AI Receptionist", "designation": "System"},
        "Proposal Created",
        decision=analysis.get("decision", ""),
        comment=analysis.get("reason", ""),
        recommended_quote=analysis.get("recommended_quote", 0),
        recommended_timeline_months=analysis.get("timeline_months", 0),
        summary="External client proposal analysed by Sales, HR, Operations, Finance, and CEO agents.",
    )

    # 3) Create client credentials. If this fails, keep proposal/history saved.
    try:
        client_account = create_client_account_for_proposal(proposal_id, client_name, client_contact)
        row.update({
            "client_id": client_account.get("client_id", ""),
            "client_user_id": client_account.get("client_user_id", ""),
            "client_password": client_account.get("client_password", ""),
            "last_update_summary": "New proposal created, internal agent analysis saved, and client portal account created.",
        })
        upsert_proposal_row(row)
        append_proposal_history(
            proposal_id,
            {"user_id": "SYSTEM", "employee_name": "Client Portal", "designation": "System"},
            "Client Portal Account Created",
            summary="Downloadable client portal credentials were generated for quotation tracking.",
        )
    except Exception as exc:
        append_proposal_history(
            proposal_id,
            {"user_id": "SYSTEM", "employee_name": "Client Portal", "designation": "System"},
            "Client Portal Account Failed",
            summary=f"Proposal and agent analysis were saved, but client credential creation failed: {exc}",
        )

    return proposal_id

def proposal_row_to_report(row):
    if hasattr(row, "to_dict"):
        row = row.to_dict()

    current_decision = (
        safe_text(row.get("ceo_final_decision"))
        or safe_text(row.get("decision"))
        or safe_text(row.get("initial_agent_decision"))
    )
    current_reason = (
        safe_text(row.get("ceo_comment"))
        or safe_text(row.get("reason"))
        or safe_text(row.get("initial_agent_reason"))
    )
    current_quote = safe_number(row.get("ceo_final_quote")) or safe_number(row.get("recommended_quote"))
    current_timeline = safe_int(row.get("ceo_final_timeline_months")) or safe_int(row.get("timeline_months"))

    analysis = {
        "client_message": safe_text(row.get("raw_client_message")),
        "project_type": safe_text(row.get("project_type")),
        "client_budget": safe_number(row.get("client_budget")),
        "timeline_months": current_timeline,
        "original_timeline_months": safe_int(row.get("timeline_months")),
        "employee_cost": safe_number(row.get("employee_cost")),
        "overhead": safe_number(row.get("overhead")),
        "cloud_cost": safe_number(row.get("cloud_cost")),
        "software_cost": safe_number(row.get("software_cost")),
        "contingency": safe_number(row.get("contingency")),
        "estimated_cost": safe_number(row.get("estimated_cost")),
        "target_margin_percent": safe_number(row.get("target_margin_percent")),
        "recommended_quote": current_quote,
        "initial_recommended_quote": safe_number(row.get("recommended_quote")),
        "expected_profit_at_client_budget": safe_number(row.get("expected_profit_at_client_budget")),
        "profit_margin_at_client_budget": safe_number(row.get("profit_margin_at_client_budget")),
        "total_skill_gap": safe_number(row.get("total_skill_gap")),
        "timeline_risk": safe_text(row.get("timeline_risk")),
        "decision": current_decision,
        "reason": current_reason,
        "initial_agent_decision": safe_text(row.get("initial_agent_decision")) or safe_text(row.get("decision")),
        "initial_agent_reason": safe_text(row.get("initial_agent_reason")) or safe_text(row.get("reason")),
        "skill_gap": decode_json(row.get("skill_gap_json"), []),
        "role_cost_breakdown": decode_json(row.get("role_cost_breakdown_json"), []),
    }

    decisions = {}
    for role_key in ["sales", "finance", "hr", "operations"]:
        decisions[role_key] = {
            "decision": safe_text(row.get(f"{role_key}_decision")),
            "comment": safe_text(row.get(f"{role_key}_comment")),
            "recommended_quote": safe_number(row.get(f"{role_key}_recommended_quote")),
            "recommended_timeline_months": safe_int(row.get(f"{role_key}_recommended_timeline_months")),
            "decided_by": safe_text(row.get(f"{role_key}_decided_by")),
            "decided_at": safe_text(row.get(f"{role_key}_decided_at")),
        }
    decisions["ceo"] = {
        "decision": safe_text(row.get("ceo_final_decision")),
        "comment": safe_text(row.get("ceo_comment")),
        "recommended_quote": safe_number(row.get("ceo_final_quote")),
        "recommended_timeline_months": safe_int(row.get("ceo_final_timeline_months")),
        "decided_by": safe_text(row.get("ceo_decided_by")),
        "decided_at": safe_text(row.get("ceo_decided_at")),
    }

    return {
        "proposal_id": safe_text(row.get("proposal_id")),
        "created_at": safe_text(row.get("created_at")),
        "client_name": safe_text(row.get("client_name"), "External Client"),
        "client_contact": safe_text(row.get("client_contact")),
        "raw_client_message": safe_text(row.get("raw_client_message")),
        "workflow_status": safe_text(row.get("workflow_status"), "Awaiting Executive Decisions"),
        "current_owner": safe_text(row.get("current_owner")),
        "decision_version": safe_int(row.get("decision_version"), 0),
        "last_updated_by": safe_text(row.get("last_updated_by")),
        "last_updated_role": safe_text(row.get("last_updated_role")),
        "last_updated_at": safe_text(row.get("last_updated_at")),
        "last_update_summary": safe_text(row.get("last_update_summary")),
        "agent_summaries": {
            "sales": safe_text(row.get("sales_agent_summary")),
            "hr": safe_text(row.get("hr_agent_summary")),
            "operations": safe_text(row.get("operations_agent_summary")),
            "finance": safe_text(row.get("finance_agent_summary")),
            "ceo": safe_text(row.get("ceo_agent_summary")),
        },
        "decisions": decisions,
        "client_id": safe_text(row.get("client_id")),
        "client_user_id": safe_text(row.get("client_user_id")),
        "client_password": safe_text(row.get("client_password")),
        "client_response": safe_text(row.get("client_response")),
        "client_response_comment": safe_text(row.get("client_response_comment")),
        "client_response_at": safe_text(row.get("client_response_at")),
        "client_quotation": safe_text(row.get("client_quotation")),
        "quotation_generated_at": safe_text(row.get("quotation_generated_at")),
        "quotation_sent": safe_text(row.get("quotation_sent"), "No"),
        "quotation_sent_at": safe_text(row.get("quotation_sent_at")),
        "analysis": analysis,
    }


def save_latest_external_client_report(raw_client_message, analysis):
    """Save in Excel for persistence and keep a session copy for immediate chat rendering."""
    report = {
        "proposal_id": None,
        "created_at": current_timestamp(),
        "raw_client_message": raw_client_message,
        "analysis": analysis,
        "excel_save_error": "",
    }

    try:
        proposal_id = save_external_client_report_to_excel(raw_client_message, analysis)
        fresh_df = read_proposal_store(create_if_missing=False)
        row = fresh_df[fresh_df["proposal_id"].astype(str) == str(proposal_id)].iloc[0]
        report = proposal_row_to_report(row)
    except Exception as exc:
        report["excel_save_error"] = str(exc)

    st.session_state.latest_external_client_report = report
    st.session_state.business_context["latest_external_client_report"] = analysis
    st.session_state.business_context["latest_project_type"] = analysis["project_type"]
    st.session_state.business_context["latest_client_message"] = raw_client_message
    st.session_state.business_context["latest_agent_outputs"] = {
        "sales": {
            "client_budget": analysis["client_budget"],
            "project_type": analysis["project_type"],
        },
        "hr": {
            "skill_gap": analysis["skill_gap"],
            "total_skill_gap": analysis["total_skill_gap"],
            "immediate_skill_gap": analysis.get("immediate_skill_gap", 0),
            "capacity_basis": analysis.get("capacity_basis", ""),
        },
        "operations": {
            "timeline_months": analysis["timeline_months"],
            "timeline_risk": analysis["timeline_risk"],
            "total_active_allocated_fte": analysis.get("total_active_allocated_fte", 0),
            "dynamic_hurdle_count": analysis.get("dynamic_hurdle_count", 0),
        },
        "finance": {
            "estimated_cost": analysis["estimated_cost"],
            "recommended_quote": analysis["recommended_quote"],
            "margin": analysis["profit_margin_at_client_budget"],
        },
        "ceo": {
            "decision": analysis["decision"],
            "reason": analysis["reason"],
        },
    }
    st.session_state.business_context["conversation_summary"] = (
        f"Latest client enquiry: {raw_client_message}. "
        f"Project type: {analysis['project_type']}. "
        f"Budget: ₹{analysis['client_budget']:,.0f}. "
        f"Timeline: {analysis['timeline_months']} months. "
        f"Initial agentic decision: {analysis['decision']}."
    )

    return report


def get_latest_external_client_report():
    report = st.session_state.get("latest_external_client_report")
    if report:
        return report

    try:
        df = read_proposal_store(create_if_missing=False)
        if not df.empty:
            df = df.copy()
            if "created_at" in df.columns:
                df = df.sort_values("created_at", ascending=False)
            return proposal_row_to_report(df.iloc[0])
    except Exception:
        pass

    context_report = st.session_state.business_context.get("latest_external_client_report")
    if context_report:
        return {
            "raw_client_message": st.session_state.business_context.get("latest_client_message", ""),
            "analysis": context_report,
        }

    return None


def get_pending_proposal_reports_for_user(user):
    column = user_notification_column(user)
    if column is None:
        return []

    df = read_proposal_store(create_if_missing=True)
    if df.empty:
        return []

    pending = df[
        df[column].fillna("No").astype(str).str.strip().str.lower() != "yes"
    ].copy()

    if pending.empty:
        return []

    if "last_updated_at" in pending.columns:
        pending = pending.sort_values("last_updated_at", ascending=False)
    elif "created_at" in pending.columns:
        pending = pending.sort_values("created_at", ascending=False)

    return [proposal_row_to_report(row) for _, row in pending.iterrows()]


def get_all_proposal_reports(limit=20):
    try:
        df = read_proposal_store(create_if_missing=True)
    except Exception as exc:
        remember_postgres_error(exc)
        return []
    if df.empty:
        return []
    if "last_updated_at" in df.columns:
        df = df.sort_values("last_updated_at", ascending=False)
    elif "created_at" in df.columns:
        df = df.sort_values("created_at", ascending=False)
    return [proposal_row_to_report(row) for _, row in df.head(limit).iterrows()]


def get_proposal_history(proposal_id):
    history = read_history_store(create_if_missing=True)
    if history.empty:
        return history
    history = history[history["proposal_id"].astype(str) == str(proposal_id)].copy()
    if not history.empty and "event_at" in history.columns:
        history = history.sort_values("event_at", ascending=False)
    return history


def mark_proposal_seen_for_user(proposal_id, user):
    column = user_notification_column(user)
    timestamp_column = user_seen_at_column(user)
    if column is None or timestamp_column is None:
        return False, "This user does not have an executive proposal notification column."

    df = read_proposal_store(create_if_missing=True)
    if df.empty or "proposal_id" not in df.columns:
        return False, "No proposal notification records found."

    mask = df["proposal_id"].astype(str) == str(proposal_id)
    if not mask.any():
        return False, f"Proposal {proposal_id} was not found in {PROPOSAL_DECISIONS_SHEET}."

    now = current_timestamp()
    df.loc[mask, column] = "Yes"
    df.loc[mask, timestamp_column] = now
    upsert_current_proposal_from_df(df, mask)
    append_proposal_history(
        proposal_id,
        user,
        "Marked Reviewed",
        summary=f"{actor_role_label(user)} marked the proposal as reviewed.",
    )
    return True, f"Marked {proposal_id} as reviewed for {actor_role_label(user)}."


def generate_client_quotation_text(report, ceo_decision, ceo_comment, final_quote, final_timeline_months):
    analysis = report["analysis"]
    fallback = (
        f"Subject: Proposal response for {analysis.get('project_type', 'your project')}\n\n"
        f"Dear {report.get('client_name') or 'Client'},\n\n"
        f"Thank you for sharing your requirement. After an internal review by our Sales, HR, "
        f"Operations, Finance, and CEO teams, our decision is: {ceo_decision}.\n\n"
        f"Recommended commercial quote: INR {safe_number(final_quote):,.0f}\n"
        f"Estimated timeline: {safe_int(final_timeline_months)} month(s)\n"
        f"Project type: {analysis.get('project_type')}\n\n"
        f"Notes: {ceo_comment or analysis.get('reason', '')}\n\n"
        "This quotation assumes the scope described in your requirement. Final contract terms, milestone plan, "
        "and payment schedule can be confirmed after a scope confirmation call.\n\n"
        "Regards,\nVirtualTech Solutions"
    )

    if LIGHTWEIGHT_FAST_MODE and not USE_LLM_FOR_LONG_DOCUMENTS:
        return fallback

    prompt = f"""
You are a professional IT services sales executive writing a client-facing quotation email.
Do not reveal internal salary, margin, or employee-level details.

Client name: {report.get('client_name') or 'Client'}
Client requirement: {report.get('raw_client_message')}
Project type: {analysis.get('project_type')}
CEO final decision: {ceo_decision}
CEO note: {ceo_comment}
Approved quote in INR: {safe_number(final_quote)}
Approved timeline in months: {safe_int(final_timeline_months)}
Internal estimated delivery cost, not to reveal: {analysis.get('estimated_cost')}
Initial agent recommendation: {analysis.get('initial_agent_decision')} - {analysis.get('initial_agent_reason')}

Write a concise quotation/response email with:
1. Thank you note
2. Understanding of requirement
3. Proposed commercial quote
4. Proposed timeline
5. Scope/assumptions
6. Next steps

Return only the email body with a clear subject line.
"""
    return ask_llm(prompt, fallback=fallback)


def submit_proposal_decision(proposal_id, user, decision, comment, recommended_quote, recommended_timeline_months):
    role_key = role_key_for_user(user)
    if role_key is None:
        return False, "Only Sales, Finance, HR, Operations executives or CEO can update proposal decisions."

    df = read_proposal_store(create_if_missing=True)
    mask = df["proposal_id"].astype(str) == str(proposal_id)
    if not mask.any():
        return False, f"Proposal {proposal_id} was not found."

    now = current_timestamp()
    name = actor_name(user)
    role_label = actor_role_label(user)
    current_version = safe_int(df.loc[mask, "decision_version"].iloc[0], 0) + 1

    if role_key == "ceo":
        df.loc[mask, "ceo_final_decision"] = decision
        df.loc[mask, "ceo_comment"] = comment
        df.loc[mask, "ceo_final_quote"] = safe_number(recommended_quote)
        df.loc[mask, "ceo_final_timeline_months"] = safe_int(recommended_timeline_months)
        df.loc[mask, "ceo_decided_by"] = name
        df.loc[mask, "ceo_decided_at"] = now
        df.loc[mask, "workflow_status"] = "Quotation Sent to Client"
        df.loc[mask, "current_owner"] = "Client"
        report_before_write = proposal_row_to_report(df.loc[mask].iloc[0])
        quotation = generate_client_quotation_text(
            report_before_write,
            decision,
            comment,
            recommended_quote,
            recommended_timeline_months,
        )
        df.loc[mask, "client_quotation"] = quotation
        df.loc[mask, "quotation_generated_at"] = now
        df.loc[mask, "quotation_sent"] = "Yes"
        df.loc[mask, "quotation_sent_at"] = now
        summary = (
            f"CEO final decision: {decision}. Client quotation generated and made visible to the client portal at "
            f"{money_text(recommended_quote)} for {safe_int(recommended_timeline_months)} month(s)."
        )
    else:
        quote_applicable = role_key in ["sales", "finance"]
        timeline_applicable = role_key == "operations"
        stored_quote = safe_number(recommended_quote) if quote_applicable else None
        stored_timeline = safe_int(recommended_timeline_months) if timeline_applicable else None

        df.loc[mask, f"{role_key}_decision"] = decision
        df.loc[mask, f"{role_key}_comment"] = comment
        df.loc[mask, f"{role_key}_recommended_quote"] = stored_quote
        df.loc[mask, f"{role_key}_recommended_timeline_months"] = stored_timeline
        df.loc[mask, f"{role_key}_decided_by"] = name
        df.loc[mask, f"{role_key}_decided_at"] = now
        df.loc[mask, "workflow_status"] = "Department Review In Progress"
        df.loc[mask, "current_owner"] = "CEO / Executive Team"
        summary = (
            f"{role_label} updated decision: {decision}. "
            "CEO and all other executives have been notified again."
        )

    df.loc[mask, "decision_version"] = current_version
    df.loc[mask, "last_updated_by"] = name
    df.loc[mask, "last_updated_role"] = role_label
    df.loc[mask, "last_updated_at"] = now
    df.loc[mask, "last_update_summary"] = summary

    if role_key == "ceo":
        # CEO can finalize and send the quotation without waiting for every
        # executive to record a separate decision. Once the CEO quotation is
        # visible to the client, the old department-review inbox should not
        # keep forcing Sales/Finance/HR/Operations to mark decisions.
        for seen_role, seen_column in PROPOSAL_NOTIFICATION_COLUMNS.items():
            df.loc[mask, seen_column] = "Yes"
            seen_at_column = PROPOSAL_SEEN_AT_COLUMNS.get(seen_role)
            if seen_at_column:
                df.loc[mask, seen_at_column] = now
    else:
        df = re_notify_everyone_except(df, mask, role_key)

    upsert_current_proposal_from_df(df, mask)
    history_quote = safe_number(recommended_quote) if role_key in ["sales", "finance", "ceo"] else ""
    history_timeline = safe_int(recommended_timeline_months) if role_key in ["operations", "ceo"] else ""
    append_proposal_history(
        proposal_id,
        user,
        "Decision Updated" if role_key != "ceo" else "CEO Final Decision",
        decision=decision,
        comment=comment,
        recommended_quote=history_quote,
        recommended_timeline_months=history_timeline,
        summary=summary,
    )

    if role_key == "ceo":
        return True, "CEO final decision saved. Client-ready quotation generated and made visible to the client portal."
    return True, f"{role_label} decision saved. CEO and every other executive were notified again."


def mark_quotation_sent_to_client(proposal_id, user):
    role_key = role_key_for_user(user)
    if role_key not in ["ceo", "sales"]:
        return False, "Only CEO or Sales Executive can mark the quotation as sent to the client."

    df = read_proposal_store(create_if_missing=True)
    mask = df["proposal_id"].astype(str) == str(proposal_id)
    if not mask.any():
        return False, f"Proposal {proposal_id} was not found."

    now = current_timestamp()
    df.loc[mask, "quotation_sent"] = "Yes"
    df.loc[mask, "quotation_sent_at"] = now
    df.loc[mask, "workflow_status"] = "Quotation Sent to Client"
    df.loc[mask, "current_owner"] = "Client"
    df.loc[mask, "last_updated_by"] = actor_name(user)
    df.loc[mask, "last_updated_role"] = actor_role_label(user)
    df.loc[mask, "last_updated_at"] = now
    df.loc[mask, "last_update_summary"] = "Client quotation was marked as sent."
    df = re_notify_everyone_except(df, mask, role_key)
    upsert_current_proposal_from_df(df, mask)
    append_proposal_history(
        proposal_id,
        user,
        "Quotation Sent",
        summary="Client quotation was marked as sent and all other executives were notified.",
    )
    return True, "Quotation marked as sent. The status was updated in Excel."


def write_decision_status(decision):
    if decision in ["Accept", "Approved", "Approve", "Support / Accept"]:
        st.success(decision)
    elif decision in [
        "Accept only with conditions",
        "Approved with Conditions",
        "Approve with Conditions",
        "Reject or Renegotiate",
        "Need Negotiation",
        "Negotiate with Client",
        "Support with Conditions",
        "Hold / Need More Review",
    ]:
        st.warning(decision)
    else:
        st.error(decision)


# ==== 04_proposal_ui.py ====

def render_dynamic_skill_gap_table(analysis):
    """Render HR/Operations skill-gap/capacity details safely.

    Some recent Operations UI cleanup versions still call this function from the
    CEO/executive decision pack, but the helper itself was missing. Keep this
    function lightweight and defensive so older proposals and newer dynamic
    capacity proposals both open without crashing.
    """
    try:
        skill_gap = analysis.get("skill_gap", []) if isinstance(analysis, dict) else []
        if isinstance(skill_gap, str):
            try:
                skill_gap = json.loads(skill_gap)
            except Exception:
                skill_gap = []
        if not isinstance(skill_gap, list):
            skill_gap = []

        rows = []
        for item in skill_gap:
            if not isinstance(item, dict):
                continue
            rows.append({
                "Role": safe_text(item.get("role") or item.get("Role") or "Required role"),
                "Needed FTE": safe_number(item.get("needed") or item.get("people_required") or item.get("required") or 0),
                "Available now": safe_number(item.get("available_capacity") or item.get("available_now") or item.get("current_available_fte") or 0),
                "Projected available": safe_number(item.get("projected_available_capacity") or item.get("projected_available_fte") or item.get("available_during_timeline") or item.get("available_capacity") or 0),
                "Immediate gap": safe_number(item.get("gap") or item.get("immediate_gap") or 0),
                "Projected gap": safe_number(item.get("projected_gap") or item.get("gap") or 0),
            })

        if rows:
            with st.expander("Role capacity and skill gap", expanded=False):
                st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
            return

        total_gap = safe_number(analysis.get("total_skill_gap", 0) if isinstance(analysis, dict) else 0)
        if total_gap:
            st.info(f"Total projected skill gap: {total_gap} FTE")
        else:
            st.caption("No detailed skill-gap table is available for this proposal.")
    except Exception as exc:
        st.caption(f"Skill-gap details are unavailable for this proposal. ({exc})")

def render_agentic_decision_pack(report):
    analysis = report["analysis"]
    summaries = report.get("agent_summaries", {})

    st.markdown(
        """
        <div class="dd-section-card">
            <div class="dd-section-title">Full multi-department agent analysis</div>
            <div class="dd-section-subtitle">
                These are the internal AI agent conclusions saved to Excel. Executives review this shared context before giving their own department opinion.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab_sales, tab_hr, tab_ops, tab_fin, tab_ceo = st.tabs([
        "🧲 Sales Agent",
        "👥 HR Agent",
        "🛠️ Operations Agent",
        "💰 Finance Agent",
        "👑 CEO Agent",
    ])

    with tab_sales:
        st.markdown("#### Sales Agent basis")
        st.write(summaries.get("sales") or "Sales summary unavailable.")
        s1, s2, s3 = st.columns(3)
        s1.metric("Client Budget", money_text(analysis["client_budget"]))
        s2.metric("Suggested Quote", money_text(analysis["recommended_quote"]))
        s3.metric("Project Type", analysis["project_type"])
        st.caption("Sales uses client budget, opportunity type, and quote direction to guide negotiation.")

    with tab_hr:
        st.markdown("#### HR Agent basis")
        st.write(summaries.get("hr") or "HR summary unavailable.")
        h1, h2 = st.columns(2)
        h1.metric("Total Skill Gap", f"{analysis['total_skill_gap']} FTE")
        hiring_flag = "Yes" if safe_number(analysis.get("total_skill_gap")) > 0 else "No"
        h2.metric("Hiring / Allocation Needed", hiring_flag)
        render_dynamic_skill_gap_table(analysis)
        st.caption("HR focuses on hiring need, available capacity, and resource risk — not quotation pricing.")

    with tab_ops:
        st.markdown("#### Operations Agent basis")
        st.write(summaries.get("operations") or "Operations summary unavailable.")
        o1, o2, o3 = st.columns(3)
        o1.metric("Requested Timeline", f"{analysis['timeline_months']} months")
        o2.metric("Timeline Risk", analysis["timeline_risk"])
        o3.metric("Resource Gap", f"{analysis['total_skill_gap']} FTE")
        st.caption("Operations checks delivery feasibility, timeline risk, blockers, and dependency planning.")

    with tab_fin:
        st.markdown("#### Finance Agent basis")
        st.write(summaries.get("finance") or "Finance summary unavailable.")
        f1, f2, f3, f4 = st.columns(4)
        f1.metric("Estimated Cost", money_text(analysis["estimated_cost"]))
        f2.metric("Recommended Quote", money_text(analysis["recommended_quote"]))
        f3.metric("Margin at Budget", f"{analysis['profit_margin_at_client_budget']}%")
        f4.metric("Target Margin", f"{analysis['target_margin_percent']}%")
        role_cost_df = pd.DataFrame(analysis.get("role_cost_breakdown", []))
        if not role_cost_df.empty:
            with st.expander("Role-level cost basis", expanded=False):
                st.dataframe(role_cost_df, use_container_width=True, hide_index=True)
        st.caption("Finance focuses on cost, profitability, payment risk, and finance-approved quote.")

    with tab_ceo:
        st.markdown("#### CEO Agent initial recommendation")
        st.write(summaries.get("ceo") or "CEO summary unavailable.")
        write_decision_status(analysis["initial_agent_decision"] or analysis["decision"])
        st.write(analysis["initial_agent_reason"] or analysis["reason"])


def render_executive_decision_summary(report):
    """Show every department opinion to every executive, while clearly marking non-applicable fields.

    HR should never appear to recommend a quote/timeline. Operations should never appear
    to recommend a quote. Sales/Finance should not be forced to recommend a delivery
    timeline. CEO is the only role with final quote + final timeline authority.
    """
    rows = []

    def quote_cell(role_key, item):
        if role_key in ["hr", "operations"]:
            return "Not applicable"
        value = item.get("recommended_quote")
        return money_text(value) if value else "Pending"

    def timeline_cell(role_key, item):
        if role_key in ["sales", "finance", "hr"]:
            return "Not applicable"
        value = item.get("recommended_timeline_months")
        return f"{value} months" if value else "Pending"

    for role_key, label in PROPOSAL_DEPARTMENT_LABELS.items():
        item = report.get("decisions", {}).get(role_key, {})
        rows.append({
            "Department": label,
            "Decision": item.get("decision") or "Pending",
            "Opinion / Reason": item.get("comment") or "",
            "Quote": quote_cell(role_key, item),
            "Timeline": timeline_cell(role_key, item),
            "By": item.get("decided_by") or "",
            "Updated At": item.get("decided_at") or "",
        })
    st.markdown(
        """
        <div class="dd-section-card">
            <div class="dd-section-title">Human executive review summary</div>
            <div class="dd-section-subtitle">
                AI prepares the decision intelligence. Human executives validate, challenge, and approve it.
                Non-applicable columns are marked clearly so each department stays in its own responsibility area.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


def render_decision_history(proposal_id):
    history = get_proposal_history(proposal_id)
    if history.empty:
        return
    with st.expander("Decision audit trail", expanded=False):
        columns = [
            "event_at",
            "actor_role",
            "actor_name",
            "action_type",
            "decision",
            "comment",
            "summary",
        ]
        available = [col for col in columns if col in history.columns]
        st.dataframe(history[available], use_container_width=True, hide_index=True)


def render_client_quotation(report, user=None):
    quotation = report.get("client_quotation")
    if not quotation:
        return

    role_key = role_key_for_user(user)
    status = report.get("quotation_sent", "No")
    generated = report.get("quotation_generated_at", "")
    sent_at = report.get("quotation_sent_at", "")

    if str(status).strip().lower() == "yes":
        st.success("Quotation is visible in the client portal after CEO approval.")
    elif role_key == "sales":
        st.info("Quotation is generated but not yet marked visible to the client portal.")

    st.markdown(
        """
        <div class="dd-section-card">
            <div class="dd-section-title">Client-ready quotation / response</div>
            <div class="dd-section-subtitle">
                This is generated after CEO final approval. It hides internal salary, cost basis, and margin details.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption(f"Generated: {generated} | Sent to client: {status}" + (f" at {sent_at}" if sent_at else ""))
    st.text_area(
        "Client quotation",
        value=quotation,
        height=280,
        key=f"quotation_text_{report.get('proposal_id')}",
    )
    if role_key in ["ceo", "sales"] and str(status).strip().lower() != "yes":
        button_label = "Send quotation to client / mark as sent" if role_key == "sales" else "Mark quotation as sent to client"
        if st.button(button_label, key=f"mark_quote_sent_{report.get('proposal_id')}_{role_key}", type="primary"):
            success, message = mark_quotation_sent_to_client(report.get("proposal_id"), user)
            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)


def render_executive_decision_form(report, user):
    role_key = role_key_for_user(user)
    if role_key not in PROPOSAL_DEPARTMENT_LABELS:
        return

    proposal_id = report.get("proposal_id")
    if not proposal_id:
        st.info("This proposal is not saved in proposal storage yet, so decisions cannot be persisted.")
        return

    analysis = report["analysis"]
    existing = report.get("decisions", {}).get(role_key, {})
    default_quote = existing.get("recommended_quote") or analysis.get("recommended_quote") or 0
    default_timeline = existing.get("recommended_timeline_months") or analysis.get("timeline_months") or 1

    role_intro = {
        "sales": (
            "Sales Executive Opinion",
            "Comment only on client fit, negotiation strategy, and client-facing commercial positioning.",
        ),
        "finance": (
            "Finance Executive Opinion",
            "Comment only on cost, margin, payment risk, and finance-safe quote.",
        ),
        "hr": (
            "HR Executive Resource Opinion",
            "Comment only on hiring need, skill gap, availability, and people/resource risk.",
        ),
        "operations": (
            "Operations Executive Delivery Opinion",
            "Comment only on delivery feasibility, timeline, blockers, and execution plan.",
        ),
        "ceo": (
            "CEO Final Decision",
            "Review every department opinion, approve the final quote/timeline, and generate the client quotation.",
        ),
    }
    title, subtitle = role_intro.get(role_key, (f"{PROPOSAL_DEPARTMENT_LABELS[role_key]} Decision", "Submit your role opinion."))

    st.markdown(
        f"""
        <div class=\"dd-section-card\">
            <div class=\"dd-section-title\">{title}</div>
            <div class=\"dd-section-subtitle\">{subtitle}</div>
            <div class=\"dd-muted-small\">Submitting updates proposal storage and re-notifies every other executive.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    options = CEO_DECISION_OPTIONS if role_key == "ceo" else EXECUTIVE_DECISION_OPTIONS
    previous_decision = existing.get("decision")
    default_index = options.index(previous_decision) if previous_decision in options else 0

    with st.form(key=f"decision_form_{proposal_id}_{role_key}"):
        decision = st.selectbox("Your decision", options, index=default_index, key=f"decision_select_{proposal_id}_{role_key}")

        if role_key == "sales":
            st.caption("Sales view: client fit, negotiation path, and commercial communication.")
            comment = st.text_area(
                "Sales opinion / negotiation plan for CEO review",
                value=existing.get("comment", ""),
                height=130,
                key=f"decision_comment_{proposal_id}_{role_key}",
            )
            recommended_quote = st.number_input(
                "Sales suggested client-facing quote (₹)",
                min_value=0.0,
                value=float(default_quote),
                step=50000.0,
                key=f"decision_quote_{proposal_id}_{role_key}",
            )
            recommended_timeline = None

        elif role_key == "finance":
            st.caption("Finance view: cost, margin, payment terms, and financially safe quote.")
            comment = st.text_area(
                "Finance opinion / margin and payment risk note",
                value=existing.get("comment", ""),
                height=130,
                key=f"decision_comment_{proposal_id}_{role_key}",
            )
            recommended_quote = st.number_input(
                "Finance-approved minimum quote (₹)",
                min_value=0.0,
                value=float(default_quote),
                step=50000.0,
                key=f"decision_quote_{proposal_id}_{role_key}",
            )
            recommended_timeline = None

        elif role_key == "hr":
            st.caption("HR-only action form active: no quotation amount and no delivery timeline fields are shown here.")
            if analysis.get("skill_gap"):
                with st.expander("Live HR/Operations capacity reference", expanded=True):
                    render_dynamic_skill_gap_table(analysis)
            comment = st.text_area(
                "HR opinion: hiring needed, roles to allocate/hire, people risk, onboarding/resource plan",
                value=existing.get("comment", ""),
                height=150,
                key=f"decision_comment_{proposal_id}_{role_key}",
            )
            recommended_quote = None
            recommended_timeline = None

        elif role_key == "operations":
            st.caption("Operations view: delivery feasibility, timeline confidence, blockers, and execution plan.")
            comment = st.text_area(
                "Operations opinion / delivery plan / blockers",
                value=existing.get("comment", ""),
                height=130,
                key=f"decision_comment_{proposal_id}_{role_key}",
            )
            recommended_quote = None
            recommended_timeline = st.number_input(
                "Operations recommended delivery timeline (months)",
                min_value=1,
                value=max(1, int(default_timeline)),
                step=1,
                key=f"decision_timeline_{proposal_id}_{role_key}",
            )

        else:
            st.caption("CEO view: final business decision, final quote, final timeline, and quotation generation.")
            comment = st.text_area(
                "CEO final note / reason / client-facing condition",
                value=existing.get("comment", ""),
                height=130,
                key=f"decision_comment_{proposal_id}_{role_key}",
            )
            c1, c2 = st.columns(2)
            with c1:
                recommended_quote = st.number_input(
                    "Final approved quote (₹)",
                    min_value=0.0,
                    value=float(default_quote),
                    step=50000.0,
                    key=f"decision_quote_{proposal_id}_{role_key}",
                )
            with c2:
                recommended_timeline = st.number_input(
                    "Final approved timeline (months)",
                    min_value=1,
                    value=max(1, int(default_timeline)),
                    step=1,
                    key=f"decision_timeline_{proposal_id}_{role_key}",
                )

        if role_key == "ceo":
            submitted = st.form_submit_button("Save CEO final decision and generate client quotation", type="primary")
        else:
            submitted = st.form_submit_button("Submit / update my department opinion", type="primary")

    if submitted:
        if not safe_text(comment).strip():
            st.error("Please add your opinion/comment before submitting. This is needed for CEO review.")
            return
        success, message = submit_proposal_decision(
            proposal_id,
            user,
            decision,
            comment,
            recommended_quote,
            recommended_timeline,
        )
        if success:
            st.success(message)
            st.rerun()
        else:
            st.error(message)


def render_external_client_report(report, user=None, compact=False):
    analysis = report["analysis"]
    st.markdown(
        """
        <div class="dd-section-card">
            <div class="dd-section-title">Client proposal decision room</div>
            <div class="dd-section-subtitle">
                Shared view for Sales, HR, Operations, Finance, and CEO. Agent analysis is generated first; human executives then review and approve.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if report.get("proposal_id"):
        st.caption(
            f"Proposal ID: {report['proposal_id']} | Created: {report.get('created_at', '')} | "
            f"Status: {report.get('workflow_status', 'Awaiting Executive Decisions')} | "
            f"Version: {report.get('decision_version', 0)}"
        )
    if report.get("last_update_summary"):
        st.info(
            f"Latest update: {report.get('last_update_summary')} "
            f"({report.get('last_updated_role')} - {report.get('last_updated_by')} at {report.get('last_updated_at')})"
        )

    render_client_requirement_box(report.get("raw_client_message", analysis.get("client_message", "")))

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Project Type", analysis["project_type"])
    c2.metric("Client Budget", money_text(analysis["client_budget"]))
    c3.metric("Timeline", f"{analysis['timeline_months']} months")
    c4.metric("Current Decision", analysis["decision"] or "Pending")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Estimated Cost", money_text(analysis["estimated_cost"]))
    m2.metric("Recommended Quote", money_text(analysis["recommended_quote"]))
    m3.metric("Margin at Budget", f"{analysis['profit_margin_at_client_budget']}%")
    m4.metric("Timeline Risk", analysis["timeline_risk"])

    st.markdown("#### Initial agentic conclusion")
    write_decision_status(analysis["initial_agent_decision"] or analysis["decision"])
    st.write(analysis["initial_agent_reason"] or analysis["reason"])

    if compact:
        return

    render_agentic_decision_pack(report)
    render_executive_decision_summary(report)
    render_client_quotation(report, user=user)
    render_decision_history(report.get("proposal_id"))
    render_executive_decision_form(report, user)


def render_pending_proposal_notifications(user, data=None):
    """Compact executive notification inbox.

    Older versions opened every pending proposal as a full expander, which made the
    CEO/executive dashboard turn into a long scrolling page. This version shows a
    single dropdown-style inbox first. The user chooses one update, then only that
    proposal is rendered below as the active dashboard item.
    """
    column = user_notification_column(user)
    if column is None:
        return

    try:
        reports = get_pending_proposal_reports_for_user(user)
    except Exception as exc:
        st.error(f"Could not load proposal notifications from proposal storage: {exc}")
        return

    if not reports:
        st.success("No new proposal decision updates for your role.")
        return

    def sort_key(report):
        return safe_text(report.get("last_updated_at") or report.get("created_at"))

    reports = sorted(reports, key=sort_key, reverse=True)
    role_key = role_key_for_user(user) or "executive"
    selected_key = f"selected_pending_proposal_{role_key}"

    st.markdown(
        f"""
        <div class="dd-section-card">
            <div class="dd-section-title">Executive update inbox</div>
            <div class="dd-section-subtitle">
                You have <b>{len(reports)}</b> pending update(s). Open the dropdown and choose one item.
                The latest updates are shown first, and only the selected proposal opens below.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    option_map = {"": None}
    labels = ["Select an update to open..."]
    for idx, report in enumerate(reports, start=1):
        analysis = report.get("analysis", {})
        updated = safe_text(report.get("last_updated_at") or report.get("created_at") or "No timestamp")
        label = (
            f"{idx}. {updated} | {report.get('proposal_id') or 'Proposal'} | "
            f"{analysis.get('project_type', 'Project')} | {report.get('workflow_status', 'Pending')} | "
            f"Last: {report.get('last_updated_role', 'System')}"
        )
        labels.append(label)
        option_map[label] = report

    with st.expander(f"{len(reports)} pending update(s) - click to open", expanded=False):
        current_label = st.session_state.get(selected_key, "Select an update to open...")
        if current_label not in labels:
            current_label = "Select an update to open..."
        selected_label = st.selectbox(
            "Choose update",
            labels,
            index=labels.index(current_label),
            key=f"pending_update_selector_{role_key}",
        )
        st.session_state[selected_key] = selected_label

        preview_rows = []
        for report in reports[:8]:
            analysis = report.get("analysis", {})
            preview_rows.append({
                "Updated": safe_text(report.get("last_updated_at") or report.get("created_at")),
                "Proposal": report.get("proposal_id"),
                "Project": analysis.get("project_type"),
                "Status": report.get("workflow_status"),
                "Last By": report.get("last_updated_role"),
            })
        if preview_rows:
            st.dataframe(pd.DataFrame(preview_rows), use_container_width=True, hide_index=True)

    selected_report = option_map.get(st.session_state.get(selected_key, ""))
    if not selected_report:
        st.info("Choose one update from the dropdown to open its full decision dashboard.")
        return

    st.markdown("### Selected update dashboard")
    is_operations_delivery_item = (
        role_key == "operations"
        and (
            safe_text(selected_report.get("client_response")) == "Accept Proposal"
            or safe_text(selected_report.get("project_id")).strip()
            or "delivery" in safe_text(selected_report.get("workflow_status")).lower()
            or "kickoff" in safe_text(selected_report.get("workflow_status")).lower()
            or "operations" in safe_text(selected_report.get("current_owner")).lower()
        )
    )
    if is_operations_delivery_item:
        st.info("This is now a delivery-readiness item, not a department-decision item. Old Sales/Finance/HR/CEO review details are hidden.")
        render_operations_delivery_workspace(user, data or {}, focus_proposal_id=selected_report.get("proposal_id"))
    else:
        render_external_client_report(selected_report, user=user, compact=False)

    if st.button(
        "Mark selected update as reviewed without changing my decision",
        key=f"mark_seen_selected_{selected_report.get('proposal_id')}_{role_key}",
    ):
        success, message = mark_proposal_seen_for_user(selected_report.get("proposal_id"), user)
        if success:
            st.success(message)
            st.session_state[selected_key] = "Select an update to open..."
            st.rerun()
        else:
            st.error(message)


def render_all_proposals_board(user):
    if role_key_for_user(user) is None:
        return
    with st.expander("All proposal decision board", expanded=False):
        reports = get_all_proposal_reports(limit=25)
        if not reports:
            last_error = st.session_state.get("proposal_storage_last_error", "")
            if last_error:
                st.warning("Could not load proposal board because Supabase is temporarily unreachable. Try refresh/restart, or check pooler URL/network.")
                with st.expander("Show proposal storage error", expanded=False):
                    st.code(last_error)
            else:
                st.info("No proposal decisions saved yet.")
            return
        rows = []
        for report in reports:
            analysis = report["analysis"]
            rows.append({
                "Proposal ID": report.get("proposal_id"),
                "Created": report.get("created_at"),
                "Project": analysis.get("project_type"),
                "Budget": safe_number(analysis.get("client_budget")),
                "Quote": safe_number(analysis.get("recommended_quote")),
                "Status": report.get("workflow_status"),
                "Initial Decision": analysis.get("initial_agent_decision"),
                "Sales": report.get("decisions", {}).get("sales", {}).get("decision") or "Pending",
                "Finance": report.get("decisions", {}).get("finance", {}).get("decision") or "Pending",
                "HR": report.get("decisions", {}).get("hr", {}).get("decision") or "Pending",
                "Operations": report.get("decisions", {}).get("operations", {}).get("decision") or "Pending",
                "CEO Final": report.get("decisions", {}).get("ceo", {}).get("decision") or "Pending",
                "Quote Sent": report.get("quotation_sent", "No"),
                "Last Updated": report.get("last_updated_at"),
            })
        board = pd.DataFrame(rows)
        st.dataframe(board, use_container_width=True, hide_index=True)
        st.caption("Open a pending notification above to comment/update your role decision. If you marked a proposal reviewed, it remains visible here.")


def render_latest_external_client_workspace(user):
    render_pending_proposal_notifications(user)
    render_all_proposals_board(user)


def write_sql_or_text_result(result):
    if isinstance(result, dict):
        st.write(result["answer"])
        if result.get("success"):
            with st.expander("Show SQL and result"):
                st.code(result["sql"], language="sql")
                st.dataframe(result["dataframe"], use_container_width=True)
    else:
        st.write(result)


# ==== 05_design_system.py ====
# ---------------- UI / PRESENTATION HELPERS ----------------

APP_NAME = "LifecycleDesk AI"
APP_TAGLINE = "End-to-end AI lifecycle platform for proposals, approvals, delivery, resources, and updates"
# APP_VERSION = "v25.29 operations cleanup"


def inject_design_system():
    st.markdown(
        """
        <style>
            :root {
                --dd-bg: #f5f7fb;
                --dd-card: #ffffff;
                --dd-ink: #0f172a;
                --dd-muted: #64748b;
                --dd-line: #d7e0ec;
                --dd-blue: #1d4ed8;
                --dd-purple: #6d28d9;
                --dd-cyan: #0891b2;
                --dd-green: #16a34a;
                --dd-yellow: #ca8a04;
                --dd-red: #dc2626;
                --dd-soft-blue: #eff6ff;
                --dd-soft-purple: #f5f3ff;
                --dd-soft-green: #f0fdf4;
                --dd-soft-yellow: #fefce8;
            }
            html, body, [data-testid="stAppViewContainer"] {
                background:
                    radial-gradient(circle at top left, rgba(37, 99, 235, 0.10), transparent 35%),
                    radial-gradient(circle at top right, rgba(124, 58, 237, 0.10), transparent 32%),
                    var(--dd-bg);
            }
            [data-testid="stSidebar"], [data-testid="collapsedControl"] {
                display: none !important;
            }
            .block-container {
                padding-top: 1.1rem;
                padding-bottom: 3.25rem;
                max-width: 1220px;
            }
            [data-testid="stVerticalBlock"] { gap: 0.85rem; }
            [data-testid="column"] { align-self: stretch; }
            .stTabs [data-baseweb="tab-list"] {
                gap: 8px;
                background: #eef2f7;
                padding: 6px;
                border-radius: 16px;
            }
            .stTabs [data-baseweb="tab"] {
                border-radius: 12px;
                font-weight: 750;
            }
            h1, h2, h3 {
                letter-spacing: -0.035em;
            }
            div[data-testid="stMetric"] {
                background: #ffffff;
                border: 1px solid var(--dd-line);
                border-radius: 16px;
                padding: 14px 16px;
                box-shadow: 0 8px 24px rgba(15, 23, 42, 0.04);
            }
            div[data-testid="stMetricLabel"] p {
                color: var(--dd-muted) !important;
                font-size: 0.86rem;
            }
            .dd-hero {
                background: linear-gradient(135deg, #0f172a 0%, #1e40af 52%, #6d28d9 100%);
                border-radius: 28px;
                padding: 34px 36px 32px 36px;
                color: white;
                margin: 4px 0 22px 0;
                box-shadow: 0 24px 60px rgba(37, 99, 235, 0.24);
                overflow: hidden;
                position: relative;
            }
            .dd-hero:after {
                content: "";
                position: absolute;
                width: 280px;
                height: 280px;
                right: -80px;
                top: -90px;
                background: rgba(255,255,255,0.10);
                border-radius: 50%;
            }
            .dd-kicker {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                padding: 7px 12px;
                background: rgba(255,255,255,0.14);
                border: 1px solid rgba(255,255,255,0.24);
                border-radius: 999px;
                font-size: 0.82rem;
                font-weight: 700;
                margin-bottom: 14px;
            }
            .dd-hero-title {
                font-size: clamp(2.2rem, 5vw, 4.2rem);
                line-height: 0.98;
                font-weight: 850;
                letter-spacing: -0.06em;
                margin: 0 0 12px 0;
            }
            .dd-hero-subtitle {
                font-size: 1.08rem;
                line-height: 1.6;
                max-width: 860px;
                opacity: 0.92;
                margin-bottom: 22px;
            }
            .dd-flow {
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                margin-top: 8px;
            }
            .dd-flow span {
                background: rgba(255,255,255,0.13);
                border: 1px solid rgba(255,255,255,0.22);
                border-radius: 13px;
                padding: 9px 12px;
                font-weight: 650;
                font-size: 0.88rem;
            }
            .dd-section-card {
                background: var(--dd-card);
                border: 1px solid var(--dd-line);
                border-radius: 22px;
                padding: 20px 22px;
                margin: 12px 0 16px 0;
                box-shadow: 0 12px 32px rgba(15, 23, 42, 0.055);
            }
            .dd-dashboard-shell {
                background: rgba(255,255,255,0.82);
                border: 1px solid rgba(215,224,236,0.95);
                border-radius: 24px;
                padding: 18px 20px;
                margin: 12px 0 18px 0;
                box-shadow: 0 16px 42px rgba(15, 23, 42, 0.06);
            }
            .dd-title-row {
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                gap: 14px;
                margin-bottom: 10px;
            }
            .dd-title-badge {
                display: inline-flex;
                align-items: center;
                padding: 6px 10px;
                border-radius: 999px;
                background: #e0f2fe;
                color: #075985;
                font-size: 0.78rem;
                font-weight: 800;
                white-space: nowrap;
            }
            .dd-quote-update-card {
                background: linear-gradient(135deg, #f8fafc, #eef2ff);
                border: 1px solid #c7d2fe;
                border-left: 5px solid #4f46e5;
                border-radius: 18px;
                padding: 15px 16px;
                margin: 12px 0 14px 0;
                line-height: 1.55;
            }
            .dd-quote-update-card b { color: #312e81; }
            .dd-quote-update-card .dd-small-line { color: #475569; font-size: 0.92rem; margin-top: 4px; }
            .dd-section-title {
                font-size: 1.35rem;
                font-weight: 820;
                color: var(--dd-ink);
                margin-bottom: 6px;
            }
            .dd-section-subtitle {
                color: var(--dd-muted);
                line-height: 1.55;
                margin-bottom: 12px;
            }
            .dd-agent-card {
                background: #ffffff;
                border: 1px solid var(--dd-line);
                border-radius: 18px;
                padding: 15px 16px;
                min-height: 142px;
                height: 100%;
                box-shadow: 0 8px 24px rgba(15, 23, 42, 0.045);
            }
            .dd-agent-name {
                font-size: 1rem;
                font-weight: 800;
                color: var(--dd-ink);
                margin-bottom: 6px;
            }
            .dd-agent-desc {
                font-size: 0.88rem;
                color: var(--dd-muted);
                line-height: 1.45;
            }
            .dd-status-pill {
                display: inline-block;
                padding: 5px 10px;
                border-radius: 999px;
                background: var(--dd-soft-green);
                color: #166534;
                font-size: 0.78rem;
                font-weight: 750;
                margin-bottom: 8px;
            }
            .dd-alert-action {
                background: linear-gradient(135deg, #ecfeff, #eff6ff);
                border: 1px solid #bfdbfe;
                border-radius: 18px;
                padding: 14px 16px;
                color: #0f172a;
                margin: 10px 0 14px 0;
            }
            .dd-muted-small {
                color: var(--dd-muted);
                font-size: 0.9rem;
                line-height: 1.45;
            }
            .dd-client-box {
                background: #f8fafc;
                border: 1px solid var(--dd-line);
                border-left: 5px solid var(--dd-blue);
                border-radius: 16px;
                padding: 15px 16px;
                line-height: 1.55;
                margin: 8px 0 16px 0;
            }
            .dd-stepper {
                display: grid;
                grid-template-columns: repeat(5, minmax(140px, 1fr));
                gap: 10px;
                margin: 12px 0 18px 0;
            }
            .dd-step {
                border: 1px solid var(--dd-line);
                background: #ffffff;
                border-radius: 16px;
                padding: 12px 14px;
                font-size: 0.86rem;
                box-shadow: 0 8px 18px rgba(15, 23, 42, 0.04);
            }
            .dd-step strong {
                display: block;
                color: var(--dd-ink);
                margin-bottom: 4px;
            }
            .dd-step span {
                color: var(--dd-muted);
            }

            .stButton > button, div[data-testid="stDownloadButton"] button {
                border-radius: 12px !important;
                border: 1px solid #bfdbfe !important;
                background: linear-gradient(135deg, #1d4ed8, #6d28d9) !important;
                color: #ffffff !important;
                font-weight: 760 !important;
                min-height: 42px;
                box-shadow: 0 10px 22px rgba(37, 99, 235, 0.18) !important;
            }
            .stButton > button:hover, div[data-testid="stDownloadButton"] button:hover {
                transform: translateY(-1px);
                box-shadow: 0 14px 28px rgba(37, 99, 235, 0.24) !important;
            }
            div[data-testid="stSelectbox"] > div, div[data-testid="stTextInput"] > div,
            div[data-testid="stTextArea"] textarea, div[data-testid="stNumberInput"] > div {
                border-radius: 12px !important;
            }
            .dd-topbar {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 16px;
                background: rgba(255,255,255,0.92);
                border: 1px solid rgba(219,228,240,0.95);
                border-radius: 20px;
                padding: 14px 18px;
                margin: 6px 0 14px 0;
                min-height: 74px;
                box-shadow: 0 12px 30px rgba(15, 23, 42, 0.06);
                backdrop-filter: blur(8px);
            }
            .dd-brand-mini {
                font-weight: 900;
                letter-spacing: -0.035em;
                color: var(--dd-ink);
                font-size: 1.15rem;
            }
            .dd-brand-mini span {
                color: var(--dd-blue);
            }
            .dd-chip {
                display: inline-flex;
                align-items: center;
                gap: 6px;
                padding: 6px 10px;
                border-radius: 999px;
                background: #eef2ff;
                color: #3730a3;
                font-size: 0.80rem;
                font-weight: 760;
            }
            .dd-lifecycle-grid {
                display: grid;
                grid-template-columns: repeat(4, minmax(180px, 1fr));
                gap: 14px;
                margin-top: 14px;
            }
            .dd-life-card {
                background: linear-gradient(180deg, #ffffff, #f8fafc);
                border: 1px solid var(--dd-line);
                border-radius: 18px;
                padding: 15px 16px;
                box-shadow: 0 10px 24px rgba(15, 23, 42, 0.045);
            }
            .dd-life-card b { color: var(--dd-ink); display: block; margin-bottom: 5px; }
            .dd-life-card span { color: var(--dd-muted); font-size: 0.88rem; line-height: 1.45; }


            /* v25.24 polish: tighter alignment, clearer cards, fewer visual jumps */
            .element-container { scroll-margin-top: 96px; }
            div[data-testid="stForm"] {
                border: 1px solid #dbe4f0;
                border-radius: 18px;
                padding: 14px 16px 16px 16px;
                background: rgba(255,255,255,0.78);
                box-shadow: 0 8px 22px rgba(15, 23, 42, 0.035);
            }
            div[data-testid="stExpander"] {
                border: 1px solid #dbe4f0 !important;
                border-radius: 18px !important;
                overflow: hidden;
                background: #ffffff;
                box-shadow: 0 8px 22px rgba(15, 23, 42, 0.035);
            }
            div[data-testid="stExpander"] summary {
                font-weight: 800;
                color: #0f172a;
            }
            div[data-baseweb="select"] > div {
                border-radius: 14px !important;
                border-color: #cbd5e1 !important;
            }
            .dd-client-progress-card {
                background: linear-gradient(135deg, #f8fafc, #f0f9ff);
                border: 1px solid #bae6fd;
                border-left: 5px solid #0284c7;
                border-radius: 20px;
                padding: 16px 18px;
                margin: 12px 0 16px 0;
                box-shadow: 0 10px 26px rgba(14, 165, 233, 0.08);
            }
            .dd-client-progress-card b {
                color: #0f172a;
                font-size: 1.04rem;
            }
            .dd-client-progress-card span {
                display: block;
                color: #475569;
                margin-top: 5px;
                line-height: 1.5;
            }
            .dd-action-path {
                background: #f8fafc;
                border: 1px dashed #94a3b8;
                border-radius: 16px;
                padding: 12px 14px;
                color: #334155;
                font-size: 0.92rem;
                line-height: 1.5;
                margin: 8px 0 14px 0;
            }

            .dd-project-card {
                background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%);
                border: 1px solid #dbe4f0;
                border-radius: 22px;
                padding: 18px 20px;
                margin: 12px 0 16px 0;
                box-shadow: 0 14px 34px rgba(15, 23, 42, 0.06);
            }
            .dd-card-header-row {
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                gap: 14px;
                margin-bottom: 14px;
            }
            .dd-card-kicker {
                color: #64748b;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                font-size: 0.72rem;
                font-weight: 850;
                margin-bottom: 4px;
            }
            .dd-card-title-small {
                color: #0f172a;
                font-weight: 900;
                font-size: 1.18rem;
                letter-spacing: -0.03em;
            }
            .dd-card-subtle {
                color: #64748b;
                font-size: 0.86rem;
                margin-top: 3px;
            }
            .dd-status-pill {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                padding: 7px 11px;
                border-radius: 999px;
                background: #ecfdf5;
                color: #047857;
                border: 1px solid #bbf7d0;
                font-weight: 850;
                font-size: 0.82rem;
                white-space: nowrap;
            }
            .dd-metric-grid {
                display: grid;
                grid-template-columns: repeat(3, minmax(150px, 1fr));
                gap: 12px;
            }
            .dd-mini-metric {
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 16px;
                padding: 12px 14px;
            }
            .dd-mini-metric span {
                display: block;
                color: #64748b;
                font-size: 0.78rem;
                font-weight: 760;
                margin-bottom: 5px;
            }
            .dd-mini-metric strong {
                color: #0f172a;
                font-size: 1rem;
                font-weight: 900;
            }
            .dd-soft-panel {
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 18px;
                padding: 14px 16px;
                color: #334155;
                margin: 10px 0 14px 0;
            }
            .dd-soft-panel span { color: #64748b; }

            @media (max-width: 900px) {
                .dd-lifecycle-grid { grid-template-columns: 1fr; }
                .dd-stepper { grid-template-columns: 1fr; }
                .dd-title-row { flex-direction: column; }
                .dd-hero { padding: 26px 22px; }
                .dd-topbar { align-items: flex-start; flex-direction: column; }
                .dd-card-header-row { flex-direction: column; }
                .dd-metric-grid { grid-template-columns: 1fr; }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_app_hero():
    st.markdown(
        f"""
        <div class=\"dd-hero\">
            <div class=\"dd-kicker\">🚀  Full lifecycle agentic operating system </div>
            <div class=\"dd-hero-title\">{APP_NAME}</div>
            <div class=\"dd-hero-subtitle\">
                {APP_TAGLINE}. One AI workspace manages the full business lifecycle: client intake, agent analysis,
                executive approval, quotation, client response, delivery readiness, resource allocation, employee updates, and operations follow-up.
            </div>
            <div class=\"dd-flow\">
                <span>1. Client intake</span>
                <span>2. Agent analysis</span>
                <span>3. Executive approval</span>
                <span>4. Quotation + client response</span>
                <span>5. Weekly project updates</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_agent_cards():
    agents = [
        ("🧲 Sales Agent", "Client fit, budget signal, quotation readiness, negotiation context."),
        ("👥 HR Agent", "Skill gap, hiring need, capacity impact, people risk."),
        ("🛠️ Operations Agent", "Delivery plan, blockers, weekly updates, employee support requests."),
        ("💰 Finance Agent", "Cost, margin, profitability, payment risk, finance-safe quote."),
        ("👑 CEO Agent", "Final approval, revised quote, strategic lifecycle decision."),
    ]
    cols = st.columns(5)
    for col, (name, desc) in zip(cols, agents):
        with col:
            st.markdown(
                f"""
                <div class=\"dd-agent-card\">
                    <div class=\"dd-status-pill\">Active</div>
                    <div class=\"dd-agent-name\">{name}</div>
                    <div class=\"dd-agent-desc\">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_process_snapshot():
    st.markdown(
        """
        <div class=\"dd-section-card\">
            <div class=\"dd-section-title\">Decision workflow</div>
            <div class=\"dd-section-subtitle\">
                The system manages the complete client-to-delivery lifecycle with compact, role-specific dashboards and clear action paths.
            </div>
            <div class=\"dd-stepper\">
                <div class=\"dd-step\"><strong>Front Desk</strong><span>Receives client proposal</span></div>
                <div class=\"dd-step\"><strong>Agent Meeting</strong><span>Sales, HR, Ops, Finance, CEO analyse</span></div>
                <div class=\"dd-step\"><strong>Executive Review</strong><span>Humans add role-specific opinions</span></div>
                <div class=\"dd-step\"><strong>CEO Decision</strong><span>Final quote and timeline approved</span></div>
                <div class=\"dd-step\"><strong>Client Quote</strong><span>Sales sends the approved response</span></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_workspace_header(user):
    role = user.get("role", "")
    department = user.get("department", "")
    designation = user.get("designation", "")
    if role == "founder":
        title = "CEO Lifecycle Command Center"
        subtitle = "Review department opinions, approve/revise quotations, and monitor live business lifecycle performance."
    elif role == "executive":
        title = f"{department} Executive Review Desk"
        subtitle = "Review selected lifecycle items, submit department decisions, and respond to project delivery updates."
    else:
        title = "Employee Project Lifecycle Workspace"
        subtitle = "Open assigned projects, submit weekly updates, and raise blockers or resource requests."
    st.markdown(
        f"""
        <div class=\"dd-section-card\">
            <div class=\"dd-section-title\">{title}</div>
            <div class=\"dd-section-subtitle\">{subtitle}</div>
            <div class=\"dd-muted-small\">Signed in as <b>{user.get('employee_name', '')}</b> · {designation}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_chat_intro():
    st.markdown(
        """
        <div class=\"dd-section-card\">
            <div class=\"dd-section-title\">AI Front Desk</div>
            <div class=\"dd-section-subtitle\">
                Use this only when you want to ask the AI receptionist something or start a new client/proposal workflow.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_client_requirement_box(text):
    st.markdown(
        f"""
        <div class=\"dd-client-box\">
            <b>Client Requirement</b><br/>
            {safe_text(text).replace(chr(10), '<br/>')}
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==== 06_streamlit_runtime.py ====
# ---------------- STREAMLIT UI ----------------

st.set_page_config(page_title=APP_NAME, layout="wide", page_icon="🚀", initial_sidebar_state="collapsed")
inject_design_system()

# Keep the landing/marketing section only for logged-out visitors.
# Once a user/client logs in, the dashboard becomes the page focus.
if not (st.session_state.get("user") or st.session_state.get("client_user")):
    render_app_hero()
    render_agent_cards()
    render_process_snapshot()

try:
    data = load_cached_company_data()
except (zipfile.BadZipFile, OSError, ValueError) as exc:
    st.error("The Excel database file appears to be corrupted or locked.")
    st.markdown(
        f"""
        **Database path:** `{DB_PATH}`

        **Technical error:** `{exc}`

        This usually happens when the `.xlsx` file is open in Excel while Streamlit is writing,
        or when the app is stopped during an Excel save.

        **Fix:**
        1. Stop Streamlit.
        2. Close `virtual_company_db_final.xlsx` in Excel.
        3. Restore the latest good file from `db/backups/`, or replace it with a clean copy of the database.
        4. Restart with `streamlit run app.py`.

        From this version onward, the app creates timestamped backups in `db/backups/` before every Excel update.
        """
    )
    st.stop()

if "user" not in st.session_state:
    st.session_state.user = None

if "client_user" not in st.session_state:
    st.session_state.client_user = None

if "show_login" not in st.session_state:
    st.session_state.show_login = False

if "messages" not in st.session_state:
    st.session_state.messages = []

if "external_enquiry_mode" not in st.session_state:
    st.session_state.external_enquiry_mode = False

if "pending_client_proposal_text" not in st.session_state:
    st.session_state.pending_client_proposal_text = ""

if "_dd_scroll_target" not in st.session_state:
    st.session_state["_dd_scroll_target"] = ""


def request_page_scroll(target):
    """Request one controlled browser scroll on the next render."""
    try:
        st.session_state["_dd_scroll_target"] = safe_text(target)
    except Exception:
        st.session_state["_dd_scroll_target"] = target or ""


def run_pending_page_scroll():
    """Scroll only to the intended UI section, not always to the receptionist chat."""
    target = st.session_state.get("_dd_scroll_target", "")
    if not target:
        return
    st.session_state["_dd_scroll_target"] = ""
    if target == "login":
        selector = "#dd-login-panel"
        block = "start"
    elif target == "dashboard":
        selector = "#dd-dashboard-panel"
        block = "start"
    elif target == "chat":
        selector = '[data-testid="stChatMessage"]:last-of-type'
        block = "end"
    else:
        selector = "body"
        block = "start"
    try:
        components.html(
            f"""
            <script>
            setTimeout(function() {{
                const doc = window.parent.document;
                let target = null;
                if ({target!r} === 'chat') {{
                    const messages = doc.querySelectorAll('[data-testid="stChatMessage"]');
                    target = messages.length ? messages[messages.length - 1] : null;
                }} else {{
                    target = doc.querySelector({selector!r});
                }}
                if (target) {{
                    target.scrollIntoView({{behavior: 'smooth', block: {block!r}}});
                }}
            }}, 120);
            </script>
            """,
            height=0,
        )
    except Exception:
        pass

if "latest_external_client_report" not in st.session_state:
    st.session_state.latest_external_client_report = None

if "business_context" not in st.session_state:
    st.session_state.business_context = {
        "latest_external_client_report": None,
        "latest_project_type": None,
        "latest_client_message": None,
        "latest_agent_outputs": {},
        "conversation_summary": ""
    }


st.markdown("<div id='dd-top-panel'></div>", unsafe_allow_html=True)

# Clean top account bar. No sidebar and no automatic scroll when Login is clicked.
left, right = st.columns([7, 1.15], vertical_alignment="center")

with left:
    if st.session_state.user:
        user = st.session_state.user
        st.markdown(
            f"""
            <div class="dd-topbar">
                <div><div class="dd-brand-mini">LifecycleDesk <span>AI</span></div>
                <div class="dd-muted-small">Signed in as <b>{user['employee_name']}</b> · {user['designation']}</div></div>
                <div class="dd-chip">Internal lifecycle workspace</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif st.session_state.client_user:
        client = st.session_state.client_user
        st.markdown(
            f"""
            <div class="dd-topbar">
                <div><div class="dd-brand-mini">LifecycleDesk <span>AI</span></div>
                <div class="dd-muted-small">Client portal: <b>{client.get('client_name', 'Client')}</b> · {client.get('client_id', '')}</div></div>
                <div class="dd-chip">Client lifecycle portal</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="dd-topbar">
                <div><div class="dd-brand-mini">LifecycleDesk <span>AI</span></div>
                <div class="dd-muted-small">Full lifecycle AI workspace for client proposals, approvals, delivery, resources, and updates.</div></div>
                <div class="dd-chip">Front desk open</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

with right:
    if st.session_state.user or st.session_state.client_user:
        if st.button("Logout", key="top_logout_button"):
            st.session_state.user = None
            st.session_state.client_user = None
            st.session_state.messages = []
            st.session_state.external_enquiry_mode = False
            st.session_state.pending_client_proposal_text = ""
            st.session_state.latest_external_client_report = None
            st.rerun()
    else:
        if st.button("Login", key="top_login_button"):
            st.session_state.show_login = True


if st.session_state.show_login and st.session_state.user is None and st.session_state.client_user is None:
    st.markdown('<div id="dd-login-panel"></div>', unsafe_allow_html=True)
    st.subheader("Login")
    emp_tab, client_tab = st.tabs(["Employee / Executive", "Client Portal"])

    with emp_tab:
        user_id = st.text_input("Employee ID")
        secret_key = st.text_input("Secret Key", type="password")

        if st.button("Submit Employee Login"):
            user = login(user_id, secret_key)

            if user:
                st.session_state.user = user
                st.session_state.client_user = None
                st.session_state.show_login = False
                # Testing fix: start a fresh receptionist chat after login.
                st.session_state.messages = []
                st.session_state.external_enquiry_mode = False
                st.session_state.pending_client_proposal_text = ""
                st.session_state.latest_external_client_report = None
                st.session_state.business_context = {
                    "latest_external_client_report": None,
                    "latest_project_type": None,
                    "latest_client_message": None,
                    "latest_agent_outputs": {},
                    "conversation_summary": ""
                }
                st.success(f"Receptionist: Identity verified. Welcome {user['employee_name']}.")
                st.rerun()
            else:
                st.error("Receptionist: Invalid employee ID or secret key.")

    with client_tab:
        client_user_id = st.text_input("Client User ID")
        client_password = st.text_input("Client Password", type="password")

        if st.button("Submit Client Login"):
            client = client_login(client_user_id, client_password)
            if client:
                st.session_state.client_user = client
                st.session_state.user = None
                st.session_state.show_login = False
                st.session_state.messages = []
                st.session_state.external_enquiry_mode = False
                st.session_state.pending_client_proposal_text = ""
                st.session_state.latest_external_client_report = None
                st.success(f"Welcome {client.get('client_name', 'Client')}. Your client portal is ready.")
                st.rerun()
            else:
                st.error("Invalid client user ID or password.")




def render_system_maintenance_panel(user):
    """Small optional admin panel replacing the old sidebar."""
    role = safe_text(user.get("role")).lower()
    if role not in ["founder", "executive"]:
        return
    with st.expander("System maintenance", expanded=False):
        st.caption("Use only when setting up Supabase or repairing old demo tables.")
        if postgres_config_available():
            st.success("Supabase URL configured. The app connects only when workflow data is needed.")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Test Supabase connection", key="maint_test_supabase"):
                    pg_ok, pg_status = test_postgres_connection()
                    if pg_ok:
                        st.success("Supabase PostgreSQL connected")
                    else:
                        st.error("Supabase connection failed.")
                        st.code(pg_status)
            with c2:
                if st.button("Initialize / repair schema", key="maint_repair_schema"):
                    try:
                        st.session_state["_dd_run_schema_repair_now"] = True
                        st.session_state["_dd_pg_schema_ready"] = False
                        ensure_postgres_tables()
                        repair_proposal_workflow_text_schema()
                        st.success("Supabase workflow schema is ready.")
                    except Exception as exc:
                        st.error("Could not initialize Supabase schema.")
                        st.code(explain_postgres_connection_error(exc))
        else:
            st.warning("Supabase is not connected. Add .streamlit/secrets.toml or .env and restart.")


def render_role_dashboard_selector(user, data):
    """Keep logged-in dashboards compact: title first, then dropdown selection."""
    role = safe_text(user.get("role")).lower()
    role_key = role_key_for_user(user)

    if role in ["employee", "new_joinee"]:
        # Employee dashboard is live-project-first. Static Excel project/activity
        # lists are intentionally not shown here.
        options = [
            "Choose dashboard item...",
            "My project workbench",
            "AI receptionist chat",
        ]
    elif role == "founder":
        options = [
            "Choose dashboard item...",
            "Executive update inbox",
            "All proposal board",
            "Live company performance",
            "AI receptionist chat",
        ]
    elif role == "executive":
        options = [
            "Choose dashboard item...",
            "Executive update inbox",
            "All proposal board",
        ]
        if role_key == "operations":
            options.append("Operations delivery workspace")
        options.append("AI receptionist chat")
    else:
        options = ["Choose dashboard item...", "AI receptionist chat"]

    st.markdown(
        """
        <div class="dd-dashboard-shell">
            <div class="dd-title-row">
                <div>
                    <div class="dd-section-title">Lifecycle dashboard</div>
                    <div class="dd-section-subtitle">Choose one item at a time. Proposal updates, delivery items, and project work open only when selected.</div>
                </div>
                <div class="dd-title-badge">Compact mode</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    default_index = 0
    if role in ["employee", "new_joinee"] and "My project workbench" in options:
        default_index = options.index("My project workbench")
    selected = st.selectbox("Open dashboard item", options, index=default_index, key=f"dashboard_selector_{actor_id(user)}")

    if selected == "Choose dashboard item...":
        st.info("Choose a dashboard item from the dropdown above.")
        return selected

    if selected == "My project workbench":
        render_employee_project_workbench(user)
    elif selected == "Executive update inbox":
        render_pending_proposal_notifications(user, data)
    elif selected == "All proposal board":
        render_all_proposals_board(user)
    elif selected == "Live company performance":
        render_company_performance_dashboard(data)
    elif selected == "Operations delivery workspace":
        render_operations_delivery_workspace(user, data)
    elif selected == "AI receptionist chat":
        st.info("Use the receptionist chat below.")
    return selected


def auto_scroll_to_chat_response():
    """Scroll to chat only after a real receptionist message is submitted."""
    request_page_scroll("chat")
    run_pending_page_scroll()


# ---------------- ROLE WORKSPACE ----------------

selected_dashboard_item = None

if st.session_state.user:
    user = st.session_state.user

    st.markdown('<div id="dd-dashboard-panel"></div>', unsafe_allow_html=True)
    run_pending_page_scroll()
    render_workspace_header(user)
    render_system_maintenance_panel(user)
    selected_dashboard_item = render_role_dashboard_selector(user, data)

elif st.session_state.client_user:
    st.markdown('<div id="dd-dashboard-panel"></div>', unsafe_allow_html=True)
    run_pending_page_scroll()
    render_client_dashboard(st.session_state.client_user)

# Keep the receptionist available for front-desk visitors and logged-in employees/executives.
# It is not shown inside the client portal. Normal dashboard/login clicks do not scroll here;
# chat scrolling is triggered only after a real chat message is submitted.
should_show_receptionist_chat = (
    st.session_state.client_user is None
)

if should_show_receptionist_chat:
    st.divider()


    # ---------------- RECEPTIONIST CHAT ----------------

    render_chat_intro()

    with st.expander("Try these demo prompts", expanded=False):
        st.markdown(
            """
            - `Company name is EduSmart, contact edu@example.com, we need an AI chatbot, budget 40 lakhs, timeline 8 months`
            - `Company name is DataNova, contact 9876543210, we need a data pipeline, budget 15 lakhs, timeline 3 months`
            - `When will my salary be credited?`
            - `Why is my salary less this month?`
            - `Show company performance`
            """
        )

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    query = None if st.session_state.client_user else st.chat_input("Type your request to the receptionist...")

    if query:
        st.session_state.messages.append({"role": "user", "content": query})

        with st.chat_message("user"):
            st.write(query)

        with st.chat_message("assistant"):
            reply = handle_receptionist_query(query, st.session_state.user, data)

            st.write(reply["message"])

            if reply["type"] == "external_client_details_received":
                st.success("Receptionist: External client details received. Calling internal agents now...")

                client_query = reply.get("client_query", query)
                external_result = run_external_client_decision(client_query, data)
                report = save_latest_external_client_report(client_query, external_result)
                st.session_state.pending_client_proposal_text = ""

                if report.get("proposal_id"):
                    st.success(
                        "Your proposal has been received. Our internal DecisionDesk AI meeting analysis is complete, "
                        "and our team will contact you soon with the next steps."
                    )

                    # Real product behavior: external clients never see internal cost, margin,
                    # HR gap, executive comments, or agent reasoning. They receive portal credentials.
                    if st.session_state.user is not None:
                        st.subheader("Internal AI Agent Meeting")
                        render_external_client_report(report, user=st.session_state.user, compact=False)
                    else:
                        st.info(
                            "For privacy, internal agent reasoning is hidden from the client view. "
                            "Your proposal is now in internal executive review. Please use the client portal credentials below to track quotation status and future updates."
                        )
                        if report.get("client_user_id") and report.get("client_password"):
                            st.success("Client portal account created.")
                            credentials_text = build_client_credentials_text(report)
                            st.download_button(
                                "Download client portal credentials",
                                data=credentials_text,
                                file_name=f"client_portal_credentials_{report.get('proposal_id')}.txt",
                                mime="text/plain",
                                key=f"download_client_credentials_{report.get('proposal_id')}",
                            )
                            st.caption("Use Login → Client Portal to view quotation updates. Credentials are provided as a downloadable note, not exposed as an internal decision view.")

                    st.caption(
                        f"Saved to {proposal_storage_backend_label()} as {report['proposal_id']}. "
                        "Executives will receive this as a pending decision-room notification."
                    )
                else:
                    st.warning(
                        "The analysis was generated, but it could not be saved to proposal storage. "
                        f"Reason: {report.get('excel_save_error', 'Unknown error')}"
                    )

            elif reply["type"] == "proposal_workflow":
                result = run_new_project_proposal_workflow(data, reply["lead_id"])

                if result is None:
                    st.error("Sales Agent: I could not find this lead in the company database.")
                else:
                    st.subheader("Internal AI Decision Meeting Completed")

                    decision = result["ceo_decision"]

                    if decision == "Approved":
                        st.success(f"CEO Agent Decision: {decision}")
                    elif decision == "Approved with Conditions":
                        st.warning(f"CEO Agent Decision: {decision}")
                    else:
                        st.error(f"CEO Agent Decision: {decision}")

                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Lead Score", result["sales_result"]["lead_score"])
                    c2.metric(
                        "Win Probability",
                        f"{result['sales_result']['win_probability_percent']}%",
                    )
                    c3.metric(
                        "Profit Margin",
                        f"{result['finance_result']['profit_margin_percent']}%",
                    )
                    c4.metric("Project Risk", result["new_project_risk"])

                    st.subheader("Sales Agent Calculation")
                    st.json(result["sales_result"])

                    st.subheader("HR Agent Skill Gap Calculation")
                    st.dataframe(result["hr_result"])

                    st.subheader("Operations Agent Risk Calculation")
                    st.dataframe(result["operations_existing_risk"])

                    st.subheader("Finance Agent Calculation")
                    st.json(result["finance_result"])

                    st.subheader("CEO Internal Meeting Report")
                    st.write(result["llm_report"])

                    report_file = generate_proposal_report(result)

                    st.download_button(
                        label="Download Internal Meeting Report",
                        data=report_file,
                        file_name=f"internal_meeting_report_{reply['lead_id']}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )

            elif reply["type"] == "company_health":
                st.subheader("CEO Agent - Dynamic Company Performance")
                render_company_performance_dashboard(data)

            elif reply["type"] == "login_required":
                st.warning(reply["message"])

            elif reply["type"] == "route_agent":
                st.success(f"You are now connected to {reply['agent']}.")

                if reply["agent"] == "HR Agent":
                    st.write(handle_hr_agent_query(query, st.session_state.user, data))

                elif reply["agent"] == "Finance Agent":
                    intent = reply.get("intent", "")
                    q = query.lower()

                    if intent == "role_salary_lookup" or is_role_salary_query(query):
                        st.write(answer_salary_by_role(query, st.session_state.user, data))
                    elif intent in ["payroll_discrepancy", "salary_difference", "salary_lower_than_expected"]:
                        st.write(explain_salary_difference(st.session_state.user, data))
                    elif any(x in q for x in ["less salary", "lesser salary", "low salary", "salary lower", "salary received is lesser"]):
                        st.write(explain_salary_difference(st.session_state.user, data))
                    elif any(x in q for x in ["inhand", "in-hand", "salary date", "credited", "monthly salary", "my salary"]):
                        st.write(get_employee_salary_info(st.session_state.user, data))
                    else:
                        result = run_sql_query(query, st.session_state.user, data)
                        write_sql_or_text_result(result)

                elif reply["agent"] == "Operations Agent":
                    latest_report = get_latest_external_client_report()
                    if latest_report and any(x in query.lower() for x in ["client", "proposal", "latest", "requirement", "decision"]):
                        render_external_client_report(latest_report, user=st.session_state.user, compact=False)
                    else:
                        result = answer_with_sql_agent(query, st.session_state.user, data, "Operations Agent")
                        write_sql_or_text_result(result)

                elif reply["agent"] == "Sales Agent":
                    latest_report = get_latest_external_client_report()
                    if latest_report and any(x in query.lower() for x in ["client", "proposal", "latest", "requirement", "decision"]):
                        render_external_client_report(latest_report, user=st.session_state.user, compact=False)
                    else:
                        result = answer_with_sql_agent(query, st.session_state.user, data, "Sales Agent")
                        write_sql_or_text_result(result)

                elif reply["agent"] == "CEO Agent":
                    if st.session_state.user and st.session_state.user["role"] == "founder":
                        render_company_performance_dashboard(data)
                    else:
                        st.error("CEO Agent: This requires Founder/CEO access.")

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": reply["message"],
                }
            )

            auto_scroll_to_chat_response()

