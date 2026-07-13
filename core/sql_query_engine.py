import json
import duckdb
import pandas as pd
from llm_client import ask_llm
from core.db_catalog import SHEET_CATALOG


def get_allowed_tables(user):
    role = user.get("role")
    designation = user.get("designation", "")

    if role == "founder":
        return list(SHEET_CATALOG.keys())

    allowed = []
    for table, meta in SHEET_CATALOG.items():
        access = meta["access"]
        if role in access or designation in access:
            allowed.append(table)

    return allowed


def build_schema_prompt(user):
    allowed_tables = get_allowed_tables(user)
    text = ""

    for table in allowed_tables:
        meta = SHEET_CATALOG[table]
        text += f"\nTable: {table}\n"
        text += f"Description: {meta['description']}\n"
        text += f"Columns: {', '.join(meta['columns'])}\n"

    return text


def generate_sql_from_question(question, user):
    schema = build_schema_prompt(user)

    prompt = f"""
You are a SQL generator.

Generate ONE safe DuckDB SQL query for the user's business question.

Rules:
- Use only the tables and columns listed below.
- Do not use INSERT, UPDATE, DELETE, DROP, ALTER, CREATE.
- Only generate SELECT queries.
- Use double quotes around table names if needed.
- Return ONLY valid JSON.
- Do not explain.

User question:
{question}

Available tables:
{schema}

JSON format:
{{
  "sql": "SELECT ...",
  "reason": "short reason"
}}
"""

    raw = ask_llm(prompt)

    try:
        result = json.loads(raw)
        return result["sql"]
    except Exception:
        return None


def is_safe_sql(sql):
    if not sql:
        return False

    blocked = ["insert", "update", "delete", "drop", "alter", "create", "truncate"]
    sql_lower = sql.lower().strip()

    if not sql_lower.startswith("select"):
        return False

    return not any(word in sql_lower for word in blocked)


def run_sql_query(question, user, data):
    sql = generate_sql_from_question(question, user)

    if not is_safe_sql(sql):
        return {
            "success": False,
            "answer": "Query Engine: I could not generate a safe SQL query for this question.",
            "sql": sql,
            "dataframe": None,
        }

    con = duckdb.connect()

    table_map = {
        "Users": "users",
        "Employees": "employees",
        "Attendance": "attendance",
        "Payroll": "payroll",
        "Projects": "projects",
        "Project_Assignments": "assignments",
        "Onboarding": "onboarding",
        "Clients": "clients",
        "Leads": "leads",
        "Company_Expenses": "expenses",
        "Project_Requirements": "requirements",
        "Project_Status_History": "status_history",
    }

    for sql_table, data_key in table_map.items():
        if data_key in data:
            con.register(sql_table, data[data_key])

    try:
        result_df = con.execute(sql).df()
    except Exception as e:
        return {
            "success": False,
            "answer": f"Query Engine: SQL execution failed: {e}",
            "sql": sql,
            "dataframe": None,
        }

    explanation = explain_sql_result(question, sql, result_df)

    return {
        "success": True,
        "answer": explanation,
        "sql": sql,
        "dataframe": result_df,
    }


def explain_sql_result(question, sql, result_df):
    sample = result_df.head(20).to_dict(orient="records")

    prompt = f"""
You are a business analyst.

User question:
{question}

SQL used:
{sql}

Query result:
{sample}

Write a clear business answer in 2-5 sentences.
Use Indian Rupee formatting if money is involved.
Do not mention raw SQL unless useful.
"""

    return ask_llm(prompt)