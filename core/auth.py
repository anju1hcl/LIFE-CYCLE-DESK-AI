from core.data_loader import load_sheet


def login(user_id: str, secret_key: str):
    users = load_sheet("Users")
    user_id = str(user_id).strip()
    secret_key = str(secret_key).strip()

    match = users[
        (users["user_id"].astype(str).str.strip() == user_id)
        & (users["secret_key"].astype(str).str.strip() == secret_key)
        & (users["status"].astype(str).str.lower().isin(["active", "joining"]))
    ]

    if match.empty:
        return None
    return match.iloc[0].to_dict()


def role_name(user: dict) -> str:
    role = str(user.get("role", "")).strip().lower()
    designation = str(user.get("designation", "")).strip().lower()
    department = str(user.get("department", "")).strip().lower()

    if role == "founder":
        return "Founder"
    if role == "new_joinee":
        return "New Joinee"
    if role == "external_client":
        return "External Client"
    if "hr" in designation or department == "hr":
        return "HR Executive"
    if "finance" in designation or department == "finance":
        return "Finance Executive"
    if "sales" in designation or department == "sales":
        return "Sales Executive"
    if "operations" in designation or department == "operations":
        return "Operations Executive"
    return "Employee"


def is_ceo(user: dict) -> bool:
    return role_name(user) == "Founder"


def is_executive(user: dict) -> bool:
    return role_name(user) in ["HR Executive", "Finance Executive", "Sales Executive", "Operations Executive"]


def can_access_agent(user: dict, agent_name: str) -> bool:
    role = role_name(user)
    if role == "Founder":
        return True
    rules = {
        "HR Agent": ["HR Executive", "Employee", "New Joinee"],
        "Finance Agent": ["Finance Executive"],
        "Sales Agent": ["Sales Executive", "External Client"],
        "Operations Agent": ["Operations Executive", "Employee", "External Client"],
        "CEO Agent": [],
    }
    return role in rules.get(agent_name, [])
