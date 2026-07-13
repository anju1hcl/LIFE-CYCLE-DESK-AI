import pandas as pd
from llm_client import ask_llm
from core.db_catalog import SHEET_CATALOG


def get_accessible_sheets(user):
    role = user.get("role")
    designation = user.get("designation", "")

    if role == "founder":
        return list(SHEET_CATALOG.keys())

    allowed = []

    for sheet, meta in SHEET_CATALOG.items():
        access = meta["access"]

        if role in access or designation in access:
            allowed.append(sheet)

    return allowed


def build_catalog_prompt(user):
    allowed_sheets = get_accessible_sheets(user)

    text = ""

    for sheet in allowed_sheets:
        meta = SHEET_CATALOG[sheet]
        text += f"\nSheet: {sheet}\n"
        text += f"Description: {meta['description']}\n"
        text += f"Columns: {', '.join(meta['columns'])}\n"

    return text


def ask_query_agent(query, user, data):
    allowed_sheets = get_accessible_sheets(user)
    catalog_text = build_catalog_prompt(user)

    prompt = f"""
You are a pandas query planner.

The user is asking a business data question.

User:
Role: {user.get("role")}
Designation: {user.get("designation")}
Department: {user.get("department")}

Question:
{query}

Available Excel sheets and columns:
{catalog_text}

Return ONLY valid JSON.

Choose the best intent from:
employee_salary_by_role
employee_availability_by_skill
project_status
employee_bandwidth
lead_summary
company_expense
attendance_lop
general_summary

JSON format:
{{
  "intent": "intent_name",
  "sheet_names": ["Sheet1", "Sheet2"],
  "filter_column": "column_name_or_null",
  "filter_value": "value_or_null",
  "reason": "short reason"
}}
"""

    import json

    try:
        raw = ask_llm(prompt)
        plan = json.loads(raw)
    except Exception:
        return "Query Agent: I could not understand the data request clearly."

    sheets = plan.get("sheet_names", [])

    for sheet in sheets:
        if sheet not in allowed_sheets:
            return f"Query Agent: You do not have access to {sheet} data."

    intent = plan.get("intent")

    if intent == "employee_salary_by_role":
        return query_employee_salary_by_role(query, data)

    if intent == "employee_availability_by_skill":
        return query_employee_availability_by_skill(query, data)

    if intent == "project_status":
        return query_project_status(data)

    if intent == "employee_bandwidth":
        return query_employee_bandwidth(data)

    if intent == "lead_summary":
        return query_lead_summary(data)

    if intent == "company_expense":
        return query_company_expenses(data)

    if intent == "attendance_lop":
        return query_lop_summary(data)

    return "Query Agent: I understood the request, but no matching query function is implemented yet."


def query_employee_salary_by_role(query, data):
    employees = data["employees"]
    q = query.lower()

    if "ai" in q or "ml" in q:
        role_filter = "ai|ml"
        label = "AI/ML engineers"
    elif "data engineer" in q:
        role_filter = "data engineer"
        label = "Data Engineers"
    elif "backend" in q:
        role_filter = "backend"
        label = "Backend Developers"
    elif "frontend" in q:
        role_filter = "frontend"
        label = "Frontend Developers"
    else:
        return "Query Agent: Please mention the role, such as AI Engineer, Data Engineer, Backend Developer, etc."

    people = employees[
        employees["designation"].astype(str).str.lower().str.contains(role_filter, regex=True, na=False)
    ]

    if people.empty:
        return f"Query Agent: No {label} found."

    avg_ctc = people["monthly_ctc"].mean()
    avg_inhand = people["monthly_inhand"].mean()
    total_ctc = people["monthly_ctc"].sum()

    lines = []
    for _, row in people.iterrows():
        lines.append(
            f"{row['employee_name']} - {row['designation']} - "
            f"CTC ₹{row['monthly_ctc']:,.0f}, In-hand ₹{row['monthly_inhand']:,.0f}"
        )

    return (
        f"Query Agent: Salary analysis for {label}:\n\n"
        f"Count: {len(people)}\n"
        f"Average Monthly CTC: ₹{avg_ctc:,.0f}\n"
        f"Average In-hand: ₹{avg_inhand:,.0f}\n"
        f"Total Monthly CTC: ₹{total_ctc:,.0f}\n\n"
        "Details:\n- " + "\n- ".join(lines)
    )


def query_employee_availability_by_skill(query, data):
    employees = data["employees"]

    available = employees[employees["availability_percent"] >= 40]

    if available.empty:
        return "Query Agent: No employees have 40% or more availability."

    summary = available.groupby("primary_skill").agg({
        "employee_id": "count",
        "availability_percent": "mean"
    }).reset_index()

    lines = []
    for _, row in summary.iterrows():
        lines.append(
            f"{row['primary_skill']}: {row['employee_id']} employee(s), "
            f"avg availability {row['availability_percent']:.1f}%"
        )

    return "Query Agent: Availability by skill:\n\n- " + "\n- ".join(lines)


def query_project_status(data):
    projects = data["projects"]

    lines = []

    for _, p in projects.iterrows():
        lines.append(
            f"{p['project_name']} - Status: {p['status']}, "
            f"Expected: {p['expected_progress']}%, Actual: {p['actual_progress']}%"
        )

    return "Query Agent: Project status:\n\n- " + "\n- ".join(lines)


def query_employee_bandwidth(data):
    assignments = data["assignments"]

    summary = assignments.groupby(["employee_id", "employee_name"])["allocation_percent"].sum().reset_index()

    overloaded = summary[summary["allocation_percent"] >= 90]

    if overloaded.empty:
        return "Query Agent: No employees are overloaded."

    lines = []
    for _, row in overloaded.iterrows():
        lines.append(
            f"{row['employee_name']} - {row['allocation_percent']}% allocated"
        )

    return "Query Agent: Overloaded employees:\n\n- " + "\n- ".join(lines)


def query_lead_summary(data):
    leads = data["leads"]

    lines = []

    for _, l in leads.iterrows():
        lines.append(
            f"{l['lead_id']} - {l['company']} - {l['project_type']} - Budget ₹{l['expected_budget']:,.0f}"
        )

    return "Query Agent: Current lead summary:\n\n- " + "\n- ".join(lines)


def query_company_expenses(data):
    expenses = data["expenses"]

    total = expenses["monthly_cost"].sum()

    lines = []
    for _, e in expenses.iterrows():
        lines.append(f"{e['expense_type']}: ₹{e['monthly_cost']:,.0f}")

    return (
        f"Query Agent: Monthly company expenses total ₹{total:,.0f}.\n\n"
        "Breakdown:\n- " + "\n- ".join(lines)
    )


def query_lop_summary(data):
    attendance = data["attendance"]

    lop = attendance[
        attendance["is_lop"].astype(str).str.lower() == "yes"
    ]

    if lop.empty:
        return "Query Agent: No LOP records found."

    summary = lop.groupby("employee_id").size().reset_index(name="lop_days")

    lines = []
    for _, row in summary.iterrows():
        lines.append(f"{row['employee_id']}: {row['lop_days']} LOP day(s)")

    return "Query Agent: LOP summary:\n\n- " + "\n- ".join(lines)