from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "db" / "virtual_company_db_final.xlsx"

SHEET_MAP = {
    "users": "Users",
    "employees": "Employees",
    "clients": "Clients",
    "projects": "Projects",
    "assignments": "Project_Assignments",
    "attendance": "Attendance",
    "payroll": "Payroll",
    "onboarding": "Onboarding",
    "requirements": "Project_Requirements",
    "leads": "Leads",
    "expenses": "Company_Expenses",
    "permissions": "Permissions",
    "status_history": "Project_Status_History",
}


def load_sheet(sheet_name: str) -> pd.DataFrame:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Excel DB not found at: {DB_PATH}")
    return pd.read_excel(DB_PATH, sheet_name=sheet_name)


def load_all_data() -> dict:
    return {key: load_sheet(sheet) for key, sheet in SHEET_MAP.items()}
