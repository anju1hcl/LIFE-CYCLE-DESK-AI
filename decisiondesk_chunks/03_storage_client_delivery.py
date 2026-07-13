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
    "operations": "Technical Architect AI Agent",
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

CLIENT_OPERATIONS_MESSAGE_COLUMNS = [
    "message_id",
    "project_id",
    "proposal_id",
    "client_id",
    "sender_type",
    "sender_id",
    "sender_name",
    "message_text",
    "created_at",
    "seen_by_client",
    "seen_by_operations",
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


def project_display_name(project=None, project_id=None, proposal_id=None, fallback="Project"):
    """Return a readable project label as 'Project Name | Project ID'.

    Accepts dicts, pandas Series rows, or plain values without triggering pandas
    truth-value errors. Keeps dashboards readable for CEO, executives,
    Technical Architect, employees, and client-safe views.
    """
    if project is None:
        project_obj = {}
    elif hasattr(project, "to_dict"):
        try:
            project_obj = project.to_dict()
        except Exception:
            project_obj = {}
    elif isinstance(project, dict):
        project_obj = project
    else:
        project_obj = {}

    pid = safe_text(project_obj.get("project_id") or project_id).strip()
    pname = safe_text(project_obj.get("project_name")).strip()

    if (not proposal_id) and project_obj.get("proposal_id"):
        proposal_id = project_obj.get("proposal_id")

    if (not pname) and proposal_id:
        try:
            found = get_project_for_proposal(proposal_id)
            if found is not None:
                if hasattr(found, "to_dict"):
                    found = found.to_dict()
                if isinstance(found, dict):
                    pname = safe_text(found.get("project_name")).strip()
                    pid = pid or safe_text(found.get("project_id")).strip()
        except Exception:
            pass

    if (not pname) and pid:
        try:
            projects = read_simple_table("projects", PROJECT_COLUMNS)
            if projects is not None and not projects.empty and "project_id" in projects.columns:
                match = projects[projects["project_id"].astype(str) == pid]
                if not match.empty:
                    pname = safe_text(match.iloc[0].get("project_name")).strip()
        except Exception:
            pass

    if pname and pid:
        return f"{pname} | {pid}"
    if pname:
        return pname
    if pid:
        return pid
    return fallback


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


def make_client_ops_message_id():
    return "COM-" + datetime.now().strftime("%Y%m%d%H%M%S%f")


def make_client_id():
    return "C-" + datetime.now().strftime("%Y%m%d%H%M%S%f")


def make_client_password():
    """Create a short client-friendly temporary password.

    Production version should hash passwords and enforce reset on first login.
    """
    return "DD-" + datetime.now().strftime("%S%f")[-4:]


def make_client_user_id(client_id):
    """Create a short client-friendly client login ID instead of a long timestamp."""
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
        df["current_owner"] = df["current_owner"].fillna("").replace("", "Sales, Finance, HR, Technical Architect, CEO")

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
    makes recovery quick during product use.
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
    Streamlit and hosted deployments.
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
    try:
        read_dynamic_capacity_sources.clear()
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
    # Fast operating mode assumes tables already exist and avoids repeated CREATE/ALTER
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
                generated_by TEXT DEFAULT 'Technical Architect AI Agent',
                generated_at TEXT,
                published_by TEXT,
                visible_to_client TEXT DEFAULT 'Yes'
            )
        """))
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS client_operations_messages (
                message_id TEXT PRIMARY KEY,
                project_id TEXT,
                proposal_id TEXT,
                client_id TEXT,
                sender_type TEXT,
                sender_id TEXT,
                sender_name TEXT,
                message_text TEXT,
                created_at TEXT,
                seen_by_client TEXT DEFAULT 'No',
                seen_by_operations TEXT DEFAULT 'No'
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
            ("client_operations_messages", CLIENT_OPERATIONS_MESSAGE_COLUMNS, "message_id"),
        ]:
            for col in columns:
                if col != key_col:
                    db.execute(text(f"ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS {col} TEXT"))


    st.session_state["_dd_pg_schema_ready"] = True


def repair_proposal_workflow_text_schema():
    """Repair older Supabase schemas that used INTEGER/DOUBLE columns.

    Earlier workflow tables sometimes stored quote/budget/timeline fields as
    INTEGER. Once real proposal values grew or a legacy row had a quote in a
    timeline column, PostgreSQL raised `integer out of range`. The app reads
    values through safe_number/safe_int anyway, so keeping workflow columns as
    TEXT is the safest product schema and avoids failed inserts from old tables.
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
        "client_operations_messages": (CLIENT_OPERATIONS_MESSAGE_COLUMNS, "message_id"),
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
    return f"""LifecycleDesk AI - Client Portal Access

Dear {client_name},

Your proposal has been received and is now under internal executive review.
Use the below temporary credentials to track quotation status and future project updates.

Client User ID: {report.get('client_user_id', '')}
Temporary Password: {report.get('client_password', '')}

Login area: Client Portal
Proposal ID: {report.get('proposal_id', '')}

Security note: These are temporary client portal credentials. The client should reset the password on first login when password reset is enabled.

Regards,
Virtual Tech AI
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
        "Accept Proposal": "Technical Architect / Delivery Planning",
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

    if response == "Accept Proposal":
        return True, "Your proposal acceptance was saved. Please submit the detailed requirement next; the Technical Architect AI Agent will generate the delivery plan and weekly targets."
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
3. Technical Architect capacity interpretation
4. Hiring/resource concern
5. CEO recommendation
"""
    return {"performance": performance, "llm_response": ask_llm(prompt, fallback=fallback)}


def render_company_performance_dashboard(data):
    health = run_company_health_workflow(data)
    perf = health.get("performance", {})
    st.markdown("### Dynamic company performance")
    st.caption("Measured from Supabase dynamic workflow tables. Excel is used only for static employee/payroll/expense context.")
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
            "Your proposal is being handled by our internal Sales, HR, Finance, Technical Architect, and CEO team. "
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
        "operations_owner_name": "Technical Architect AI Agent",
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
            df.loc[mask, "current_owner"] = "Client / Technical Architect"
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
    fallback = f"""Technical Architect AI Agent Delivery Readiness Plan

1. Business Objective
Deliver {analysis.get('project_type', 'the requested solution')} for the client based on the accepted quotation and detailed requirement.

2. Functional Requirements
- User-facing workflow based on the client requirement
- Admin/operations dashboard for managing core records
- Reporting/status visibility for the client
- Role-based access for internal users and client users

3. Suggested Tools and Software
- Frontend / App: Streamlit or React enterprise web UI
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
- Technical Architect delivery planning
- Employee allocation and notifications
- Weekly client update generation

7. Roles Needed
- Technical Architect AI Agent / Project Owner
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
You are the Technical Architect AI Agent for an IT services company.
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
        "suggested_tools": "See Technical Architect AI Agent plan",
        "cloud_plan": "See Technical Architect AI Agent plan",
        "security_plan": "See Technical Architect AI Agent plan",
        "module_breakdown": "See Technical Architect AI Agent plan",
        "risks_and_blockers": "See Technical Architect AI Agent plan",
        "client_clarifications_needed": "Please confirm final feature priorities, user roles and permissions, external integrations, branding/UI expectations, and deployment preference.",
        "approval_status": "Technical Architect AI Agent Drafted - Manager Review Pending",
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
            df.loc[mask, "workflow_status"] = "Detailed Requirement Submitted - Technical Architect Review Pending"
            df.loc[mask, "current_owner"] = "Technical Architect AI Agent"
            df.loc[mask, "operations_seen"] = "No"
            df.loc[mask, "operations_seen_at"] = ""
            df.loc[mask, "last_updated_by"] = safe_text(client_account.get("client_name"), "Client")
            df.loc[mask, "last_updated_role"] = "Client"
            df.loc[mask, "last_updated_at"] = now
            df.loc[mask, "last_update_summary"] = "Client submitted detailed requirement. Technical Architect AI Agent created delivery plan for manager review."
            upsert_current_proposal_from_df(df, mask)
    except Exception:
        pass
    append_proposal_history(
        report.get("proposal_id"),
        {"user_id": safe_text(client_account.get("client_user_id")), "employee_name": safe_text(client_account.get("client_name")), "designation": "Client"},
        "Detailed Requirement Submitted",
        summary="Client submitted detailed requirement; Technical Architect AI Agent created delivery plan.",
    )
    return True, "Detailed requirement submitted. Technical Architect AI Agent has created a delivery plan and notified the Technical Architect AI Agent."


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
    """Employee requests/updates that Technical Architect has not marked as done."""
    updates = get_employee_project_updates(project_id=project_id, employee_id=employee_id)
    if updates.empty:
        return updates
    if "operations_status" not in updates.columns:
        updates["operations_status"] = "Open"
    status = updates["operations_status"].fillna("Open").astype(str).str.lower().str.strip()
    open_updates = updates[~status.isin(["done", "closed", "resolved", "completed"])]
    return open_updates.copy()


def mark_employee_project_update_done(employee_update_id, user, resolution_note=""):
    """Close one employee update/request and create a fresh lifecycle update for executives."""
    update_id = safe_text(employee_update_id).strip()
    if not update_id:
        return False, "No employee update selected."
    if not postgres_config_available():
        require_postgres_or_raise()
    ensure_postgres_tables()
    now = current_timestamp()

    proposal_id = ""
    project_id = ""
    employee_name = "Employee"
    try:
        updates = get_employee_project_updates()
        if not updates.empty and "employee_update_id" in updates.columns:
            matched = updates[updates["employee_update_id"].astype(str) == update_id]
            if not matched.empty:
                update_row = matched.iloc[0].to_dict()
                proposal_id = safe_text(update_row.get("proposal_id"))
                project_id = safe_text(update_row.get("project_id"))
                employee_name = safe_text(update_row.get("employee_name"), "Employee")
    except Exception:
        pass

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
                "status": "Closed",
                "done_by": actor_name(user),
                "done_at": now,
                "note": safe_text(resolution_note),
                "update_id": update_id,
            })
        clear_workflow_read_cache()

        if proposal_id:
            notify_proposal_lifecycle_change(
                proposal_id,
                user=user,
                summary=f"Technical Architect closed an employee request/update from {employee_name} for project {project_id or proposal_id}.",
                notify_actor=True,
            )
            try:
                append_proposal_history(
                    proposal_id,
                    user,
                    "Employee Request Closed",
                    comment=safe_text(resolution_note),
                    summary=f"Technical Architect marked an employee request/update from {employee_name} as Closed.",
                )
            except Exception:
                pass

        return True, "Request/update closed successfully. It remains visible as Closed in project history."
    except Exception as exc:
        remember_postgres_error(exc)
        return False, f"Could not mark this request as done: {exc}"


def mark_employee_notification_done(notification_id, user=None):
    """Mark a project notification as reviewed/done for Technical Architect."""
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
    """Return Technical Architect AI Agent user IDs that should receive delivery/update alerts."""
    recipients = []

    # Prefer the actual Technical Architect owner for this project if it has been assigned.
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

    # Also notify all Technical Architect executives from the Users sheet as a fallback.
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

    Employees may describe risk in many styles and languages. The Technical Architect AI Agent
    should infer whether Technical Architect needs to step in, what the problem is, and how
    urgent it is from the full update context. The fallback is conservative: if the
    LLM is unavailable, Technical Architect still gets an alert for human review rather than
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
        "problem_summary": "LLM review was unavailable, so Technical Architect should review the employee update manually.",
        "recommended_action": "Open the employee update and decide whether follow-up, access, clarification, or backup support is needed.",
        "client_safe_summary": "Internal delivery update received from the project team.",
        "confidence": 0.5,
    })

    prompt = f"""
You are LifecycleDesk AI's Technical Architect AI Agent.
Read the employee's weekly project update and decide whether the Technical Architect AI Agent needs to take action.
Do not use keyword matching. Understand the meaning, tone, and delivery risk.

Return only valid JSON with these keys:
- needs_operations_attention: boolean
- urgency: one of [No action, Watch, Review, Urgent]
- problem_summary: one concise sentence explaining the real issue, or say no issue reported
- recommended_action: one concise instruction for the Technical Architect AI Agent
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
            "problem_summary": safe_text(parsed.get("problem_summary"), "Employee update needs Technical Architect review."),
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

    attention_text = "Technical Architect attention needed" if agent_review.get("needs_operations_attention") else "No immediate action needed"
    message = (
        f"Technical Architect AI Agent alert: {actor_name(user)} submitted a weekly update for project {project_id}, "
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
                f"Technical Architect AI Agent assessment: {agent_review.get('urgency')} - {agent_review.get('problem_summary')}"
            ),
            summary=f"{actor_name(user)} shared a project update for {module or project_id}. Technical Architect was notified with AI assessment.",
        )
    except Exception:
        pass

    notify_proposal_lifecycle_change(
        proposal_id,
        user=user,
        summary=(
            f"New employee weekly update/request from {actor_name(user)} for project {project_id}. "
            f"Status: {status_text}; progress {safe_text(progress_percent)}%."
        ),
        notify_actor=False,
    )

    if recipients:
        return True, "Thanks. Your weekly update/request was saved. The Technical Architect AI Agent has been notified and will connect with you soon if follow-up is needed."
    return True, "Thanks. Your weekly update/request was saved. Technical Architect can review it in the delivery dashboard and will connect with you soon if follow-up is needed."


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
        f"Technical Architect plan status: {plan_status}. "
        f"Allocated team members: {allocation_count}. "
        "At the moment, there are no major blockers recorded. If you have any change in priority, scope, branding, or integrations, please share it with the Technical Architect AI Agent through this portal."
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
            "client_action_needed": "Share changes/blockers with Technical Architect AI Agent if any",
            "generated_by": "Technical Architect AI Agent",
            "generated_at": current_timestamp(),
            "published_by": "Technical Architect AI Agent",
            "visible_to_client": "Yes",
        }
        upsert_simple_row("weekly_project_updates", "update_id", WEEKLY_UPDATE_COLUMNS, row)
        return row

    prompt = f"""
Write a short, professional weekly project update for a client portal.
Do not reveal internal employee bandwidth, salary, margin, or private comments.

Project: {project.get('project_name')}
Project status: {project.get('project_status')}
Technical Architect plan status: {plan_status}
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
        "client_action_needed": "Share changes/blockers with Technical Architect AI Agent if any",
        "generated_by": "Technical Architect AI Agent",
        "generated_at": current_timestamp(),
        "published_by": "Technical Architect AI Agent",
        "visible_to_client": "Yes",
    }
    upsert_simple_row("weekly_project_updates", "update_id", WEEKLY_UPDATE_COLUMNS, row)
    return row


def approve_delivery_plan_and_allocate(project, plan, user, manager_plan_text, selected_rows):
    now = current_timestamp()
    plan.update({
        "operations_manager_plan": manager_plan_text,
        "approval_status": "Approved by Technical Architect AI Agent",
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

    # Replace active allocations for the project to keep the UI clean during repeated updates.
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
            df.loc[mask, "current_owner"] = "Technical Architect / Delivery Team"
            df.loc[mask, "last_updated_by"] = actor_name(user)
            df.loc[mask, "last_updated_role"] = actor_role_label(user)
            df.loc[mask, "last_updated_at"] = now
            df.loc[mask, "last_update_summary"] = "Technical Architect AI Agent approved delivery plan and allocated project team."
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
        summary=f"Technical Architect AI Agent approved delivery plan and allocated {len(selected_rows)} employee(s).",
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



def get_client_operations_messages(project_id=None, proposal_id=None, client_id=None):
    """Return project/client Technical Architect conversation messages, newest first."""
    df = read_simple_table("client_operations_messages", CLIENT_OPERATIONS_MESSAGE_COLUMNS)
    if df.empty:
        return df
    if project_id and "project_id" in df.columns:
        df = df[df["project_id"].astype(str) == safe_text(project_id)]
    if proposal_id and "proposal_id" in df.columns:
        df = df[df["proposal_id"].astype(str) == safe_text(proposal_id)]
    if client_id and "client_id" in df.columns:
        df = df[df["client_id"].astype(str) == safe_text(client_id)]
    if "created_at" in df.columns:
        df = df.sort_values("created_at", ascending=False)
    return normalise_simple_store(df, CLIENT_OPERATIONS_MESSAGE_COLUMNS)


def save_client_operations_message(project, report, client_account, message_text, sender_type="Client", sender_user=None):
    """Persist one client/Technical Architect conversation message."""
    message_text = safe_text(message_text).strip()
    if not message_text:
        return False, "Please type a message before sending."

    project_id = safe_text(project.get("project_id"))
    proposal_id = safe_text(project.get("proposal_id") or report.get("proposal_id"))
    client_id = safe_text(project.get("client_id") or client_account.get("client_id") or report.get("client_id"))
    now = current_timestamp()

    if sender_type == "Technical Architect":
        sender_id = actor_id(sender_user or {})
        sender_name = actor_name(sender_user or {}) or "Technical Architect AI Agent"
        seen_by_client = "No"
        seen_by_operations = "Yes"
    else:
        sender_id = safe_text(client_account.get("client_user_id") or client_account.get("client_id"))
        sender_name = safe_text(client_account.get("client_name") or report.get("client_name"), "Client")
        seen_by_client = "Yes"
        seen_by_operations = "No"

    row = {
        "message_id": make_client_ops_message_id(),
        "project_id": project_id,
        "proposal_id": proposal_id,
        "client_id": client_id,
        "sender_type": sender_type,
        "sender_id": sender_id,
        "sender_name": sender_name,
        "message_text": message_text,
        "created_at": now,
        "seen_by_client": seen_by_client,
        "seen_by_operations": seen_by_operations,
    }
    upsert_simple_row("client_operations_messages", "message_id", CLIENT_OPERATIONS_MESSAGE_COLUMNS, row)
    return True, "Message saved."


def save_client_message_to_operations(project, report, client_account, message_text):
    """Send a client portal message to the Technical Architect AI Agent and keep conversation history."""
    message_text = safe_text(message_text).strip()
    if not message_text:
        return False, "Please type a message before sending."

    ok, msg = save_client_operations_message(project, report, client_account, message_text, sender_type="Client")
    if not ok:
        return ok, msg

    project_id = safe_text(project.get("project_id"))
    proposal_id = safe_text(project.get("proposal_id") or report.get("proposal_id"))
    client_name = safe_text(client_account.get("client_name") or report.get("client_name"), "Client")
    now = current_timestamp()

    recipients = get_operations_notification_recipients(project_id)
    if not recipients:
        recipients = [safe_text(project.get("operations_owner_id"))]
    recipients = [safe_text(r).upper() for r in recipients if safe_text(r)]

    note = f"Client message from {client_name} for {project_display_name(project=project)}: {message_text}"
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

    # Keep client/Technical Architect conversation inside the project conversation table only.
    # Do not reopen CEO/executive proposal updates for normal chat messages.
    return True, "Your message has been sent to the Technical Architect AI Agent."


def save_operations_reply_to_client(project, report, user, message_text):
    """Technical Architect reply visible in the client portal conversation list."""
    message_text = safe_text(message_text).strip()
    if not message_text:
        return False, "Please type a reply before sending."

    client_context_account = {
        "client_id": safe_text(project.get("client_id") or report.get("client_id")),
        "client_name": safe_text(report.get("client_name"), "Client"),
    }
    ok, msg = save_client_operations_message(project, report, client_context_account, message_text, sender_type="Technical Architect", sender_user=user)
    if not ok:
        return ok, msg

    # Keep client/Technical Architect conversation inside the project conversation table only.
    # Do not reopen CEO/executive proposal updates for normal chat replies.
    return True, "Reply sent to the client portal."


def render_client_operations_conversation(project, report, client_account, viewer="client", user=None):
    """Compact recent-first conversation between client and Technical Architect."""
    messages = get_client_operations_messages(
        project_id=project.get("project_id"),
        proposal_id=project.get("proposal_id") or report.get("proposal_id"),
        client_id=project.get("client_id") or client_account.get("client_id") if isinstance(client_account, dict) else None,
    )
    if messages.empty:
        st.caption("No messages yet.")
        return

    labels = []
    rows = []
    for idx, (_, row) in enumerate(messages.iterrows(), start=1):
        sender = safe_text(row.get("sender_name")) or safe_text(row.get("sender_type")) or "Message"
        created = safe_text(row.get("created_at")) or "Time not captured"
        preview = safe_text(row.get("message_text"))[:70]
        labels.append(f"{idx}. {created} | {sender} | {preview}")
        rows.append(row)

    selected = st.selectbox("Previous / recent messages", labels, key=f"client_ops_convo_{viewer}_{safe_text(project.get('project_id'))}")
    row = rows[labels.index(selected)]
    sender_type = safe_text(row.get("sender_type"))
    sender = safe_text(row.get("sender_name")) or sender_type
    created = safe_text(row.get("created_at"))
    st.markdown(
        f"""
        <div class="dd-soft-panel">
            <strong>{sender}</strong> <span class="dd-muted-small">({sender_type}) · {created}</span><br>
            <span>{safe_text(row.get('message_text'))}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_client_delivery_section(report, client_account):
    response = safe_text(report.get("client_response"))
    if response != "Accept Proposal":
        return

    st.markdown("### Weekly delivery update")
    project = ensure_project_for_accepted_proposal(report, client_account)
    plan = get_delivery_plan_for_client_project(project.get("project_id"))

    if plan is None:
        st.success("Proposal accepted. Our delivery team is ready to start the next step.")
        st.info("Please share your detailed requirement so our Technical Architect AI Agent can prepare the delivery plan and weekly targets.")
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
            submitted = st.form_submit_button("Submit detailed requirement and generate weekly targets", type="primary")
        if submitted:
            ok, msg = save_client_detailed_requirement(report, client_account, requirement_text, uploaded_name)
            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)
        return

    status = safe_text(plan.get("approval_status"))
    if status in ["Approved by Technical Architect AI Agent", "Approved by Operations Manager"]:
        allocations = get_project_allocations(project.get("project_id"))
        latest_update = generate_weekly_update_if_needed(project, plan, allocations)
        progress = get_client_safe_project_progress(project.get("project_id"))
        info_needed = get_client_safe_information_needed(plan, latest_update)

        st.success("Your project is active. Team work is going on.")
        week_info = get_project_week_info(project.get("project_id"), progress.get("updated_at")) if "get_project_week_info" in globals() else {"week_label": "Week 1", "start_label": "allocation date not captured", "latest_update_week_label": "Week 1"}
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Delivery status", "In progress")
        c2.metric("Average weekly update", progress.get("weekly_progress_percent") or progress.get("progress_percent"))
        c3.metric("Team allocation", "Allocated" if not allocations.empty else "Being finalized")
        c4.metric("Project week", week_info.get("latest_update_week_label") or week_info.get("week_label") or "Week 1")

        latest_line = f"Latest weekly project update: {progress['updated_at']}" if progress.get("updated_at") else "The first weekly project update is not submitted yet."
        week_line = f"Project week: {week_info.get('latest_update_week_label') or week_info.get('week_label') or 'Week 1'} · calculated from allocation start date: {week_info.get('start_label') or 'not captured'}"
        st.markdown(
            f"""
            <div class="dd-client-progress-card">
                <b>Average weekly project progress</b>
                <span>Your delivery team is working on the approved requirement. This percentage is the average of the latest mandatory weekly updates submitted by assigned employees.</span>
                <span>{latest_line}</span>
                <span>{week_line}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.info(f"Information needed from your side: {info_needed}")

        with st.expander("Message Technical Architect AI Agent", expanded=False):
            st.caption("Recent-first conversation. Your Technical Architect AI Agent can reply from the project dashboard.")
            render_client_operations_conversation(project, report, client_account, viewer="client")
            sent_key = f"client_ops_msg_sent_{safe_text(project.get('project_id'))}"
            if st.session_state.get(sent_key, False):
                st.success("Your message has been sent to the Technical Architect AI Agent.")
                if st.button("Send another message", key=f"client_ops_msg_again_{project.get('project_id')}"):
                    st.session_state[sent_key] = False
                    st.rerun()
            else:
                with st.form(f"client_ops_message_form_{project.get('project_id')}"):
                    msg = st.text_area(
                        "Type your message for the Technical Architect AI Agent",
                        height=110,
                        placeholder="Example: Please confirm the branch-wise rollout order / integration priority / access details.",
                    )
                    submitted_msg = st.form_submit_button("Send message to Technical Architect AI Agent", type="primary")
                if submitted_msg:
                    ok, message = save_client_message_to_operations(project, report, client_account, msg)
                    if ok:
                        st.session_state[sent_key] = True
                        st.rerun()
                    else:
                        st.error(message)
    else:
        st.info("Your detailed requirement has been received. The Technical Architect AI Agent has generated the delivery plan and weekly targets for internal review.")
        st.caption("Once delivery is approved and the team is allocated, this portal will show only client-safe project progress and any information needed from your side.")




def render_operations_notification_inbox_with_done(unread_alerts, user, key_prefix="ops_alerts_done"):
    """Compact Technical Architect notification inbox with a Done action."""
    if unread_alerts is None or unread_alerts.empty:
        return
    working = unread_alerts.copy()
    if "created_at" in working.columns:
        working = working.sort_values("created_at", ascending=False)
    labels = []
    rows = []
    for idx, (_, row) in enumerate(working.iterrows(), start=1):
        labels.append(
            f"{idx}. {safe_text(row.get('created_at'))} | {project_display_name(project_id=row.get('project_id'))} | {safe_text(row.get('notification_type'))}"
        )
        rows.append(row)
    st.markdown("#### Technical Architect request inbox")
    selected = st.selectbox("Open request / alert", labels, key=f"{key_prefix}_select")
    row = rows[labels.index(selected)]
    with st.container(border=True):
        st.write(f"**Project:** {project_display_name(project_id=row.get('project_id'))}")
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
    """Project-scoped employee request/update inbox for Technical Architect.

    Shows every unresolved employee weekly update/resource request for the selected
    project. Technical Architect can pick one item, add a closing note, and mark it done so
    it disappears from the active dashboard.
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

    if working.empty:
        st.markdown(
            """
            <div class="dd-soft-panel">
                <strong>No employee request/update history for this project yet.</strong><br>
                <span>Weekly updates, blockers, and resource requests will appear here when assigned employees submit them.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    if "created_at" in working.columns:
        working = working.sort_values("created_at", ascending=False)

    status_series = working["operations_status"].fillna("Open").astype(str).str.lower().str.strip()
    open_count = int((~status_series.isin(["done", "closed", "resolved", "completed"])).sum())

    st.markdown("### Employee requests / weekly updates")
    st.caption(f"Recent first. Open items need Technical Architect action. Closed items stay visible as history. Open: {open_count} · Total: {len(working)}")

    labels = []
    row_by_label = {}
    for idx, (_, row) in enumerate(working.iterrows(), start=1):
        employee = safe_text(row.get("employee_name")) or safe_text(row.get("employee_id")) or "Employee"
        status = safe_text(row.get("progress_status")) or "Weekly update"
        progress = safe_text(row.get("progress_percent")) or "0"
        module = safe_text(row.get("assigned_module")) or "Assigned module"
        created = safe_text(row.get("created_at")) or "Time not captured"
        issue = safe_text(row.get("support_needed")).strip() or safe_text(row.get("hurdles")).strip() or safe_text(row.get("notes")).strip() or "No blocker mentioned"
        ops_status_raw = safe_text(row.get("operations_status")).strip() or "Open"
        ops_status_norm = ops_status_raw.lower()
        is_closed = ops_status_norm in ["done", "closed", "resolved", "completed"]
        display_status = "Closed" if is_closed else "Open"
        pill_class = "dd-status-pill" if not is_closed else "dd-status-pill dd-muted-pill"
        label = f"{idx}. {created} | {employee} | {status} | {progress}% | {module} | {display_status}"
        labels.append(label)
        row_by_label[label] = row

        st.markdown(
            f"""
            <div class="dd-soft-panel" style="margin-bottom:0.55rem;">
                <div style="display:flex;justify-content:space-between;gap:1rem;align-items:flex-start;">
                    <div>
                        <strong>{idx}. {employee}</strong><br>
                        <span>{created} · {module} · {status} · {progress}%</span><br>
                        <span><strong>Request:</strong> {issue}</span>
                    </div>
                    <div class="{pill_class}">{display_status}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("#### Review selected request/update")
    selected = st.selectbox(
        "Choose open request/update",
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

    ops_status_raw = safe_text(row.get("operations_status")).strip() or "Open"
    ops_status_norm = ops_status_raw.lower()
    is_closed = ops_status_norm in ["done", "closed", "resolved", "completed"]
    display_status = "Closed" if is_closed else "Open"
    pill_class = "dd-status-pill" if not is_closed else "dd-status-pill dd-muted-pill"

    st.markdown('<div id="dd-selected-project-detail"></div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="dd-project-card">
            <div class="dd-card-header-row">
                <div>
                    <div class="dd-card-kicker">Selected employee request</div>
                    <div class="dd-card-title-small">{employee}</div>
                    <div class="dd-card-subtle">{safe_text(row.get('created_at')) or '-'}</div>
                </div>
                <div class="{pill_class}">{display_status}</div>
            </div>
            <div class="dd-metric-grid">
                <div class="dd-mini-metric"><span>Status</span><strong>{status}</strong></div>
                <div class="dd-mini-metric"><span>Weekly progress</span><strong>{progress}%</strong></div>
                <div class="dd-mini-metric"><span>Module</span><strong>{module}</strong></div>
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

    if is_closed:
        closed_by = safe_text(row.get("operations_done_by")) or "Technical Architect"
        closed_at = safe_text(row.get("operations_done_at")) or "time not captured"
        close_note = safe_text(row.get("operations_resolution_note")).strip()
        st.success(f"This request is closed by {closed_by} at {closed_at}.")
        if close_note:
            st.caption(f"Resolution note: {close_note}")
    else:
        resolution_note = st.text_area(
            "Technical Architect closing note",
            placeholder="Example: AWS access shared, issue discussed, backup assigned, no further action needed...",
            key=f"{key_prefix}_{update_id}_note",
        )

        c1, c2 = st.columns([1, 2])
        with c1:
            close_clicked = st.button(
                "Mark as done / close request",
                key=f"{key_prefix}_{update_id}_done",
                type="primary",
                use_container_width=True,
            )
        with c2:
            st.caption("After closing, this item status becomes Closed. It remains visible in project history and is no longer counted as open.")

        if close_clicked:
            ok, msg = mark_employee_project_update_done(update_id, user, resolution_note)
            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)


def render_operations_delivery_workspace(user, data, focus_proposal_id=None):
    """Clean Technical Architect AI Agent delivery workspace.

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
                Select one accepted project, review the client requirement, check the Technical Architect AI Agent conclusion,
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
        st.info("No delivery plan found for this accepted project yet. Once the client submits the detailed requirement, the Technical Architect AI Agent analysis and allocation controls will appear here.")
        return

    if "created_at" in merged.columns:
        merged = merged.sort_values("created_at", ascending=False)

    labels = []
    rows = []
    for idx, (_, row) in enumerate(merged.iterrows(), start=1):
        project_name = safe_text(row.get("project_name")) or safe_text(row.get("project_id")) or "Accepted client project"
        status = safe_text(row.get("approval_status")) or "Waiting for review"
        created = safe_text(row.get("created_at")) or safe_text(row.get("updated_at"))
        labels.append(f"{idx}. {project_display_name(project=row)} - {status} - {created}")
        rows.append(row)

    selected_label = st.selectbox(
        f"Accepted projects - recent first ({len(labels)} project(s))",
        labels,
        key=f"ops_delivery_selected_project_{actor_id(user)}_{safe_text(focus_proposal_id) or 'all'}",
    )
    ops_project_memory_key = f"_dd_last_ops_delivery_project_selection_{actor_id(user)}_{safe_text(focus_proposal_id) or 'all'}"
    previous_ops_project = st.session_state.get(ops_project_memory_key)
    if previous_ops_project is not None and selected_label != previous_ops_project:
        try:
            request_page_scroll("selected_project_detail")
        except Exception:
            st.session_state["_dd_scroll_target"] = "selected_project_detail"
    st.session_state[ops_project_memory_key] = selected_label

    selected_row = rows[labels.index(selected_label)]

    project = {col: selected_row.get(col, "") for col in PROJECT_COLUMNS}
    plan = {col: selected_row.get(col, "") for col in DELIVERY_PLAN_COLUMNS}
    project_id = project.get("project_id")
    plan_id = plan.get("delivery_plan_id")

    existing_allocations = get_project_allocations(project_id)
    all_employee_updates = get_employee_project_updates(project_id=project_id)
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
    with st.expander("Technical Architect AI Agent conclusion", expanded=False):
        if agent_conclusion:
            st.text_area(
                "AI delivery analysis and conclusion",
                value=agent_conclusion,
                height=220,
                disabled=True,
                key=f"ops_agent_conclusion_{plan_id}",
            )
        else:
            st.info("Technical Architect AI Agent analysis is not available yet. It is generated after the client submits a detailed requirement.")

    st.markdown("### Client / Technical Architect conversation")
    st.caption("Client messages and Technical Architect replies are kept here as recent-first history.")
    render_client_operations_conversation(project, proposal_report or {}, {"client_id": project.get("client_id"), "client_name": safe_text((proposal_report or {}).get("client_name"))}, viewer="operations", user=user)

    # Keep the Technical Architect reply UX similar to the client portal:
    # after a successful send, hide/clear the input and show a delivered message.
    # The form key includes a small counter so Streamlit creates a fresh empty
    # text area for the next reply instead of preserving the previous text.
    ops_reply_sent_key = f"ops_reply_sent_{safe_text(project_id)}"
    ops_reply_counter_key = f"ops_reply_counter_{safe_text(project_id)}"
    if ops_reply_counter_key not in st.session_state:
        st.session_state[ops_reply_counter_key] = 0

    if st.session_state.get(ops_reply_sent_key, False):
        st.success("Reply sent to the client portal.")
        if st.button("Send another reply", key=f"ops_reply_again_{safe_text(project_id)}"):
            st.session_state[ops_reply_sent_key] = False
            st.session_state[ops_reply_counter_key] = int(st.session_state.get(ops_reply_counter_key, 0)) + 1
            st.rerun()
    else:
        reply_form_key = f"ops_reply_to_client_{safe_text(project_id)}_{st.session_state.get(ops_reply_counter_key, 0)}"
        with st.form(reply_form_key):
            reply_text = st.text_area(
                "Reply to client",
                height=100,
                placeholder="Example: Thanks for the update. We will proceed with the branch-wise access plan and confirm next steps.",
            )
            reply_clicked = st.form_submit_button("Send reply to client", type="primary")
        if reply_clicked:
            ok, msg = save_operations_reply_to_client(project, proposal_report or {}, user, reply_text)
            if ok:
                st.session_state[ops_reply_sent_key] = True
                st.session_state[ops_reply_counter_key] = int(st.session_state.get(ops_reply_counter_key, 0)) + 1
                try:
                    request_page_scroll("selected_project_detail")
                except Exception:
                    st.session_state["_dd_scroll_target"] = "selected_project_detail"
                st.rerun()
            else:
                st.error(msg)

    render_employee_update_inbox_with_done(
        all_employee_updates,
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
            "Technical Architect AI Agent delivery plan",
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

        button_text = "Approve delivery plan and notify selected employees" if safe_text(plan.get("approval_status")) not in ["Approved by Technical Architect AI Agent", "Approved by Operations Manager"] else "Update team allocation and notify selected employees"
        if st.button(button_text, key=f"approve_delivery_{plan_id}", type="primary"):
            if not selected_rows:
                st.error("Select at least one employee before approving/updating the delivery team.")
            elif not safe_text(manager_plan).strip():
                st.error("Please keep or edit the delivery plan before approving.")
            else:
                ok, msg = approve_delivery_plan_and_allocate(project, plan, user, manager_plan, selected_rows)
                if ok:
                    st.success(msg)
                    try:
                        request_page_scroll("selected_project_detail")
                    except Exception:
                        st.session_state["_dd_scroll_target"] = "selected_project_detail"
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
    a time, the client requirement, the Technical Architect AI Agent conclusion, and the
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
                "Latest Technical Architect notification",
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
                hurdles, access needs, and resource requests with Technical Architect.
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
        labels.append(f"{idx}. {project_display_name(project_id=project_id)} | {role} | {module}")
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
        st.success("Your update/request has been sent to the Technical Architect AI Agent.")
        st.info("Technical Architect AI Agent will connect with you soon if follow-up is needed.")
        if st.button("Send another update for this project", key=f"emp_send_another_{alloc.get('allocation_id')}"):
            st.session_state[ack_key] = False
            st.rerun()
        return

    st.info(
        "Correct path: choose project -> review customer requirement and AI conclusion -> send weekly progress, blockers, or resource needs below."
    )

    # Keep the bench clean: show only assignment context, client requirement,
    # Technical Architect AI Agent conclusion, and the required weekly update form.
    c1, c2, c3 = st.columns(3)
    c1.metric("Project", project_display_name(project_id=project_id, fallback="Live project"))
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
                "Technical Architect AI Agent conclusion on the requirement",
                value=agent_conclusion,
                height=220,
                disabled=True,
                key=f"emp_agent_conclusion_{alloc.get('allocation_id')}",
            )
        else:
            st.info("Technical Architect AI Agent conclusion is not available yet.")
    else:
        st.info("Delivery requirement and Technical Architect AI Agent conclusion are not available yet for this project.")

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
            "Mandatory: please share this week's project status before continuing: completion, blockers, "
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
            "Short summary for Technical Architect AI Agent",
            placeholder="Example: Completed authentication flow; integration work is pending sample data from client.",
            key=f"emp_notes_{alloc.get('allocation_id')}",
        )
        submitted = st.form_submit_button("Submit mandatory weekly update / request", type="primary")

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

    Workflow tables are intentionally stored as TEXT for product reliability.
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
    when the table had older workflow records. This helper keeps UI actions light:
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
    immediate_gap = safe_number(analysis.get("immediate_skill_gap"), 0)
    active_fte = safe_number(analysis.get("total_active_allocated_fte"), 0)
    hurdle_count = safe_int(analysis.get("dynamic_hurdle_count"), 0)
    timeline_risk = safe_text(analysis.get("timeline_risk"))
    decision = safe_text(analysis.get("decision"))
    reason = safe_text(analysis.get("reason"))

    return {
        "sales_agent_summary": (
            f"Sales captured a {analysis.get('project_type', 'project')} opportunity with client budget "
            f"{money_text(budget)}. Recommended client-facing quote is {money_text(quote)}."
        ),
        "hr_agent_summary": (
            f"HR checked current project allocations, project progress, pending work, release timing, and open requests before recommending capacity action. "
            f"Immediate gap: {immediate_gap} FTE; projected gap during timeline: {skill_gap} FTE; active allocated load: {active_fte} FTE."
        ),
        "operations_agent_summary": (
            f"Technical Architect reviewed a {timeline}-month timeline against live Supabase project list, start dates, weekly progress, pending work, and open requests. "
            f"Timeline risk is {timeline_risk}; open hurdle/resource requests considered: {hurdle_count}."
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
        "current_owner": "Sales, Finance, HR, Technical Architect, CEO",
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
        "last_updated_by": "AI Front Desk",
        "last_updated_role": "System",
        "last_updated_at": now,
        "last_update_summary": "New proposal created and shared with all executives.",
    })

    # 1) Save the internal decision packet no matter what happens to client portal setup.
    upsert_proposal_row(row)

    # 2) Save audit history immediately after the proposal row.
    append_proposal_history(
        proposal_id,
        {"user_id": "SYSTEM", "employee_name": "AI Front Desk", "designation": "System"},
        "Proposal Created",
        decision=analysis.get("decision", ""),
        comment=analysis.get("reason", ""),
        recommended_quote=analysis.get("recommended_quote", 0),
        recommended_timeline_months=analysis.get("timeline_months", 0),
        summary="External client proposal analysed by Sales, HR, Technical Architect, Finance, and CEO agents.",
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


def notify_proposal_lifecycle_change(proposal_id, user=None, summary="", notify_actor=False):
    """
    Re-open executive update visibility only when the project/proposal actually changes.

    This supports the workflow:
            - It appears again only when a real lifecycle change happens, such as a new
      employee request/update, a closed request, client response, delivery update, etc.
    """
    proposal_id = safe_text(proposal_id).strip()
    if not proposal_id:
        return False

    try:
        df = read_proposal_store(create_if_missing=True)
        if df.empty or "proposal_id" not in df.columns:
            return False

        mask = df["proposal_id"].astype(str) == proposal_id
        if not mask.any():
            return False

        now = current_timestamp()
        df.loc[mask, "last_updated_by"] = actor_name(user) if user else "System"
        df.loc[mask, "last_updated_role"] = actor_role_label(user) if user else "System"
        df.loc[mask, "last_updated_at"] = now
        if summary:
            df.loc[mask, "last_update_summary"] = safe_text(summary)

        for role_key, column in PROPOSAL_NOTIFICATION_COLUMNS.items():
            df.loc[mask, column] = "No"
            df.loc[mask, PROPOSAL_SEEN_AT_COLUMNS[role_key]] = ""

        if notify_actor and user:
            actor_role = role_key_for_user(user)
            if actor_role in PROPOSAL_NOTIFICATION_COLUMNS:
                df.loc[mask, PROPOSAL_NOTIFICATION_COLUMNS[actor_role]] = "Yes"
                df.loc[mask, PROPOSAL_SEEN_AT_COLUMNS[actor_role]] = now

        upsert_current_proposal_from_df(df, mask)
        return True
    except Exception as exc:
        try:
            remember_postgres_error(exc)
        except Exception:
            pass
        return False


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
        f"Technical Architect, Finance, and CEO teams, our decision is: {ceo_decision}.\n\n"
        f"Recommended commercial quote: INR {safe_number(final_quote):,.0f}\n"
        f"Estimated timeline: {safe_int(final_timeline_months)} month(s)\n"
        f"Project type: {analysis.get('project_type')}\n\n"
        f"Notes: {ceo_comment or analysis.get('reason', '')}\n\n"
        "This quotation assumes the scope described in your requirement. Final contract terms, milestone plan, "
        "and payment schedule can be confirmed after a scope confirmation call.\n\n"
        "Regards,\nVirtual Tech AI"
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
        return False, "Only Sales, Finance, HR, Technical Architect executives or CEO can update proposal decisions."

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
        # keep forcing Sales/Finance/HR/Technical Architect to mark decisions.
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
