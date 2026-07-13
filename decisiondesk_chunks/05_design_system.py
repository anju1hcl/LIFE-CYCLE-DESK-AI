# ---------------- UI / PRESENTATION HELPERS ----------------

APP_NAME = "LifecycleDesk AI"
APP_TAGLINE = "End-to-end AI lifecycle platform for proposals, approvals, delivery, resources, and updates"
APP_VERSION = ""


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

            .dd-muted-pill {
                background: #f8fafc !important;
                color: #475569 !important;
                border: 1px solid #cbd5e1 !important;
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
            <div class=\"dd-kicker\">🚀 Full lifecycle agentic operating system</div>
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
        ("🛠️ Technical Architect Agent", "Delivery plan, blockers, weekly updates, employee support requests."),
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
            <div class=\"dd-section-title\">Lifecycle workflow</div>
            <div class=\"dd-section-subtitle\">
                The system manages the complete client-to-delivery lifecycle with compact, role-specific dashboards and clear action paths.
            </div>
            <div class=\"dd-stepper\">
                <div class=\"dd-step\"><strong>Front Desk</strong><span>Receives client proposal</span></div>
                <div class=\"dd-step\"><strong>Agent Meeting</strong><span>Sales, HR, Technical Architect, Finance, CEO analyse</span></div>
                <div class=\"dd-step\"><strong>CEO Quote</strong><span>CEO approves and sends quotation to client</span></div>
                <div class=\"dd-step\"><strong>Client Response</strong><span>Client accepts, declines, or requests reconsideration</span></div>
                <div class=\"dd-step\"><strong>Technical Readiness</strong><span>Technical Architect Agent prepares requirement list after acceptance</span></div>
                <div class=\"dd-step\"><strong>Team Allocation</strong><span>Technical Architect Agent assigns employees to the project</span></div>
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
                Use this only when you want to ask the AI Front Desk something or start a new client/proposal workflow.
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


# ---------------- V43 CURRENT WORKING PATCH: INITIAL REQUIREMENT + TECH ARCHITECT + FINANCE COSTING ----------------
# This patch is intentionally appended late in the chunk order so it overrides
# only the required functions while keeping the working v43 workflow intact.

INITIAL_REQUIREMENT_COLUMNS = [
    "initial_requirement_summary",
    "technical_architect_requirement",
    "technical_architect_stack_json",
    "technical_architect_timeline_basis",
    "client_requested_timeline_months",
    "scope_complexity",
    "scope_effort_months",
    "hiring_recommendation",
    "total_hiring_needed_fte",
    "calendar_carry_cost",
    "hiring_or_contract_premium",
    "pending_work_risk_buffer",
    "costing_method",
]
try:
    insert_after = "role_cost_breakdown_json"
    insert_at = PROPOSAL_DECISION_COLUMNS.index(insert_after) + 1 if insert_after in PROPOSAL_DECISION_COLUMNS else len(PROPOSAL_DECISION_COLUMNS)
    for _col in INITIAL_REQUIREMENT_COLUMNS:
        if _col not in PROPOSAL_DECISION_COLUMNS:
            PROPOSAL_DECISION_COLUMNS.insert(insert_at, _col)
            insert_at += 1
except Exception:
    pass


def _keyword_hits(text_value, words):
    text_value = safe_text(text_value).lower()
    return [word for word in words if word in text_value]


def has_basic_project_requirement_in_query(query):
    """Require an initial basic requirement, not just 'AI chatbot'.

    The client does not need to submit the final SRS here. But they must share
    enough modules/features/users/integrations for the Technical Architect AI
    Agent to infer stack, scope, realistic timeline, bandwidth, and cost.
    """
    text_value = safe_text(query).strip()
    q = text_value.lower()
    if len(text_value) < 90:
        return False
    requirement_words = [
        "login", "role", "permission", "access", "dashboard", "report", "analytics",
        "upload", "document", "workflow", "approval", "notification", "alert", "api",
        "integration", "database", "cloud", "deployment", "security", "admin", "user",
        "employee", "client", "student", "staff", "branch", "module", "feature", "data",
        "etl", "pipeline", "chatbot", "assistant", "faq", "ticket", "mobile", "web",
        "payment", "audit", "export", "email", "sms", "authentication", "authorization",
    ]
    hits = set(_keyword_hits(q, requirement_words))
    has_action = bool(re.search(r"\b(?:need|want|build|create|develop|require|looking for|platform|software|application|system)\b", q))
    has_detail_connector = any(token in q for token in [" with ", " including ", " for ", " and ", ","])
    return has_action and has_detail_connector and len(hits) >= 3


def missing_client_proposal_fields(query):
    missing = []
    if not detect_project_type_from_query(query):
        missing.append("project type / solution category")
    if not has_basic_project_requirement_in_query(query):
        missing.append("basic project requirement with modules/features, users/roles, integrations, reports, cloud/security needs")
    if not has_budget_in_query(query):
        missing.append("expected budget")
    if not has_timeline_in_query(query):
        missing.append("expected timeline")
    if not has_company_name_in_query(query):
        missing.append("company name")
    if not has_contact_in_query(query):
        missing.append("contact email or phone number")
    return missing


def is_complete_client_proposal(query):
    return not is_company_performance_query(query) and len(missing_client_proposal_fields(query)) == 0


def format_missing_client_fields_message(missing):
    if not missing:
        return ""
    return (
        "AI Front Desk: I can start the internal LifecycleDesk AI meeting after I have all required client details. "
        "Please share: " + ", ".join(missing) + ".\n\n"
        "Example: 'Company name is EduSmart, contact edu@example.com. We need an AI chatbot for students and staff "
        "with login, role-based access, document upload, FAQs, admin dashboard, reports, notifications, and cloud deployment. "
        "Budget 40 lakhs, timeline 8 months.'"
    )


def _extract_basic_requirement_text(query):
    text_value = re.sub(r"\s+", " ", safe_text(query)).strip()
    # Remove obvious commercial/contact fragments while preserving project intent.
    cleaned = re.sub(r"\b(?:budget|cost)\s*(?:is|of|:)?\s*₹?\s*\d+\s*(?:lakh|lakhs|lac|lacs|l|crore|crores|cr)?", "", text_value, flags=re.IGNORECASE)
    cleaned = re.sub(r"\b(?:timeline|time line|duration)\s*(?:is|of|:)?\s*\d+\s*(?:month|months|week|weeks)", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "", cleaned)
    cleaned = re.sub(r"(?:\+91[-\s]?)?[6-9]\d{9}", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" .,-")
    return cleaned or text_value


def derive_initial_requirement_profile(query, project_type=""):
    """Create the Technical Architect Agent's first-pass requirement copy."""
    q = safe_text(query).lower()
    requirement_text = _extract_basic_requirement_text(query)

    module_rules = [
        ("Authentication and login", ["login", "authentication", "signin", "sign in"]),
        ("Role-based access and permissions", ["role", "permission", "access", "authorization"]),
        ("AI chatbot / assistant", ["chatbot", "assistant", "faq", "query", "copilot"]),
        ("Admin dashboard", ["admin", "dashboard", "management console"]),
        ("Reports and analytics", ["report", "analytics", "insight", "dashboard", "export"]),
        ("Document upload and processing", ["upload", "document", "pdf", "docx", "file"]),
        ("Workflow approvals", ["workflow", "approval", "review", "status"]),
        ("Notifications and alerts", ["notification", "alert", "email", "sms", "reminder"]),
        ("API / external integrations", ["api", "integration", "webhook", "third party", "external"]),
        ("Data pipeline / ETL", ["pipeline", "etl", "ingestion", "validation", "warehouse"]),
        ("Mobile or responsive access", ["mobile", "android", "ios", "responsive"]),
        ("Cloud deployment", ["cloud", "deployment", "hosting", "aws", "azure", "gcp"]),
        ("Security and audit controls", ["security", "audit", "encryption", "compliance"]),
    ]
    modules = [label for label, keys in module_rules if any(key in q for key in keys)]
    if not modules:
        modules = [safe_text(project_type) or "Client software solution"]

    user_roles = []
    for label, keys in [
        ("Admin users", ["admin"]),
        ("Employees / internal users", ["employee", "staff", "internal"]),
        ("Client users", ["client", "customer"]),
        ("Students", ["student"]),
        ("Managers / approvers", ["manager", "approval", "approver"]),
    ]:
        if any(key in q for key in keys):
            user_roles.append(label)
    if not user_roles:
        user_roles = ["Admin users", "End users"]

    integrations = []
    for label, keys in [
        ("Existing APIs", ["api", "webhook", "integration"]),
        ("Document/file storage", ["document", "file", "upload", "pdf"]),
        ("Email/SMS notification channel", ["email", "sms", "notification"]),
        ("Cloud database/storage", ["database", "storage", "cloud"]),
        ("Data connectors / ETL sources", ["etl", "pipeline", "ingestion", "data source"]),
    ]:
        if any(key in q for key in keys):
            integrations.append(label)

    unknowns = []
    if not integrations:
        unknowns.append("External integration list must be confirmed during detailed requirement stage.")
    if "security" not in q and "compliance" not in q:
        unknowns.append("Security/compliance depth must be confirmed before kickoff.")
    if "cloud" not in q and "deploy" not in q and "hosting" not in q:
        unknowns.append("Deployment environment must be confirmed before kickoff.")

    return {
        "requirement_copy": requirement_text,
        "derived_summary": (
            f"Build {safe_text(project_type) or 'the requested solution'} with "
            + ", ".join(modules[:8])
            + "."
        ),
        "modules": modules,
        "user_roles": user_roles,
        "integrations": integrations,
        "unknowns_for_detailed_requirement": unknowns,
    }


def infer_technical_stack_from_requirement(requirement_profile, project_type=""):
    modules = " ".join(requirement_profile.get("modules", [])).lower()
    req_text = safe_text(requirement_profile.get("requirement_copy")).lower()
    q = modules + " " + req_text + " " + safe_text(project_type).lower()

    stack = {
        "frontend": ["React or Streamlit enterprise UI"],
        "backend": ["Python FastAPI service layer"],
        "database": ["Supabase PostgreSQL"],
        "ai_layer": [],
        "storage": [],
        "integrations": [],
        "cloud_devops": ["Docker/GitHub based deployment pipeline", "Streamlit Cloud or enterprise cloud hosting"],
        "security": ["Role-based access control", "Secrets-managed configuration"],
        "testing": ["Functional testing", "User acceptance testing"],
    }

    if any(x in q for x in ["chatbot", "assistant", "faq", "query", "ai"]):
        stack["ai_layer"].extend(["OpenAI-compatible LLM", "Prompt orchestration"])
    if any(x in q for x in ["document", "upload", "pdf", "docx", "file"]):
        stack["ai_layer"].append("Document extraction / RAG pipeline")
        stack["storage"].append("Object/file storage for uploads")
    if any(x in q for x in ["pipeline", "etl", "ingestion", "validation", "warehouse"]):
        stack["backend"].append("Scheduled ETL jobs")
        stack["database"].append("Analytics/data mart tables")
        stack["integrations"].append("Source data connectors")
    if any(x in q for x in ["api", "integration", "webhook", "third party", "external"]):
        stack["integrations"].append("REST API / webhook integrations")
    if any(x in q for x in ["report", "analytics", "dashboard", "export"]):
        stack["frontend"].append("Reporting dashboard UI")
        stack["backend"].append("Reporting/export services")
    if any(x in q for x in ["mobile", "android", "ios"]):
        stack["frontend"].append("Responsive/mobile-ready UI")
    if any(x in q for x in ["security", "audit", "compliance", "encryption"]):
        stack["security"].extend(["Audit trail", "Encryption and access logging"])

    for key, values in list(stack.items()):
        clean = []
        for item in values:
            if item and item not in clean:
                clean.append(item)
        stack[key] = clean or ["To be finalized in detailed requirement stage"]
    return stack


def _scope_score_from_requirement(requirement_profile, tech_stack):
    modules = requirement_profile.get("modules", []) or []
    integrations = requirement_profile.get("integrations", []) or []
    stack_text = json.dumps(tech_stack, ensure_ascii=False).lower()
    score = 0
    score += len(modules)
    score += len(integrations) * 2
    if "rag" in stack_text or "document extraction" in stack_text:
        score += 2
    if "etl" in stack_text or "data connector" in stack_text:
        score += 2
    if "audit" in stack_text or "encryption" in stack_text:
        score += 1
    if "mobile" in stack_text:
        score += 1
    if score <= 4:
        return "Low", 3
    if score <= 8:
        return "Medium", 5
    if score <= 12:
        return "High", 7
    return "Very High", 9


def _role_delivery_allocation(scope_complexity, role):
    role = safe_text(role).lower()
    base_by_complexity = {
        "Low": 0.32,
        "Medium": 0.42,
        "High": 0.52,
        "Very High": 0.58,
    }
    allocation = base_by_complexity.get(scope_complexity, 0.42)
    if "project manager" in role:
        allocation *= 0.55
    elif "devops" in role:
        allocation *= 0.55
    elif "qa" in role or "test" in role:
        allocation *= 0.65
    elif "frontend" in role:
        allocation *= 0.85
    elif "backend" in role:
        allocation *= 1.0
    elif "ai" in role or "ml" in role or "data" in role:
        allocation *= 1.0
    return round(min(0.75, max(0.18, allocation)), 2)


def _role_phase_factor(role):
    role = safe_text(role).lower()
    if "project manager" in role:
        return 0.80
    if "devops" in role:
        return 0.45
    if "qa" in role or "test" in role:
        return 0.55
    if "frontend" in role:
        return 0.70
    if "backend" in role:
        return 0.85
    if "ai" in role or "ml" in role or "data" in role:
        return 0.85
    return 0.70


def _capacity_delay_months(total_immediate_gap, total_projected_gap, total_hurdles, total_active_pending_fte):
    delay = 0.0
    if total_immediate_gap > 0.5 and total_projected_gap <= 0.5:
        delay += 1.0
    elif total_projected_gap > 0.5:
        delay += min(2.0, 0.75 + total_projected_gap * 0.35)
    if total_hurdles > 0:
        delay += min(1.0, total_hurdles * 0.25)
    if total_active_pending_fte > 3:
        delay += 0.5
    return min(3.0, delay)


def _hiring_recommendation(total_hiring_needed, total_immediate_gap, total_projected_gap, timeline_risk):
    if total_hiring_needed <= 0.25:
        if total_immediate_gap > 0.5 and total_projected_gap <= 0.5:
            return "No hiring now. Rebalance bandwidth and wait for near-release capacity."
        return "No hiring needed for the initial quotation. Existing bandwidth can cover with allocation planning."
    if total_hiring_needed <= 1.0:
        return "Hiring is optional. Prefer short-term contractor/backfill only if client timeline cannot move."
    if timeline_risk == "High":
        return "Hiring or contract support is recommended before committing to this timeline."
    return "Hiring/backfill recommended for material projected capacity gap."


def _flatten_stack(stack):
    parts = []
    for key, values in stack.items():
        if isinstance(values, list):
            parts.append(f"{key}: " + ", ".join(values[:3]))
        else:
            parts.append(f"{key}: {values}")
    return " | ".join(parts)


def derive_technical_architect_assessment(query, project_type, client_requested_timeline):
    requirement_profile = derive_initial_requirement_profile(query, project_type)
    stack = infer_technical_stack_from_requirement(requirement_profile, project_type)
    scope_complexity, scope_effort_months = _scope_score_from_requirement(requirement_profile, stack)
    base_timeline = max(2, int(scope_effort_months))
    client_timeline = max(1, safe_int(client_requested_timeline, base_timeline))
    timeline_basis = (
        f"Technical Architect Agent derived {base_timeline} month(s) from initial scope complexity "
        f"({scope_complexity}), modules ({len(requirement_profile.get('modules', []))}), integrations "
        f"({len(requirement_profile.get('integrations', []))}), and stack depth. Client requested {client_timeline} month(s)."
    )
    return {
        "requirement_profile": requirement_profile,
        "technical_stack": stack,
        "scope_complexity": scope_complexity,
        "scope_effort_months": base_timeline,
        "timeline_basis": timeline_basis,
    }


def run_external_client_decision(query, data):
    budget = extract_budget(query)
    client_requested_timeline = extract_timeline_months(query)
    project_type = detect_project_type_from_query(query) or "AI Chatbot"

    requirements = data["requirements"]
    employees = data["employees"]
    req = requirements[requirements["project_type"].astype(str) == project_type]
    if req.empty:
        project_type = "AI Chatbot"
        req = requirements[requirements["project_type"].astype(str) == project_type]

    architect = derive_technical_architect_assessment(query, project_type, client_requested_timeline)
    scope_complexity = architect["scope_complexity"]
    scope_effort_months = safe_int(architect["scope_effort_months"], client_requested_timeline)

    # First pass: capacity/bandwidth using the scope-derived timeline, not the client guess.
    capacity_rows = build_dynamic_role_capacity(req, employees, scope_effort_months)
    capacity_by_role = {item["role"]: item for item in capacity_rows}

    total_immediate_gap_pre = sum(safe_number(item.get("immediate_gap"), 0) for item in capacity_rows)
    total_projected_gap_pre = sum(safe_number(item.get("gap"), 0) for item in capacity_rows)
    total_hurdles_pre = sum(safe_int(item.get("hurdle_or_support_request_count"), 0) for item in capacity_rows)
    total_active_pending_fte_pre = sum(safe_number(item.get("active_allocated_fte"), 0) for item in capacity_rows)
    bandwidth_delay = _capacity_delay_months(
        total_immediate_gap_pre,
        total_projected_gap_pre,
        total_hurdles_pre,
        total_active_pending_fte_pre,
    )
    realistic_timeline = int(max(scope_effort_months, round(scope_effort_months + bandwidth_delay)))

    # Re-check projected release/bandwidth using the final realistic timeline.
    capacity_rows = build_dynamic_role_capacity(req, employees, realistic_timeline)
    capacity_by_role = {item["role"]: item for item in capacity_rows}
    live_project_snapshot = build_live_project_capacity_snapshot(limit=8)

    productive_effort_cost = 0.0
    calendar_carry_cost = 0.0
    hiring_or_contract_premium = 0.0
    pending_work_risk_buffer = 0.0
    role_cost_breakdown = []
    skill_gap = []

    for _, row in req.iterrows():
        role = safe_text(row.get("required_role"))
        needed = safe_number(row.get("required_people"), 0)
        capacity = capacity_by_role.get(role, {})
        avg_salary = safe_number(capacity.get("avg_monthly_salary"), 90000)
        available_now = safe_number(capacity.get("available_now_fte"), 0)
        projected_available = safe_number(capacity.get("projected_available_fte"), 0)
        active_pending = safe_number(capacity.get("active_allocated_fte"), 0)
        immediate_gap = max(0.0, needed - available_now)
        projected_gap = max(0.0, needed - projected_available)
        hiring_needed = projected_gap if projected_gap > 0.30 else 0.0
        allocation = _role_delivery_allocation(scope_complexity, role)
        phase_factor = _role_phase_factor(role)
        productive_months = max(1.0, min(realistic_timeline, scope_effort_months * phase_factor))
        base_effort_cost = avg_salary * needed * allocation * productive_months
        stretch_months = max(0.0, realistic_timeline - scope_effort_months)
        carry_cost = avg_salary * needed * allocation * stretch_months * 0.12
        hurdles = safe_int(capacity.get("hurdle_or_support_request_count"), 0)
        risk_rate = min(0.06, active_pending * 0.012 + hurdles * 0.012)
        risk_buffer = base_effort_cost * risk_rate
        hire_premium = 0.0
        if hiring_needed > 0:
            hire_premium = avg_salary * hiring_needed * min(2.0, productive_months) * 0.30
            if hurdles:
                hire_premium *= 1.05

        productive_effort_cost += base_effort_cost
        calendar_carry_cost += carry_cost
        hiring_or_contract_premium += hire_premium
        pending_work_risk_buffer += risk_buffer

        role_total = base_effort_cost + carry_cost + hire_premium + risk_buffer
        role_cost_breakdown.append({
            "role": role,
            "people_required": round(needed, 2),
            "avg_monthly_salary": round(avg_salary, 2),
            "allocation_used": round(allocation, 2),
            "scope_effort_months": scope_effort_months,
            "productive_effort_months": round(productive_months, 2),
            "realistic_calendar_months": realistic_timeline,
            "base_effort_cost": round(base_effort_cost, 2),
            "calendar_carry_cost": round(carry_cost, 2),
            "hiring_or_contract_premium": round(hire_premium, 2),
            "pending_work_risk_buffer": round(risk_buffer, 2),
            "role_cost": round(role_total, 2),
            "available_now_fte": round(available_now, 2),
            "projected_available_fte": round(projected_available, 2),
            "active_pending_work_fte": round(active_pending, 2),
            "immediate_gap_fte": round(immediate_gap, 2),
            "projected_gap_fte": round(projected_gap, 2),
            "hiring_needed_fte": round(hiring_needed, 2),
            "avg_current_project_progress_percent": capacity.get("avg_current_project_progress_percent", 0),
            "open_hurdles_or_support_requests": hurdles,
            "nearest_release_date": capacity.get("nearest_release_date", ""),
            "cost_formula": "salary x required FTE x allocation x productive effort months + small calendar carry cost + hiring premium only for material projected gap + capped pending-work risk buffer",
            "dynamic_capacity_basis": capacity.get("capacity_notes", ""),
        })
        skill_gap.append({
            "role": role,
            "needed": round(needed, 2),
            "available_capacity": round(projected_available, 2),
            "available_now_fte": round(available_now, 2),
            "projected_available_fte": round(projected_available, 2),
            "active_allocated_fte": round(active_pending, 2),
            "immediate_gap": round(immediate_gap, 2),
            "gap": round(projected_gap, 2),
            "hiring_needed_fte": round(hiring_needed, 2),
            "avg_current_project_progress_percent": capacity.get("avg_current_project_progress_percent", 0),
            "hurdle_or_support_request_count": hurdles,
            "nearest_release_date": capacity.get("nearest_release_date", ""),
            "capacity_notes": capacity.get("capacity_notes", ""),
        })

    labor_and_capacity_cost = productive_effort_cost + calendar_carry_cost + hiring_or_contract_premium + pending_work_risk_buffer
    overhead = labor_and_capacity_cost * 0.12
    complexity_cloud_rate = {"Low": 0.04, "Medium": 0.055, "High": 0.075, "Very High": 0.09}.get(scope_complexity, 0.055)
    complexity_contingency_rate = {"Low": 0.05, "Medium": 0.07, "High": 0.09, "Very High": 0.11}.get(scope_complexity, 0.07)
    cloud_cost = max(75000, labor_and_capacity_cost * complexity_cloud_rate)
    software_cost = max(40000, labor_and_capacity_cost * 0.03)
    contingency = labor_and_capacity_cost * complexity_contingency_rate
    total_cost = labor_and_capacity_cost + overhead + cloud_cost + software_cost + contingency

    target_margin = 0.30 if scope_complexity in ["Low", "Medium"] else 0.35
    recommended_quote = total_cost / (1 - target_margin) if target_margin < 1 else total_cost
    profit_at_client_budget = budget - total_cost
    margin_at_client_budget = profit_at_client_budget / budget if budget else 0

    total_skill_gap = sum(safe_number(item.get("gap"), 0) for item in skill_gap)
    immediate_skill_gap = sum(safe_number(item.get("immediate_gap"), 0) for item in skill_gap)
    total_hiring_needed = sum(safe_number(item.get("hiring_needed_fte"), 0) for item in skill_gap)
    total_active_allocated_fte = sum(safe_number(item.get("active_allocated_fte"), 0) for item in skill_gap)
    total_hurdles = sum(safe_int(item.get("hurdle_or_support_request_count"), 0) for item in skill_gap)

    if client_requested_timeline < realistic_timeline or total_hiring_needed > 1.0 or total_hurdles >= 3:
        timeline_risk = "High"
    elif bandwidth_delay > 0 or total_hurdles > 0 or immediate_skill_gap > 0.5:
        timeline_risk = "Medium"
    else:
        timeline_risk = "Low"

    hiring_recommendation = _hiring_recommendation(total_hiring_needed, immediate_skill_gap, total_skill_gap, timeline_risk)

    if budget < total_cost:
        decision = "Reject or Renegotiate"
        reason = (
            "Client budget is below the corrected delivery cost calculated from derived requirement scope, "
            "productive role effort, live bandwidth, pending work, cloud/tools, overhead, and risk buffers."
        )
    elif budget < recommended_quote:
        decision = "Accept only with conditions"
        reason = "Client budget covers estimated cost, but is below the target-margin quote. Negotiate scope, price, or payment terms."
    elif client_requested_timeline < realistic_timeline:
        decision = "Accept only with conditions"
        reason = f"Technical Architect Agent estimates {realistic_timeline} month(s) are realistic, while the client requested {client_requested_timeline} month(s)."
    elif total_hiring_needed > 1.0:
        decision = "Accept only with conditions"
        reason = "Commercials are feasible, but hiring/contract support is needed for the projected bandwidth gap."
    else:
        decision = "Accept"
        reason = "Budget, derived technical scope, realistic timeline, and live bandwidth are feasible."

    costing_method = (
        "productive project effort cost + small calendar carry cost for bandwidth stretch + hiring/contract premium only when projected release/rebalance cannot cover gap + capped pending-work risk buffer + overhead + cloud/tools + contingency + target margin"
    )

    return {
        "client_message": query,
        "client_budget": round(budget, 2),
        "project_type": project_type,
        "timeline_months": realistic_timeline,
        "client_requested_timeline_months": client_requested_timeline,
        "scope_effort_months": scope_effort_months,
        "scope_complexity": scope_complexity,
        "initial_requirement_summary": architect["requirement_profile"].get("derived_summary", ""),
        "technical_architect_requirement": json.dumps(architect["requirement_profile"], ensure_ascii=False),
        "technical_architect_stack": architect["technical_stack"],
        "technical_architect_stack_json": json.dumps(architect["technical_stack"], ensure_ascii=False),
        "technical_architect_timeline_basis": architect["timeline_basis"],
        "employee_cost": round(productive_effort_cost, 2),
        "productive_effort_cost": round(productive_effort_cost, 2),
        "calendar_carry_cost": round(calendar_carry_cost, 2),
        "hiring_or_contract_premium": round(hiring_or_contract_premium, 2),
        "pending_work_risk_buffer": round(pending_work_risk_buffer, 2),
        "labor_and_capacity_cost": round(labor_and_capacity_cost, 2),
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
        "total_hiring_needed_fte": round(total_hiring_needed, 2),
        "total_active_allocated_fte": round(total_active_allocated_fte, 2),
        "dynamic_hurdle_count": int(total_hurdles),
        "timeline_risk": timeline_risk,
        "hiring_recommendation": hiring_recommendation,
        "costing_method": costing_method,
        "capacity_basis": "Excel employee master/payroll + Supabase projects, allocations, delivery plans, weekly progress, pending work, release timing, and open employee requests.",
        "live_project_capacity_snapshot": live_project_snapshot,
        "decision": decision,
        "reason": reason,
    }


def build_agent_summaries(analysis):
    budget = safe_number(analysis.get("client_budget"))
    quote = safe_number(analysis.get("recommended_quote"))
    cost = safe_number(analysis.get("estimated_cost"))
    margin = safe_number(analysis.get("profit_margin_at_client_budget"))
    real_timeline = safe_int(analysis.get("timeline_months"))
    client_timeline = safe_int(analysis.get("client_requested_timeline_months"), real_timeline)
    immediate_gap = safe_number(analysis.get("immediate_skill_gap"), 0)
    projected_gap = safe_number(analysis.get("total_skill_gap"), 0)
    hiring_needed = safe_number(analysis.get("total_hiring_needed_fte"), 0)
    active_fte = safe_number(analysis.get("total_active_allocated_fte"), 0)
    hurdle_count = safe_int(analysis.get("dynamic_hurdle_count"), 0)
    timeline_risk = safe_text(analysis.get("timeline_risk"))
    decision = safe_text(analysis.get("decision"))
    reason = safe_text(analysis.get("reason"))
    stack = analysis.get("technical_architect_stack") or decode_json(analysis.get("technical_architect_stack_json"), {})
    stack_text = _flatten_stack(stack) if isinstance(stack, dict) else safe_text(stack)
    return {
        "sales_agent_summary": (
            f"Sales captured a {analysis.get('project_type', 'project')} opportunity with client budget {money_text(budget)}. "
            f"Recommended client-facing quote is {money_text(quote)} after technical scope and finance review."
        ),
        "hr_agent_summary": (
            f"HR checked live bandwidth, pending work, release timing, and open blockers. Immediate gap: {immediate_gap} FTE; "
            f"projected gap: {projected_gap} FTE; hiring needed: {hiring_needed} FTE. {analysis.get('hiring_recommendation', '')}"
        ),
        "operations_agent_summary": (
            f"Technical Architect Agent derived the initial requirement as: {analysis.get('initial_requirement_summary', '')} "
            f"Suggested stack: {stack_text}. Realistic timeline: {real_timeline} month(s); client requested {client_timeline} month(s). "
            f"Timeline risk: {timeline_risk}; active pending load considered: {active_fte} FTE; open blockers/support requests: {hurdle_count}."
        ),
        "finance_agent_summary": (
            f"Finance estimated corrected delivery cost at {money_text(cost)}, target quote at {money_text(quote)}, and margin at client budget at {margin}%. "
            f"Method: {analysis.get('costing_method', '')}"
        ),
        "ceo_agent_summary": f"Initial CEO-style recommendation: {decision}. Reason: {reason}",
    }


try:
    _v43_original_proposal_row_to_report = proposal_row_to_report
except Exception:
    _v43_original_proposal_row_to_report = None


def proposal_row_to_report(row):
    if _v43_original_proposal_row_to_report is not None:
        report = _v43_original_proposal_row_to_report(row)
    else:
        report = {}
    if hasattr(row, "to_dict"):
        row_dict = row.to_dict()
    elif isinstance(row, dict):
        row_dict = row
    else:
        row_dict = {}
    analysis = report.setdefault("analysis", {})
    analysis.update({
        "client_requested_timeline_months": safe_int(row_dict.get("client_requested_timeline_months"), analysis.get("timeline_months", 0)),
        "scope_complexity": safe_text(row_dict.get("scope_complexity")),
        "scope_effort_months": safe_int(row_dict.get("scope_effort_months"), 0),
        "initial_requirement_summary": safe_text(row_dict.get("initial_requirement_summary")),
        "technical_architect_requirement": decode_json(row_dict.get("technical_architect_requirement"), {}),
        "technical_architect_stack": decode_json(row_dict.get("technical_architect_stack_json"), {}),
        "technical_architect_stack_json": safe_text(row_dict.get("technical_architect_stack_json")),
        "technical_architect_timeline_basis": safe_text(row_dict.get("technical_architect_timeline_basis")),
        "hiring_recommendation": safe_text(row_dict.get("hiring_recommendation")),
        "total_hiring_needed_fte": safe_number(row_dict.get("total_hiring_needed_fte"), 0),
        "calendar_carry_cost": safe_number(row_dict.get("calendar_carry_cost"), 0),
        "hiring_or_contract_premium": safe_number(row_dict.get("hiring_or_contract_premium"), 0),
        "pending_work_risk_buffer": safe_number(row_dict.get("pending_work_risk_buffer"), 0),
        "costing_method": safe_text(row_dict.get("costing_method")),
    })
    return report


def save_external_client_report_to_excel(raw_client_message, analysis):
    """Persist the agent decision packet with initial requirement + tech architect copy."""
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
        "initial_requirement_summary": analysis.get("initial_requirement_summary", ""),
        "technical_architect_requirement": analysis.get("technical_architect_requirement", ""),
        "technical_architect_stack_json": analysis.get("technical_architect_stack_json", encode_json(analysis.get("technical_architect_stack", {}))),
        "technical_architect_timeline_basis": analysis.get("technical_architect_timeline_basis", ""),
        "client_requested_timeline_months": analysis.get("client_requested_timeline_months", ""),
        "scope_complexity": analysis.get("scope_complexity", ""),
        "scope_effort_months": analysis.get("scope_effort_months", ""),
        "hiring_recommendation": analysis.get("hiring_recommendation", ""),
        "total_hiring_needed_fte": analysis.get("total_hiring_needed_fte", 0),
        "calendar_carry_cost": analysis.get("calendar_carry_cost", 0),
        "hiring_or_contract_premium": analysis.get("hiring_or_contract_premium", 0),
        "pending_work_risk_buffer": analysis.get("pending_work_risk_buffer", 0),
        "costing_method": analysis.get("costing_method", ""),
        "sales_seen": "No",
        "finance_seen": "No",
        "hr_seen": "No",
        "operations_seen": "No",
        "ceo_seen": "No",
        "quotation_sent": "No",
        "last_updated_by": "AI Front Desk",
        "last_updated_role": "System",
        "last_updated_at": now,
        "last_update_summary": "New proposal created with basic client requirement, Technical Architect Agent scope, and corrected finance costing.",
    })

    upsert_proposal_row(row)
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
    append_proposal_history(
        proposal_id,
        {"user_id": "SYSTEM", "employee_name": "Technical Architect Agent", "designation": "System"},
        "Initial Requirement Derived",
        comment=analysis.get("initial_requirement_summary", ""),
        recommended_timeline_months=analysis.get("timeline_months", 0),
        summary="Technical Architect Agent saved the derived initial requirement copy, stack recommendation, and realistic timeline basis.",
    )

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


def render_agentic_decision_pack(report):
    analysis = report["analysis"]
    summaries = report.get("agent_summaries", {})
    stack = analysis.get("technical_architect_stack") or {}
    requirement_profile = analysis.get("technical_architect_requirement") or {}

    st.markdown(
        """
        <div class="dd-section-card">
            <div class="dd-section-title">Full multi-department agent analysis</div>
            <div class="dd-section-subtitle">
                These are the internal AI agent conclusions saved to proposal storage. Executives review this shared context before giving their own department opinion.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab_sales, tab_hr, tab_arch, tab_fin, tab_ceo = st.tabs([
        "🧲 Sales Agent",
        "👥 HR Agent",
        "🛠️ Technical Architect Agent",
        "💰 Finance Agent",
        "👑 CEO Agent",
    ])

    with tab_sales:
        st.markdown("#### Sales Agent basis")
        st.write(summaries.get("sales") or "Sales summary unavailable.")
        s1, s2, s3 = st.columns(3)
        s1.metric("Client Budget", money_text(analysis.get("client_budget")))
        s2.metric("Suggested Quote", money_text(analysis.get("recommended_quote")))
        s3.metric("Project Type", analysis.get("project_type"))
        st.caption("Sales uses client budget, opportunity type, requirement clarity, and quote direction to guide negotiation.")

    with tab_hr:
        st.markdown("#### HR Agent basis")
        st.write(summaries.get("hr") or "HR summary unavailable.")
        h1, h2, h3 = st.columns(3)
        h1.metric("Projected Gap", f"{analysis.get('total_skill_gap', 0)} FTE")
        h2.metric("Hiring Needed", f"{analysis.get('total_hiring_needed_fte', 0)} FTE")
        h3.metric("Bandwidth Load", f"{analysis.get('total_active_allocated_fte', 0)} FTE")
        if analysis.get("hiring_recommendation"):
            st.info(analysis.get("hiring_recommendation"))
        render_dynamic_skill_gap_table(analysis)
        st.caption("HR focuses on hiring need, available capacity, pending work, and people/resource risk — not quotation pricing.")

    with tab_arch:
        st.markdown("#### Technical Architect Agent basis")
        render_technical_architect_basis_key_value(analysis, summaries)
        a1, a2, a3, a4 = st.columns(4)
        a1.metric("Client Requested", f"{analysis.get('client_requested_timeline_months') or analysis.get('timeline_months')} months")
        a2.metric("Realistic Timeline", f"{analysis.get('timeline_months')} months")
        a3.metric("Scope Complexity", analysis.get("scope_complexity") or "Not captured")
        a4.metric("Timeline Risk", analysis.get("timeline_risk"))
        if requirement_profile:
            with st.expander("Saved derived initial requirement copy", expanded=True):
                st.write(requirement_profile.get("derived_summary") or analysis.get("initial_requirement_summary"))
                if requirement_profile.get("modules"):
                    st.write("**Derived modules/features:** " + ", ".join(requirement_profile.get("modules", [])))
                if requirement_profile.get("user_roles"):
                    st.write("**User roles:** " + ", ".join(requirement_profile.get("user_roles", [])))
                if requirement_profile.get("integrations"):
                    st.write("**Likely integrations:** " + ", ".join(requirement_profile.get("integrations", [])))
                if requirement_profile.get("unknowns_for_detailed_requirement"):
                    st.write("**To confirm after quotation acceptance:** " + ", ".join(requirement_profile.get("unknowns_for_detailed_requirement", [])))
                if requirement_profile.get("requirement_copy"):
                    st.text_area("Original/basic requirement copy used by Technical Architect", value=requirement_profile.get("requirement_copy"), height=120, disabled=True, key=f"derived_req_{report.get('proposal_id')}")
        if stack:
            with st.expander("Suggested technical stack", expanded=True):
                rows = []
                for layer, values in stack.items():
                    rows.append({"Layer": layer.replace("_", " ").title(), "Suggested stack": ", ".join(values) if isinstance(values, list) else safe_text(values)})
                st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        st.caption("The detailed requirement is still requested after the client accepts the quotation; this saved copy is only the initial requirement derived for quotation/costing.")

    with tab_fin:
        st.markdown("#### Finance Agent basis")
        st.write(summaries.get("finance") or "Finance summary unavailable.")
        f1, f2, f3, f4 = st.columns(4)
        f1.metric("Estimated Cost", money_text(analysis.get("estimated_cost")))
        f2.metric("Recommended Quote", money_text(analysis.get("recommended_quote")))
        f3.metric("Margin at Budget", f"{analysis.get('profit_margin_at_client_budget')}%")
        f4.metric("Target Margin", f"{analysis.get('target_margin_percent')}%")
        c1, c2, c3 = st.columns(3)
        c1.metric("Carry Cost", money_text(analysis.get("calendar_carry_cost", 0)))
        c2.metric("Hiring Premium", money_text(analysis.get("hiring_or_contract_premium", 0)))
        c3.metric("Pending-work Buffer", money_text(analysis.get("pending_work_risk_buffer", 0)))
        if analysis.get("costing_method"):
            st.caption("Costing method: " + safe_text(analysis.get("costing_method")))
        role_cost_df = pd.DataFrame(analysis.get("role_cost_breakdown", []))
        if not role_cost_df.empty:
            with st.expander("Role-level corrected cost basis", expanded=False):
                st.dataframe(role_cost_df, use_container_width=True, hide_index=True)
        st.caption("Finance now treats pending work as bandwidth/timeline/hiring input first, not as automatic full salary burn.")

    with tab_ceo:
        st.markdown("#### CEO Agent initial recommendation")
        st.write(summaries.get("ceo") or "CEO summary unavailable.")
        write_decision_status(analysis.get("initial_agent_decision") or analysis.get("decision"))
        st.write(analysis.get("initial_agent_reason") or analysis.get("reason"))


# ---------------- AI FRONT DESK + COMPANY PROFILE + WEEKLY TARGETS PATCH ----------------
# Late overrides only. The working v43 flow remains intact; this section adds
# company identity, weekly target planning, and mandatory employee weekly updates.

COMPANY_NAME = "Virtual Tech AI"
COMPANY_LOCATION = "Bangalore"
COMPANY_DESCRIPTION = "Virtual Tech AI is a Bangalore-based company that provides AI and data solutions."
APP_TAGLINE = "Virtual Tech AI's AI and data solutions lifecycle platform"

try:
    if "weekly_targets" not in DELIVERY_PLAN_COLUMNS:
        insert_after = "module_breakdown" if "module_breakdown" in DELIVERY_PLAN_COLUMNS else "operations_manager_plan"
        insert_at = DELIVERY_PLAN_COLUMNS.index(insert_after) + 1
        DELIVERY_PLAN_COLUMNS.insert(insert_at, "weekly_targets")
except Exception:
    pass


def company_profile_text():
    return COMPANY_DESCRIPTION


def render_app_hero():
    st.markdown(
        f"""
        <div class=\"dd-hero\">
            <div class=\"dd-kicker\">🚀 {COMPANY_NAME} · {COMPANY_LOCATION}</div>
            <div class=\"dd-hero-title\">{APP_NAME}</div>
            <div class=\"dd-hero-subtitle\">
                {COMPANY_DESCRIPTION} This workspace manages the full client-to-delivery lifecycle:
                basic requirement intake, agent analysis, executive approval, quotation, client confirmation,
                detailed requirement, weekly targets, resource allocation, and employee updates.
            </div>
            <div class=\"dd-flow\">
                <span>1. AI Front Desk intake</span>
                <span>2. Agent analysis</span>
                <span>3. Executive approval</span>
                <span>4. Quotation + client response</span>
                <span>5. Weekly targets + project updates</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_process_snapshot():
    st.markdown(
        f"""
        <div class=\"dd-section-card\">
            <div class=\"dd-section-title\">Lifecycle workflow</div>
            <div class=\"dd-section-subtitle\">
                {COMPANY_NAME} uses this AI workspace to manage AI and data solution delivery from first enquiry to weekly project execution.
            </div>
            <div class=\"dd-stepper\">
                <div class=\"dd-step\"><strong>AI Front Desk</strong><span>Receives company details and basic requirement</span></div>
                <div class=\"dd-step\"><strong>Agent Meeting</strong><span>Sales, HR, Technical Architect, Finance, CEO analyse</span></div>
                <div class=\"dd-step\"><strong>CEO Quote</strong><span>CEO approves and sends quotation to client</span></div>
                <div class=\"dd-step\"><strong>Client Response</strong><span>Client accepts, declines, or requests reconsideration</span></div>
                <div class=\"dd-step\"><strong>Detailed Requirement</strong><span>Client confirms the detailed requirement after acceptance</span></div>
                <div class=\"dd-step\"><strong>Weekly Targets</strong><span>Technical Architect Agent fixes weekly targets and shares them with the project team</span></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_chat_intro():
    st.markdown(
        f"""
        <div class=\"dd-section-card\">
            <div class=\"dd-section-title\">AI Front Desk</div>
            <div class=\"dd-section-subtitle\">
                {COMPANY_DESCRIPTION} Use AI Front Desk to start a new client/proposal workflow or route internal requests.
                For a project enquiry, share company name, contact, basic project requirement, expected budget, and expected timeline.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


try:
    _frontdesk_original_format_missing_client_fields_message = format_missing_client_fields_message
except Exception:
    _frontdesk_original_format_missing_client_fields_message = None


def format_missing_client_fields_message(missing):
    if not missing:
        return ""
    return (
        f"AI Front Desk: Welcome to {COMPANY_NAME}. {COMPANY_DESCRIPTION} "
        "I can start the internal LifecycleDesk AI meeting after I have all required client details. "
        "Please share: " + ", ".join(missing) + ".\n\n"
        "Example: 'Company name is EduSmart, contact edu@example.com. We need an AI chatbot for students and staff "
        "with login, role-based access, document upload, FAQs, admin dashboard, reports, notifications, and cloud deployment. "
        "Budget 40 lakhs, timeline 8 months.'"
    )


def _safe_analysis_from_report(report):
    if isinstance(report, dict):
        return report.get("analysis", {}) or {}
    return {}


def _delivery_week_count_from_report(report):
    analysis = _safe_analysis_from_report(report)
    months = (
        safe_int(analysis.get("timeline_months"), 0)
        or safe_int(report.get("ceo_final_timeline_months") if isinstance(report, dict) else 0, 0)
        or safe_int(report.get("timeline_months") if isinstance(report, dict) else 0, 0)
        or 3
    )
    return max(4, min(52, int(months) * 4))


def _modules_for_weekly_targets(report, detailed_requirement_text):
    analysis = _safe_analysis_from_report(report)
    modules = []
    tech_req = analysis.get("technical_architect_requirement") or {}
    if isinstance(tech_req, str):
        tech_req = decode_json(tech_req, {})
    if isinstance(tech_req, dict):
        modules.extend([safe_text(x) for x in tech_req.get("modules", []) if safe_text(x)])
    try:
        derived = derive_initial_requirement_profile(detailed_requirement_text, analysis.get("project_type", ""))
        modules.extend([safe_text(x) for x in derived.get("modules", []) if safe_text(x)])
    except Exception:
        pass
    clean = []
    for item in modules:
        if item and item not in clean:
            clean.append(item)
    return clean or ["Requirement confirmation", "Core development", "Testing", "Deployment readiness"]


def build_weekly_targets_for_delivery(report, detailed_requirement_text):
    """Create weekly targets after quotation acceptance and detailed requirement submission."""
    analysis = _safe_analysis_from_report(report)
    project_type = safe_text(analysis.get("project_type"), "Client project")
    week_count = _delivery_week_count_from_report(report)
    modules = _modules_for_weekly_targets(report, detailed_requirement_text)
    target_lines = [
        "Technical Architect Agent - Weekly Delivery Targets",
        f"Project type: {project_type}",
        f"Planned duration: {week_count} week(s)",
        "These targets are generated after client quotation acceptance using the detailed requirement. All allocated employees must submit one weekly update for their assigned project every week.",
        "",
    ]

    base_plan = [
        "Kickoff, requirement confirmation, access/dependency checklist, and sprint plan finalization",
        "Architecture/design finalization, database/API design, backlog and acceptance criteria",
        "Core module implementation and integration foundation",
        "Core module implementation, AI/data workflow setup, and internal review",
        "Feature completion, reporting/dashboard work, and integration hardening",
        "QA cycle, security/access validation, bug fixing, and client review preparation",
        "UAT support, deployment readiness, documentation, and handover preparation",
        "Production deployment support, stabilization, and final closure actions",
    ]

    for week in range(1, week_count + 1):
        if week == 1:
            target = base_plan[0]
        elif week == 2:
            target = base_plan[1]
        elif week >= week_count - 1:
            target = base_plan[7]
        elif week >= week_count - 3:
            target = base_plan[6]
        elif week >= max(5, int(week_count * 0.70)):
            target = base_plan[5]
        elif week >= max(4, int(week_count * 0.45)):
            target = base_plan[4]
        else:
            module = modules[(week - 3) % len(modules)] if modules else "core module"
            target = f"Build and review {module}"
        target_lines.append(f"Week {week}: {target}.")

    target_lines.extend([
        "",
        "Employee update rule: every allocated employee must submit weekly progress, blockers, support needs, and notes from the employee project workbench before the week closes.",
    ])
    return "\n".join(target_lines)


try:
    _weekly_original_build_operations_agent_delivery_plan = build_operations_agent_delivery_plan
except Exception:
    _weekly_original_build_operations_agent_delivery_plan = None


def build_operations_agent_delivery_plan(report, requirement_text):
    weekly_targets = build_weekly_targets_for_delivery(report, requirement_text)
    fallback = ""
    if _weekly_original_build_operations_agent_delivery_plan is not None:
        try:
            fallback = _weekly_original_build_operations_agent_delivery_plan(report, requirement_text)
        except Exception:
            fallback = ""
    if not fallback:
        analysis = _safe_analysis_from_report(report)
        fallback = f"""Technical Architect Agent Delivery Readiness Plan

1. Business Objective
Deliver {analysis.get('project_type', 'the requested solution')} for the client based on the accepted quotation and detailed requirement.

2. Detailed Requirement Source
{safe_text(requirement_text)}

3. Technical Delivery Focus
- Confirm final modules, roles, integrations, reports, cloud, security, and access needs
- Prepare architecture, sprint plan, employee allocation, QA path, and deployment readiness
"""
    if "Weekly Delivery Targets" not in fallback:
        fallback = fallback.rstrip() + "\n\n" + weekly_targets
    return fallback


try:
    _weekly_original_save_client_detailed_requirement = save_client_detailed_requirement
except Exception:
    _weekly_original_save_client_detailed_requirement = None


def save_client_detailed_requirement(report, client_account, requirement_text, uploaded_file_name=""):
    requirement_text = safe_text(requirement_text).strip()
    if len(requirement_text) < 20:
        return False, "Please provide a more detailed requirement before submitting."
    project = ensure_project_for_accepted_proposal(report, client_account)
    now = current_timestamp()
    weekly_targets = build_weekly_targets_for_delivery(report, requirement_text)
    plan_text = build_operations_agent_delivery_plan(report, requirement_text)
    row = {column: "" for column in DELIVERY_PLAN_COLUMNS}
    row.update({
        "delivery_plan_id": make_delivery_plan_id(),
        "project_id": project.get("project_id"),
        "proposal_id": report.get("proposal_id"),
        "client_id": client_account.get("client_id"),
        "requirement_source": "Client Portal Text/File",
        "uploaded_file_name": uploaded_file_name,
        "raw_requirement_text": requirement_text,
        "operations_agent_plan": plan_text,
        "operations_manager_plan": plan_text,
        "suggested_tools": "See Technical Architect Agent plan",
        "cloud_plan": "See Technical Architect Agent plan",
        "security_plan": "See Technical Architect Agent plan",
        "module_breakdown": "See Technical Architect Agent plan and weekly targets",
        "weekly_targets": weekly_targets,
        "risks_and_blockers": "See Technical Architect Agent plan",
        "client_clarifications_needed": "Please confirm final feature priorities, user roles and permissions, external integrations, branding/UI expectations, deployment preference, and weekly acceptance checkpoints.",
        "approval_status": "Technical Architect Agent Drafted - Review Pending",
        "approved_by": "",
        "approved_at": "",
        "created_at": now,
        "updated_at": now,
    })
    upsert_simple_row("delivery_plans", "delivery_plan_id", DELIVERY_PLAN_COLUMNS, row)
    try:
        df = read_proposal_store(create_if_missing=True)
        mask = df["proposal_id"].astype(str) == safe_text(report.get("proposal_id"))
        if mask.any():
            df.loc[mask, "workflow_status"] = "Detailed Requirement Submitted - Technical Architect Review Pending"
            df.loc[mask, "current_owner"] = "Technical Architect Agent"
            df.loc[mask, "operations_seen"] = "No"
            df.loc[mask, "operations_seen_at"] = ""
            df.loc[mask, "last_updated_by"] = safe_text(client_account.get("client_name"), "Client")
            df.loc[mask, "last_updated_role"] = "Client"
            df.loc[mask, "last_updated_at"] = now
            df.loc[mask, "last_update_summary"] = "Client submitted detailed requirement. Technical Architect Agent created delivery plan and weekly targets."
            upsert_current_proposal_from_df(df, mask)
    except Exception:
        pass
    append_proposal_history(
        report.get("proposal_id"),
        {"user_id": safe_text(client_account.get("client_user_id")), "employee_name": safe_text(client_account.get("client_name")), "designation": "Client"},
        "Detailed Requirement Submitted",
        summary="Client submitted detailed requirement; Technical Architect Agent created delivery plan and weekly targets.",
    )
    append_proposal_history(
        report.get("proposal_id"),
        {"user_id": "SYSTEM", "employee_name": "Technical Architect Agent", "designation": "System"},
        "Weekly Targets Created",
        comment=weekly_targets,
        summary="Weekly delivery targets were fixed and shared with the delivery requirement plan.",
    )
    return True, "Detailed requirement submitted. Technical Architect Agent has created the delivery plan and weekly targets for the project team."


try:
    _mandatory_original_render_employee_project_workbench = render_employee_project_workbench
except Exception:
    _mandatory_original_render_employee_project_workbench = None


def _employee_missing_weekly_updates(employee_id):
    allocations = get_employee_allocations(employee_id)
    if allocations is None or allocations.empty:
        return []
    current_week = current_week_label()
    missing = []
    for _, alloc in allocations.iterrows():
        project_id = safe_text(alloc.get("project_id"))
        updates = get_employee_project_updates(project_id=project_id, employee_id=employee_id)
        has_update = False
        if updates is not None and not updates.empty and "week_label" in updates.columns:
            has_update = any(updates["week_label"].astype(str) == current_week)
        if not has_update:
            missing.append({
                "project_id": project_id,
                "project": project_display_name(project_id=project_id, fallback=project_id or "Project"),
                "role": safe_text(alloc.get("project_role")),
                "module": safe_text(alloc.get("assigned_module")),
            })
    return missing


def render_employee_project_workbench(user):
    emp_id = safe_text(user.get("user_id")).upper()
    missing = _employee_missing_weekly_updates(emp_id)
    if missing:
        st.error(
            f"Mandatory weekly update pending: you have {len(missing)} assigned project(s) without this week's update. "
            "Please submit the weekly progress, blockers, support needs, and notes before continuing delivery work."
        )
        with st.expander("Projects missing this week's update", expanded=True):
            st.dataframe(pd.DataFrame(missing), use_container_width=True, hide_index=True)
    if _mandatory_original_render_employee_project_workbench is not None:
        _mandatory_original_render_employee_project_workbench(user)
    else:
        st.warning("Employee project workbench is unavailable.")


try:
    _weekly_original_generate_weekly_update_if_needed = generate_weekly_update_if_needed
except Exception:
    _weekly_original_generate_weekly_update_if_needed = None


def generate_weekly_update_if_needed(project, delivery_plan, allocations):
    # Keep client-safe weekly status generation, but include internal target context
    # in the source record for executives/project team. The client-facing text still
    # avoids salary, margin, employee names, and private blockers.
    return _weekly_original_generate_weekly_update_if_needed(project, delivery_plan, allocations) if _weekly_original_generate_weekly_update_if_needed else {}

# ---------------- V44 SMALL IMPROVEMENT PATCH: INTERNAL HIRING, ALLOCATION FILTER, CLIENT TARGETS ----------------
# Late overrides only. This keeps the working build intact and adds:
# 1) internal hiring-necessity column at CEO approval,
# 2) project allocation restricted to non-executive delivery employees,
# 3) clean client-input storage,
# 4) client/operations/CEO weekly target list with visible week numbers.

INTERNAL_HIRING_COLUMNS = [
    "hiring_necessary",
    "hiring_necessity_basis",
]
try:
    insert_after = "hiring_recommendation" if "hiring_recommendation" in PROPOSAL_DECISION_COLUMNS else "total_skill_gap"
    insert_at = PROPOSAL_DECISION_COLUMNS.index(insert_after) + 1 if insert_after in PROPOSAL_DECISION_COLUMNS else len(PROPOSAL_DECISION_COLUMNS)
    for _col in INTERNAL_HIRING_COLUMNS:
        if _col not in PROPOSAL_DECISION_COLUMNS:
            PROPOSAL_DECISION_COLUMNS.insert(insert_at, _col)
            insert_at += 1
except Exception:
    pass

EXCLUDED_PROJECT_ALLOCATION_SKILLS = [
    "Project Management",
    "HR Operations",
    "Financial Planning",
    "Enterprise Sales",
    "Business Strategy",
]

EXCLUDED_PROJECT_ALLOCATION_ALIASES = [
    "project manager",
    "project management",
    "hr operations",
    "human resource operations",
    "financial planning",
    "finance planning",
    "enterprise sales",
    "sales strategy",
    "business strategy",
    "strategy planning",
]


def clean_ai_frontdesk_client_input(raw_text):
    """Keep stored client input limited to the client's own requirement details."""
    text_value = safe_text(raw_text).strip()
    if not text_value:
        return ""
    cleaned_lines = []
    for line in text_value.splitlines():
        line_text = safe_text(line).strip()
        if not line_text:
            continue
        lower = line_text.lower()
        if lower.startswith("ai front desk:") or lower.startswith("receptionist:"):
            # Remove any accidental assistant prefix if the text was pasted back.
            line_text = re.sub(r"^\s*(ai\s+front\s+desk|receptionist)\s*:\s*", "", line_text, flags=re.IGNORECASE).strip()
        if not line_text:
            continue
        if line_text.lower().startswith("welcome to virtual tech ai"):
            continue
        cleaned_lines.append(line_text)
    cleaned = "\n".join(cleaned_lines).strip()
    return cleaned or text_value


def _derive_internal_hiring_status(analysis):
    """Return internal yes/no hiring flag plus basis. This is never client-visible."""
    analysis = analysis or {}
    hiring_fte = safe_number(analysis.get("total_hiring_needed_fte"), 0)
    projected_gap = safe_number(analysis.get("total_skill_gap"), 0)
    immediate_gap = safe_number(analysis.get("immediate_skill_gap"), 0)
    recommendation = safe_text(analysis.get("hiring_recommendation"))
    timeline_risk = safe_text(analysis.get("timeline_risk"))

    recommendation_lower = recommendation.lower()
    explicit_no = any(phrase in recommendation_lower for phrase in [
        "no hiring",
        "hiring is not",
        "not required",
        "not necessary",
        "rebalance",
        "release planning",
    ])
    explicit_yes = any(phrase in recommendation_lower for phrase in [
        "hiring/contract support recommended",
        "hiring recommended",
        "hire",
        "contract support recommended",
        "contractor",
    ])

    material_hiring_need = (hiring_fte >= 0.50) or (projected_gap >= 1.00 and immediate_gap >= 0.50) or explicit_yes
    if explicit_no and hiring_fte < 0.75:
        material_hiring_need = False

    status = "Yes" if material_hiring_need else "No"
    if status == "Yes":
        basis = (
            f"Hiring/contract support is recommended internally. Hiring FTE: {round(hiring_fte, 2)}, "
            f"projected gap: {round(projected_gap, 2)} FTE, immediate gap: {round(immediate_gap, 2)} FTE, "
            f"timeline risk: {timeline_risk or 'Not captured'}. {recommendation}"
        ).strip()
    else:
        basis = (
            f"No separate hiring is necessary at approval time. Use current employees, release planning, or allocation rebalance. "
            f"Hiring FTE: {round(hiring_fte, 2)}, projected gap: {round(projected_gap, 2)} FTE, "
            f"immediate gap: {round(immediate_gap, 2)} FTE, timeline risk: {timeline_risk or 'Not captured'}. {recommendation}"
        ).strip()
    return status, basis


def _enrich_analysis_with_internal_hiring(analysis):
    enriched = dict(analysis or {})
    status, basis = _derive_internal_hiring_status(enriched)
    enriched["hiring_necessary"] = status
    enriched["hiring_necessity_basis"] = basis
    return enriched


def _update_proposal_internal_hiring_columns(proposal_id, analysis=None):
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
        if analysis is None:
            report = proposal_row_to_report(df.loc[mask].iloc[0])
            analysis = report.get("analysis", {})
        status, basis = _derive_internal_hiring_status(analysis)
        df.loc[mask, "hiring_necessary"] = status
        df.loc[mask, "hiring_necessity_basis"] = basis
        upsert_current_proposal_from_df(df, mask)
        return True
    except Exception:
        return False


try:
    _v44_original_run_external_client_decision = run_external_client_decision
except Exception:
    _v44_original_run_external_client_decision = None


def run_external_client_decision(query, data):
    analysis = _v44_original_run_external_client_decision(query, data) if _v44_original_run_external_client_decision else {}
    return _enrich_analysis_with_internal_hiring(analysis)


try:
    _v44_original_save_external_client_report_to_excel = save_external_client_report_to_excel
except Exception:
    _v44_original_save_external_client_report_to_excel = None


def save_external_client_report_to_excel(raw_client_message, analysis):
    clean_message = clean_ai_frontdesk_client_input(raw_client_message)
    enriched_analysis = _enrich_analysis_with_internal_hiring(analysis)
    if _v44_original_save_external_client_report_to_excel is None:
        raise RuntimeError("Proposal save function is unavailable.")
    proposal_id = _v44_original_save_external_client_report_to_excel(clean_message, enriched_analysis)
    _update_proposal_internal_hiring_columns(proposal_id, enriched_analysis)
    return proposal_id


try:
    _v44_original_save_latest_external_client_report = save_latest_external_client_report
except Exception:
    _v44_original_save_latest_external_client_report = None


def save_latest_external_client_report(raw_client_message, analysis):
    clean_message = clean_ai_frontdesk_client_input(raw_client_message)
    enriched_analysis = _enrich_analysis_with_internal_hiring(analysis)
    if _v44_original_save_latest_external_client_report is None:
        raise RuntimeError("Latest proposal save function is unavailable.")
    return _v44_original_save_latest_external_client_report(clean_message, enriched_analysis)


try:
    _v44_original_proposal_row_to_report = proposal_row_to_report
except Exception:
    _v44_original_proposal_row_to_report = None


def proposal_row_to_report(row):
    report = _v44_original_proposal_row_to_report(row) if _v44_original_proposal_row_to_report is not None else {}
    if hasattr(row, "to_dict"):
        row_dict = row.to_dict()
    elif isinstance(row, dict):
        row_dict = row
    else:
        row_dict = {}
    analysis = report.setdefault("analysis", {})
    saved_status = safe_text(row_dict.get("hiring_necessary"))
    saved_basis = safe_text(row_dict.get("hiring_necessity_basis"))
    if saved_status:
        analysis["hiring_necessary"] = saved_status
        analysis["hiring_necessity_basis"] = saved_basis
    else:
        status, basis = _derive_internal_hiring_status(analysis)
        analysis["hiring_necessary"] = status
        analysis["hiring_necessity_basis"] = basis
    return report


try:
    _v44_original_submit_proposal_decision = submit_proposal_decision
except Exception:
    _v44_original_submit_proposal_decision = None


def submit_proposal_decision(proposal_id, user, decision, comment, recommended_quote, recommended_timeline_months):
    if _v44_original_submit_proposal_decision is None:
        return False, "Decision function is unavailable."
    success, message = _v44_original_submit_proposal_decision(
        proposal_id,
        user,
        decision,
        comment,
        recommended_quote,
        recommended_timeline_months,
    )
    if success and role_key_for_user(user) == "ceo":
        try:
            report = get_proposal_report_by_id(proposal_id)
            analysis = report.get("analysis", {}) if report else None
            _update_proposal_internal_hiring_columns(proposal_id, analysis)
            append_proposal_history(
                proposal_id,
                user,
                "Internal Hiring Necessity Captured",
                decision=safe_text((analysis or {}).get("hiring_necessary")),
                comment=safe_text((analysis or {}).get("hiring_necessity_basis")),
                summary="CEO approval captured the internal hiring-necessary column. This is hidden from the client portal.",
            )
        except Exception:
            pass
    return success, message


try:
    _v44_original_render_agentic_decision_pack = render_agentic_decision_pack
except Exception:
    _v44_original_render_agentic_decision_pack = None


def render_agentic_decision_pack(report):
    if _v44_original_render_agentic_decision_pack is not None:
        _v44_original_render_agentic_decision_pack(report)
    analysis = report.get("analysis", {}) if isinstance(report, dict) else {}
    status, basis = _derive_internal_hiring_status(analysis)
    with st.expander("Internal hiring necessity - executives only", expanded=False):
        c1, c2, c3 = st.columns(3)
        c1.metric("Hiring necessary", status)
        c2.metric("Hiring FTE", f"{safe_number(analysis.get('total_hiring_needed_fte'), 0)}")
        c3.metric("Projected gap", f"{safe_number(analysis.get('total_skill_gap'), 0)} FTE")
        st.write(basis)
        st.caption("Internal only. This hiring decision column is saved for executives and is not shown in the client portal or client quotation.")


def _row_has_blocked_allocation_skill(row):
    if row is None:
        return False
    if hasattr(row, "to_dict"):
        row = row.to_dict()
    fields = []
    for key in [
        "primary_skill",
        "skill",
        "skills",
        "domain",
        "department",
        "designation",
        "employee_designation",
        "project_role",
        "assigned_module",
        "responsibility_summary",
    ]:
        fields.append(safe_text(row.get(key)))
    combined = " | ".join(fields).lower()
    return any(alias in combined for alias in EXCLUDED_PROJECT_ALLOCATION_ALIASES)


def _executive_user_ids_from_data(data):
    ids = set()
    try:
        users = (data or {}).get("users", pd.DataFrame()) if isinstance(data, dict) else pd.DataFrame()
    except Exception:
        users = pd.DataFrame()
    if users is None or users.empty:
        return ids
    for _, row in users.iterrows():
        role = safe_text(row.get("role")).lower()
        designation = safe_text(row.get("designation")).lower()
        department = safe_text(row.get("department")).lower()
        user_id = safe_text(row.get("user_id") or row.get("employee_id")).upper()
        is_exec = (
            role in ["executive", "founder", "ceo"]
            or "executive" in designation
            or "ceo" in designation
            or "founder" in designation
            or "manager" in designation and any(word in department for word in ["sales", "finance", "hr", "business", "strategy"])
        )
        if is_exec and user_id:
            ids.add(user_id)
    return ids


def filter_project_delivery_employees(employees, data=None):
    """Allow only delivery employees in project allocation, excluding executives and business-support skills."""
    if employees is None or getattr(employees, "empty", True):
        return employees
    executive_ids = _executive_user_ids_from_data(data)
    allowed_rows = []
    for _, row in employees.iterrows():
        row_dict = row.to_dict()
        emp_id = safe_text(row_dict.get("employee_id") or row_dict.get("user_id")).upper()
        role_value = safe_text(row_dict.get("role")).lower()
        designation = safe_text(row_dict.get("designation") or row_dict.get("employee_designation")).lower()
        if emp_id and emp_id in executive_ids:
            continue
        if role_value in ["executive", "founder", "ceo"]:
            continue
        if "executive" in designation or "ceo" in designation or "founder" in designation:
            continue
        if _row_has_blocked_allocation_skill(row_dict):
            continue
        allowed_rows.append(row_dict)
    return pd.DataFrame(allowed_rows, columns=list(employees.columns)) if allowed_rows else employees.iloc[0:0].copy()


try:
    _v44_original_approve_delivery_plan_and_allocate = approve_delivery_plan_and_allocate
except Exception:
    _v44_original_approve_delivery_plan_and_allocate = None


def approve_delivery_plan_and_allocate(project, plan, user, manager_plan_text, selected_rows):
    if _v44_original_approve_delivery_plan_and_allocate is None:
        return False, "Allocation function is unavailable."
    cleaned_rows = []
    blocked_count = 0
    for item in selected_rows or []:
        if _row_has_blocked_allocation_skill(item):
            blocked_count += 1
            continue
        designation = safe_text(item.get("designation") or item.get("employee_designation") or item.get("project_role")).lower()
        department = safe_text(item.get("department") or item.get("employee_department")).lower()
        if "executive" in designation or "ceo" in designation or "founder" in designation:
            blocked_count += 1
            continue
        if any(word in department for word in ["sales", "finance", "hr", "strategy"]) and any(word in designation for word in ["manager", "executive", "lead"]):
            blocked_count += 1
            continue
        cleaned_rows.append(item)
    if not cleaned_rows:
        return False, (
            "Select at least one delivery employee. Executives and the skills Project Management, HR Operations, "
            "Financial Planning, Enterprise Sales, and Business Strategy cannot be allocated to project delivery work."
        )
    ok, msg = _v44_original_approve_delivery_plan_and_allocate(project, plan, user, manager_plan_text, cleaned_rows)
    if ok and blocked_count:
        msg += f" {blocked_count} blocked executive/business-support allocation(s) were skipped."
    return ok, msg


def weekly_targets_text_from_plan(plan):
    if not isinstance(plan, dict):
        return ""
    for key in ["weekly_targets", "module_breakdown", "operations_agent_plan", "operations_manager_plan"]:
        value = safe_text(plan.get(key)).strip()
        if "Week 1" in value or "Weekly Delivery Targets" in value:
            return value
    return safe_text(plan.get("weekly_targets"))


def parse_weekly_targets_to_rows(target_text):
    rows = []
    for line in safe_text(target_text).splitlines():
        item = line.strip().lstrip("-*").strip()
        if not item:
            continue
        match = re.match(r"^Week\s*(\d+)\s*[:\-]\s*(.+)$", item, flags=re.IGNORECASE)
        if match:
            week_no = safe_int(match.group(1), 0)
            target = match.group(2).strip()
            rows.append({
                "Week Number": f"Week {week_no}",
                "Target": target,
            })
    return rows


def render_weekly_targets_panel(plan, *, title="Weekly target list", expanded=True, client_safe=True, key_prefix="weekly_targets"):
    text_value = weekly_targets_text_from_plan(plan)
    rows = parse_weekly_targets_to_rows(text_value)
    if not rows:
        return False
    with st.expander(title, expanded=expanded):
        if client_safe:
            st.caption("Client-safe weekly targets only. Internal cost, margin, salary, employee names, blockers, and hiring details are hidden.")
        else:
            st.caption("Weekly targets fixed by the Technical Architect Agent after quotation acceptance and detailed requirement submission.")
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    return True


def render_weekly_targets_overview(focus_proposal_id=None, *, title="Weekly target list", expanded=False, client_safe=False, key_prefix="weekly_targets_overview"):
    try:
        plans = read_simple_table("delivery_plans", DELIVERY_PLAN_COLUMNS)
    except Exception:
        plans = pd.DataFrame(columns=DELIVERY_PLAN_COLUMNS)
    if plans is None or plans.empty:
        return False
    working = plans.copy()
    if focus_proposal_id and "proposal_id" in working.columns:
        working = working[working["proposal_id"].astype(str) == safe_text(focus_proposal_id)]
    if working.empty:
        return False
    if "created_at" in working.columns:
        working = working.sort_values("created_at", ascending=False)

    if len(working) == 1:
        return render_weekly_targets_panel(
            working.iloc[0].to_dict(),
            title=title,
            expanded=expanded,
            client_safe=client_safe,
            key_prefix=key_prefix,
        )

    with st.expander(title, expanded=expanded):
        labels = []
        rows = []
        for idx, (_, plan_row) in enumerate(working.iterrows(), start=1):
            project_label = project_display_name(project_id=plan_row.get("project_id"), proposal_id=plan_row.get("proposal_id"), fallback="Project")
            labels.append(f"{idx}. {project_label} | {safe_text(plan_row.get('approval_status')) or 'Targets'}")
            rows.append(plan_row.to_dict())
        selected = st.selectbox("Choose project weekly target list", labels, key=f"{key_prefix}_{safe_text(focus_proposal_id) or 'all'}")
        plan = rows[labels.index(selected)]
        inner_rows = parse_weekly_targets_to_rows(weekly_targets_text_from_plan(plan))
        if inner_rows:
            st.dataframe(pd.DataFrame(inner_rows), use_container_width=True, hide_index=True)
        else:
            st.info("Weekly targets are not available for the selected project yet.")
    return True


try:
    _v44_original_render_client_delivery_section = render_client_delivery_section
except Exception:
    _v44_original_render_client_delivery_section = None


def render_client_delivery_section(report, client_account):
    if _v44_original_render_client_delivery_section is not None:
        _v44_original_render_client_delivery_section(report, client_account)
    if safe_text(report.get("client_response")) != "Accept Proposal":
        return
    try:
        project = get_project_for_proposal(report.get("proposal_id"))
        if not project:
            return
        plan = get_delivery_plan_for_client_project(project.get("project_id"))
        if plan:
            render_weekly_targets_panel(
                plan,
                title="Weekly target list shared by Virtual Tech AI",
                expanded=True,
                client_safe=True,
                key_prefix=f"client_weekly_targets_{safe_text(project.get('project_id'))}",
            )
    except Exception:
        pass


try:
    _v44_original_render_operations_delivery_workspace = render_operations_delivery_workspace
except Exception:
    _v44_original_render_operations_delivery_workspace = None


def render_operations_delivery_workspace(user, data, focus_proposal_id=None):
    filtered_data = dict(data or {}) if isinstance(data, dict) else {}
    try:
        filtered_data["employees"] = filter_project_delivery_employees(filtered_data.get("employees", pd.DataFrame()), filtered_data)
    except Exception:
        pass
    if _v44_original_render_operations_delivery_workspace is not None:
        _v44_original_render_operations_delivery_workspace(user, filtered_data, focus_proposal_id=focus_proposal_id)
    render_weekly_targets_overview(
        focus_proposal_id,
        title="Weekly target list - Technical Architect / Operations dashboard",
        expanded=bool(focus_proposal_id),
        client_safe=False,
        key_prefix="ops_weekly_targets",
    )


try:
    _v44_original_render_ceo_project_lifecycle_dashboard = render_ceo_project_lifecycle_dashboard
except Exception:
    _v44_original_render_ceo_project_lifecycle_dashboard = None


def render_ceo_project_lifecycle_dashboard(report, user=None, data=None):
    if _v44_original_render_ceo_project_lifecycle_dashboard is not None:
        _v44_original_render_ceo_project_lifecycle_dashboard(report, user=user, data=data)
    try:
        project = get_project_for_proposal(report.get("proposal_id"))
        if not project:
            return
        plan = get_delivery_plan_for_client_project(project.get("project_id"))
        if plan:
            render_weekly_targets_panel(
                plan,
                title="Weekly target list - CEO dashboard",
                expanded=False,
                client_safe=False,
                key_prefix=f"ceo_weekly_targets_{safe_text(project.get('project_id'))}",
            )
    except Exception:
        pass



# ---------------- V43 READABILITY PATCH: PROJECT WEEK + TECH ARCHITECT KEY/VALUE BASIS ----------------
# Late helper functions used by the patched client progress panel and executive agentic analysis.

def _dd_html_escape(value):
    text_value = safe_text(value)
    return (
        text_value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def _dd_parse_datetime(value):
    try:
        parsed = pd.to_datetime(safe_text(value), errors="coerce")
        if pd.isna(parsed):
            return None
        if getattr(parsed, "tzinfo", None) is not None:
            parsed = parsed.tz_localize(None)
        return parsed.to_pydatetime()
    except Exception:
        return None


def _dd_project_allocation_start_date(project_id):
    project_id = safe_text(project_id)
    date_values = []
    try:
        allocations = get_project_allocations(project_id)
        if allocations is not None and not allocations.empty:
            for _, alloc in allocations.iterrows():
                for col in ["start_date", "assigned_at", "created_at"]:
                    parsed = _dd_parse_datetime(alloc.get(col))
                    if parsed:
                        date_values.append(parsed)
    except Exception:
        pass
    try:
        projects = read_simple_table("projects", PROJECT_COLUMNS)
        if projects is not None and not projects.empty and "project_id" in projects.columns:
            match = projects[projects["project_id"].astype(str) == project_id]
            if not match.empty:
                project = match.iloc[0]
                for col in ["kickoff_date", "created_at", "updated_at"]:
                    parsed = _dd_parse_datetime(project.get(col))
                    if parsed:
                        date_values.append(parsed)
    except Exception:
        pass
    return min(date_values) if date_values else None


def get_project_week_info(project_id, reference_date=""):
    """Calculate project week from the first allocation/start date.

    The client and executive dashboards use this to show a readable Week N value
    beside the latest weekly delivery update. If the latest employee update time
    is supplied, that update is mapped to its project week; otherwise current date
    is used.
    """
    start_dt = _dd_project_allocation_start_date(project_id)
    ref_dt = _dd_parse_datetime(reference_date) or datetime.now()
    if not start_dt:
        return {
            "week_number": 1,
            "week_label": "Week 1",
            "latest_update_week_number": 1,
            "latest_update_week_label": "Week 1",
            "start_label": "not captured",
        }
    days = max(0, (ref_dt.date() - start_dt.date()).days)
    week_number = max(1, int(days // 7) + 1)
    current_days = max(0, (datetime.now().date() - start_dt.date()).days)
    current_week = max(1, int(current_days // 7) + 1)
    return {
        "week_number": current_week,
        "week_label": f"Week {current_week}",
        "latest_update_week_number": week_number,
        "latest_update_week_label": f"Week {week_number}",
        "start_label": start_dt.strftime("%Y-%m-%d"),
    }


def _dd_sentence_list(values, empty_text="To be finalized in detailed requirement stage"):
    if isinstance(values, str):
        values = [values]
    clean = [safe_text(item).strip() for item in (values or []) if safe_text(item).strip()]
    if not clean:
        return empty_text
    return ", ".join(clean) + "."


def _dd_stack_line(stack, key, label):
    return label, _dd_sentence_list(stack.get(key) if isinstance(stack, dict) else [])


def _dd_architect_key_value_rows(analysis, summaries=None):
    summaries = summaries or {}
    stack = analysis.get("technical_architect_stack") or {}
    if isinstance(stack, str):
        stack = decode_json(stack, {})
    req_profile = analysis.get("technical_architect_requirement") or {}
    if isinstance(req_profile, str):
        req_profile = decode_json(req_profile, {})
    derived_summary = safe_text(req_profile.get("derived_summary") if isinstance(req_profile, dict) else "") or safe_text(analysis.get("initial_requirement_summary"))
    modules = req_profile.get("modules", []) if isinstance(req_profile, dict) else []
    roles = req_profile.get("user_roles", []) if isinstance(req_profile, dict) else []
    integrations = req_profile.get("integrations", []) if isinstance(req_profile, dict) else []
    unknowns = req_profile.get("unknowns_for_detailed_requirement", []) if isinstance(req_profile, dict) else []

    rows = []
    rows.append(("Derived requirement", derived_summary or "Initial requirement summary is not available."))
    if modules:
        rows.append(("Modules / features", _dd_sentence_list(modules)))
    if roles:
        rows.append(("User roles", _dd_sentence_list(roles)))
    if integrations:
        rows.append(("Likely integrations", _dd_sentence_list(integrations)))
    for key, label in [
        ("frontend", "Frontend"),
        ("backend", "Backend"),
        ("database", "Database"),
        ("ai_layer", "AI layer"),
        ("storage", "Storage"),
        ("integrations", "Integration stack"),
        ("cloud_devops", "Cloud / DevOps"),
        ("security", "Security"),
        ("testing", "Testing"),
    ]:
        if stack:
            rows.append(_dd_stack_line(stack, key, label))
    rows.append(("Realistic timeline", f"{safe_int(analysis.get('timeline_months'), 0)} month(s)."))
    rows.append(("Client requested timeline", f"{safe_int(analysis.get('client_requested_timeline_months') or analysis.get('original_timeline_months') or analysis.get('timeline_months'), 0)} month(s)."))
    rows.append(("Scope complexity", safe_text(analysis.get("scope_complexity"), "Not captured") + "."))
    rows.append(("Timeline risk", safe_text(analysis.get("timeline_risk"), "Not captured") + "."))
    rows.append(("Pending workload considered", f"{safe_number(analysis.get('total_active_allocated_fte'), 0):.2f} FTE active pending load was considered."))
    rows.append(("Open blockers / support requests", f"{safe_int(analysis.get('dynamic_hurdle_count'), 0)} open blocker/support request(s) were considered."))
    if unknowns:
        rows.append(("To confirm after acceptance", _dd_sentence_list(unknowns)))
    if analysis.get("technical_architect_timeline_basis"):
        rows.append(("Timeline basis", safe_text(analysis.get("technical_architect_timeline_basis"))))
    return rows


def render_technical_architect_basis_key_value(analysis, summaries=None):
    rows = _dd_architect_key_value_rows(analysis or {}, summaries or {})
    html_rows = []
    for key, value in rows:
        html_rows.append(
            "<div class='dd-kv-row'>"
            f"<div class='dd-kv-key'>{_dd_html_escape(key)}</div>"
            f"<div class='dd-kv-value'>{_dd_html_escape(value)}</div>"
            "</div>"
        )
    st.markdown(
        """
        <style>
            .dd-kv-panel {
                background: #ffffff;
                border: 1px solid #dbe4f0;
                border-radius: 18px;
                padding: 14px 16px;
                margin: 8px 0 14px 0;
                box-shadow: 0 8px 22px rgba(15, 23, 42, 0.035);
            }
            .dd-kv-row {
                display: grid;
                grid-template-columns: 230px 1fr;
                gap: 12px;
                padding: 9px 0;
                border-bottom: 1px solid #eef2f7;
                align-items: start;
            }
            .dd-kv-row:last-child { border-bottom: 0; }
            .dd-kv-key {
                font-weight: 900;
                color: #0f172a;
            }
            .dd-kv-value {
                color: #334155;
                line-height: 1.45;
            }
            @media (max-width: 760px) {
                .dd-kv-row { grid-template-columns: 1fr; gap: 4px; }
            }
        </style>
        """ + "<div class='dd-kv-panel'>" + "".join(html_rows) + "</div>",
        unsafe_allow_html=True,
    )

# ---------------- V45 PATCH: CEO HIRING CONTROL + SMART AI FRONT DESK ----------------
# Late overrides so the latest working build stays intact.
# Adds a visible CEO-only internal hiring decision field, hides logged-in static
# AI Front Desk helper content via runtime patch, and makes AI Front Desk use a
# prompt-based meaning classifier before deterministic fallbacks.

FRONTDESK_COMPANY_FACTS = (
    "Virtual Tech AI is a Bangalore-based company that provides AI and data solutions. "
    "We help clients with AI assistants, data platforms, dashboards, automation, cloud deployment, "
    "and secure role-based business applications."
)


def _frontdesk_json_loads(value, default=None):
    if default is None:
        default = {}
    text_value = safe_text(value).strip()
    if not text_value:
        return default
    try:
        return json.loads(text_value)
    except Exception:
        pass
    # LLMs may wrap JSON in short prose or markdown. Extract the first object.
    match = re.search(r"\{.*\}", text_value, flags=re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except Exception:
            return default
    return default


def _frontdesk_local_semantic_fallback(query, user=None):
    """Local fallback used only if the LLM classifier is unavailable."""
    q = safe_text(query).strip().lower()
    clean_q = re.sub(r"[^a-z0-9\s]", " ", q)
    clean_q = re.sub(r"\s+", " ", clean_q).strip()

    if is_simple_greeting_query(query):
        return {"intent": "greeting", "agent": "AI Front Desk", "confidence": 1.0, "needs_login": False}

    asks_company_identity = (
        any(phrase in clean_q for phrase in [
            "about this company", "about your company", "about virtual tech", "who are you", "what is virtual tech",
            "tell me about company", "tell me about this company", "company details", "what does this company do",
        ])
        and not any(word in clean_q for word in ["performance", "report", "profit", "revenue", "margin", "health", "financial"])
    )
    if asks_company_identity:
        return {"intent": "company_identity", "agent": "AI Front Desk", "confidence": 0.95, "needs_login": False}

    asks_company_performance = any(phrase in clean_q for phrase in [
        "company performance", "performance report", "company report", "company health", "business performance",
        "revenue", "profit", "margin", "financial performance",
    ])
    if asks_company_performance:
        return {"intent": "company_performance", "agent": "CEO Agent", "confidence": 0.90, "needs_login": True}

    if any(phrase in clean_q for phrase in ["reporting manager", "my manager", "manager name", "who do i report"]):
        return {"intent": "reporting_manager", "agent": "HR Agent", "confidence": 0.92, "needs_login": True}

    if any(phrase in clean_q for phrase in ["apply for leave", "leave application", "request leave", "take leave", "leave process", "leave policy"]):
        return {"intent": "leave_help", "agent": "HR Agent", "confidence": 0.90, "needs_login": True}

    if any(phrase in clean_q for phrase in ["salary less", "salary lower", "less salary", "low salary", "why is my salary", "salary deducted"]):
        return {"intent": "salary_discrepancy", "agent": "Finance Agent", "confidence": 0.90, "needs_login": True}

    if any(phrase in clean_q for phrase in ["my salary", "salary", "in hand", "inhand", "pay credited", "salary credited", "ctc"]):
        return {"intent": "salary_info", "agent": "Finance Agent", "confidence": 0.86, "needs_login": True}

    if user is None and (
        is_project_proposal_query(query)
        or any(word in clean_q for word in ["budget", "timeline", "requirement", "project", "software", "chatbot", "pipeline", "dashboard"])
    ):
        return {"intent": "project_intake", "agent": "Sales Agent", "confidence": 0.84, "needs_login": False}

    return {"intent": "general", "agent": "AI Front Desk", "confidence": 0.50, "needs_login": False}


def frontdesk_understand_meaning(query, user=None):
    """Use an LLM prompt to understand the user's meaning before routing.

    The intent list intentionally separates company identity questions from
    company performance reports so questions like "tell me about this company"
    are answered directly instead of being blocked as CEO-only reports.
    """
    fallback_obj = _frontdesk_local_semantic_fallback(query, user)
    fallback = json.dumps(fallback_obj, ensure_ascii=False)
    user_context = {
        "logged_in": bool(user),
        "role": safe_text((user or {}).get("role")),
        "department": safe_text((user or {}).get("department")),
        "designation": safe_text((user or {}).get("designation")),
    }
    prompt = f"""
You are LifecycleDesk AI's AI Front Desk for Virtual Tech AI.
Understand the user's meaning, not just keywords. Return only valid JSON.

Company identity to use for general company questions:
{FRONTDESK_COMPANY_FACTS}

Allowed intents:
- greeting: simple hello/thanks
- company_identity: asking who/what Virtual Tech AI is, where it is located, or what the company provides
- company_performance: asking internal performance, revenue, profit, margins, business health, company report, or financial report
- reporting_manager: asking who the user's manager/reporting manager is
- leave_help: asking how to apply for leave or leave process
- salary_info: asking own salary, in-hand, CTC, salary date/credited status
- salary_discrepancy: asking why salary is lower/deducted/less
- project_intake: client/new project requirement, budget, timeline, proposal, software solution, AI/data solution enquiry
- route_hr: other HR employee help
- route_finance: other finance/payroll help
- route_sales: sales/client/proposal help
- route_architect: delivery/technical/project execution help
- route_ceo: CEO-only strategic internal request
- general: normal small question that can be answered safely by AI Front Desk

Important distinctions:
- "tell me about this company" means company_identity, not company_performance.
- "show company performance" or "company performance report" means company_performance.
- For internal personal data such as salary or manager, needs_login must be true.

Return JSON with keys:
intent, agent, confidence, needs_login, direct_answer.
Use agent values: AI Front Desk, HR Agent, Finance Agent, Sales Agent, Technical Architect Agent, CEO Agent.
For company_identity, direct_answer should be a short helpful answer using the company identity above.
For leave_help, direct_answer may explain the leave process in a general way.

User context:
{json.dumps(user_context, ensure_ascii=False)}

User message:
{safe_text(query)}
"""
    try:
        raw = ask_llm(prompt, fallback=fallback)
        parsed = _frontdesk_json_loads(raw, fallback_obj)
        if not isinstance(parsed, dict):
            parsed = fallback_obj
    except Exception:
        parsed = fallback_obj

    # Normalize so downstream code is safe.
    parsed["intent"] = safe_text(parsed.get("intent") or fallback_obj.get("intent") or "general")

    # Safety net for frequent employee questions: the LLM is primary, but if it
    # returns a broad route/general answer for a clearly personal HR/Finance
    # request, use the local semantic fallback so AI Front Desk answers fully.
    fallback_specific = safe_text(fallback_obj.get("intent"))
    if fallback_specific in [
        "company_identity", "company_performance", "reporting_manager",
        "leave_help", "salary_info", "salary_discrepancy"
    ] and parsed["intent"] not in [
        "company_identity", "company_performance", "reporting_manager",
        "leave_help", "salary_info", "salary_discrepancy"
    ]:
        parsed = dict(fallback_obj)
        parsed["intent"] = fallback_specific

    parsed["agent"] = safe_text(parsed.get("agent") or fallback_obj.get("agent") or "AI Front Desk")
    if parsed["agent"] == "Operations Agent":
        parsed["agent"] = "Technical Architect Agent"
    if parsed["agent"] == "Receptionist":
        parsed["agent"] = "AI Front Desk"
    parsed["confidence"] = safe_number(parsed.get("confidence"), safe_number(fallback_obj.get("confidence"), 0.5))
    parsed["needs_login"] = bool(parsed.get("needs_login", fallback_obj.get("needs_login", False)))
    parsed["direct_answer"] = safe_text(parsed.get("direct_answer"))
    return parsed


try:
    _v45_original_handle_receptionist_query = handle_receptionist_query
except Exception:
    _v45_original_handle_receptionist_query = None


def _frontdesk_login_required(agent, intent):
    return {
        "type": "login_required",
        "agent": agent,
        "intent": intent,
        "message": "AI Front Desk: Please login first so I can verify your access and answer this safely.",
    }


def _frontdesk_company_identity_answer():
    return (
        "AI Front Desk: Virtual Tech AI is a Bangalore-based company that provides AI and data solutions. "
        "We build AI assistants, data platforms, dashboards, automation workflows, cloud deployments, "
        "and secure role-based applications for clients."
    )


def _frontdesk_leave_answer(user):
    name = actor_name(user) if user else "there"
    return (
        f"AI Front Desk: {name}, for leave application you can share the leave dates, reason, and leave type with HR or your reporting manager. "
        "HR will validate the request against attendance/project needs and confirm approval. "
        "HR Agent will guide the leave request based on your role, reporting manager, and company policy access."
    )


def handle_receptionist_query(query, user, data):
    """Prompt-led AI Front Desk router with direct answers for common meaning-level questions."""
    understanding = frontdesk_understand_meaning(query, user)
    intent = safe_text(understanding.get("intent"), "general")
    agent = safe_text(understanding.get("agent"), "AI Front Desk")
    confidence = safe_number(understanding.get("confidence"), 0.0)

    if intent == "greeting":
        name = actor_name(user) if user else "there"
        return {
            "type": "general",
            "agent": "AI Front Desk",
            "intent": intent,
            "confidence": confidence,
            "message": f"AI Front Desk: Hello {name}. How can I help you today?",
        }

    if intent == "company_identity":
        answer = understanding.get("direct_answer") or _frontdesk_company_identity_answer()
        if not safe_text(answer).lower().startswith("ai front desk"):
            answer = "AI Front Desk: " + safe_text(answer)
        return {
            "type": "text",
            "agent": "AI Front Desk",
            "intent": intent,
            "confidence": confidence,
            "message": answer,
        }

    if intent == "company_performance":
        if user is None:
            return _frontdesk_login_required("CEO Agent", intent)
        if safe_text(user.get("role")).lower() == "founder":
            return {
                "type": "company_health",
                "agent": "CEO Agent",
                "intent": intent,
                "confidence": confidence,
                "message": "AI Front Desk: Connecting you to CEO Agent for company performance analysis.",
            }
        return {
            "type": "text",
            "agent": "CEO Agent",
            "intent": intent,
            "confidence": confidence,
            "message": "AI Front Desk: Company performance reports require Founder/CEO access.",
        }

    if intent == "reporting_manager":
        if user is None:
            return _frontdesk_login_required("HR Agent", intent)
        return {
            "type": "text",
            "agent": "HR Agent",
            "intent": intent,
            "confidence": confidence,
            "message": "AI Front Desk: I checked this through HR Agent.\n\n" + handle_hr_agent_query(query, user, data),
        }

    if intent == "leave_help":
        if user is None:
            return _frontdesk_login_required("HR Agent", intent)
        direct = safe_text(understanding.get("direct_answer")) or _frontdesk_leave_answer(user)
        if not direct.lower().startswith("ai front desk") and not direct.lower().startswith("hr agent"):
            direct = "AI Front Desk: " + direct
        return {
            "type": "text",
            "agent": "HR Agent",
            "intent": intent,
            "confidence": confidence,
            "message": direct,
        }

    if intent == "salary_info":
        if user is None:
            return _frontdesk_login_required("Finance Agent", intent)
        if is_role_salary_query(query):
            answer = answer_salary_by_role(query, user, data)
        else:
            answer = get_employee_salary_info(user, data)
        return {
            "type": "text",
            "agent": "Finance Agent",
            "intent": intent,
            "confidence": confidence,
            "message": "AI Front Desk: I checked this through Finance Agent.\n\n" + answer,
        }

    if intent == "salary_discrepancy":
        if user is None:
            return _frontdesk_login_required("Finance Agent", intent)
        return {
            "type": "text",
            "agent": "Finance Agent",
            "intent": intent,
            "confidence": confidence,
            "message": "AI Front Desk: I checked this through Finance Agent.\n\n" + explain_salary_difference(user, data),
        }

    if intent == "project_intake":
        if _v45_original_handle_receptionist_query is not None:
            return _v45_original_handle_receptionist_query(query, user, data)

    route_map = {
        "route_hr": "HR Agent",
        "route_finance": "Finance Agent",
        "route_sales": "Sales Agent",
        "route_architect": "Technical Architect Agent",
        "route_ceo": "CEO Agent",
    }
    if intent in route_map:
        mapped_agent = route_map[intent]
        if user is None and mapped_agent in ["HR Agent", "Finance Agent", "Technical Architect Agent", "CEO Agent"]:
            return _frontdesk_login_required(mapped_agent, intent)
        return {
            "type": "route_agent",
            "agent": mapped_agent,
            "intent": intent,
            "confidence": confidence,
            "message": f"AI Front Desk: Connecting you to {mapped_agent}.",
        }

    # For anything not confidently handled by the LLM classifier, keep the working
    # application behavior as a fallback.
    if _v45_original_handle_receptionist_query is not None:
        original = _v45_original_handle_receptionist_query(query, user, data)
        if isinstance(original, dict):
            original["message"] = safe_text(original.get("message")).replace("Receptionist:", "AI Front Desk:")
            if original.get("agent") == "Receptionist":
                original["agent"] = "AI Front Desk"
        return original

    return {
        "type": "text",
        "agent": "AI Front Desk",
        "intent": intent,
        "confidence": confidence,
        "message": "AI Front Desk: I can help with client project intake, HR, Finance, Technical Architect, Sales, or CEO requests. Please tell me what you need.",
    }


# --- CEO visible hiring decision field ---

def _save_ceo_manual_hiring_decision(proposal_id, user, hiring_status, hiring_note=""):
    proposal_id = safe_text(proposal_id).strip()
    hiring_status = safe_text(hiring_status).strip()
    if hiring_status not in ["Yes", "No"] or not proposal_id:
        return False
    try:
        df = read_proposal_store(create_if_missing=True)
        if df.empty or "proposal_id" not in df.columns:
            return False
        mask = df["proposal_id"].astype(str) == proposal_id
        if not mask.any():
            return False
        note = safe_text(hiring_note).strip()
        if not note:
            report = proposal_row_to_report(df.loc[mask].iloc[0])
            _, auto_basis = _derive_internal_hiring_status(report.get("analysis", {}))
            note = auto_basis
        df.loc[mask, "hiring_necessary"] = hiring_status
        df.loc[mask, "hiring_necessity_basis"] = note
        upsert_current_proposal_from_df(df, mask)
        append_proposal_history(
            proposal_id,
            user,
            "CEO Internal Hiring Decision",
            decision=hiring_status,
            comment=note,
            summary="CEO selected the internal hiring-necessary value. This is not visible to the client.",
        )
        return True
    except Exception:
        return False


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
            "Technical Architect Agent Delivery Opinion",
            "Comment only on delivery feasibility, timeline, blockers, and execution plan.",
        ),
        "ceo": (
            "CEO Final Decision",
            "Review every department opinion, approve the final quote/timeline, choose whether hiring is necessary internally, and generate the client quotation.",
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

    auto_hiring_status, auto_hiring_basis = _derive_internal_hiring_status(analysis)
    saved_hiring_status = safe_text(analysis.get("hiring_necessary")) or auto_hiring_status
    if saved_hiring_status not in ["Yes", "No"]:
        saved_hiring_status = auto_hiring_status

    ceo_hiring_status = ""
    ceo_hiring_note = ""

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
                with st.expander("Live HR/Technical Architect capacity reference", expanded=True):
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
            st.caption("Technical Architect view: delivery feasibility, timeline confidence, blockers, and execution plan.")
            comment = st.text_area(
                "Technical Architect opinion / delivery plan / blockers",
                value=existing.get("comment", ""),
                height=130,
                key=f"decision_comment_{proposal_id}_{role_key}",
            )
            recommended_quote = None
            recommended_timeline = st.number_input(
                "Technical Architect recommended delivery timeline (months)",
                min_value=1,
                value=max(1, int(default_timeline)),
                step=1,
                key=f"decision_timeline_{proposal_id}_{role_key}",
            )

        else:
            st.caption("CEO view: final business decision, final quote, final timeline, internal hiring necessity, and quotation generation.")
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

            st.markdown("#### Internal hiring decision")
            st.caption("CEO-only internal field. It is saved in proposal storage but hidden from the client portal and client quotation.")
            default_hiring_index = ["No", "Yes"].index(saved_hiring_status) if saved_hiring_status in ["No", "Yes"] else 0
            ceo_hiring_status = st.radio(
                "Is hiring or contract support necessary for this project?",
                ["No", "Yes"],
                index=default_hiring_index,
                horizontal=True,
                key=f"ceo_hiring_needed_{proposal_id}",
            )
            ceo_hiring_note = st.text_area(
                "Internal hiring basis / note for executives",
                value=safe_text(analysis.get("hiring_necessity_basis")) or auto_hiring_basis,
                height=100,
                key=f"ceo_hiring_basis_{proposal_id}",
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
            if role_key == "ceo":
                _save_ceo_manual_hiring_decision(proposal_id, user, ceo_hiring_status, ceo_hiring_note)
            st.success(message)
            try:
                request_page_scroll("selected_update_dashboard")
            except Exception:
                st.session_state["_dd_scroll_target"] = "selected_update_dashboard"
            st.rerun()
        else:
            st.error(message)


# ---------------- V46 PATCH: COMPACT FRONT DESK HISTORY + RELIABLE ROUTER + READABLE TABLES ----------------
# Late overrides only. Keeps the working v43/v45 logic intact, but makes the
# logged-in AI Front Desk compact, prompt-led, and easier to inspect in tables.


def render_ai_frontdesk_history_dropdown(messages):
    """Show logged-in AI Front Desk history as one compact dropdown, not a long scroll."""
    try:
        clean_messages = [m for m in (messages or []) if isinstance(m, dict) and safe_text(m.get("content")).strip()]
        if not clean_messages:
            return

        records = []
        i = 0
        while i < len(clean_messages):
            msg = clean_messages[i]
            if safe_text(msg.get("role")) == "user":
                user_text = safe_text(msg.get("content"))
                assistant_text = ""
                if i + 1 < len(clean_messages) and safe_text(clean_messages[i + 1].get("role")) == "assistant":
                    assistant_text = safe_text(clean_messages[i + 1].get("content"))
                    i += 2
                else:
                    i += 1
                records.append({"user": user_text, "assistant": assistant_text})
            else:
                records.append({"user": "", "assistant": safe_text(msg.get("content"))})
                i += 1

        if not records:
            return

        with st.container(border=True):
            st.caption("AI Front Desk conversation history is collapsed. Open only when you need to review an earlier exchange.")
            labels = []
            for idx, item in enumerate(records, start=1):
                preview = safe_text(item.get("user") or item.get("assistant"))
                preview = re.sub(r"\s+", " ", preview).strip()
                if len(preview) > 80:
                    preview = preview[:77] + "..."
                labels.append(f"{idx}. {preview or 'Previous AI Front Desk response'}")

            selected = st.selectbox(
                "Previous AI Front Desk messages",
                labels,
                key="logged_in_frontdesk_history_select",
            )
            selected_item = records[labels.index(selected)]
            if selected_item.get("user"):
                st.text_area(
                    "Your message",
                    value=safe_text(selected_item.get("user")),
                    height=90,
                    disabled=True,
                    key="logged_in_frontdesk_history_user",
                )
            if selected_item.get("assistant"):
                st.text_area(
                    "AI Front Desk response",
                    value=safe_text(selected_item.get("assistant")),
                    height=150,
                    disabled=True,
                    key="logged_in_frontdesk_history_assistant",
                )
    except Exception:
        # History is optional UI. Never block the chat input.
        return


try:
    _v46_previous_frontdesk_understand_meaning = frontdesk_understand_meaning
except Exception:
    _v46_previous_frontdesk_understand_meaning = None

try:
    _v46_previous_handle_receptionist_query = handle_receptionist_query
except Exception:
    _v46_previous_handle_receptionist_query = None


def _frontdesk_user_access_context(user):
    role_key = role_key_for_user(user) if user else None
    return {
        "logged_in": bool(user),
        "role_key": role_key or "visitor",
        "role": safe_text((user or {}).get("role")),
        "department": safe_text((user or {}).get("department")),
        "designation": safe_text((user or {}).get("designation")),
        "employee_name": actor_name(user) if user else "Visitor",
        "access_rules": [
            "Visitors may ask about Virtual Tech AI and may submit client project enquiries.",
            "Personal employee data needs login and should be routed to HR or Finance.",
            "Company performance, revenue, margin, and internal strategy are CEO/founder-only.",
            "Project delivery/allocation questions are handled by the Technical Architect Agent.",
            "Do not reveal salary, margin, hiring, internal cost, employee allocation, or executive comments to clients/visitors.",
        ],
    }


def _frontdesk_normalize_intent(value):
    value = safe_text(value).strip().lower().replace("-", "_").replace(" ", "_")
    aliases = {
        "company_details": "company_identity",
        "about_company": "company_identity",
        "company_info": "company_identity",
        "general_company_question": "company_identity",
        "business_health": "company_performance",
        "financial_report": "company_performance",
        "manager": "reporting_manager",
        "reporting": "reporting_manager",
        "leave": "leave_help",
        "leave_application": "leave_help",
        "payroll": "salary_info",
        "salary": "salary_info",
        "salary_question": "salary_info",
        "salary_issue": "salary_discrepancy",
        "payroll_discrepancy": "salary_discrepancy",
        "new_project": "project_intake",
        "client_project": "project_intake",
        "proposal": "project_intake",
        "technical": "route_architect",
        "operations": "route_architect",
        "operation": "route_architect",
        "hr": "route_hr",
        "finance": "route_finance",
        "sales": "route_sales",
        "ceo": "route_ceo",
        "direct_answer": "general_answer",
        "answer": "general_answer",
    }
    return aliases.get(value, value or "general_answer")


def frontdesk_understand_meaning(query, user=None):
    """Prompt-first understanding for AI Front Desk.

    The LLM decides whether to answer, route, request login, deny access, or start
    project intake. Local semantic fallback is used only when the LLM is not
    available or returns malformed JSON.
    """
    fallback_obj = _frontdesk_local_semantic_fallback(query, user) if "_frontdesk_local_semantic_fallback" in globals() else {
        "intent": "general_answer",
        "agent": "AI Front Desk",
        "confidence": 0.45,
        "needs_login": False,
        "direct_answer": "",
    }
    fallback_obj = dict(fallback_obj or {})
    fallback_obj["intent"] = _frontdesk_normalize_intent(fallback_obj.get("intent"))
    fallback = json.dumps(fallback_obj, ensure_ascii=False)

    access_context = _frontdesk_user_access_context(user)
    prompt = f"""
You are LifecycleDesk AI's AI Front Desk for Virtual Tech AI.
Virtual Tech AI is a Bangalore-based company that provides AI and data solutions.

Your job is to understand the user's meaning and choose the safest useful action.
Do not behave like a keyword matcher. Read the whole message and infer intent.

You can do five things:
1. answer directly when the answer is public, general, or safe for the current user;
2. route to the right internal agent when company data or workflow tools are needed;
3. ask the user to log in when personal/internal data is requested by a visitor;
4. refuse or limit the answer when the logged-in user lacks access;
5. start project intake when a client gives a project requirement, budget, timeline, and contact details.

Access context and rules:
{json.dumps(access_context, ensure_ascii=False)}

Allowed intents:
- greeting
- company_identity
- company_performance
- reporting_manager
- leave_help
- salary_info
- salary_discrepancy
- project_intake
- route_hr
- route_finance
- route_sales
- route_architect
- route_ceo
- general_answer
- access_denied
- login_required

Allowed agents:
- AI Front Desk
- HR Agent
- Finance Agent
- Sales Agent
- Technical Architect Agent
- CEO Agent

Return only valid JSON with exactly these keys:
- intent: one allowed intent
- agent: one allowed agent
- confidence: number from 0 to 1
- needs_login: true/false
- access_denied: true/false
- direct_answer: concise answer if AI Front Desk can answer directly; otherwise empty string
- reason: one short reason for the routing/access decision

Rules:
- For "tell me about this company", answer company_identity directly.
- For company performance, revenue, profit, margin, business health, or internal financial reports, use company_performance and CEO Agent.
- For employee salary/payroll, use Finance Agent and require login.
- For manager, leave, attendance, onboarding, employee profile, or HR process, use HR Agent and require login when personal data is involved.
- For delivery, implementation, architecture, allocation, project targets, or blockers, use Technical Architect Agent.
- For new client/project requirements, use project_intake.
- For safe general questions, use general_answer and put the answer in direct_answer.
- If the user lacks access, use access_denied and explain politely in direct_answer.

User message:
{safe_text(query)}
"""
    try:
        raw = ask_llm(prompt, fallback=fallback)
        parsed = _frontdesk_json_loads(raw, fallback_obj)
        if not isinstance(parsed, dict):
            parsed = fallback_obj
    except Exception:
        parsed = fallback_obj

    parsed["intent"] = _frontdesk_normalize_intent(parsed.get("intent") or fallback_obj.get("intent"))
    parsed["agent"] = safe_text(parsed.get("agent") or fallback_obj.get("agent") or "AI Front Desk")
    if parsed["agent"] in ["Receptionist", "Front Desk"]:
        parsed["agent"] = "AI Front Desk"
    if parsed["agent"] == "Operations Agent":
        parsed["agent"] = "Technical Architect Agent"
    if parsed["agent"] not in ["AI Front Desk", "HR Agent", "Finance Agent", "Sales Agent", "Technical Architect Agent", "CEO Agent"]:
        parsed["agent"] = safe_text(fallback_obj.get("agent"), "AI Front Desk")
    if parsed["agent"] == "Operations Agent":
        parsed["agent"] = "Technical Architect Agent"

    parsed["confidence"] = safe_number(parsed.get("confidence"), safe_number(fallback_obj.get("confidence"), 0.5))
    parsed["needs_login"] = bool(parsed.get("needs_login", fallback_obj.get("needs_login", False)))
    parsed["access_denied"] = bool(parsed.get("access_denied", False))
    parsed["direct_answer"] = safe_text(parsed.get("direct_answer"))
    parsed["reason"] = safe_text(parsed.get("reason"))

    # Reliability safety net: if the LLM gave a vague answer for the most common
    # private employee questions, use the local semantic fallback to keep the app useful.
    fallback_specific = _frontdesk_normalize_intent(fallback_obj.get("intent"))
    specific_intents = {
        "company_identity", "company_performance", "reporting_manager", "leave_help",
        "salary_info", "salary_discrepancy", "project_intake"
    }
    if fallback_specific in specific_intents and parsed["intent"] not in specific_intents:
        parsed.update(fallback_obj)
        parsed["intent"] = fallback_specific
        parsed["agent"] = "Technical Architect Agent" if parsed.get("agent") == "Operations Agent" else safe_text(parsed.get("agent"), "AI Front Desk")
    return parsed


def _frontdesk_prefix(answer):
    answer = safe_text(answer).strip()
    if not answer:
        return "AI Front Desk: I can help with client intake, HR, Finance, Sales, Technical Architecture, CEO requests, and safe general questions."
    lowered = answer.lower()
    if lowered.startswith("ai front desk:") or lowered.startswith("hr agent:") or lowered.startswith("finance agent:") or lowered.startswith("sales agent:") or lowered.startswith("ceo agent:"):
        return answer
    return "AI Front Desk: " + answer


def _frontdesk_access_denied_message(agent, intent, direct_answer=""):
    answer = safe_text(direct_answer).strip()
    if not answer:
        if agent == "CEO Agent" or intent == "company_performance":
            answer = "This is internal CEO-level information. Please use a Founder/CEO login to view it."
        else:
            answer = "I cannot show that information with your current access. Please login with the right role or contact the responsible team."
    return {
        "type": "text",
        "agent": agent or "AI Front Desk",
        "intent": intent,
        "message": _frontdesk_prefix(answer),
    }


def handle_receptionist_query(query, user, data):
    """Reliable AI Front Desk: prompt-led first, role/access-aware, then safe fallback."""
    understanding = frontdesk_understand_meaning(query, user)
    intent = _frontdesk_normalize_intent(understanding.get("intent"))
    agent = safe_text(understanding.get("agent"), "AI Front Desk")
    confidence = safe_number(understanding.get("confidence"), 0.0)

    if understanding.get("access_denied") or intent == "access_denied":
        return _frontdesk_access_denied_message(agent, intent, understanding.get("direct_answer"))

    if understanding.get("needs_login") and user is None:
        return _frontdesk_login_required(agent, intent) if "_frontdesk_login_required" in globals() else {
            "type": "login_required",
            "agent": agent,
            "intent": intent,
            "confidence": confidence,
            "message": "AI Front Desk: Please login first so I can verify your access and answer this safely.",
        }

    if intent == "greeting":
        name = actor_name(user) if user else "there"
        return {"type": "general", "agent": "AI Front Desk", "intent": intent, "confidence": confidence, "message": f"AI Front Desk: Hello {name}. How can I help you today?"}

    if intent in ["company_identity", "general_answer"] and safe_text(understanding.get("direct_answer")):
        return {"type": "text", "agent": "AI Front Desk", "intent": intent, "confidence": confidence, "message": _frontdesk_prefix(understanding.get("direct_answer"))}

    if intent == "company_identity":
        return {"type": "text", "agent": "AI Front Desk", "intent": intent, "confidence": confidence, "message": _frontdesk_company_identity_answer() if "_frontdesk_company_identity_answer" in globals() else _frontdesk_prefix(FRONTDESK_COMPANY_FACTS)}

    if intent == "company_performance":
        if user is None:
            return _frontdesk_login_required("CEO Agent", intent)
        if safe_text(user.get("role")).lower() == "founder":
            return {"type": "company_health", "agent": "CEO Agent", "intent": intent, "confidence": confidence, "message": "AI Front Desk: Connecting you to CEO Agent for company performance analysis."}
        return _frontdesk_access_denied_message("CEO Agent", intent, understanding.get("direct_answer"))

    if intent == "reporting_manager":
        if user is None:
            return _frontdesk_login_required("HR Agent", intent)
        return {"type": "text", "agent": "HR Agent", "intent": intent, "confidence": confidence, "message": "AI Front Desk: I checked this through HR Agent.\n\n" + handle_hr_agent_query(query, user, data)}

    if intent == "leave_help":
        if user is None:
            return _frontdesk_login_required("HR Agent", intent)
        direct = safe_text(understanding.get("direct_answer")) or (_frontdesk_leave_answer(user) if "_frontdesk_leave_answer" in globals() else "You can raise a leave request with dates, leave type, and reason. HR or your reporting manager will review it.")
        return {"type": "text", "agent": "HR Agent", "intent": intent, "confidence": confidence, "message": _frontdesk_prefix(direct)}

    if intent == "salary_info":
        if user is None:
            return _frontdesk_login_required("Finance Agent", intent)
        answer = answer_salary_by_role(query, user, data) if is_role_salary_query(query) else get_employee_salary_info(user, data)
        return {"type": "text", "agent": "Finance Agent", "intent": intent, "confidence": confidence, "message": "AI Front Desk: I checked this through Finance Agent.\n\n" + answer}

    if intent == "salary_discrepancy":
        if user is None:
            return _frontdesk_login_required("Finance Agent", intent)
        return {"type": "text", "agent": "Finance Agent", "intent": intent, "confidence": confidence, "message": "AI Front Desk: I checked this through Finance Agent.\n\n" + explain_salary_difference(user, data)}

    if intent == "project_intake":
        if _v46_previous_handle_receptionist_query is not None:
            return _v46_previous_handle_receptionist_query(query, user, data)

    route_map = {
        "route_hr": "HR Agent",
        "route_finance": "Finance Agent",
        "route_sales": "Sales Agent",
        "route_architect": "Technical Architect Agent",
        "route_ceo": "CEO Agent",
    }
    if intent in route_map:
        mapped_agent = route_map[intent]
        if user is None and mapped_agent in ["HR Agent", "Finance Agent", "Technical Architect Agent", "CEO Agent"]:
            return _frontdesk_login_required(mapped_agent, intent)
        if mapped_agent == "CEO Agent" and user is not None and safe_text(user.get("role")).lower() != "founder":
            return _frontdesk_access_denied_message(mapped_agent, intent, understanding.get("direct_answer"))
        return {"type": "route_agent", "agent": mapped_agent, "intent": intent, "confidence": confidence, "message": f"AI Front Desk: Connecting you to {mapped_agent}."}

    if safe_text(understanding.get("direct_answer")):
        return {"type": "text", "agent": "AI Front Desk", "intent": intent, "confidence": confidence, "message": _frontdesk_prefix(understanding.get("direct_answer"))}

    if _v46_previous_handle_receptionist_query is not None:
        original = _v46_previous_handle_receptionist_query(query, user, data)
        if isinstance(original, dict):
            original["message"] = safe_text(original.get("message")).replace("Receptionist:", "AI Front Desk:").replace("Operations Agent", "Technical Architect Agent")
            if original.get("agent") in ["Receptionist", "Operations Agent"]:
                original["agent"] = "AI Front Desk" if original.get("agent") == "Receptionist" else "Technical Architect Agent"
        return original

    return {"type": "text", "agent": "AI Front Desk", "intent": intent, "confidence": confidence, "message": _frontdesk_prefix("I can help with client intake, HR, Finance, Sales, Technical Architecture, CEO requests, or safe general questions. Please tell me what you need.")}


# Readable dataframe patch: preserve normal table display, then offer a full-cell
# viewer only when long values are likely to be truncated in the UI.

def _dd_dataframe_has_long_values(df, threshold=75):
    try:
        if df is None or df.empty:
            return False
        sample = df.head(50).astype(str)
        return bool((sample.applymap(lambda x: len(safe_text(x)) > threshold)).any().any())
    except Exception:
        return False


def _dd_dataframe_full_value_viewer(df, key_prefix):
    try:
        if df is None or df.empty or not _dd_dataframe_has_long_values(df):
            return
        st.caption("Some table values are long. Use the viewer below to read any full cell or full row.")
        show_viewer = st.checkbox("Open full table value viewer", key=f"{key_prefix}_toggle")
        if not show_viewer:
            return

        display_df = df.reset_index(drop=True).copy()
        row_labels = []
        for idx, row in display_df.head(200).iterrows():
            preview_parts = []
            for col in list(display_df.columns)[:3]:
                value = safe_text(row.get(col)).replace("\n", " ").strip()
                if value:
                    preview_parts.append(value[:35])
            preview = " | ".join(preview_parts) or f"Row {idx + 1}"
            row_labels.append(f"{idx + 1}. {preview}")

        selected_row_label = st.selectbox("Select row", row_labels, key=f"{key_prefix}_row")
        row_index = row_labels.index(selected_row_label)
        selected_column = st.selectbox("Select column", list(display_df.columns), key=f"{key_prefix}_col")
        cell_value = safe_text(display_df.iloc[row_index].get(selected_column))
        st.text_area(
            "Full selected cell value",
            value=cell_value,
            height=180,
            disabled=True,
            key=f"{key_prefix}_cell",
        )

        row_lines = []
        for col in display_df.columns:
            value = safe_text(display_df.iloc[row_index].get(col)).strip()
            if value:
                row_lines.append(f"{col}: {value}")
        st.text_area(
            "Full selected row",
            value="\n\n".join(row_lines),
            height=220,
            disabled=True,
            key=f"{key_prefix}_full_row",
        )
    except Exception:
        return


def _dd_install_readable_dataframe_patch():
    try:
        if getattr(st, "_dd_readable_dataframe_patch_installed", False):
            return
        original_dataframe = st.dataframe
        st._dd_original_dataframe = original_dataframe

        def readable_dataframe(data=None, *args, **kwargs):
            result = original_dataframe(data, *args, **kwargs)
            try:
                if isinstance(data, pd.DataFrame):
                    df = data.copy()
                elif hasattr(data, "data") and isinstance(getattr(data, "data"), pd.DataFrame):
                    df = getattr(data, "data").copy()
                else:
                    df = pd.DataFrame(data)
                if _dd_dataframe_has_long_values(df):
                    import hashlib
                    import inspect
                    frame = inspect.currentframe().f_back
                    callsite = f"{getattr(frame, 'f_code', None).co_filename if frame else 'unknown'}:{getattr(frame, 'f_lineno', 0) if frame else 0}"
                    sample = "|".join(map(str, list(df.columns))) + "|" + "|".join(df.astype(str).head(2).to_numpy().ravel().tolist())[:400]
                    digest = hashlib.md5((callsite + sample + str(df.shape)).encode("utf-8", errors="ignore")).hexdigest()[:12]
                    _dd_dataframe_full_value_viewer(df, f"dd_table_value_{digest}")
            except Exception:
                pass
            return result

        st.dataframe = readable_dataframe
        st._dd_readable_dataframe_patch_installed = True
    except Exception:
        pass


_dd_install_readable_dataframe_patch()

# -----------------------------------------------------------------------------
# Reviewed items workflow patch
# -----------------------------------------------------------------------------
# Keep the review action only for read-only lifecycle updates. Active proposal
# decision items stay in the inbox until the executive submits or updates the
# appropriate department/CEO opinion.


def _dd_is_project_started_or_delivery_item(report):
    if not isinstance(report, dict):
        return False
    status_text = safe_text(report.get("workflow_status")).lower()
    response_text = safe_text(report.get("client_response"))
    return bool(
        response_text == "Accept Proposal"
        or safe_text(report.get("project_id")).strip()
        or safe_text(report.get("project_created")).strip().lower() == "yes"
        or "delivery" in status_text
        or "kickoff" in status_text
        or "team allocated" in status_text
        or get_project_for_proposal(report.get("proposal_id")) is not None
    )


def _dd_role_has_action_required_for_update(report, role_key):
    """Return True when hiding the notification would skip a real role action."""
    role_key = safe_text(role_key).lower()
    if role_key not in ["sales", "finance", "hr", "operations", "ceo"]:
        return False

    ceo_quote_sent = proposal_has_ceo_quote_sent(report) if "proposal_has_ceo_quote_sent" in globals() else bool(safe_text(report.get("client_quotation")).strip())
    delivery_item = _dd_is_project_started_or_delivery_item(report)

    # Before CEO quotation, all executives are expected to review and give/update
    # their relevant opinion. Do not allow a simple reviewed action here.
    if not ceo_quote_sent and not delivery_item:
        return True

    # Technical Architect / Operations owns the delivery-readiness path after
    # client acceptance. Keep those alerts actionable instead of dismissible.
    if role_key == "operations" and delivery_item:
        return True

    # CEO must give final quote/decision before quotation is sent. After delivery
    # starts, CEO alerts are informational monitoring updates.
    if role_key == "ceo" and not ceo_quote_sent and not delivery_item:
        return True

    return False


def _dd_can_mark_update_as_reviewed(report, role_key):
    """Allow review-only dismissal only for informational lifecycle updates."""
    if not isinstance(report, dict):
        return False
    return not _dd_role_has_action_required_for_update(report, role_key)


def get_reviewed_proposal_reports_for_user(user, limit=20):
    """Return recently reviewed/read items for the logged-in executive."""
    column = user_notification_column(user)
    if column is None:
        return []
    try:
        df = read_proposal_store(create_if_missing=True)
    except Exception as exc:
        try:
            remember_postgres_error(exc)
        except Exception:
            pass
        return []
    if df is None or df.empty or column not in df.columns:
        return []

    reviewed = df[df[column].fillna("No").astype(str).str.strip().str.lower() == "yes"].copy()
    if reviewed.empty:
        return []

    seen_at_column = user_seen_at_column(user)
    sort_columns = []
    if seen_at_column and seen_at_column in reviewed.columns:
        sort_columns.append(seen_at_column)
    if "last_updated_at" in reviewed.columns:
        sort_columns.append("last_updated_at")
    if "created_at" in reviewed.columns:
        sort_columns.append("created_at")

    if sort_columns:
        reviewed = reviewed.sort_values(sort_columns, ascending=False)

    return [proposal_row_to_report(row) for _, row in reviewed.head(limit).iterrows()]


def render_reviewed_proposal_reference_list(user, data=None, limit=20):
    """Collapsed reference list for items marked/read by the current role."""
    role_key = role_key_for_user(user) or "executive"
    reports = get_reviewed_proposal_reports_for_user(user, limit=limit)
    with st.expander("Reviewed items reference", expanded=False):
        if not reports:
            st.info("No reviewed items are available yet for your role.")
            return

        st.caption("Items moved here remain available for future reference.")
        option_map = {"Select a reviewed item...": None}
        labels = ["Select a reviewed item..."]
        rows = []
        for idx, report in enumerate(reports, start=1):
            analysis = report.get("analysis", {})
            reviewed_at = safe_text(report.get("last_updated_at") or report.get("created_at") or "No timestamp")
            project_label = project_display_name(
                project=get_project_for_proposal(report.get("proposal_id")) or {},
                project_id=report.get("project_id"),
                proposal_id=report.get("proposal_id"),
                fallback=analysis.get("project_type", "Project"),
            )
            label = f"{idx}. {reviewed_at} | {project_label} | {report.get('workflow_status', 'Status unavailable')}"
            labels.append(label)
            option_map[label] = report
            rows.append({
                "Updated": reviewed_at,
                "Proposal": report.get("proposal_id"),
                "Project": project_label,
                "Status": report.get("workflow_status"),
                "Last update": report.get("last_update_summary"),
            })

        if rows:
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        selected_label = st.selectbox(
            "Open reviewed item",
            labels,
            key=f"reviewed_item_selector_{actor_id(user)}_{role_key}",
        )
        selected_report = option_map.get(selected_label)
        if not selected_report:
            return

        analysis = selected_report.get("analysis", {})
        st.markdown("#### Reviewed item summary")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Project", analysis.get("project_type", "Project"))
        c2.metric("Status", selected_report.get("workflow_status", "Status unavailable"))
        c3.metric("Quote", money_text(analysis.get("recommended_quote", 0)))
        c4.metric("Timeline", f"{analysis.get('timeline_months', 0)} month(s)")
        if selected_report.get("last_update_summary"):
            st.info(selected_report.get("last_update_summary"))

        with st.expander("Open read-only proposal snapshot", expanded=False):
            render_external_client_report(selected_report, user=user, compact=True)
            st.caption("This is a read-only reference view. Active decisions are handled from the pending update inbox.")


def render_pending_proposal_notifications(user, data=None):
    """Executive inbox with decision-safe reviewed item handling."""
    column = user_notification_column(user)
    if column is None:
        return

    try:
        reports = get_pending_proposal_reports_for_user(user)
    except Exception as exc:
        st.error(f"Could not load proposal notifications from proposal storage: {exc}")
        return

    role_key = role_key_for_user(user) or "executive"
    selected_key = f"selected_pending_proposal_{role_key}"

    if not reports:
        st.success("No new proposal or lifecycle updates for your role.")
        render_reviewed_proposal_reference_list(user, data=data)
        return

    def sort_key(report):
        return safe_text(report.get("last_updated_at") or report.get("created_at"))

    reports = sorted(reports, key=sort_key, reverse=True)

    st.markdown(
        f"""
        <div class="dd-section-card">
            <div class="dd-section-title">Executive update inbox</div>
            <div class="dd-section-subtitle">
                You have <b>{len(reports)}</b> pending update(s). Open the dropdown and choose one item.
                Decision-stage items stay here until the right executive opinion is submitted. Informational lifecycle updates can be marked as reviewed.
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
        linked_project = get_project_for_proposal(report.get("proposal_id"))
        project_label = project_display_name(
            project=linked_project or {},
            project_id=report.get("project_id"),
            proposal_id=report.get("proposal_id"),
            fallback=analysis.get("project_type", "Project"),
        )
        action_label = "Action needed" if _dd_role_has_action_required_for_update(report, role_key) else "Information only"
        label = (
            f"{idx}. {updated} | {project_label} | {report.get('workflow_status', 'Pending')} | "
            f"{action_label} | Last: {report.get('last_updated_role', 'System')}"
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
                "Project": project_display_name(project=get_project_for_proposal(report.get("proposal_id")) or {}, project_id=report.get("project_id"), proposal_id=report.get("proposal_id"), fallback=analysis.get("project_type")),
                "Status": report.get("workflow_status"),
                "Inbox Type": "Action needed" if _dd_role_has_action_required_for_update(report, role_key) else "Information only",
                "Last By": report.get("last_updated_role"),
            })
        if preview_rows:
            st.dataframe(pd.DataFrame(preview_rows), use_container_width=True, hide_index=True)

    selected_report = option_map.get(st.session_state.get(selected_key, ""))
    if not selected_report:
        st.info("Choose one update from the dropdown to open its dashboard.")
        render_reviewed_proposal_reference_list(user, data=data)
        return

    st.markdown("### Selected update dashboard")
    is_operations_delivery_item = (
        role_key == "operations"
        and _dd_is_project_started_or_delivery_item(selected_report)
    )
    project_started_for_selected = get_project_for_proposal(selected_report.get("proposal_id")) is not None
    is_ceo_live_project_item = (
        role_key == "ceo"
        and (
            project_started_for_selected
            or "kickoff" in safe_text(selected_report.get("workflow_status")).lower()
            or "team allocated" in safe_text(selected_report.get("workflow_status")).lower()
            or "delivery" in safe_text(selected_report.get("workflow_status")).lower()
        )
    )

    if is_operations_delivery_item:
        st.info("This is a delivery-readiness item for the Technical Architect team.")
        render_operations_delivery_workspace(user, data or {}, focus_proposal_id=selected_report.get("proposal_id"))
    elif is_ceo_live_project_item:
        render_ceo_project_lifecycle_dashboard(selected_report, user=user, data=data or {})
    else:
        render_external_client_report(selected_report, user=user, compact=False)

    if _dd_can_mark_update_as_reviewed(selected_report, role_key):
        st.markdown("#### Review action")
        st.caption("This update is informational for your role. Mark it as reviewed to move it into the reviewed-items reference list.")
        if st.button(
            "Mark as reviewed",
            key=f"mark_reviewed_selected_{selected_report.get('proposal_id')}_{role_key}",
            type="primary",
        ):
            success, message = mark_proposal_seen_for_user(selected_report.get("proposal_id"), user)
            if success:
                st.success(message)
                st.session_state[selected_key] = "Select an update to open..."
                st.rerun()
            else:
                st.error(message)
    else:
        st.caption("This item needs a role action, so it will remain in the inbox until the appropriate opinion or delivery action is completed.")

    render_reviewed_proposal_reference_list(user, data=data)

# -----------------------------------------------------------------------------
# CEO live project visibility restoration patch
# -----------------------------------------------------------------------------
# CEO should retain full project monitoring after client acceptance/kickoff.
# Sales, Finance, and HR keep the compact role-safe lifecycle view.


def _dd_is_ceo_delivery_monitoring_item(report):
    """Return True when CEO should see the live project monitor instead of compact lifecycle status."""
    if not isinstance(report, dict):
        return False
    status_text = safe_text(report.get("workflow_status")).lower()
    client_response = safe_text(report.get("client_response"))
    proposal_id = safe_text(report.get("proposal_id"))
    return bool(
        client_response == "Accept Proposal"
        or safe_text(report.get("project_id")).strip()
        or safe_text(report.get("project_created")).strip().lower() == "yes"
        or "delivery" in status_text
        or "kickoff" in status_text
        or "team allocated" in status_text
        or get_project_for_proposal(proposal_id) is not None
    )


def _dd_read_table_rows_safe(table_name, columns, filters=None, sort_column="created_at", limit=12):
    """Read a workflow table for CEO monitoring without interrupting the dashboard."""
    try:
        df = read_simple_table(table_name, columns)
    except Exception:
        return pd.DataFrame(columns=columns)
    if df is None or df.empty:
        return pd.DataFrame(columns=columns)
    working = df.copy()
    filters = filters or {}
    for col, expected in filters.items():
        if col in working.columns and safe_text(expected):
            working = working[working[col].astype(str) == safe_text(expected)]
    if sort_column in working.columns:
        working = working.sort_values(sort_column, ascending=False)
    return working.head(limit)


def _dd_render_ceo_live_activity_panels(report):
    """Extra CEO-only panels showing what is happening inside the project."""
    if not isinstance(report, dict):
        return
    project = get_project_for_proposal(report.get("proposal_id"))
    if not project:
        return

    project_id = safe_text(project.get("project_id"))
    proposal_id = safe_text(project.get("proposal_id") or report.get("proposal_id"))
    plan = get_delivery_plan_for_client_project(project_id)

    st.markdown(
        """
        <div class="dd-section-card dd-dashboard-shell">
            <div class="dd-section-eyebrow">CEO project monitor</div>
            <div class="dd-section-title">Live project activity</div>
            <div class="dd-section-subtitle">
                CEO view includes delivery progress, weekly targets, client messages, published weekly updates,
                employee updates, and Technical Architect actions after project kickoff.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    a1, a2, a3, a4 = st.columns(4)
    a1.metric("Project status", safe_text(project.get("project_status"), "In progress"))
    a2.metric("Delivery plan", safe_text(plan.get("approval_status") if plan else "Pending"))
    a3.metric("Client status", safe_text(report.get("client_response"), "Awaiting response"))
    a4.metric("Project", project_display_name(project=project, project_id=project_id))

    if plan:
        render_weekly_targets_panel(
            plan,
            title="Weekly target list - CEO view",
            expanded=True,
            client_safe=False,
            key_prefix=f"ceo_activity_weekly_targets_{project_id}",
        )

    messages = _dd_read_table_rows_safe(
        "client_operations_messages",
        CLIENT_OPERATIONS_MESSAGE_COLUMNS,
        filters={"project_id": project_id},
        sort_column="created_at",
        limit=10,
    )
    if not messages.empty:
        with st.expander("Recent client / Technical Architect messages", expanded=False):
            view_rows = []
            for _, row in messages.iterrows():
                view_rows.append({
                    "Time": safe_text(row.get("created_at")),
                    "Sender": safe_text(row.get("sender_name")) or safe_text(row.get("sender_type")),
                    "Type": safe_text(row.get("sender_type")),
                    "Message": safe_text(row.get("message_text")),
                })
            st.dataframe(pd.DataFrame(view_rows), use_container_width=True, hide_index=True)
    else:
        st.caption("No client / Technical Architect messages have been recorded for this project yet.")

    weekly_updates = _dd_read_table_rows_safe(
        "weekly_project_updates",
        WEEKLY_UPDATE_COLUMNS,
        filters={"project_id": project_id},
        sort_column="generated_at",
        limit=10,
    )
    if not weekly_updates.empty:
        with st.expander("Published weekly client updates", expanded=False):
            rows = []
            for _, row in weekly_updates.iterrows():
                rows.append({
                    "Week": safe_text(row.get("week_label")),
                    "Generated at": safe_text(row.get("generated_at")),
                    "Update": safe_text(row.get("update_text")),
                    "Client action needed": safe_text(row.get("client_action_needed")),
                })
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.caption("No weekly client update has been published yet.")

    employee_updates = get_employee_project_updates(project_id=project_id)
    if employee_updates is not None and not employee_updates.empty:
        with st.expander("All employee weekly updates and requests", expanded=False):
            working = employee_updates.copy()
            if "created_at" in working.columns:
                working = working.sort_values("created_at", ascending=False)
            rows = []
            for _, row in working.head(20).iterrows():
                issue = (
                    safe_text(row.get("support_needed")).strip()
                    or safe_text(row.get("hurdles")).strip()
                    or safe_text(row.get("notes")).strip()
                    or "No issue mentioned"
                )
                rows.append({
                    "Time": safe_text(row.get("created_at")),
                    "Employee": safe_text(row.get("employee_name")),
                    "Week": safe_text(row.get("week_label")),
                    "Status": safe_text(row.get("progress_status")),
                    "Progress": (safe_text(row.get("progress_percent")) + "%") if safe_text(row.get("progress_percent")) else "",
                    "Module": safe_text(row.get("assigned_module")),
                    "Request / note": issue,
                    "Technical Architect status": safe_text(row.get("operations_status"), "Open"),
                })
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.success("No employee updates or requests are recorded yet for this project.")


try:
    _v46_original_render_ceo_project_lifecycle_dashboard = render_ceo_project_lifecycle_dashboard
except Exception:
    _v46_original_render_ceo_project_lifecycle_dashboard = None


def render_ceo_project_lifecycle_dashboard(report, user=None, data=None):
    """CEO full live delivery monitor after client acceptance or project kickoff."""
    if _v46_original_render_ceo_project_lifecycle_dashboard is not None:
        _v46_original_render_ceo_project_lifecycle_dashboard(report, user=user, data=data)
    _dd_render_ceo_live_activity_panels(report)


try:
    _v46_original_render_post_ceo_readonly_lifecycle_view = render_post_ceo_readonly_lifecycle_view
except Exception:
    _v46_original_render_post_ceo_readonly_lifecycle_view = None


def render_post_ceo_readonly_lifecycle_view(report, user=None, compact=False):
    """Keep compact lifecycle status for non-CEO roles; CEO gets full live monitor."""
    if role_key_for_user(user) == "ceo" and _dd_is_ceo_delivery_monitoring_item(report):
        render_ceo_project_lifecycle_dashboard(report, user=user, data={})
        return
    if _v46_original_render_post_ceo_readonly_lifecycle_view is not None:
        _v46_original_render_post_ceo_readonly_lifecycle_view(report, user=user, compact=compact)


def render_reviewed_proposal_reference_list(user, data=None, limit=20):
    """Collapsed reference list with full CEO monitoring for reviewed delivery items."""
    role_key = role_key_for_user(user) or "executive"
    reports = get_reviewed_proposal_reports_for_user(user, limit=limit)
    with st.expander("Reviewed items reference", expanded=False):
        if not reports:
            st.info("No reviewed items are available yet for your role.")
            return

        st.caption("Items moved here remain available for future reference.")
        option_map = {"Select a reviewed item...": None}
        labels = ["Select a reviewed item..."]
        rows = []
        for idx, report in enumerate(reports, start=1):
            analysis = report.get("analysis", {})
            reviewed_at = safe_text(report.get("last_updated_at") or report.get("created_at") or "No timestamp")
            project_label = project_display_name(
                project=get_project_for_proposal(report.get("proposal_id")) or {},
                project_id=report.get("project_id"),
                proposal_id=report.get("proposal_id"),
                fallback=analysis.get("project_type", "Project"),
            )
            label = f"{idx}. {reviewed_at} | {project_label} | {report.get('workflow_status', 'Status unavailable')}"
            labels.append(label)
            option_map[label] = report
            rows.append({
                "Updated": reviewed_at,
                "Proposal": report.get("proposal_id"),
                "Project": project_label,
                "Status": report.get("workflow_status"),
                "Last update": report.get("last_update_summary"),
            })

        if rows:
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        selected_label = st.selectbox(
            "Open reviewed item",
            labels,
            key=f"reviewed_item_selector_{actor_id(user)}_{role_key}",
        )
        reviewed_memory_key = f"_dd_last_reviewed_item_selection_{actor_id(user)}_{role_key}"
        previous_reviewed_selection = st.session_state.get(reviewed_memory_key)
        if (
            previous_reviewed_selection is not None
            and selected_label != previous_reviewed_selection
            and selected_label != "Select a reviewed item..."
        ):
            try:
                request_page_scroll("reviewed_item_detail")
            except Exception:
                st.session_state["_dd_scroll_target"] = "reviewed_item_detail"
        st.session_state[reviewed_memory_key] = selected_label

        selected_report = option_map.get(selected_label)
        if not selected_report:
            return

        st.markdown('<div id="dd-reviewed-item-detail"></div>', unsafe_allow_html=True)

        if role_key == "ceo" and _dd_is_ceo_delivery_monitoring_item(selected_report):
            st.markdown("#### Reviewed project monitor")
            render_ceo_project_lifecycle_dashboard(selected_report, user=user, data=data or {})
            return

        analysis = selected_report.get("analysis", {})
        st.markdown("#### Reviewed item summary")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Project", analysis.get("project_type", "Project"))
        c2.metric("Status", selected_report.get("workflow_status", "Status unavailable"))
        c3.metric("Quote", money_text(analysis.get("recommended_quote", 0)))
        c4.metric("Timeline", f"{analysis.get('timeline_months', 0)} month(s)")
        if selected_report.get("last_update_summary"):
            st.info(selected_report.get("last_update_summary"))

        with st.expander("Open read-only proposal snapshot", expanded=False):
            render_external_client_report(selected_report, user=user, compact=True)
            st.caption("This is a read-only reference view. Active decisions are handled from the pending update inbox.")


def render_pending_proposal_notifications(user, data=None):
    """Executive inbox with CEO delivery monitoring preserved."""
    column = user_notification_column(user)
    if column is None:
        return

    try:
        reports = get_pending_proposal_reports_for_user(user)
    except Exception as exc:
        st.error(f"Could not load proposal notifications from proposal storage: {exc}")
        return

    role_key = role_key_for_user(user) or "executive"
    selected_key = f"selected_pending_proposal_{role_key}"

    if not reports:
        st.success("No new proposal or lifecycle updates for your role.")
        render_reviewed_proposal_reference_list(user, data=data)
        return

    def sort_key(report):
        return safe_text(report.get("last_updated_at") or report.get("created_at"))

    reports = sorted(reports, key=sort_key, reverse=True)

    st.markdown(
        f"""
        <div class="dd-section-card">
            <div class="dd-section-title">Executive update inbox</div>
            <div class="dd-section-subtitle">
                You have <b>{len(reports)}</b> pending update(s). Open the dropdown and choose one item.
                Decision-stage items stay here until the right executive opinion is submitted. Informational lifecycle updates can be marked as reviewed.
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
        linked_project = get_project_for_proposal(report.get("proposal_id"))
        project_label = project_display_name(
            project=linked_project or {},
            project_id=report.get("project_id"),
            proposal_id=report.get("proposal_id"),
            fallback=analysis.get("project_type", "Project"),
        )
        action_label = "Action needed" if _dd_role_has_action_required_for_update(report, role_key) else "Information only"
        label = (
            f"{idx}. {updated} | {project_label} | {report.get('workflow_status', 'Pending')} | "
            f"{action_label} | Last: {report.get('last_updated_role', 'System')}"
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
        pending_memory_key = f"_dd_last_pending_update_selection_{role_key}"
        previous_pending_selection = st.session_state.get(pending_memory_key)
        if (
            previous_pending_selection is not None
            and selected_label != previous_pending_selection
            and selected_label != "Select an update to open..."
        ):
            try:
                request_page_scroll("selected_update_dashboard")
            except Exception:
                st.session_state["_dd_scroll_target"] = "selected_update_dashboard"
        st.session_state[pending_memory_key] = selected_label
        st.session_state[selected_key] = selected_label

        preview_rows = []
        for report in reports[:8]:
            analysis = report.get("analysis", {})
            preview_rows.append({
                "Updated": safe_text(report.get("last_updated_at") or report.get("created_at")),
                "Proposal": report.get("proposal_id"),
                "Project": project_display_name(project=get_project_for_proposal(report.get("proposal_id")) or {}, project_id=report.get("project_id"), proposal_id=report.get("proposal_id"), fallback=analysis.get("project_type")),
                "Status": report.get("workflow_status"),
                "Inbox Type": "Action needed" if _dd_role_has_action_required_for_update(report, role_key) else "Information only",
                "Last By": report.get("last_updated_role"),
            })
        if preview_rows:
            st.dataframe(pd.DataFrame(preview_rows), use_container_width=True, hide_index=True)

    selected_report = option_map.get(st.session_state.get(selected_key, ""))
    if not selected_report:
        st.info("Choose one update from the dropdown to open its dashboard.")
        render_reviewed_proposal_reference_list(user, data=data)
        return

    st.markdown('<div id="dd-selected-update-dashboard"></div>', unsafe_allow_html=True)
    st.markdown("### Selected update dashboard")
    is_operations_delivery_item = role_key == "operations" and _dd_is_project_started_or_delivery_item(selected_report)
    is_ceo_live_project_item = role_key == "ceo" and _dd_is_ceo_delivery_monitoring_item(selected_report)

    if is_operations_delivery_item:
        st.info("This is a delivery-readiness item for the Technical Architect team.")
        render_operations_delivery_workspace(user, data or {}, focus_proposal_id=selected_report.get("proposal_id"))
    elif is_ceo_live_project_item:
        render_ceo_project_lifecycle_dashboard(selected_report, user=user, data=data or {})
    else:
        render_external_client_report(selected_report, user=user, compact=False)

    if _dd_can_mark_update_as_reviewed(selected_report, role_key):
        st.markdown("#### Review action")
        st.caption("This update is informational for your role. Mark it as reviewed to move it into the reviewed-items reference list.")
        if st.button(
            "Mark as reviewed",
            key=f"mark_reviewed_selected_{selected_report.get('proposal_id')}_{role_key}",
            type="primary",
        ):
            success, message = mark_proposal_seen_for_user(selected_report.get("proposal_id"), user)
            if success:
                st.success(message)
                st.session_state[selected_key] = "Select an update to open..."
                st.rerun()
            else:
                st.error(message)
    else:
        st.caption("This item needs a role action, so it will remain in the inbox until the appropriate opinion or delivery action is completed.")

    try:
        run_pending_page_scroll()
    except Exception:
        pass

    render_reviewed_proposal_reference_list(user, data=data)

# -----------------------------------------------------------------------------
# Project-week status patch
# -----------------------------------------------------------------------------
# Each employee update is now mapped to a project-relative week. Week 1 starts
# on the project kickoff date and covers the first seven calendar days. The
# weekly checkpoint date is the Friday that falls inside that project week.

from datetime import timedelta


def _v47_dt(value):
    try:
        if value is None:
            return None
        try:
            if pd.isna(value):
                return None
        except Exception:
            pass
        text_value = safe_text(value).strip()
        if not text_value:
            return None
        parsed = pd.to_datetime(text_value, errors="coerce")
        if pd.isna(parsed):
            return None
        return parsed.to_pydatetime()
    except Exception:
        return None


def _v47_project_start_date(project_id):
    """Use project kickoff date first, then allocation start date as fallback."""
    project_id = safe_text(project_id).strip()
    if not project_id:
        return None

    try:
        projects = read_simple_table("projects", PROJECT_COLUMNS)
        if projects is not None and not projects.empty and "project_id" in projects.columns:
            match = projects[projects["project_id"].astype(str) == project_id]
            if not match.empty:
                project = match.iloc[0]
                for col in ["kickoff_date", "created_at", "updated_at"]:
                    parsed = _v47_dt(project.get(col))
                    if parsed:
                        return parsed
    except Exception:
        pass

    date_values = []
    try:
        allocations = get_project_allocations(project_id)
        if allocations is not None and not allocations.empty:
            for _, alloc in allocations.iterrows():
                for col in ["start_date", "assigned_at", "created_at"]:
                    parsed = _v47_dt(alloc.get(col))
                    if parsed:
                        date_values.append(parsed)
    except Exception:
        pass
    return min(date_values) if date_values else None


def _v47_week_number_from_dates(start_dt, reference_dt):
    if not start_dt:
        return 1
    reference_dt = reference_dt or datetime.now()
    days = max(0, (reference_dt.date() - start_dt.date()).days)
    return max(1, int(days // 7) + 1)


def _v47_friday_for_week_start(week_start_date):
    try:
        return week_start_date + timedelta(days=(4 - week_start_date.weekday()) % 7)
    except Exception:
        return week_start_date


def get_project_week_info(project_id, reference_date=""):
    """Return project-relative Week N details for a date.

    Week 1 starts on project kickoff date and includes days 0-6. Week 2 starts
    on day 7, and so on. The checkpoint date is the Friday inside that week.
    """
    start_dt = _v47_project_start_date(project_id)
    ref_dt = _v47_dt(reference_date) or datetime.now()
    if not start_dt:
        return {
            "week_number": 1,
            "week_label": "Week 1",
            "latest_update_week_number": 1,
            "latest_update_week_label": "Week 1",
            "week_start": "",
            "week_end": "",
            "friday_checkpoint": "",
            "start_label": "not captured",
            "reference_label": ref_dt.strftime("%Y-%m-%d"),
        }

    week_number = _v47_week_number_from_dates(start_dt, ref_dt)
    current_week = _v47_week_number_from_dates(start_dt, datetime.now())
    week_start_date = start_dt.date() + timedelta(days=(week_number - 1) * 7)
    week_end_date = week_start_date + timedelta(days=6)
    friday_date = _v47_friday_for_week_start(week_start_date)

    return {
        "week_number": current_week,
        "week_label": f"Week {current_week}",
        "latest_update_week_number": week_number,
        "latest_update_week_label": f"Week {week_number}",
        "week_start": week_start_date.strftime("%Y-%m-%d"),
        "week_end": week_end_date.strftime("%Y-%m-%d"),
        "friday_checkpoint": friday_date.strftime("%Y-%m-%d"),
        "start_label": start_dt.strftime("%Y-%m-%d"),
        "reference_label": ref_dt.strftime("%Y-%m-%d"),
    }


def _v47_current_week_window(project_id):
    start_dt = _v47_project_start_date(project_id)
    info = get_project_week_info(project_id, datetime.now())
    if not start_dt:
        today = datetime.now().date()
        return info, today, today + timedelta(days=6)
    week_number = safe_int(info.get("week_number"), 1)
    week_start = start_dt.date() + timedelta(days=(week_number - 1) * 7)
    week_end = week_start + timedelta(days=6)
    return info, week_start, week_end


def _v47_update_in_project_week(project_id, update_row, week_start, week_end):
    created = _v47_dt(update_row.get("created_at"))
    if not created:
        return False
    return week_start <= created.date() <= week_end


def _v47_latest_update_for_employee(project_id, employee_id, *, current_week_only=False):
    updates = get_employee_project_updates(project_id=project_id, employee_id=employee_id)
    if updates is None or updates.empty:
        return None, 0
    working = updates.copy()
    if "created_at" in working.columns:
        working["_created_dt"] = pd.to_datetime(working["created_at"], errors="coerce")
        working = working.sort_values("_created_dt", ascending=False)
    if not current_week_only:
        return working.iloc[0], len(working)
    _, week_start, week_end = _v47_current_week_window(project_id)
    in_week = []
    for _, row in working.iterrows():
        if _v47_update_in_project_week(project_id, row, week_start, week_end):
            in_week.append(row)
    if not in_week:
        return None, 0
    return in_week[0], len(in_week)


def _v47_employee_week_rows(project_id):
    """Build current-week mandatory update status rows for the project team."""
    try:
        allocations = get_project_allocations(project_id)
    except Exception:
        allocations = pd.DataFrame()
    if allocations is None or allocations.empty:
        return [], get_project_week_info(project_id, datetime.now())

    info, week_start, week_end = _v47_current_week_window(project_id)
    rows = []
    for _, alloc in allocations.iterrows():
        status_text = safe_text(alloc.get("allocation_status"), "Active").strip().lower()
        if status_text and status_text not in ["active", "assigned", "in progress", "approved"]:
            continue
        emp_id = safe_text(alloc.get("employee_id")).upper()
        latest_this_week, count_this_week = _v47_latest_update_for_employee(project_id, emp_id, current_week_only=True)
        latest_any, _ = _v47_latest_update_for_employee(project_id, emp_id, current_week_only=False)

        if latest_this_week is not None:
            last_row = latest_this_week
            update_week = get_project_week_info(project_id, last_row.get("created_at"))
            mandatory_status = "Updated"
            this_week_status = safe_text(last_row.get("progress_status"), "Submitted")
            progress_text = (safe_text(last_row.get("progress_percent")) + "%") if safe_text(last_row.get("progress_percent")) else "Submitted"
            updated_at = safe_text(last_row.get("created_at"))
            issue_text = safe_text(last_row.get("support_needed")).strip() or safe_text(last_row.get("hurdles")).strip() or safe_text(last_row.get("notes")).strip() or "No issue mentioned"
        else:
            last_row = latest_any
            update_week = get_project_week_info(project_id, last_row.get("created_at")) if last_row is not None else info
            mandatory_status = "Pending weekly update"
            this_week_status = "Not submitted"
            progress_text = "Not submitted"
            updated_at = ""
            issue_text = "No current-week update submitted"

        rows.append({
            "Employee": safe_text(alloc.get("employee_name")) or emp_id,
            "Employee ID": emp_id,
            "Project role": safe_text(alloc.get("project_role")),
            "Module / work area": safe_text(alloc.get("assigned_module")),
            "Current project week": info.get("week_label"),
            "Week start": info.get("week_start"),
            "Friday checkpoint": info.get("friday_checkpoint"),
            "Updates this week": int(count_this_week),
            "Mandatory status": mandatory_status,
            "This week's submitted status": this_week_status,
            "This week's progress": progress_text,
            "Last update time": updated_at,
            "Last updated week": update_week.get("latest_update_week_label") if last_row is not None else "No update yet",
            "Request / note": issue_text,
        })
    return rows, info


def _v47_project_week_status_counts(project_id):
    rows, info = _v47_employee_week_rows(project_id)
    required = len(rows)
    updated = sum(1 for row in rows if safe_text(row.get("Mandatory status")) == "Updated")
    pending = max(0, required - updated)
    return {
        "required": required,
        "updated": updated,
        "pending": pending,
        "info": info,
        "rows": rows,
    }


def render_project_week_status_panel(project_id, *, title="Current week update status", expanded=True, client_safe=False, key_prefix="project_week_status"):
    """Render mandatory weekly update status for the current project week."""
    project_id = safe_text(project_id)
    if not project_id:
        return
    counts = _v47_project_week_status_counts(project_id)
    info = counts.get("info", {})
    rows = counts.get("rows", [])
    with st.expander(title, expanded=expanded):
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Project week", info.get("week_label", "Week 1"))
        c2.metric("Week window", f"{info.get('week_start', '-') } to {info.get('week_end', '-')}")
        c3.metric("Friday checkpoint", info.get("friday_checkpoint", "-"))
        c4.metric("Mandatory updates", f"{counts.get('updated', 0)} / {counts.get('required', 0)}")

        if counts.get("pending", 0):
            st.warning(f"{counts.get('pending')} team member(s) have not submitted the {info.get('week_label', 'current week')} status yet.")
        elif counts.get("required", 0):
            st.success(f"All allocated team members have submitted at least one update for {info.get('week_label', 'this week')}.")
        else:
            st.info("Team allocation is not available yet.")

        if client_safe:
            st.caption("This is a client-safe summary. Internal employee names, blockers, and comments are not shown here.")
            return

        if rows:
            df = pd.DataFrame(rows)
            st.dataframe(df, use_container_width=True, hide_index=True)


def get_client_safe_project_progress(project_id):
    """Client-safe current-week progress with project-relative week details."""
    project_id = safe_text(project_id)
    counts = _v47_project_week_status_counts(project_id)
    info = counts.get("info", get_project_week_info(project_id, datetime.now()))
    rows = counts.get("rows", [])

    current_week_values = []
    latest_times = []
    latest_status = "Team work is going on"
    for row in rows:
        if safe_text(row.get("Mandatory status")) != "Updated":
            continue
        progress_text = safe_text(row.get("This week's progress")).replace("%", "")
        value = safe_number(progress_text, None)
        if value is not None:
            current_week_values.append(max(0, min(100, value)))
        if safe_text(row.get("Last update time")):
            latest_times.append(safe_text(row.get("Last update time")))
        if safe_text(row.get("This week's submitted status")) and safe_text(row.get("This week's submitted status")) != "Not submitted":
            latest_status = safe_text(row.get("This week's submitted status"))

    if current_week_values:
        pct = f"{round(sum(current_week_values) / len(current_week_values))}%"
    else:
        pct = "Not updated yet"

    latest_at = max(latest_times) if latest_times else ""
    return {
        "weekly_progress_percent": pct,
        "progress_percent": pct,
        "status": latest_status,
        "updated_at": latest_at,
        "project_week_label": info.get("week_label", "Week 1"),
        "week_start": info.get("week_start", ""),
        "week_end": info.get("week_end", ""),
        "friday_checkpoint": info.get("friday_checkpoint", ""),
        "mandatory_updates_required": counts.get("required", 0),
        "mandatory_updates_received": counts.get("updated", 0),
        "mandatory_updates_pending": counts.get("pending", 0),
    }


def save_employee_project_update(alloc, user, progress_status, progress_percent, hurdles, support_needed, notes):
    """Save employee update with project-relative week label."""
    now = current_timestamp()
    project_id = safe_text(alloc.get("project_id"))
    proposal_id = safe_text(alloc.get("proposal_id"))
    module = safe_text(alloc.get("assigned_module"))
    status_text = safe_text(progress_status)
    hurdles_text = safe_text(hurdles).strip()
    support_text = safe_text(support_needed).strip()
    notes_text = safe_text(notes).strip()
    week_info = get_project_week_info(project_id, now)
    project_week_label = week_info.get("latest_update_week_label") or week_info.get("week_label") or "Week 1"

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
        "week_label": project_week_label,
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
        f"Technical Architect Agent alert: {actor_name(user)} submitted {project_week_label} status for project {project_id}, "
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
                f"{project_week_label}: {status_text}; {safe_text(progress_percent)}% complete. "
                f"Technical Architect Agent assessment: {agent_review.get('urgency')} - {agent_review.get('problem_summary')}"
            ),
            summary=f"{actor_name(user)} shared {project_week_label} status for {module or project_id}. Technical Architect was notified with AI assessment.",
        )
    except Exception:
        pass

    notify_proposal_lifecycle_change(
        proposal_id,
        user=user,
        summary=(
            f"New {project_week_label} employee update/request from {actor_name(user)} for project {project_id}. "
            f"Status: {status_text}; progress {safe_text(progress_percent)}%."
        ),
        notify_actor=False,
    )

    if recipients:
        return True, f"Thanks. Your {project_week_label} update/request was saved. The Technical Architect Agent has been notified and will connect with you soon if follow-up is needed."
    return True, f"Thanks. Your {project_week_label} update/request was saved. Technical Architect can review it in the delivery dashboard and will connect with you soon if follow-up is needed."


def generate_weekly_update_if_needed(project, delivery_plan, allocations):
    """Create one client-safe weekly update per project-relative week."""
    updates = read_simple_table("weekly_project_updates", WEEKLY_UPDATE_COLUMNS)
    project_id = safe_text(project.get("project_id"))
    week_info = get_project_week_info(project_id, datetime.now())
    week = week_info.get("week_label", "Week 1")
    if not updates.empty:
        matched = updates[(updates["project_id"].astype(str) == project_id) & (updates["week_label"].astype(str) == week)]
        if not matched.empty:
            return matched.iloc[0].to_dict()

    counts = _v47_project_week_status_counts(project_id)
    allocation_count = 0 if allocations is None or allocations.empty else len(allocations)
    plan_status = safe_text(delivery_plan.get("approval_status"), "Planning") if delivery_plan else "Planning"
    progress = get_client_safe_project_progress(project_id)
    update_text = (
        f"Hi, hope you are doing well. This is the {week} delivery update. "
        f"Current delivery status: {safe_text(project.get('project_status'), 'Planning')}. "
        f"Delivery plan status: {plan_status}. Team allocation count: {allocation_count}. "
        f"Mandatory team updates received: {counts.get('updated', 0)} of {counts.get('required', 0)}. "
        f"Average current-week progress: {progress.get('weekly_progress_percent')}. "
        f"The weekly checkpoint date is {week_info.get('friday_checkpoint') or 'this Friday'}."
    )
    row = {
        "update_id": make_weekly_update_id(),
        "project_id": project_id,
        "proposal_id": safe_text(project.get("proposal_id")),
        "client_id": safe_text(project.get("client_id")),
        "week_label": week,
        "update_text": update_text,
        "blockers": "No client-visible blocker recorded",
        "client_action_needed": "Share requirement changes or clarifications with Technical Architect if any",
        "generated_by": "Technical Architect Agent",
        "generated_at": current_timestamp(),
        "published_by": "Technical Architect Agent",
        "visible_to_client": "Yes",
    }
    upsert_simple_row("weekly_project_updates", "update_id", WEEKLY_UPDATE_COLUMNS, row)
    return row


try:
    _v47_previous_render_client_delivery_section = render_client_delivery_section
except Exception:
    _v47_previous_render_client_delivery_section = None


def render_client_delivery_section(report, client_account):
    """Client delivery view with project-week number and client-safe update counts."""
    if _v47_previous_render_client_delivery_section is not None:
        _v47_previous_render_client_delivery_section(report, client_account)
    try:
        if safe_text(report.get("client_response")) != "Accept Proposal":
            return
        project = get_project_for_proposal(report.get("proposal_id")) or ensure_project_for_accepted_proposal(report, client_account)
        project_id = safe_text(project.get("project_id"))
        plan = get_delivery_plan_for_client_project(project_id)
        status = safe_text(plan.get("approval_status") if plan else "")
        if status not in ["Approved by Technical Architect Agent", "Approved by Operations Manager"]:
            return
        progress = get_client_safe_project_progress(project_id)
        with st.expander("Project week and mandatory update summary", expanded=True):
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Project week", progress.get("project_week_label", "Week 1"))
            c2.metric("Week window", f"{progress.get('week_start', '-') } to {progress.get('week_end', '-')}")
            c3.metric("Friday checkpoint", progress.get("friday_checkpoint", "-"))
            c4.metric("Team updates", f"{progress.get('mandatory_updates_received', 0)} / {progress.get('mandatory_updates_required', 0)}")
            if safe_int(progress.get("mandatory_updates_pending"), 0) > 0:
                st.info("Some internal team updates are still pending for this project week. The delivery team is following up internally.")
            else:
                st.success("All mandatory internal team updates are submitted for this project week.")
            st.caption("This summary is client-safe and does not expose internal employee names, blockers, salaries, or private notes.")
    except Exception:
        return


def render_employee_project_workbench(user):
    """Employee workbench with mandatory project-week status update checks."""
    emp_id = safe_text(user.get("user_id")).upper()
    allocations = get_employee_allocations(emp_id)
    notifications = get_employee_notifications(emp_id)

    if allocations.empty:
        st.markdown(
            """
            <div class="dd-section-card">
                <div class="dd-section-title">My live project workbench</div>
                <div class="dd-section-subtitle">
                    No live project allocation is assigned to you yet.
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
                Choose a live project. For each project, submit at least one update for the current project week.
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
        week_info = get_project_week_info(project_id, datetime.now())
        latest_this_week, count_this_week = _v47_latest_update_for_employee(project_id, emp_id, current_week_only=True)
        status_hint = "updated" if count_this_week else "pending update"
        labels.append(f"{idx}. {project_display_name(project_id=project_id)} | {role} | {module} | {week_info.get('week_label')} {status_hint}")
        rows.append(alloc_row)

    selected_label = st.selectbox(
        f"Open live project ({len(labels)} assigned project(s))",
        labels,
        key=f"emp_live_project_selector_{emp_id}",
    )
    employee_project_memory_key = f"_dd_last_employee_project_selection_{emp_id}"
    previous_employee_project = st.session_state.get(employee_project_memory_key)
    if previous_employee_project is not None and selected_label != previous_employee_project:
        try:
            request_page_scroll("selected_project_detail")
        except Exception:
            st.session_state["_dd_scroll_target"] = "selected_project_detail"
    st.session_state[employee_project_memory_key] = selected_label

    alloc = rows[labels.index(selected_label)]
    project_id = safe_text(alloc.get("project_id"))
    st.markdown('<div id="dd-selected-project-detail"></div>', unsafe_allow_html=True)
    ack_key = f"emp_update_sent_ack_{safe_text(alloc.get('allocation_id'))}"
    week_info = get_project_week_info(project_id, datetime.now())
    latest_this_week, count_this_week = _v47_latest_update_for_employee(project_id, emp_id, current_week_only=True)

    if st.session_state.get(ack_key, False):
        st.success(f"Your {week_info.get('week_label', 'current week')} update/request has been sent to the Technical Architect Agent.")
        st.info("Technical Architect Agent will connect with you soon if follow-up is needed.")
        if st.button("Send another update for this project", key=f"emp_send_another_{alloc.get('allocation_id')}"):
            st.session_state[ack_key] = False
            st.rerun()
        return

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Project", project_display_name(project_id=project_id, fallback="Live project"))
    c2.metric("My role", safe_text(alloc.get("project_role")) or "Assigned")
    c3.metric("Module", safe_text(alloc.get("assigned_module")) or "Project work")
    c4.metric("Current project week", week_info.get("week_label", "Week 1"))
    st.caption(f"Week window: {week_info.get('week_start', '-')} to {week_info.get('week_end', '-')} | Friday checkpoint: {week_info.get('friday_checkpoint', '-')}")

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
                height=170,
                disabled=True,
                key=f"emp_customer_requirement_{alloc.get('allocation_id')}",
            )
        else:
            st.info("Customer requirement is not available yet.")
        if agent_conclusion:
            st.text_area(
                "Technical Architect Agent conclusion on the requirement",
                value=agent_conclusion,
                height=190,
                disabled=True,
                key=f"emp_agent_conclusion_{alloc.get('allocation_id')}",
            )
        else:
            st.info("Technical Architect Agent conclusion is not available yet.")
    else:
        st.info("Delivery requirement and Technical Architect Agent conclusion are not available yet for this project.")

    st.markdown("#### Mandatory weekly progress, blocker, and resource request")
    if count_this_week:
        st.success(f"{week_info.get('week_label', 'This week')} status already submitted. You can submit again if progress, blocker, or support need changed.")
        if latest_this_week is not None:
            st.caption(
                f"Latest {week_info.get('week_label', 'current week')} update: "
                f"{safe_text(latest_this_week.get('created_at'))} | "
                f"{safe_text(latest_this_week.get('progress_status'))} | "
                f"{safe_text(latest_this_week.get('progress_percent'))}%"
            )
    else:
        st.warning(
            f"Mandatory: {week_info.get('week_label', 'current week')} status update is pending. "
            f"Submit at least one update for this week by the Friday checkpoint."
        )

    with st.form(key=f"employee_weekly_update_{alloc.get('allocation_id')}_{week_info.get('week_label', 'week').replace(' ', '_')}"):
        u1, u2 = st.columns([1, 1])
        with u1:
            status = st.selectbox(
                f"How is the project doing in {week_info.get('week_label', 'this week')}?",
                ["On track", "Minor risk", "Blocked", "Ahead of plan"],
                key=f"emp_status_{alloc.get('allocation_id')}_{week_info.get('week_label', 'week')}",
            )
        with u2:
            progress = st.slider(
                "How much of your weekly target is completed?",
                min_value=0,
                max_value=100,
                value=70,
                step=5,
                key=f"emp_progress_{alloc.get('allocation_id')}_{week_info.get('week_label', 'week')}",
            )
        hurdles = st.text_area(
            "Any blockers, problems, hurdles, or dependencies?",
            placeholder="Example: waiting for API access, client sample data, cloud permission, review feedback...",
            key=f"emp_hurdles_{alloc.get('allocation_id')}_{week_info.get('week_label', 'week')}",
        )
        support = st.text_area(
            "Any extra resource, access, backup support, or clarification needed?",
            placeholder="Example: need DevOps help, database access, QA support, extra engineer, client clarification...",
            key=f"emp_support_{alloc.get('allocation_id')}_{week_info.get('week_label', 'week')}",
        )
        notes = st.text_area(
            "Short summary for Technical Architect Agent",
            placeholder="Example: Completed authentication flow; integration work is pending sample data from client.",
            key=f"emp_notes_{alloc.get('allocation_id')}_{week_info.get('week_label', 'week')}",
        )
        submitted = st.form_submit_button(f"Submit {week_info.get('week_label', 'weekly')} update", type="primary")

    if submitted:
        ok, msg = save_employee_project_update(alloc, user, status, progress, hurdles, support, notes)
        if ok:
            st.session_state[ack_key] = True
            try:
                request_page_scroll("selected_project_detail")
            except Exception:
                st.session_state["_dd_scroll_target"] = "selected_project_detail"
            st.rerun()
        else:
            st.error(msg)

    updates = get_employee_project_updates(project_id=project_id, employee_id=emp_id)
    if updates is not None and not updates.empty:
        with st.expander("Previous updates for this project", expanded=False):
            working_updates = updates.copy()
            if "created_at" in working_updates.columns:
                working_updates = working_updates.sort_values("created_at", ascending=False)
            history_rows = []
            for _, upd in working_updates.iterrows():
                upd_week = get_project_week_info(project_id, upd.get("created_at"))
                history_rows.append({
                    "Project week": upd_week.get("latest_update_week_label"),
                    "Submitted at": safe_text(upd.get("created_at")),
                    "Status": safe_text(upd.get("progress_status")),
                    "Progress": (safe_text(upd.get("progress_percent")) + "%") if safe_text(upd.get("progress_percent")) else "",
                    "Hurdles": safe_text(upd.get("hurdles")),
                    "Support needed": safe_text(upd.get("support_needed")),
                    "Notes": safe_text(upd.get("notes")),
                })
            if history_rows:
                st.dataframe(pd.DataFrame(history_rows), use_container_width=True, hide_index=True)


try:
    _v47_previous_render_operations_delivery_workspace = render_operations_delivery_workspace
except Exception:
    _v47_previous_render_operations_delivery_workspace = None


def render_operations_delivery_workspace(user, data, focus_proposal_id=None):
    """Technical Architect workspace plus current project-week update matrix."""
    if _v47_previous_render_operations_delivery_workspace is not None:
        _v47_previous_render_operations_delivery_workspace(user, data, focus_proposal_id=focus_proposal_id)
    try:
        project = get_project_for_proposal(focus_proposal_id) if focus_proposal_id else None
        if project:
            render_project_week_status_panel(
                project.get("project_id"),
                title="Current project week update status - Technical Architect view",
                expanded=True,
                client_safe=False,
                key_prefix=f"ops_project_week_status_{safe_text(project.get('project_id'))}",
            )
    except Exception:
        pass


try:
    _v47_previous_ceo_activity_panels = _dd_render_ceo_live_activity_panels
except Exception:
    _v47_previous_ceo_activity_panels = None


def _dd_render_ceo_live_activity_panels(report):
    """CEO live monitor with project-week update visibility."""
    if not isinstance(report, dict):
        return
    project = get_project_for_proposal(report.get("proposal_id"))
    if not project:
        return

    project_id = safe_text(project.get("project_id"))
    proposal_id = safe_text(project.get("proposal_id") or report.get("proposal_id"))
    plan = get_delivery_plan_for_client_project(project_id)
    progress = get_client_safe_project_progress(project_id)

    st.markdown(
        """
        <div class="dd-section-card dd-dashboard-shell">
            <div class="dd-section-eyebrow">CEO project monitor</div>
            <div class="dd-section-title">Live project activity</div>
            <div class="dd-section-subtitle">
                CEO view includes project-week status, weekly targets, team updates, client messages, and Technical Architect actions after kickoff.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    a1, a2, a3, a4 = st.columns(4)
    a1.metric("Project status", safe_text(project.get("project_status"), "In progress"))
    a2.metric("Delivery plan", safe_text(plan.get("approval_status") if plan else "Pending"))
    a3.metric("Current project week", progress.get("project_week_label", "Week 1"))
    a4.metric("Team weekly updates", f"{progress.get('mandatory_updates_received', 0)} / {progress.get('mandatory_updates_required', 0)}")
    st.caption(
        f"Week window: {progress.get('week_start', '-') } to {progress.get('week_end', '-')} | "
        f"Friday checkpoint: {progress.get('friday_checkpoint', '-')} | "
        f"Project: {project_display_name(project=project, project_id=project_id)}"
    )

    render_project_week_status_panel(
        project_id,
        title="Current project week mandatory update status - CEO view",
        expanded=True,
        client_safe=False,
        key_prefix=f"ceo_project_week_status_{project_id}",
    )

    if plan:
        render_weekly_targets_panel(
            plan,
            title="Weekly target list - CEO view",
            expanded=True,
            client_safe=False,
            key_prefix=f"ceo_activity_weekly_targets_{project_id}",
        )

    messages = _dd_read_table_rows_safe(
        "client_operations_messages",
        CLIENT_OPERATIONS_MESSAGE_COLUMNS,
        filters={"project_id": project_id},
        sort_column="created_at",
        limit=10,
    )
    if not messages.empty:
        with st.expander("Recent client / Technical Architect messages", expanded=False):
            view_rows = []
            for _, row in messages.iterrows():
                view_rows.append({
                    "Time": safe_text(row.get("created_at")),
                    "Sender": safe_text(row.get("sender_name")) or safe_text(row.get("sender_type")),
                    "Type": safe_text(row.get("sender_type")),
                    "Message": safe_text(row.get("message_text")),
                })
            st.dataframe(pd.DataFrame(view_rows), use_container_width=True, hide_index=True)
    else:
        st.caption("No client / Technical Architect messages have been recorded for this project yet.")

    weekly_updates = _dd_read_table_rows_safe(
        "weekly_project_updates",
        WEEKLY_UPDATE_COLUMNS,
        filters={"project_id": project_id},
        sort_column="generated_at",
        limit=10,
    )
    if not weekly_updates.empty:
        with st.expander("Published weekly client updates", expanded=False):
            rows = []
            for _, row in weekly_updates.iterrows():
                update_week = safe_text(row.get("week_label")) or get_project_week_info(project_id, row.get("generated_at")).get("latest_update_week_label")
                rows.append({
                    "Project week": update_week,
                    "Generated at": safe_text(row.get("generated_at")),
                    "Update": safe_text(row.get("update_text")),
                    "Client action needed": safe_text(row.get("client_action_needed")),
                })
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.caption("No weekly client update has been published yet.")

    employee_updates = get_employee_project_updates(project_id=project_id)
    if employee_updates is not None and not employee_updates.empty:
        with st.expander("All employee weekly updates and requests", expanded=False):
            working = employee_updates.copy()
            if "created_at" in working.columns:
                working = working.sort_values("created_at", ascending=False)
            rows = []
            for _, row in working.head(30).iterrows():
                issue = (
                    safe_text(row.get("support_needed")).strip()
                    or safe_text(row.get("hurdles")).strip()
                    or safe_text(row.get("notes")).strip()
                    or "No issue mentioned"
                )
                update_week = get_project_week_info(project_id, row.get("created_at"))
                rows.append({
                    "Project week": update_week.get("latest_update_week_label"),
                    "Submitted at": safe_text(row.get("created_at")),
                    "Employee": safe_text(row.get("employee_name")),
                    "Status": safe_text(row.get("progress_status")),
                    "Progress": (safe_text(row.get("progress_percent")) + "%") if safe_text(row.get("progress_percent")) else "",
                    "Module": safe_text(row.get("assigned_module")),
                    "Request / note": issue,
                    "Technical Architect status": safe_text(row.get("operations_status"), "Open"),
                })
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.info("No employee updates or requests are recorded yet for this project.")

# Keep review button behavior decision-safe. Only informational lifecycle updates
# can be marked as reviewed; proposal decision and Technical Architect action
# items remain in the pending inbox until the appropriate action is completed.

# -----------------------------------------------------------------------------
# V48 PATCH: project week visibility for Client + Technical Architect,
# with employee dashboard kept private to the logged-in employee.
# -----------------------------------------------------------------------------
# Week numbering remains project-relative: Week 1 starts on kickoff/allocation
# start date and covers the first seven calendar days. Every employee update is
# mapped to the project week that contains its submitted timestamp.

try:
    _v48_previous_v47_project_start_date = _v47_project_start_date
except Exception:
    _v48_previous_v47_project_start_date = None


def _v47_project_start_date(project_id):
    """Project start date used for Week 1 calculation.

    Priority:
    1. Project kickoff date
    2. Earliest allocation start/assigned date
    3. Project created/updated date fallback
    """
    project_id = safe_text(project_id).strip()
    if not project_id:
        return None

    project_row = None
    try:
        projects = read_simple_table("projects", PROJECT_COLUMNS)
        if projects is not None and not projects.empty and "project_id" in projects.columns:
            match = projects[projects["project_id"].astype(str) == project_id]
            if not match.empty:
                project_row = match.iloc[0]
                kickoff = _v47_dt(project_row.get("kickoff_date"))
                if kickoff:
                    return kickoff
    except Exception:
        project_row = None

    allocation_dates = []
    try:
        allocations = get_project_allocations(project_id)
        if allocations is not None and not allocations.empty:
            for _, alloc in allocations.iterrows():
                for col in ["start_date", "assigned_at", "created_at"]:
                    parsed = _v47_dt(alloc.get(col))
                    if parsed:
                        allocation_dates.append(parsed)
    except Exception:
        pass
    if allocation_dates:
        return min(allocation_dates)

    if project_row is not None:
        for col in ["created_at", "updated_at"]:
            parsed = _v47_dt(project_row.get(col))
            if parsed:
                return parsed

    if _v48_previous_v47_project_start_date is not None:
        try:
            return _v48_previous_v47_project_start_date(project_id)
        except Exception:
            return None
    return None


def _v48_project_week_summary_values(project_id):
    counts = _v47_project_week_status_counts(project_id)
    info = counts.get("info", get_project_week_info(project_id, datetime.now()))
    progress = get_client_safe_project_progress(project_id)
    return counts, info, progress


def render_client_visible_project_week_card(project_id, *, title="Project week status", key_prefix="client_project_week_card"):
    """Always-visible client-safe week summary.

    This shows Week 1 / Week 2 etc. directly in the client dashboard without
    exposing employee names, internal blockers, salary, margin, or private notes.
    """
    project_id = safe_text(project_id).strip()
    if not project_id:
        return
    counts, info, progress = _v48_project_week_summary_values(project_id)
    st.markdown(f"### {title}")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Current project week", info.get("week_label", progress.get("project_week_label", "Week 1")))
    c2.metric("Week window", f"{info.get('week_start', progress.get('week_start', '-'))} to {info.get('week_end', progress.get('week_end', '-'))}")
    c3.metric("Friday checkpoint", info.get("friday_checkpoint", progress.get("friday_checkpoint", "-")))
    c4.metric("Team updates", f"{counts.get('updated', progress.get('mandatory_updates_received', 0))} / {counts.get('required', progress.get('mandatory_updates_required', 0))}")

    latest_update = safe_text(progress.get("updated_at"))
    if latest_update:
        st.caption(f"Latest client-safe team progress update received for {info.get('week_label', 'this week')}: {latest_update}")
    else:
        st.caption(f"No team progress update has been submitted yet for {info.get('week_label', 'this week')}.")

    pending = safe_int(counts.get("pending", progress.get("mandatory_updates_pending", 0)), 0)
    if pending:
        st.info(f"{pending} internal team update(s) are pending for {info.get('week_label', 'the current project week')}. The delivery team is following up internally.")
    elif safe_int(counts.get("required", 0), 0):
        st.success(f"All required team updates are submitted for {info.get('week_label', 'the current project week')}.")
    else:
        st.info("Team allocation is not finalized yet, so weekly update counts will appear after allocation.")
    st.caption("Client-safe view: employee names, internal blockers, salary, margin, and private notes are hidden.")


try:
    _v48_previous_render_client_delivery_section = render_client_delivery_section
except Exception:
    _v48_previous_render_client_delivery_section = None


def render_client_delivery_section(report, client_account):
    """Client delivery section with visible project Week N summary."""
    if _v48_previous_render_client_delivery_section is not None:
        _v48_previous_render_client_delivery_section(report, client_account)

    try:
        if safe_text(report.get("client_response")) != "Accept Proposal":
            return
        project = get_project_for_proposal(report.get("proposal_id")) or ensure_project_for_accepted_proposal(report, client_account)
        project_id = safe_text(project.get("project_id"))
        if not project_id:
            return
        plan = get_delivery_plan_for_client_project(project_id)
        plan_status = safe_text(plan.get("approval_status") if plan else "").lower()
        project_status = safe_text(project.get("project_status")).lower()
        if not any(word in (plan_status + " " + project_status) for word in ["approved", "allocated", "in progress", "delivery", "active", "kickoff"]):
            return
        render_client_visible_project_week_card(
            project_id,
            title="Current project week and update status",
            key_prefix=f"client_visible_week_{project_id}",
        )
    except Exception:
        return


def _v48_project_week_label_for_project_row(project_row):
    project_id = safe_text(project_row.get("project_id")) if hasattr(project_row, "get") else ""
    if not project_id:
        return "Week 1"
    return get_project_week_info(project_id, datetime.now()).get("week_label", "Week 1")


def _v48_active_delivery_projects(focus_proposal_id=None):
    try:
        projects = read_simple_table("projects", PROJECT_COLUMNS)
    except Exception:
        return pd.DataFrame(columns=PROJECT_COLUMNS)
    if projects is None or projects.empty:
        return pd.DataFrame(columns=PROJECT_COLUMNS)

    working = projects.copy()
    if focus_proposal_id:
        working = working[working["proposal_id"].astype(str) == safe_text(focus_proposal_id)]
    if working.empty:
        return working

    if "project_status" in working.columns:
        status = working["project_status"].fillna("").astype(str).str.lower()
        closed_words = ["closed", "cancelled", "canceled", "declined", "rejected"]
        keep = ~status.apply(lambda value: any(word in value for word in closed_words))
        working = working[keep]
    if working.empty:
        return working

    sort_col = "updated_at" if "updated_at" in working.columns else "created_at" if "created_at" in working.columns else "project_id"
    try:
        working = working.sort_values(sort_col, ascending=False)
    except Exception:
        pass
    return working


def render_technical_architect_project_week_overview(user, data=None, focus_proposal_id=None):
    """Technical Architect view of Week N status for active delivery projects."""
    if role_key_for_user(user) != "operations":
        return
    projects = _v48_active_delivery_projects(focus_proposal_id=focus_proposal_id)
    if projects is None or projects.empty:
        return

    st.markdown("### Project week status - Technical Architect view")
    st.caption("Each allocated employee must submit at least one status update for the current project week. Week numbers are calculated from kickoff date first, then allocation start date if kickoff is not captured.")

    rows = []
    labels = []
    row_by_label = {}
    for idx, (_, project) in enumerate(projects.iterrows(), start=1):
        project_id = safe_text(project.get("project_id"))
        counts, info, _ = _v48_project_week_summary_values(project_id)
        label = (
            f"{idx}. {project_display_name(project=project, project_id=project_id)} | "
            f"{info.get('week_label', 'Week 1')} | updates {counts.get('updated', 0)}/{counts.get('required', 0)}"
        )
        labels.append(label)
        row_by_label[label] = project
        rows.append({
            "Project": project_display_name(project=project, project_id=project_id),
            "Current project week": info.get("week_label", "Week 1"),
            "Week start": info.get("week_start", ""),
            "Week end": info.get("week_end", ""),
            "Friday checkpoint": info.get("friday_checkpoint", ""),
            "Mandatory updates": f"{counts.get('updated', 0)} / {counts.get('required', 0)}",
            "Pending updates": counts.get("pending", 0),
        })

    if rows:
        with st.expander("Active project week summary", expanded=False):
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    if not labels:
        return
    if focus_proposal_id and len(labels) == 1:
        selected_project = row_by_label[labels[0]]
    else:
        selected_label = st.selectbox(
            "Choose project to inspect Week 1 / Week 2 status",
            labels,
            key=f"ta_week_project_selector_{actor_id(user)}_{safe_text(focus_proposal_id) or 'all'}",
        )
        ta_project_memory_key = f"_dd_last_ta_week_project_selection_{actor_id(user)}_{safe_text(focus_proposal_id) or 'all'}"
        previous_ta_project = st.session_state.get(ta_project_memory_key)
        if previous_ta_project is not None and selected_label != previous_ta_project:
            try:
                request_page_scroll("ta_project_week_detail")
            except Exception:
                st.session_state["_dd_scroll_target"] = "ta_project_week_detail"
        st.session_state[ta_project_memory_key] = selected_label
        selected_project = row_by_label[selected_label]

    selected_project_id = safe_text(selected_project.get("project_id"))
    st.markdown('<div id="dd-ta-selected-week-project-detail"></div>', unsafe_allow_html=True)
    render_project_week_status_panel(
        selected_project_id,
        title=f"Current project week update matrix - {project_display_name(project=selected_project, project_id=selected_project_id)}",
        expanded=True,
        client_safe=False,
        key_prefix=f"ta_week_matrix_{selected_project_id}",
    )
    plan = get_delivery_plan_for_client_project(selected_project_id)
    if plan:
        render_weekly_targets_panel(
            plan,
            title="Weekly targets for selected project",
            expanded=False,
            client_safe=False,
            key_prefix=f"ta_week_targets_{selected_project_id}",
        )
    try:
        run_pending_page_scroll()
    except Exception:
        pass


try:
    _v48_previous_render_operations_delivery_workspace = render_operations_delivery_workspace
except Exception:
    _v48_previous_render_operations_delivery_workspace = None


def render_operations_delivery_workspace(user, data, focus_proposal_id=None):
    """Technical Architect delivery workspace with visible Week N overview."""
    if _v48_previous_render_operations_delivery_workspace is not None:
        _v48_previous_render_operations_delivery_workspace(user, data, focus_proposal_id=focus_proposal_id)
    try:
        render_technical_architect_project_week_overview(user, data=data, focus_proposal_id=focus_proposal_id)
    except Exception as exc:
        st.caption(f"Project week status is not available right now: {exc}")

# Employee privacy note: the employee project workbench already queries
# get_employee_project_updates(project_id=project_id, employee_id=logged_in_id),
# so an employee sees only their own assigned project context and their own
# submitted update history. CEO and Technical Architect views remain team-level.

# -----------------------------------------------------------------------------
# V49 TECHNICAL ARCHITECT DELIVERY VIEW CLEANUP
# -----------------------------------------------------------------------------
# Final late override for the Technical Architect / Operations workspace.
# Purpose:
# - Show current project week status immediately after the selected project card.
# - Remove duplicate project-week panels produced by older wrapper layers.
# - Keep weekly targets and team update status easy to read.
# - Preserve existing delivery, conversation, employee request, allocation, and
#   notification logic.


def _v49_project_week_status_first_panel(project_id, *, project_label="", key_prefix="ops_week_first"):
    """Readable non-duplicated Week N status block for Technical Architect view."""
    project_id = safe_text(project_id).strip()
    if not project_id:
        return
    try:
        counts = _v47_project_week_status_counts(project_id)
    except Exception:
        render_project_week_status_panel(
            project_id,
            title="Current project week update status",
            expanded=True,
            client_safe=False,
            key_prefix=key_prefix,
        )
        return

    info = counts.get("info", {}) or {}
    rows = counts.get("rows", []) or []
    week_label = safe_text(info.get("week_label"), "Week 1")
    week_start = safe_text(info.get("week_start"), "-")
    week_end = safe_text(info.get("week_end"), "-")
    friday = safe_text(info.get("friday_checkpoint"), "-")
    required = safe_int(counts.get("required", 0), 0)
    updated = safe_int(counts.get("updated", 0), 0)
    pending = safe_int(counts.get("pending", 0), 0)

    st.markdown(
        f"""
        <div class="dd-section-card dd-dashboard-shell">
            <div class="dd-section-eyebrow">Current week control point</div>
            <div class="dd-section-title">{week_label} update status</div>
            <div class="dd-section-subtitle">
                First check this section after selecting a project. Each allocated delivery employee must submit
                at least one status update in the current project week.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Project week", week_label)
    c2.metric("Week window", f"{week_start} to {week_end}")
    c3.metric("Friday checkpoint", friday)
    c4.metric("Mandatory updates", f"{updated} / {required}")

    if pending:
        st.warning(f"{pending} team member(s) have not submitted the {week_label} status yet.")
    elif required:
        st.success(f"All allocated team members have submitted at least one update for {week_label}.")
    else:
        st.info("Team allocation is not finalized yet. Weekly update counts will appear after employees are allocated.")

    if not rows:
        return

    updated_rows = []
    pending_rows = []
    full_rows = []
    for item in rows:
        clean_row = {
            "Employee": safe_text(item.get("Employee")),
            "Role": safe_text(item.get("Project role")),
            "Module": safe_text(item.get("Module / work area")),
            "Week": safe_text(item.get("Current project week")) or week_label,
            "Updates this week": safe_int(item.get("Updates this week"), 0),
            "Status": safe_text(item.get("Mandatory status")),
            "Progress": safe_text(item.get("This week's progress")),
            "Submitted status": safe_text(item.get("This week's submitted status")),
            "Last update": safe_text(item.get("Last update time")),
            "Request / note": safe_text(item.get("Request / note")),
        }
        full_rows.append(clean_row)
        if safe_text(item.get("Mandatory status")) == "Updated":
            updated_rows.append(clean_row)
        else:
            pending_rows.append({
                "Employee": clean_row["Employee"],
                "Role": clean_row["Role"],
                "Module": clean_row["Module"],
                "Week": clean_row["Week"],
                "Status needed": week_label,
                "Last updated week": safe_text(item.get("Last updated week")),
            })

    if updated_rows:
        with st.expander(f"Submitted in {week_label} ({len(updated_rows)})", expanded=True):
            st.dataframe(pd.DataFrame(updated_rows), use_container_width=True, hide_index=True)
    else:
        st.info(f"No employee has submitted a {week_label} update yet.")

    if pending_rows:
        with st.expander(f"Pending {week_label} updates ({len(pending_rows)})", expanded=True):
            st.dataframe(pd.DataFrame(pending_rows), use_container_width=True, hide_index=True)

    with st.expander("Full current-week update matrix", expanded=False):
        st.caption("This full matrix is kept for audit/reference. Long cells can be opened through the full-value viewer below the table.")
        st.dataframe(pd.DataFrame(full_rows), use_container_width=True, hide_index=True)


def _v49_select_delivery_project_row(user, merged, focus_proposal_id=None):
    """Render project selector and return the selected merged row."""
    if merged is None or merged.empty:
        return None
    if "created_at" in merged.columns:
        try:
            merged = merged.sort_values("created_at", ascending=False)
        except Exception:
            pass
    labels = []
    rows = []
    for idx, (_, row) in enumerate(merged.iterrows(), start=1):
        project_name = safe_text(row.get("project_name")) or safe_text(row.get("project_id")) or "Accepted client project"
        status = safe_text(row.get("approval_status")) or safe_text(row.get("project_status")) or "Waiting for review"
        created = safe_text(row.get("created_at")) or safe_text(row.get("updated_at")) or safe_text(row.get("created_at_project"))
        label = f"{idx}. {project_name} | {safe_text(row.get('project_id'))} - {status} - {created}"
        labels.append(label)
        rows.append(row)
    if not labels:
        return None

    selector_key = f"ops_delivery_selected_project_v49_{actor_id(user)}_{safe_text(focus_proposal_id) or 'all'}"
    selected_label = st.selectbox(
        f"Accepted projects - recent first ({len(labels)} project(s))",
        labels,
        key=selector_key,
    )
    memory_key = f"_dd_last_ops_project_selection_v49_{actor_id(user)}_{safe_text(focus_proposal_id) or 'all'}"
    previous_label = st.session_state.get(memory_key)
    if previous_label is not None and selected_label != previous_label:
        try:
            request_page_scroll("selected_project_detail")
        except Exception:
            st.session_state["_dd_scroll_target"] = "selected_project_detail"
    st.session_state[memory_key] = selected_label
    return rows[labels.index(selected_label)]


def _v49_make_project_plan_from_selected_row(selected_row):
    project = {col: selected_row.get(col, "") for col in PROJECT_COLUMNS}
    plan = {col: selected_row.get(col, "") for col in DELIVERY_PLAN_COLUMNS}
    # In merged rows, project created/updated timestamps may be suffixed.
    if not safe_text(project.get("created_at")) and safe_text(selected_row.get("created_at_project")):
        project["created_at"] = selected_row.get("created_at_project")
    if not safe_text(project.get("updated_at")) and safe_text(selected_row.get("updated_at_project")):
        project["updated_at"] = selected_row.get("updated_at_project")
    return project, plan


def _v49_delivery_rows_for_operations(focus_proposal_id=None):
    try:
        projects = read_simple_table("projects", PROJECT_COLUMNS)
    except Exception:
        projects = pd.DataFrame(columns=PROJECT_COLUMNS)
    try:
        plans = read_simple_table("delivery_plans", DELIVERY_PLAN_COLUMNS)
    except Exception:
        plans = pd.DataFrame(columns=DELIVERY_PLAN_COLUMNS)

    if projects is None or projects.empty:
        return pd.DataFrame()
    projects = projects.copy()
    if focus_proposal_id:
        projects = projects[projects["proposal_id"].astype(str) == safe_text(focus_proposal_id)]
    if projects.empty:
        return projects

    if plans is None or plans.empty:
        rows = projects.copy()
        for col in DELIVERY_PLAN_COLUMNS:
            if col not in rows.columns:
                rows[col] = ""
        return rows

    plans = plans.copy()
    if focus_proposal_id:
        plans = plans[plans["proposal_id"].astype(str) == safe_text(focus_proposal_id)]

    if plans.empty:
        rows = projects.copy()
        for col in DELIVERY_PLAN_COLUMNS:
            if col not in rows.columns:
                rows[col] = ""
        return rows

    merged = plans.merge(projects, on=["project_id", "proposal_id", "client_id"], how="right", suffixes=("", "_project"))
    return merged


def render_operations_delivery_workspace(user, data, focus_proposal_id=None):
    """Clean Technical Architect delivery workspace.

    Layout order:
    1. Project selector and selected-project summary.
    2. Current project week update status.
    3. Weekly targets.
    4. Requirement and Technical Architect conclusion.
    5. Client conversation.
    6. Employee requests/weekly updates.
    7. Allocation and delivery-plan controls.
    """
    if role_key_for_user(user) != "operations":
        return

    st.markdown(
        """
        <div class="dd-section-card dd-dashboard-shell">
            <div class="dd-section-eyebrow">Technical Architect workspace</div>
            <div class="dd-section-title">Project delivery control center</div>
            <div class="dd-section-subtitle">
                Select an accepted project. The current project week status appears first, followed by weekly targets,
                client requirement, conversation, employee requests, and allocation controls.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    merged = _v49_delivery_rows_for_operations(focus_proposal_id=focus_proposal_id)
    if merged is None or merged.empty:
        st.info("No accepted client projects are available yet.")
        return

    selected_row = _v49_select_delivery_project_row(user, merged, focus_proposal_id=focus_proposal_id)
    if selected_row is None:
        st.info("Select a project to open its delivery workspace.")
        return

    project, plan = _v49_make_project_plan_from_selected_row(selected_row)
    project_id = safe_text(project.get("project_id"))
    proposal_report = get_proposal_report_by_id(project.get("proposal_id"))
    existing_allocations = get_project_allocations(project_id) if project_id else pd.DataFrame()
    all_employee_updates = get_employee_project_updates(project_id=project_id) if project_id else pd.DataFrame()
    employee_updates = get_open_employee_project_updates(project_id=project_id) if project_id else pd.DataFrame()
    client_response = safe_text((proposal_report or {}).get("client_response")) or "Accepted"
    plan_id = safe_text(plan.get("delivery_plan_id")) or project_id or "project"

    st.markdown('<div id="dd-selected-project-detail"></div>', unsafe_allow_html=True)
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
                <div class="dd-mini-metric"><span>Delivery status</span><strong>{safe_text(plan.get('approval_status')) or safe_text(project.get('project_status')) or 'Waiting for review'}</strong></div>
                <div class="dd-mini-metric"><span>Allocated employees</span><strong>{0 if existing_allocations.empty else len(existing_allocations)}</strong></div>
                <div class="dd-mini-metric"><span>Open employee requests</span><strong>{0 if employee_updates.empty else len(employee_updates)}</strong></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # First and most important delivery control section.
    _v49_project_week_status_first_panel(
        project_id,
        project_label=project_display_name(project=project, project_id=project_id),
        key_prefix=f"ops_week_first_{project_id}",
    )

    # Second: weekly targets fixed by Technical Architect after detailed requirement.
    if safe_text(plan.get("delivery_plan_id")):
        rendered_targets = render_weekly_targets_panel(
            plan,
            title="Weekly targets for this project",
            expanded=True,
            client_safe=False,
            key_prefix=f"ops_clean_weekly_targets_{project_id}",
        )
        if not rendered_targets:
            st.info("Weekly targets are not captured yet. They will appear after the detailed requirement plan is generated.")
    else:
        st.info("Accepted project exists, but the client has not submitted the detailed requirement yet. Weekly targets will appear after Technical Architect planning.")
        return

    st.markdown("### Requirement and Technical Architect analysis")
    requirement_text = safe_text(plan.get("raw_requirement_text")).strip()
    if requirement_text:
        with st.expander("Client requirement", expanded=True):
            st.text_area(
                "Requirement provided by client",
                value=requirement_text,
                height=160,
                disabled=True,
                key=f"ops_clean_client_req_{plan_id}",
            )
    else:
        st.info("No detailed client requirement text was captured for this project yet.")

    agent_conclusion = safe_text(plan.get("operations_agent_plan")).strip()
    with st.expander("Technical Architect Agent conclusion", expanded=False):
        if agent_conclusion:
            st.text_area(
                "AI delivery analysis and conclusion",
                value=agent_conclusion,
                height=240,
                disabled=True,
                key=f"ops_clean_agent_conclusion_{plan_id}",
            )
        else:
            st.info("Technical Architect Agent conclusion is not available yet. It is generated after the client submits a detailed requirement.")

    st.markdown("### Client / Technical Architect conversation")
    st.caption("Client messages and Technical Architect replies are kept here as recent-first history.")
    render_client_operations_conversation(
        project,
        proposal_report or {},
        {"client_id": project.get("client_id"), "client_name": safe_text((proposal_report or {}).get("client_name"))},
        viewer="operations",
        user=user,
    )

    ops_reply_sent_key = f"ops_reply_sent_{safe_text(project_id)}"
    ops_reply_counter_key = f"ops_reply_counter_{safe_text(project_id)}"
    if ops_reply_counter_key not in st.session_state:
        st.session_state[ops_reply_counter_key] = 0

    if st.session_state.get(ops_reply_sent_key, False):
        st.success("Reply sent to the client portal.")
        if st.button("Send another reply", key=f"ops_clean_reply_again_{safe_text(project_id)}"):
            st.session_state[ops_reply_sent_key] = False
            st.session_state[ops_reply_counter_key] = int(st.session_state.get(ops_reply_counter_key, 0)) + 1
            try:
                request_page_scroll("selected_project_detail")
            except Exception:
                st.session_state["_dd_scroll_target"] = "selected_project_detail"
            st.rerun()
    else:
        reply_form_key = f"ops_clean_reply_to_client_{safe_text(project_id)}_{st.session_state.get(ops_reply_counter_key, 0)}"
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

    st.markdown("### Employee requests and weekly updates")
    render_employee_update_inbox_with_done(
        all_employee_updates,
        user,
        project_id,
        key_prefix=f"ops_clean_weekly_updates_{project_id}",
    )

    with st.expander("Allocated team summary", expanded=False):
        if existing_allocations.empty:
            st.info("No employees are allocated to this project yet.")
        else:
            cols = [c for c in ["employee_name", "project_role", "assigned_module", "allocation_percent", "allocation_status"] if c in existing_allocations.columns]
            st.dataframe(existing_allocations[cols], use_container_width=True, hide_index=True)

    with st.expander("Delivery plan and team allocation", expanded=False):
        st.caption("Open this only when you need to approve/update the delivery plan or add eligible delivery employees to the project.")
        manager_plan = st.text_area(
            "Technical Architect delivery plan",
            value=safe_text(plan.get("operations_manager_plan") or plan.get("operations_agent_plan")),
            height=240,
            key=f"ops_clean_manager_plan_{plan_id}",
        )

        employees = data.get("employees", pd.DataFrame()).copy() if isinstance(data, dict) else pd.DataFrame()
        try:
            employees = filter_project_delivery_employees(employees, data)
        except Exception:
            pass
        if employees.empty:
            st.warning("No eligible delivery employees are available for allocation.")
            return

        employees["label"] = employees.apply(
            lambda r: f"{r.get('employee_id')} - {r.get('employee_name')} ({r.get('designation')}, availability {r.get('availability_percent', '')}%)",
            axis=1,
        )
        selected = st.multiselect("Add eligible delivery employees to this project", employees["label"].tolist(), key=f"ops_clean_alloc_select_{plan_id}")
        st.caption("Executives and business/support skills are excluded from project delivery allocation.")

        selected_rows = []
        for label in selected:
            emp = employees[employees["label"] == label].iloc[0].to_dict()
            c1, c2, c3 = st.columns([1, 1, 1])
            with c1:
                module = st.text_input(
                    f"Module for {emp.get('employee_name')}",
                    value=safe_text(emp.get("primary_skill")) or safe_text(emp.get("designation")),
                    key=f"ops_clean_module_{plan_id}_{emp.get('employee_id')}",
                )
            with c2:
                role = st.text_input(
                    f"Project role for {emp.get('employee_name')}",
                    value=safe_text(emp.get("designation")),
                    key=f"ops_clean_role_{plan_id}_{emp.get('employee_id')}",
                )
            with c3:
                alloc = st.number_input(
                    f"Allocation % for {emp.get('employee_name')}",
                    min_value=5,
                    max_value=100,
                    value=40,
                    step=5,
                    key=f"ops_clean_pct_{plan_id}_{emp.get('employee_id')}",
                )
            selected_rows.append({
                "employee_id": safe_text(emp.get("employee_id")),
                "employee_name": safe_text(emp.get("employee_name")),
                "department": safe_text(emp.get("department")),
                "designation": safe_text(emp.get("designation")),
                "project_role": role,
                "assigned_module": module,
                "responsibility_summary": f"Own {module} delivery for {project.get('project_name')}. Submit weekly progress and raise blockers/resource needs from the employee workbench.",
                "allocation_percent": str(alloc),
            })

        approved_statuses = ["Approved by Technical Architect Agent", "Approved by Operations Manager"]
        button_text = "Approve delivery plan and notify selected employees" if safe_text(plan.get("approval_status")) not in approved_statuses else "Update team allocation and notify selected employees"
        if st.button(button_text, key=f"ops_clean_approve_delivery_{plan_id}", type="primary"):
            if not selected_rows:
                st.error("Select at least one eligible delivery employee before approving/updating the delivery team.")
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

    try:
        run_pending_page_scroll()
    except Exception:
        pass

# -----------------------------------------------------------------------------
# V50 CLIENT DELIVERY WEEK SUMMARY DEDUPLICATION
# -----------------------------------------------------------------------------
# Final client-delivery override. Do not call the older stacked wrappers here,
# because they were adding both "Project week and mandatory update summary" and
# "Current project week and update status" in the client portal. This version
# keeps one clean client-safe weekly update section.


def _v50_client_project_week_counts(project_id):
    """Return one safe count/info bundle for the client delivery summary."""
    project_id = safe_text(project_id).strip()
    counts = {"required": 0, "updated": 0, "pending": 0, "info": {}}
    try:
        counts = _v47_project_week_status_counts(project_id)
    except Exception:
        counts = {"required": 0, "updated": 0, "pending": 0, "info": {}}
    try:
        info = counts.get("info") or get_project_week_info(project_id, datetime.now())
    except Exception:
        info = counts.get("info") or {}
    counts["info"] = info or {}
    return counts


def render_client_delivery_section(report, client_account):
    """Client delivery view with one clean project-week section.

    The client sees the active week's completion percentage, Week N, week window,
    Friday checkpoint, team update count, weekly targets, and the message channel.
    Internal employee names, blockers, salary, margin, and private notes remain hidden.
    """
    response = safe_text(report.get("client_response"))
    if response != "Accept Proposal":
        return

    st.markdown("### Weekly delivery update")
    project = ensure_project_for_accepted_proposal(report, client_account)
    project_id = safe_text(project.get("project_id"))
    plan = get_delivery_plan_for_client_project(project_id)

    if plan is None:
        st.success("Proposal accepted. Our delivery team is ready to start the next step.")
        st.info("Please share your detailed requirement so our Technical Architect Agent can prepare the delivery plan and weekly targets.")
        uploaded_text = ""
        uploaded_name = ""
        upload = st.file_uploader(
            "Optional: upload a text requirement file",
            type=["txt", "md"],
            key=f"client_req_file_{project_id}",
        )
        if upload is not None:
            uploaded_name = upload.name
            try:
                uploaded_text = upload.read().decode("utf-8", errors="ignore")
            except Exception:
                uploaded_text = ""
        with st.form(f"client_requirement_form_{project_id}"):
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
                try:
                    request_page_scroll("dashboard")
                except Exception:
                    pass
                st.rerun()
            else:
                st.error(msg)
        return

    status = safe_text(plan.get("approval_status"))
    approved_statuses = ["Approved by Technical Architect Agent", "Approved by Operations Manager"]
    if status not in approved_statuses:
        st.info("Your detailed requirement has been received. The Technical Architect Agent has generated the delivery plan and weekly targets for internal review.")
        st.caption("Once delivery is approved and the team is allocated, this portal will show the weekly project progress and any information needed from your side.")
        render_weekly_targets_panel(
            plan,
            title="Weekly target list shared by Virtual Tech AI",
            expanded=True,
            client_safe=True,
            key_prefix=f"client_weekly_targets_pending_{project_id}",
        )
        return

    allocations = get_project_allocations(project_id)
    latest_update = generate_weekly_update_if_needed(project, plan, allocations)
    progress = get_client_safe_project_progress(project_id)
    counts = _v50_client_project_week_counts(project_id)
    info = counts.get("info", {}) or {}

    week_label = safe_text(info.get("week_label") or progress.get("project_week_label"), "Week 1")
    week_start = safe_text(info.get("week_start") or progress.get("week_start"), "-")
    week_end = safe_text(info.get("week_end") or progress.get("week_end"), "-")
    friday = safe_text(info.get("friday_checkpoint") or progress.get("friday_checkpoint"), "-")
    required = safe_int(counts.get("required", progress.get("mandatory_updates_required", 0)), 0)
    updated = safe_int(counts.get("updated", progress.get("mandatory_updates_received", 0)), 0)
    pending = max(0, required - updated)
    completion = safe_text(progress.get("weekly_progress_percent") or progress.get("progress_percent") or "Not updated yet")
    latest_time = safe_text(progress.get("updated_at"))

    st.success("Your project is active. Team work is going on.")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Delivery status", "In progress")
    c2.metric(f"{week_label} completion", completion)
    c3.metric("Project week", week_label)
    c4.metric("Team updates", f"{updated} / {required}")

    latest_line = f"Latest team progress update received: {latest_time}" if latest_time else f"No team progress update has been submitted yet for {week_label}."
    pending_line = (
        f"{pending} team update(s) are still pending for {week_label}. The delivery team is following up internally."
        if pending else
        f"All required team updates are submitted for {week_label}."
    )
    st.markdown(
        f"""
        <div class="dd-client-progress-card">
            <b>{week_label} project progress</b>
            <span>Week window: {week_start} to {week_end}</span>
            <span>Friday checkpoint: {friday}</span>
            <span>{latest_line}</span>
            <span>{pending_line}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_weekly_targets_panel(
        plan,
        title="Weekly target list shared by Virtual Tech AI",
        expanded=True,
        client_safe=True,
        key_prefix=f"client_weekly_targets_{project_id}",
    )

    info_needed = get_client_safe_information_needed(plan, latest_update)
    st.info(f"Information needed from your side: {info_needed}")

    with st.expander("Message Technical Architect Agent", expanded=False):
        st.caption("Recent-first conversation. Your Technical Architect Agent can reply from the project dashboard.")
        render_client_operations_conversation(project, report, client_account, viewer="client")
        sent_key = f"client_ops_msg_sent_{project_id}"
        if st.session_state.get(sent_key, False):
            st.success("Your message has been sent to the Technical Architect Agent.")
            if st.button("Send another message", key=f"client_ops_msg_again_{project_id}"):
                st.session_state[sent_key] = False
                try:
                    request_page_scroll("dashboard")
                except Exception:
                    pass
                st.rerun()
        else:
            with st.form(f"client_ops_message_form_{project_id}"):
                msg = st.text_area(
                    "Type your message for the Technical Architect Agent",
                    height=110,
                    placeholder="Example: Please confirm the branch-wise rollout order / integration priority / access details.",
                )
                submitted_msg = st.form_submit_button("Send message to Technical Architect Agent", type="primary")
            if submitted_msg:
                ok, message = save_client_message_to_operations(project, report, client_account, msg)
                if ok:
                    st.session_state[sent_key] = True
                    try:
                        request_page_scroll("dashboard")
                    except Exception:
                        pass
                    st.rerun()
                else:
                    st.error(message)

# =============================================================================
# FINAL STRICT WORKFLOW PATCH
# LifecycleDesk AI - proposal-to-delivery rules
# Add this block at the very bottom of decisiondesk_chunks/05_design_system.py
# =============================================================================

# -----------------------------------------------------------------------------
# New proposal columns for renegotiation tracking
# -----------------------------------------------------------------------------

FINAL_WORKFLOW_EXTRA_COLUMNS = [
    "negotiation_basis",
    "negotiation_terms_json",
    "negotiation_requested_at",
    "negotiation_round",
    "renegotiation_source_message",
    "previous_client_message",
]

try:
    insert_after = "client_response_comment" if "client_response_comment" in PROPOSAL_DECISION_COLUMNS else "client_response"
    insert_at = PROPOSAL_DECISION_COLUMNS.index(insert_after) + 1 if insert_after in PROPOSAL_DECISION_COLUMNS else len(PROPOSAL_DECISION_COLUMNS)
    for _col in FINAL_WORKFLOW_EXTRA_COLUMNS:
        if _col not in PROPOSAL_DECISION_COLUMNS:
            PROPOSAL_DECISION_COLUMNS.insert(insert_at, _col)
            insert_at += 1
except Exception:
    pass


def _final_reset_seen_flags(df, mask):
    """Make the proposal active/unread for every executive."""
    for role_key, column in PROPOSAL_NOTIFICATION_COLUMNS.items():
        df.loc[mask, column] = "No"
        seen_at_column = PROPOSAL_SEEN_AT_COLUMNS.get(role_key)
        if seen_at_column:
            df.loc[mask, seen_at_column] = ""
    return df


def _final_set_seen_for_actor_only(df, mask, role_key):
    """After one department opinion, actor has read it; all others must be notified."""
    now = current_timestamp()
    for seen_role, seen_column in PROPOSAL_NOTIFICATION_COLUMNS.items():
        seen_at_column = PROPOSAL_SEEN_AT_COLUMNS.get(seen_role)
        if seen_role == role_key:
            df.loc[mask, seen_column] = "Yes"
            if seen_at_column:
                df.loc[mask, seen_at_column] = now
        else:
            df.loc[mask, seen_column] = "No"
            if seen_at_column:
                df.loc[mask, seen_at_column] = ""
    return df


def _final_is_quote_sent_event(report):
    """CEO sent quotation; all executives should read it as an active inbox item."""
    if not isinstance(report, dict):
        return False
    status = safe_text(report.get("workflow_status")).lower()
    return bool(
        safe_text(report.get("client_quotation")).strip()
        and safe_text(report.get("quotation_sent")).strip().lower() == "yes"
        and "quotation sent" in status
        and safe_text(report.get("client_response")) not in ["Accept Proposal", "Decline Proposal", "Request Reconsideration"]
    )


def _final_is_client_declined_event(report):
    if not isinstance(report, dict):
        return False
    return safe_text(report.get("client_response")) == "Decline Proposal" or "declined" in safe_text(report.get("workflow_status")).lower()


def _final_is_client_renegotiation_event(report):
    if not isinstance(report, dict):
        return False
    status = safe_text(report.get("workflow_status")).lower()
    return safe_text(report.get("client_response")) == "Request Reconsideration" or "renegotiation" in status or "reconsideration" in status


def _final_project_started(report):
    if not isinstance(report, dict):
        return False
    status = safe_text(report.get("workflow_status")).lower()
    return bool(
        safe_text(report.get("project_id")).strip()
        or safe_text(report.get("project_created")).strip().lower() == "yes"
        or safe_text(report.get("client_response")) == "Accept Proposal"
        or "delivery" in status
        or "kickoff" in status
        or "team allocated" in status
        or get_project_for_proposal(report.get("proposal_id")) is not None
    )


def _final_split_negotiation_comment(comment):
    """Parse client negotiation basis and terms from saved comment text."""
    text_value = safe_text(comment).strip()
    basis = []
    terms = text_value

    basis_match = re.search(r"Negotiation basis\s*:\s*(.+)", text_value, flags=re.IGNORECASE)
    if basis_match:
        basis_line = basis_match.group(1).splitlines()[0]
        basis = [item.strip() for item in re.split(r",|\|", basis_line) if item.strip()]

    terms_match = re.search(r"New terms / reason\s*:\s*(.+)", text_value, flags=re.IGNORECASE | re.DOTALL)
    if terms_match:
        terms = terms_match.group(1).strip()

    return basis, terms


def _final_build_renegotiation_input(original_message, comment):
    basis, terms = _final_split_negotiation_comment(comment)
    basis_text = ", ".join(basis) if basis else "Client requested reconsideration"
    return (
        "Client requested renegotiation / reconsideration.\n"
        f"Renegotiation basis: {basis_text}\n"
        f"New terms or reason from client: {terms}\n\n"
        "Original unchanged client details are below. Keep unchanged details unless the new terms override them.\n"
        f"{safe_text(original_message)}"
    )


def _final_update_analysis_columns(df, mask, analysis):
    """Rewrite current proposal analysis after client renegotiation."""
    summaries = build_agent_summaries(analysis)

    column_value_map = {
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
        "sales_agent_summary": summaries.get("sales_agent_summary", ""),
        "hr_agent_summary": summaries.get("hr_agent_summary", ""),
        "operations_agent_summary": summaries.get("operations_agent_summary", ""),
        "finance_agent_summary": summaries.get("finance_agent_summary", ""),
        "ceo_agent_summary": summaries.get("ceo_agent_summary", ""),
        "skill_gap_json": encode_json(analysis.get("skill_gap", [])),
        "role_cost_breakdown_json": encode_json(analysis.get("role_cost_breakdown", [])),
        "initial_requirement_summary": analysis.get("initial_requirement_summary", ""),
        "technical_architect_requirement": analysis.get("technical_architect_requirement", ""),
        "technical_architect_stack_json": analysis.get("technical_architect_stack_json", encode_json(analysis.get("technical_architect_stack", {}))),
        "technical_architect_timeline_basis": analysis.get("technical_architect_timeline_basis", ""),
        "client_requested_timeline_months": analysis.get("client_requested_timeline_months", ""),
        "scope_complexity": analysis.get("scope_complexity", ""),
        "scope_effort_months": analysis.get("scope_effort_months", ""),
        "hiring_recommendation": analysis.get("hiring_recommendation", ""),
        "total_hiring_needed_fte": analysis.get("total_hiring_needed_fte", 0),
        "calendar_carry_cost": analysis.get("calendar_carry_cost", 0),
        "hiring_or_contract_premium": analysis.get("hiring_or_contract_premium", 0),
        "pending_work_risk_buffer": analysis.get("pending_work_risk_buffer", 0),
        "costing_method": analysis.get("costing_method", ""),
        "hiring_necessary": analysis.get("hiring_necessary", ""),
        "hiring_necessity_basis": analysis.get("hiring_necessity_basis", ""),
    }

    for col, value in column_value_map.items():
        if col in df.columns:
            df.loc[mask, col] = value

    return df


def _final_clear_human_decisions_for_renegotiation(df, mask):
    """Client renegotiation starts a fresh executive review cycle."""
    fields = []
    for role_key in ["sales", "finance", "hr", "operations"]:
        fields.extend([
            f"{role_key}_decision",
            f"{role_key}_comment",
            f"{role_key}_recommended_quote",
            f"{role_key}_recommended_timeline_months",
            f"{role_key}_decided_by",
            f"{role_key}_decided_at",
        ])

    fields.extend([
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
    ])

    for field in fields:
        if field in df.columns:
            df.loc[mask, field] = "No" if field == "quotation_sent" else ""

    return df


# -----------------------------------------------------------------------------
# CEO / executive decisions
# -----------------------------------------------------------------------------

def submit_proposal_decision(proposal_id, user, decision, comment, recommended_quote, recommended_timeline_months):
    """Strict collaboration rule.

    - Any department opinion notifies every other executive.
    - CEO quotation also becomes an active unread notification for every executive.
    - CEO quotation does not automatically move to reviewed.
    """
    role_key = role_key_for_user(user)
    if role_key is None:
        return False, "Only Sales, Finance, HR, Technical Architect executives or CEO can update proposal decisions."

    df = read_proposal_store(create_if_missing=True)
    if df.empty or "proposal_id" not in df.columns:
        return False, "No proposal records were found."

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
        df.loc[mask, "workflow_status"] = "Quotation Sent to Client - Executive Read Pending"
        df.loc[mask, "current_owner"] = "Client / Executive Read Confirmation"

        summary = (
            f"CEO sent quotation to client at {money_text(recommended_quote)} "
            f"for {safe_int(recommended_timeline_months)} month(s). "
            "All executives must read this update."
        )

        # Important: quotation sent is an active notification for everyone.
        df = _final_reset_seen_flags(df, mask)

    else:
        quote_applicable = role_key in ["sales", "finance"]
        timeline_applicable = role_key == "operations"

        df.loc[mask, f"{role_key}_decision"] = decision
        df.loc[mask, f"{role_key}_comment"] = comment
        df.loc[mask, f"{role_key}_recommended_quote"] = safe_number(recommended_quote) if quote_applicable else ""
        df.loc[mask, f"{role_key}_recommended_timeline_months"] = safe_int(recommended_timeline_months) if timeline_applicable else ""
        df.loc[mask, f"{role_key}_decided_by"] = name
        df.loc[mask, f"{role_key}_decided_at"] = now
        df.loc[mask, "workflow_status"] = "Department Review In Progress"
        df.loc[mask, "current_owner"] = "CEO / Executive Team"

        summary = (
            f"{role_label} updated decision: {decision}. "
            "CEO and all other executives have been notified."
        )

        # Actor has read their own action; others must read.
        df = _final_set_seen_for_actor_only(df, mask, role_key)

    df.loc[mask, "decision_version"] = current_version
    df.loc[mask, "last_updated_by"] = name
    df.loc[mask, "last_updated_role"] = role_label
    df.loc[mask, "last_updated_at"] = now
    df.loc[mask, "last_update_summary"] = summary

    upsert_current_proposal_from_df(df, mask)

    history_quote = safe_number(recommended_quote) if role_key in ["sales", "finance", "ceo"] else ""
    history_timeline = safe_int(recommended_timeline_months) if role_key in ["operations", "ceo"] else ""

    append_proposal_history(
        proposal_id,
        user,
        "CEO Quotation Sent" if role_key == "ceo" else "Executive Opinion Updated",
        decision=decision,
        comment=comment,
        recommended_quote=history_quote,
        recommended_timeline_months=history_timeline,
        summary=summary,
    )

    if role_key == "ceo":
        try:
            report = get_proposal_report_by_id(proposal_id)
            analysis = report.get("analysis", {}) if report else {}
            _update_proposal_internal_hiring_columns(proposal_id, analysis)
        except Exception:
            pass
        return True, "CEO quotation sent to client. Every executive has been notified in the active inbox."

    return True, f"{role_label} opinion saved. Every other executive has been notified."


def mark_quotation_sent_to_client(proposal_id, user):
    """If quotation is manually marked as sent, notify every executive until they mark read."""
    role_key = role_key_for_user(user)
    if role_key not in ["ceo", "sales"]:
        return False, "Only CEO or Sales Executive can mark the quotation as sent to the client."

    df = read_proposal_store(create_if_missing=True)
    if df.empty or "proposal_id" not in df.columns:
        return False, "No proposal records found."

    mask = df["proposal_id"].astype(str) == str(proposal_id)
    if not mask.any():
        return False, f"Proposal {proposal_id} was not found."

    now = current_timestamp()
    df.loc[mask, "quotation_sent"] = "Yes"
    df.loc[mask, "quotation_sent_at"] = now
    df.loc[mask, "workflow_status"] = "Quotation Sent to Client - Executive Read Pending"
    df.loc[mask, "current_owner"] = "Client / Executive Read Confirmation"
    df.loc[mask, "last_updated_by"] = actor_name(user)
    df.loc[mask, "last_updated_role"] = actor_role_label(user)
    df.loc[mask, "last_updated_at"] = now
    df.loc[mask, "last_update_summary"] = "Quotation was sent to client. All executives must read this update."
    df = _final_reset_seen_flags(df, mask)

    upsert_current_proposal_from_df(df, mask)
    append_proposal_history(
        proposal_id,
        user,
        "Quotation Sent",
        summary="Quotation was marked as sent to client and all executives were notified.",
    )
    return True, "Quotation marked as sent. Every executive has been notified."


# -----------------------------------------------------------------------------
# Client response: accept / decline / renegotiate
# -----------------------------------------------------------------------------

def save_client_response(proposal_id, client_account, response, comment):
    """Strict client response workflow.

    Accept:
      create delivery project and notify executives.

    Decline:
      close permanently, no project consideration after this.

    Request Reconsideration:
      reopen same proposal as a fresh executive item, combine old unchanged details
      with new client terms, rerun internal agent analysis, clear old human decisions,
      reset every executive read flag.
    """
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

    old_message = safe_text(df.loc[mask, "raw_client_message"].iloc[0])
    old_round = safe_int(df.loc[mask, "negotiation_round"].iloc[0], 0) if "negotiation_round" in df.columns else 0
    client_name = safe_text(client_account.get("client_name")) or "Client"

    df.loc[mask, "client_id"] = client_id
    df.loc[mask, "client_response"] = response
    df.loc[mask, "client_response_comment"] = comment
    df.loc[mask, "client_response_at"] = now
    df.loc[mask, "last_updated_by"] = client_name
    df.loc[mask, "last_updated_role"] = "Client"
    df.loc[mask, "last_updated_at"] = now

    if response == "Accept Proposal":
        df.loc[mask, "workflow_status"] = "Client Accepted - Awaiting Detailed Requirement"
        df.loc[mask, "current_owner"] = "Client / Technical Architect"
        df.loc[mask, "last_update_summary"] = "Client accepted the quotation. Detailed requirement is now required."
        df = _final_reset_seen_flags(df, mask)
        upsert_current_proposal_from_df(df, mask)

        try:
            latest_df = read_proposal_store(create_if_missing=True)
            latest_match = latest_df[latest_df["proposal_id"].astype(str) == str(proposal_id)]
            if not latest_match.empty:
                updated_report = proposal_row_to_report(latest_match.iloc[0])
                ensure_project_for_accepted_proposal(updated_report, client_account)
        except Exception:
            pass

        append_proposal_history(
            proposal_id,
            {"user_id": safe_text(client_account.get("client_user_id")), "employee_name": client_name, "designation": "Client"},
            "Client Accepted Proposal",
            comment=comment,
            summary="Client accepted the quotation. Delivery project is created and detailed requirement is required.",
        )

        _final_insert_client_response_record(proposal_id, client_id, response, comment, now)
        return True, "Your proposal acceptance was saved. Please submit the detailed requirement next."

    if response == "Decline Proposal":
        df.loc[mask, "workflow_status"] = "Client Declined - Closed"
        df.loc[mask, "current_owner"] = "Closed"
        df.loc[mask, "last_update_summary"] = "Client declined the proposal. This proposal is closed and will not be considered further."
        df = _final_reset_seen_flags(df, mask)
        upsert_current_proposal_from_df(df, mask)

        try:
            project = get_project_for_proposal(proposal_id)
            if project:
                project["project_status"] = "Client Declined - Closed"
                project["updated_at"] = now
                upsert_simple_row("projects", "project_id", PROJECT_COLUMNS, project)
        except Exception:
            pass

        append_proposal_history(
            proposal_id,
            {"user_id": safe_text(client_account.get("client_user_id")), "employee_name": client_name, "designation": "Client"},
            "Client Declined Proposal",
            comment=comment,
            summary="Client declined the quotation. Proposal closed permanently.",
        )

        _final_insert_client_response_record(proposal_id, client_id, response, comment, now)
        return True, "Your response was saved. The proposal is now closed."

    # Request Reconsideration
    if response == "Request Reconsideration":
        if not comment.strip():
            return False, "Please share what you want to renegotiate, such as budget, timeline, scope, payment terms, or another reason."

        basis, terms = _final_split_negotiation_comment(comment)
        renegotiation_input = _final_build_renegotiation_input(old_message, comment)

        analysis = {}
        try:
            company_data = load_cached_company_data() if "load_cached_company_data" in globals() else None
            if company_data is not None:
                analysis = run_external_client_decision(renegotiation_input, company_data)
        except Exception:
            analysis = {}

        if analysis:
            df = _final_update_analysis_columns(df, mask, analysis)

        df = _final_clear_human_decisions_for_renegotiation(df, mask)
        df.loc[mask, "workflow_status"] = "Client Requested Renegotiation - Fresh Executive Review"
        df.loc[mask, "current_owner"] = "Sales, Finance, HR, Technical Architect, CEO"
        df.loc[mask, "negotiation_basis"] = ", ".join(basis) if basis else "Client reconsideration"
        df.loc[mask, "negotiation_terms_json"] = encode_json({"basis": basis, "terms": terms})
        df.loc[mask, "negotiation_requested_at"] = now
        df.loc[mask, "negotiation_round"] = old_round + 1
        df.loc[mask, "previous_client_message"] = old_message
        df.loc[mask, "renegotiation_source_message"] = renegotiation_input
        df.loc[mask, "decision_version"] = safe_int(df.loc[mask, "decision_version"].iloc[0], 0) + 1
        df.loc[mask, "last_update_summary"] = (
            "Client requested renegotiation. Internal agents re-analysed the same project using unchanged original details plus the new client terms. "
            "All executives must review this as a fresh notification."
        )
        df = _final_reset_seen_flags(df, mask)

        upsert_current_proposal_from_df(df, mask)

        append_proposal_history(
            proposal_id,
            {"user_id": safe_text(client_account.get("client_user_id")), "employee_name": client_name, "designation": "Client"},
            "Client Requested Renegotiation",
            comment=comment,
            summary="Client requested renegotiation; agent analysis was refreshed and all executive read flags were reset.",
        )

        if analysis:
            append_proposal_history(
                proposal_id,
                {"user_id": "SYSTEM", "employee_name": "LifecycleDesk AI", "designation": "System"},
                "Renegotiation Agent Meeting Rebuilt",
                decision=analysis.get("decision", ""),
                comment=analysis.get("reason", ""),
                recommended_quote=analysis.get("recommended_quote", 0),
                recommended_timeline_months=analysis.get("timeline_months", 0),
                summary="Internal agent meeting was regenerated using original proposal details plus the client's new negotiation terms.",
            )

        _final_insert_client_response_record(proposal_id, client_id, response, comment, now)
        return True, "Your renegotiation request was saved. Our internal team will review the new terms and send an updated quotation."

    return False, "Unsupported client response."


def _final_insert_client_response_record(proposal_id, client_id, response, comment, responded_at):
    try:
        if not postgres_config_available():
            return
        ensure_postgres_tables()
        row = {
            "response_id": make_response_id(),
            "proposal_id": proposal_id,
            "client_id": client_id,
            "response": response,
            "comment": comment,
            "responded_at": responded_at,
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
        clear_workflow_read_cache()
    except Exception:
        pass


# -----------------------------------------------------------------------------
# Client dashboard with clear negotiation terms
# -----------------------------------------------------------------------------

def render_client_dashboard(client_account):
    st.markdown(
        f"""
        <div class="dd-section-card">
            <div class="dd-section-title">Client Portal</div>
            <div class="dd-section-subtitle">
                Welcome {safe_text(client_account.get('client_name'), 'Client')}. This portal shows only client-safe proposal status, quotation, and delivery progress.
            </div>
            <div class="dd-muted-small">Client ID: <b>{safe_text(client_account.get('client_id'))}</b></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    reports = get_client_proposal_reports(client_account)
    if not reports:
        st.warning("No proposal is linked to this client account yet.")
        return

    for report in reports:
        analysis = report.get("analysis", {})

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
                    <div class="dd-title-badge">Client-safe view</div>
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
            "Your proposal is being handled internally by our Sales, HR, Finance, Technical Architect, and CEO team. "
            "Internal comments, cost, margin, hiring notes, and employee details are private."
        )

        existing_response = safe_text(report.get("client_response"))
        quotation = safe_text(report.get("client_quotation"))

        if existing_response == "Decline Proposal":
            st.warning("You declined this proposal. This proposal is now closed.")
            if safe_text(report.get("client_response_comment")):
                st.caption(f"Your note: {safe_text(report.get('client_response_comment'))}")
            return

        if existing_response == "Request Reconsideration" and not quotation:
            st.success("Your renegotiation request has been received and is under internal executive review.")
            if safe_text(report.get("client_response_comment")):
                st.caption(f"Your request: {safe_text(report.get('client_response_comment'))}")
            st.info("An updated quotation will appear here once approved by the CEO.")
            return

        if not quotation:
            st.warning("Quotation is not ready yet. Please check this dashboard later for CEO-approved updates.")
            return

        st.markdown("#### Company quotation")
        quote_label = "Reconsidered quotation" if existing_response == "Request Reconsideration" else "CEO-approved quotation"

        if existing_response in ["Accept Proposal"]:
            st.success(f"Your current response: {existing_response}")
            render_latest_quotation_panel(
                report,
                title="Quotation and client decision summary",
                expanded=False,
                key_prefix="client_final_quote",
            )
            render_client_delivery_section(report, client_account)
            return

        st.text_area(
            quote_label,
            value=quotation,
            height=260,
            key=f"client_quote_{report.get('proposal_id')}",
            disabled=True,
        )

        with st.form(f"client_response_form_{report.get('proposal_id')}_{existing_response or 'new'}"):
            response = st.radio(
                "Your response",
                CLIENT_RESPONSE_OPTIONS,
                index=0,
                horizontal=True,
                key=f"client_response_radio_{report.get('proposal_id')}",
            )

            negotiation_basis = st.multiselect(
                "If you are requesting renegotiation, select the basis",
                ["Budget", "Timeline", "Scope", "Payment terms", "Other"],
                key=f"client_negotiation_basis_{report.get('proposal_id')}",
            )

            comment = st.text_area(
                "Your note / updated terms",
                height=110,
                placeholder="Example: We can proceed if the budget is revised to 35 lakhs, or if timeline can be reduced to 6 months.",
                key=f"client_response_comment_{report.get('proposal_id')}",
            )

            submitted = st.form_submit_button("Submit response", type="primary")

        if submitted:
            final_comment = safe_text(comment).strip()
            if response == "Request Reconsideration":
                if not negotiation_basis and not final_comment:
                    st.error("Please select the negotiation basis or enter the updated terms/reason.")
                    return
                final_comment = (
                    "Negotiation basis: " + (", ".join(negotiation_basis) if negotiation_basis else "Not specified") +
                    "\nNew terms / reason: " + (final_comment or "Not specified")
                )

            ok, msg = save_client_response(report.get("proposal_id"), client_account, response, final_comment)
            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)


# -----------------------------------------------------------------------------
# Read / review logic
# -----------------------------------------------------------------------------

def _dd_role_has_action_required_for_update(report, role_key):
    """Return True only when the role must actually act.

    CEO quotation sent, client decline, kickoff notices for Sales/HR/Finance are
    informational and should show Mark as read.
    """
    role_key = safe_text(role_key).lower()

    if _final_is_client_declined_event(report):
        return False

    if _final_is_quote_sent_event(report):
        return False

    if _final_is_client_renegotiation_event(report):
        # Fresh executive review required after client renegotiation.
        return role_key in ["sales", "finance", "hr", "operations", "ceo"]

    if _final_project_started(report):
        # Technical Architect owns delivery actions. Others only read project status.
        return role_key == "operations"

    ceo_quote_sent = proposal_has_ceo_quote_sent(report) if "proposal_has_ceo_quote_sent" in globals() else bool(safe_text(report.get("client_quotation")).strip())
    if ceo_quote_sent:
        return False

    # Before quotation is sent, all executives should review and give/update their role opinion.
    return role_key in ["sales", "finance", "hr", "operations", "ceo"]


def _dd_can_mark_update_as_reviewed(report, role_key):
    return not _dd_role_has_action_required_for_update(report, role_key)


def _final_render_quote_sent_summary(report, role_key):
    analysis = report.get("analysis", {}) if isinstance(report, dict) else {}
    st.markdown(
        """
        <div class="dd-section-card">
            <div class="dd-section-title">CEO quotation sent</div>
            <div class="dd-section-subtitle">
                CEO has sent the quotation to the client. This is an active executive notification until you mark it as read.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Project", analysis.get("project_type", "Project"))
    c2.metric("Quotation", money_text(report.get("ceo_final_quote") or analysis.get("recommended_quote", 0)))
    c3.metric("Timeline", f"{safe_text(report.get('ceo_final_timeline_months') or analysis.get('timeline_months'))} month(s)")
    c4.metric("Client status", safe_text(report.get("client_response")) or "Awaiting response")

    st.info(safe_text(report.get("last_update_summary")) or "CEO sent quotation to the client.")
    with st.expander("View quotation sent to client", expanded=False):
        st.text_area(
            "Client quotation",
            value=safe_text(report.get("client_quotation")),
            height=240,
            disabled=True,
            key=f"quote_sent_summary_{report.get('proposal_id')}_{role_key}",
        )


def _final_render_declined_summary(report, role_key):
    analysis = report.get("analysis", {}) if isinstance(report, dict) else {}
    st.markdown(
        """
        <div class="dd-section-card">
            <div class="dd-section-title">Client declined proposal</div>
            <div class="dd-section-subtitle">
                The client declined the proposal. This proposal is closed and no further delivery action is required.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns(3)
    c1.metric("Project", analysis.get("project_type", "Project"))
    c2.metric("Status", "Closed")
    c3.metric("Client response", "Declined")
    if safe_text(report.get("client_response_comment")):
        st.info("Client note: " + safe_text(report.get("client_response_comment")))


def _final_role_safe_delivery_summary(report, user=None, data=None):
    """Sales/HR/Finance see only kickoff/week/progress summary after delivery starts."""
    role_key = role_key_for_user(user) or "executive"
    project = get_project_for_proposal(report.get("proposal_id"))
    analysis = report.get("analysis", {}) if isinstance(report, dict) else {}

    st.markdown(
        """
        <div class="dd-section-card dd-dashboard-shell">
            <div class="dd-section-title">Project kickoff / weekly delivery status</div>
            <div class="dd-section-subtitle">
                This project has moved into delivery. This role-safe view shows only kickoff status, project week, and client-safe weekly progress.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not project:
        st.info("Project has not been created yet.")
        return

    project_id = safe_text(project.get("project_id"))
    plan = get_delivery_plan_for_client_project(project_id)
    progress = get_client_safe_project_progress(project_id)
    week_info = get_project_week_info(project_id, progress.get("updated_at")) if "get_project_week_info" in globals() else {"week_label": "Week 1"}

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Project", analysis.get("project_type", "Project"))
    c2.metric("Delivery status", safe_text(project.get("project_status"), "In progress"))
    c3.metric("Project week", progress.get("project_week_label") or week_info.get("week_label") or "Week 1")
    c4.metric("Weekly progress", progress.get("weekly_progress_percent") or progress.get("progress_percent") or "Not updated")

    st.info(
        f"Weekly update status: {progress.get('mandatory_updates_received', 0)} / "
        f"{progress.get('mandatory_updates_required', 0)} team update(s) received for the current project week."
    )

    if plan:
        render_weekly_targets_panel(
            plan,
            title="Weekly target list",
            expanded=False,
            client_safe=True,
            key_prefix=f"role_safe_targets_{role_key}_{project_id}",
        )


def render_post_ceo_readonly_lifecycle_view(report, user=None, compact=False):
    role_key = role_key_for_user(user) or "executive"

    if role_key == "ceo" and _final_project_started(report):
        render_ceo_project_lifecycle_dashboard(report, user=user, data={})
        return

    if role_key in ["sales", "finance", "hr"] and _final_project_started(report):
        _final_role_safe_delivery_summary(report, user=user, data={})
        return

    if _final_is_client_declined_event(report):
        _final_render_declined_summary(report, role_key)
        return

    if _final_is_quote_sent_event(report) or proposal_has_ceo_quote_sent(report):
        _final_render_quote_sent_summary(report, role_key)
        return

    # fallback to older behavior if needed
    try:
        _v46_original_render_post_ceo_readonly_lifecycle_view(report, user=user, compact=compact)
    except Exception:
        st.info("Lifecycle status is available from the executive inbox.")


def render_external_client_report(report, user=None, compact=False):
    """Final safe proposal renderer.

    Prevents CEO/other executives from reopening the decision form after quote is sent.
    """
    role_key = role_key_for_user(user)

    if not compact:
        if _final_is_client_declined_event(report):
            _final_render_declined_summary(report, role_key)
            return
        if _final_is_quote_sent_event(report):
            _final_render_quote_sent_summary(report, role_key)
            return
        if role_key in ["sales", "finance", "hr"] and proposal_has_ceo_quote_sent(report):
            render_post_ceo_readonly_lifecycle_view(report, user=user, compact=compact)
            return
        if role_key == "ceo" and proposal_has_ceo_quote_sent(report) and not _final_project_started(report) and not _final_is_client_renegotiation_event(report):
            _final_render_quote_sent_summary(report, role_key)
            return

    analysis = report["analysis"]

    st.markdown(
        """
        <div class="dd-section-card">
            <div class="dd-section-title">Client proposal decision room</div>
            <div class="dd-section-subtitle">
                Shared internal view for Sales, HR, Technical Architect, Finance, and CEO. The client cannot see this internal meeting outcome.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if report.get("proposal_id"):
        st.caption(
            f"Proposal ID: {report['proposal_id']} | Created: {report.get('created_at', '')} | "
            f"Status: {report.get('workflow_status', 'Awaiting Executive Decisions')}"
        )

    if report.get("last_update_summary"):
        st.info(
            f"Latest update: {report.get('last_update_summary')} "
            f"({report.get('last_updated_role')} - {report.get('last_updated_by')} at {report.get('last_updated_at')})"
        )

    if _final_is_client_renegotiation_event(report):
        st.warning("Client requested renegotiation. This is a fresh executive review using original unchanged details plus the new client terms.")
        if safe_text(report.get("client_response_comment")):
            st.caption("Client renegotiation request:")
            st.text_area(
                "Client negotiation terms",
                value=safe_text(report.get("client_response_comment")),
                height=120,
                disabled=True,
                key=f"renegotiation_terms_{report.get('proposal_id')}_{role_key}",
            )

    render_client_requirement_box(report.get("raw_client_message", analysis.get("client_message", "")))

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Project Type", analysis.get("project_type"))
    c2.metric("Client Budget", money_text(analysis.get("client_budget")))
    c3.metric("Timeline", f"{analysis.get('timeline_months')} months")
    c4.metric("Current Decision", analysis.get("decision") or "Pending")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Estimated Cost", money_text(analysis.get("estimated_cost")))
    m2.metric("Recommended Quote", money_text(analysis.get("recommended_quote")))
    m3.metric("Margin at Budget", f"{analysis.get('profit_margin_at_client_budget')}%")
    m4.metric("Timeline Risk", analysis.get("timeline_risk"))

    st.markdown("#### Initial agentic conclusion")
    write_decision_status(analysis.get("initial_agent_decision") or analysis.get("decision"))
    st.write(analysis.get("initial_agent_reason") or analysis.get("reason"))

    if compact:
        return

    render_agentic_decision_pack(report)
    render_executive_decision_summary(report)
    render_client_quotation(report, user=user)
    render_decision_history(report.get("proposal_id"))
    render_executive_decision_form(report, user)


def render_pending_proposal_notifications(user, data=None):
    """Executive inbox with strict active/read behavior."""
    column = user_notification_column(user)
    if column is None:
        return

    try:
        reports = get_pending_proposal_reports_for_user(user)
    except Exception as exc:
        st.error(f"Could not load proposal notifications from proposal storage: {exc}")
        return

    role_key = role_key_for_user(user) or "executive"
    selected_key = f"selected_pending_proposal_{role_key}"

    if not reports:
        st.success("No new proposal or lifecycle updates for your role.")
        render_reviewed_proposal_reference_list(user, data=data)
        return

    reports = sorted(reports, key=lambda report: safe_text(report.get("last_updated_at") or report.get("created_at")), reverse=True)

    st.markdown(
        f"""
        <div class="dd-section-card">
            <div class="dd-section-title">Executive update inbox</div>
            <div class="dd-section-subtitle">
                You have <b>{len(reports)}</b> active update(s). Use the dropdown to open one item.
                Quotation/client-response updates move to reviewed only after you mark them as read.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    option_map = {"Select an update to open...": None}
    labels = ["Select an update to open..."]

    for idx, report in enumerate(reports, start=1):
        analysis = report.get("analysis", {})
        updated = safe_text(report.get("last_updated_at") or report.get("created_at") or "No timestamp")
        linked_project = get_project_for_proposal(report.get("proposal_id"))
        project_label = project_display_name(
            project=linked_project or {},
            project_id=report.get("project_id"),
            proposal_id=report.get("proposal_id"),
            fallback=analysis.get("project_type", "Project"),
        )
        inbox_type = "Action needed" if _dd_role_has_action_required_for_update(report, role_key) else "Read confirmation"
        label = f"{idx}. {updated} | {project_label} | {report.get('workflow_status', 'Pending')} | {inbox_type}"
        labels.append(label)
        option_map[label] = report

    with st.expander(f"{len(reports)} active update(s) - click to open", expanded=False):
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
                "Project": project_display_name(
                    project=get_project_for_proposal(report.get("proposal_id")) or {},
                    project_id=report.get("project_id"),
                    proposal_id=report.get("proposal_id"),
                    fallback=analysis.get("project_type"),
                ),
                "Status": report.get("workflow_status"),
                "Inbox Type": "Action needed" if _dd_role_has_action_required_for_update(report, role_key) else "Read confirmation",
                "Last By": report.get("last_updated_role"),
            })
        if preview_rows:
            st.dataframe(pd.DataFrame(preview_rows), use_container_width=True, hide_index=True)

    selected_report = option_map.get(st.session_state.get(selected_key, "Select an update to open..."))
    if not selected_report:
        st.info("Choose one update from the dropdown to open its dashboard.")
        render_reviewed_proposal_reference_list(user, data=data)
        return

    st.markdown('<div id="dd-selected-update-dashboard"></div>', unsafe_allow_html=True)
    st.markdown("### Selected update dashboard")

    if _final_is_client_declined_event(selected_report):
        _final_render_declined_summary(selected_report, role_key)
    elif _final_is_quote_sent_event(selected_report):
        _final_render_quote_sent_summary(selected_report, role_key)
    elif role_key == "operations" and _final_project_started(selected_report):
        st.info("This is a delivery-readiness item for the Technical Architect team.")
        render_operations_delivery_workspace(user, data or {}, focus_proposal_id=selected_report.get("proposal_id"))
    elif role_key == "ceo" and _final_project_started(selected_report):
        render_ceo_project_lifecycle_dashboard(selected_report, user=user, data=data or {})
    elif role_key in ["sales", "finance", "hr"] and _final_project_started(selected_report):
        _final_role_safe_delivery_summary(selected_report, user=user, data=data or {})
    else:
        render_external_client_report(selected_report, user=user, compact=False)

    if _dd_can_mark_update_as_reviewed(selected_report, role_key):
        st.markdown("#### Read confirmation")
        st.caption("This update is informational for your role. Mark it as read to move it into Reviewed items reference.")
        if st.button(
            "Mark as read",
            key=f"mark_read_selected_{selected_report.get('proposal_id')}_{role_key}",
            type="primary",
        ):
            success, message = mark_proposal_seen_for_user(selected_report.get("proposal_id"), user)
            if success:
                st.success(message)
                st.session_state[selected_key] = "Select an update to open..."
                st.rerun()
            else:
                st.error(message)
    else:
        st.caption("This item needs a role action, so it will remain in the inbox until the appropriate opinion or delivery action is completed.")

    try:
        run_pending_page_scroll()
    except Exception:
        pass

    render_reviewed_proposal_reference_list(user, data=data)


# -----------------------------------------------------------------------------
# Remove unnecessary long-table full-cell / select-column viewer everywhere
# -----------------------------------------------------------------------------

def _dd_dataframe_has_long_values(df, threshold=75):
    """Disable the automatic full-cell viewer. Tables now stay simple."""
    return False


def _dd_dataframe_full_value_viewer(df, key_prefix):
    """Disabled: no Select row / Select column viewer."""
    return None


# -----------------------------------------------------------------------------
# Cleaner AI Front Desk missing-field message
# -----------------------------------------------------------------------------

def format_missing_client_fields_message(missing):
    if not missing:
        return ""

    clean_missing = [safe_text(item).strip() for item in missing if safe_text(item).strip()]
    if not clean_missing:
        return ""

    if len(clean_missing) == 1:
        return f"AI Front Desk: Thanks, I have the other details. Please share only the missing {clean_missing[0]}."

    return (
        "AI Front Desk: Thanks, I have the details shared so far. "
        "Please share only these missing items: " + ", ".join(clean_missing) + "."
    )


# -----------------------------------------------------------------------------
# Delivery employee allocation: exclude executives and show live bandwidth
# -----------------------------------------------------------------------------

def filter_project_delivery_employees(employees, data=None):
    """Allow only real delivery employees and show current available bandwidth."""
    if employees is None or getattr(employees, "empty", True):
        return employees

    working = employees.copy()

    try:
        working = adjust_employee_availability_with_dynamic_allocations(working)
    except Exception:
        pass

    executive_ids = _executive_user_ids_from_data(data)
    allowed_rows = []

    for _, row in working.iterrows():
        row_dict = row.to_dict()
        emp_id = safe_text(row_dict.get("employee_id") or row_dict.get("user_id")).upper()
        role_value = safe_text(row_dict.get("role")).lower()
        designation = safe_text(row_dict.get("designation") or row_dict.get("employee_designation")).lower()
        department = safe_text(row_dict.get("department") or row_dict.get("employee_department")).lower()

        if emp_id and emp_id in executive_ids:
            continue
        if role_value in ["executive", "founder", "ceo"]:
            continue
        if any(word in designation for word in ["executive", "ceo", "founder", "sales", "finance", "hr"]):
            continue
        if any(word in department for word in ["sales", "finance", "hr", "business", "strategy"]):
            continue
        if _row_has_blocked_allocation_skill(row_dict):
            continue

        available = safe_number(row_dict.get("availability_percent"), 0)
        row_dict["available_bandwidth"] = f"{available:.0f}%"
        allowed_rows.append(row_dict)

    if not allowed_rows:
        return working.iloc[0:0].copy()

    return pd.DataFrame(allowed_rows)


# -----------------------------------------------------------------------------
# Ensure client -> Technical Architect message remains actively notified
# -----------------------------------------------------------------------------

def save_client_message_to_operations(project, report, client_account, message_text):
    """Client can message Technical Architect; Technical Architect receives active notification."""
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

    return True, "Your message has been sent to the Technical Architect AI Agent."

# =============================================================================
# SMALL PATCH: SHOW CEO HIRING YES IN EXECUTIVE QUOTATION NOTIFICATION
# Add at the very bottom of decisiondesk_chunks/05_design_system.py
# =============================================================================

try:
    _hiring_notify_previous_submit_proposal_decision = submit_proposal_decision
except Exception:
    _hiring_notify_previous_submit_proposal_decision = None


def _hiring_notify_get_saved_decision_from_session(proposal_id, analysis):
    """Read CEO hiring Yes/No selection from Streamlit session if available."""
    auto_status, auto_basis = _derive_internal_hiring_status(analysis or {})

    session_key_status = f"ceo_hiring_needed_{proposal_id}"
    session_key_basis = f"ceo_hiring_basis_{proposal_id}"

    try:
        selected_status = safe_text(st.session_state.get(session_key_status, auto_status)).strip()
        selected_basis = safe_text(st.session_state.get(session_key_basis, auto_basis)).strip()
    except Exception:
        selected_status = auto_status
        selected_basis = auto_basis

    if selected_status not in ["Yes", "No"]:
        selected_status = auto_status

    if not selected_basis:
        selected_basis = auto_basis

    return selected_status, selected_basis


def _hiring_notify_append_to_quote_summary(summary, hiring_status, hiring_basis):
    """Add internal hiring note only for executives, never for client quotation."""
    if safe_text(hiring_status) == "Yes":
        return (
            safe_text(summary)
            + " Internal hiring/contract support is required for this project. "
            + "HR and leadership should treat this as an active internal hiring action. "
            + f"Basis: {safe_text(hiring_basis)}"
        )
    return safe_text(summary)


def submit_proposal_decision(proposal_id, user, decision, comment, recommended_quote, recommended_timeline_months):
    """
    Wrapper over the existing submit_proposal_decision.

    Change:
    If CEO selects Hiring = Yes and sends quotation, all executives see that
    hiring/contract support is required in the active inbox notification.
    This remains internal only and is not added to the client quotation.
    """
    if _hiring_notify_previous_submit_proposal_decision is None:
        return False, "Decision function is unavailable."

    role_key = role_key_for_user(user)

    hiring_status = ""
    hiring_basis = ""

    if role_key == "ceo":
        try:
            report = get_proposal_report_by_id(proposal_id)
            analysis = report.get("analysis", {}) if report else {}
            hiring_status, hiring_basis = _hiring_notify_get_saved_decision_from_session(proposal_id, analysis)
        except Exception:
            hiring_status, hiring_basis = "", ""

    success, message = _hiring_notify_previous_submit_proposal_decision(
        proposal_id,
        user,
        decision,
        comment,
        recommended_quote,
        recommended_timeline_months,
    )

    if not success:
        return success, message

    if role_key == "ceo":
        try:
            df = read_proposal_store(create_if_missing=True)
            mask = df["proposal_id"].astype(str) == safe_text(proposal_id)

            if mask.any():
                # Save the CEO-selected hiring decision clearly.
                df.loc[mask, "hiring_necessary"] = hiring_status
                df.loc[mask, "hiring_necessity_basis"] = hiring_basis

                # Make the active executive notification explicitly mention hiring.
                existing_summary = safe_text(df.loc[mask, "last_update_summary"].iloc[0])
                df.loc[mask, "last_update_summary"] = _hiring_notify_append_to_quote_summary(
                    existing_summary,
                    hiring_status,
                    hiring_basis,
                )

                # Keep quotation sent as active unread notification for every executive.
                for role, seen_col in PROPOSAL_NOTIFICATION_COLUMNS.items():
                    df.loc[mask, seen_col] = "No"
                    seen_at_col = PROPOSAL_SEEN_AT_COLUMNS.get(role)
                    if seen_at_col:
                        df.loc[mask, seen_at_col] = ""

                upsert_current_proposal_from_df(df, mask)

                if hiring_status == "Yes":
                    append_proposal_history(
                        proposal_id,
                        user,
                        "CEO Hiring Required With Quotation",
                        decision="Hiring Required",
                        comment=hiring_basis,
                        recommended_quote=recommended_quote,
                        recommended_timeline_months=recommended_timeline_months,
                        summary=(
                            "CEO sent quotation and marked internal hiring/contract support as required. "
                            "All executives were notified in the active inbox."
                        ),
                    )

        except Exception:
            pass

    if role_key == "ceo" and hiring_status == "Yes":
        return True, (
            "CEO quotation sent to client. Every executive has been notified, "
            "and the active inbox now clearly shows that hiring/contract support is required."
        )

    return success, message

# =============================================================================
# FINAL PATCH: CLIENT ACTIVE PROJECT DASHBOARD + CLEAN TECH ARCHITECT UPDATE INBOX
# Add this at the very bottom of decisiondesk_chunks/05_design_system.py
# =============================================================================

# -----------------------------------------------------------------------------
# 1. Client dashboard: always show project dashboard after proposal acceptance
# -----------------------------------------------------------------------------

def is_client_delivery_kickstarted(report):
    """Route accepted proposals into the client delivery dashboard.

    Even if the detailed requirement or allocation is still pending, the client
    should see the delivery/progress area after accepting the quotation.
    """
    if not isinstance(report, dict):
        return False

    if safe_text(report.get("client_response")) != "Accept Proposal":
        return False

    try:
        project = get_project_for_proposal(report.get("proposal_id"))
        if project:
            return True
    except Exception:
        pass

    status_text = safe_text(report.get("workflow_status")).lower()
    return any(word in status_text for word in ["accepted", "delivery", "kickoff", "allocated", "project"])


def render_client_active_delivery_only(report, client_account):
    """Client-safe active project page."""
    st.markdown(
        """
        <div class="dd-dashboard-shell">
            <div class="dd-title-row">
                <div>
                    <div class="dd-section-title">Project delivery dashboard</div>
                    <div class="dd-section-subtitle">
                        Track your accepted project, current week, weekly progress, and Technical Architect messages.
                    </div>
                </div>
                <div class="dd-title-badge">Client-safe view</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_client_delivery_section(report, client_account)


def _client_latest_technical_architect_message(project_id):
    """Return latest Technical Architect / internal reply visible to client."""
    try:
        messages = read_simple_table("client_operations_messages", CLIENT_OPERATIONS_MESSAGE_COLUMNS)
    except Exception:
        return None

    if messages is None or messages.empty or "project_id" not in messages.columns:
        return None

    working = messages[messages["project_id"].astype(str) == safe_text(project_id)].copy()
    if working.empty:
        return None

    # Hide client's own messages; show latest Technical Architect/internal reply.
    if "sender_type" in working.columns:
        sender_type = working["sender_type"].fillna("").astype(str).str.lower()
        working = working[~sender_type.isin(["client", "external client"])]

    if working.empty:
        return None

    if "created_at" in working.columns:
        working = working.sort_values("created_at", ascending=False)

    return working.iloc[0].to_dict()


def _client_latest_weekly_update(project_id):
    """Return latest client-safe weekly update row."""
    try:
        updates = read_simple_table("weekly_project_updates", WEEKLY_UPDATE_COLUMNS)
    except Exception:
        return None

    if updates is None or updates.empty or "project_id" not in updates.columns:
        return None

    working = updates[updates["project_id"].astype(str) == safe_text(project_id)].copy()
    if working.empty:
        return None

    if "visible_to_client" in working.columns:
        visible = working["visible_to_client"].fillna("Yes").astype(str).str.lower()
        working = working[visible.isin(["yes", "true", "1", ""])]

    if working.empty:
        return None

    sort_col = "generated_at" if "generated_at" in working.columns else "created_at" if "created_at" in working.columns else None
    if sort_col:
        working = working.sort_values(sort_col, ascending=False)

    return working.iloc[0].to_dict()


def _client_plan_is_ready_for_targets(project_id, plan):
    """Client sees weekly targets only after Technical Architect approval and team allocation."""
    if not isinstance(plan, dict):
        return False

    status = safe_text(plan.get("approval_status")).lower()
    plan_approved = any(word in status for word in ["approved", "team allocated", "operations manager"])

    try:
        allocations = get_project_allocations(project_id)
        has_team = allocations is not None and not allocations.empty
    except Exception:
        has_team = False

    return plan_approved and has_team


def render_client_delivery_section(report, client_account):
    """Final client delivery dashboard.

    Client sees:
    - detailed requirement submission form before planning,
    - waiting message while Technical Architect verifies/allocation is pending,
    - after project starts: week number, completion %, weekly update, target list,
      and latest Technical Architect message.
    """
    if safe_text(report.get("client_response")) != "Accept Proposal":
        return

    project = ensure_project_for_accepted_proposal(report, client_account)
    project_id = safe_text(project.get("project_id"))
    plan = get_delivery_plan_for_client_project(project_id)

    st.markdown("### Project delivery update")

    # Step 1: accepted but no detailed requirement yet.
    if plan is None:
        st.success("Proposal accepted. Please submit the detailed requirement to start delivery planning.")
        st.info(
            "After you submit the detailed requirement, our Technical Architect AI Agent will draft the plan. "
            "The Technical Architect will verify it and allocate the delivery team before weekly targets are shown here."
        )

        uploaded_text = ""
        uploaded_name = ""

        upload = st.file_uploader(
            "Optional: upload a text requirement file",
            type=["txt", "md"],
            key=f"client_req_file_{project_id}",
        )

        if upload is not None:
            uploaded_name = upload.name
            try:
                uploaded_text = upload.read().decode("utf-8", errors="ignore")
            except Exception:
                uploaded_text = ""

        with st.form(f"client_requirement_form_{project_id}"):
            requirement_text = st.text_area(
                "Detailed requirement",
                value=uploaded_text,
                height=190,
                placeholder="Describe modules, user roles, integrations, cloud/access needs, reports, security needs, and priorities.",
            )
            submitted = st.form_submit_button("Submit detailed requirement", type="primary")

        if submitted:
            ok, msg = save_client_detailed_requirement(report, client_account, requirement_text, uploaded_name)
            if ok:
                st.success(
                    "Detailed requirement submitted. The Technical Architect will verify the delivery plan and allocate the team before weekly targets appear here."
                )
                st.rerun()
            else:
                st.error(msg)
        return

    # Step 2: detailed requirement exists, but team is not fully ready.
    client_ready = _client_plan_is_ready_for_targets(project_id, plan)

    if not client_ready:
        st.success("Your detailed requirement has been received.")
        st.info(
            "The Technical Architect AI Agent has drafted the delivery plan. "
            "Our Technical Architect is verifying the plan and allocating the delivery team. "
            "Weekly targets and progress percentage will appear here once the project team is allocated."
        )

        c1, c2, c3 = st.columns(3)
        c1.metric("Project", project_display_name(project=project, project_id=project_id))
        c2.metric("Planning status", safe_text(plan.get("approval_status"), "Technical Architect review pending"))

        try:
            allocations = get_project_allocations(project_id)
            team_count = 0 if allocations is None or allocations.empty else len(allocations)
        except Exception:
            team_count = 0

        c3.metric("Allocated team", team_count)

        latest_ta_msg = _client_latest_technical_architect_message(project_id)
        if latest_ta_msg:
            st.markdown("#### Latest message from Technical Architect")
            st.info(
                f"{safe_text(latest_ta_msg.get('message_text'))}\n\n"
                f"Sent at: {safe_text(latest_ta_msg.get('created_at'))}"
            )

        with st.expander("Message Technical Architect Agent", expanded=False):
            render_client_operations_conversation(project, report, client_account, viewer="client")

            with st.form(f"client_ops_message_form_pending_{project_id}"):
                msg = st.text_area(
                    "Type your message for the Technical Architect Agent",
                    height=110,
                    placeholder="Example: Please confirm rollout priority, access details, or integration sequence.",
                )
                submitted_msg = st.form_submit_button("Send message to Technical Architect Agent", type="primary")

            if submitted_msg:
                ok, message = save_client_message_to_operations(project, report, client_account, msg)
                if ok:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
        return

    # Step 3: project active, plan approved, team allocated.
    allocations = get_project_allocations(project_id)
    latest_generated_update = generate_weekly_update_if_needed(project, plan, allocations)
    latest_saved_update = _client_latest_weekly_update(project_id) or latest_generated_update
    progress = get_client_safe_project_progress(project_id)

    week_label = safe_text(progress.get("project_week_label"), "Week 1")
    completion = safe_text(progress.get("weekly_progress_percent") or progress.get("progress_percent") or "Not updated yet")
    week_start = safe_text(progress.get("week_start"), "-")
    week_end = safe_text(progress.get("week_end"), "-")
    friday = safe_text(progress.get("friday_checkpoint"), "-")
    required = safe_int(progress.get("mandatory_updates_required"), 0)
    received = safe_int(progress.get("mandatory_updates_received"), 0)
    pending = max(0, required - received)

    st.success("Your project has started. The delivery team is working on the verified requirement.")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Delivery status", "In progress")
    c2.metric(f"{week_label} completion", completion)
    c3.metric("Project week", week_label)
    c4.metric("Team updates", f"{received} / {required}")

    latest_update_text = safe_text(latest_saved_update.get("update_text") if isinstance(latest_saved_update, dict) else "")
    if not latest_update_text:
        latest_update_text = (
            f"This is the {week_label} delivery update. Team work is in progress. "
            f"Current completion is {completion}."
        )

    pending_line = (
        f"{pending} internal team update(s) are still pending for {week_label}. The delivery team is following up internally."
        if pending else
        f"All required team updates are submitted for {week_label}."
    )

    st.markdown(
        f"""
        <div class="dd-client-progress-card">
            <b>{week_label} project progress</b>
            <span>Completion: {completion}</span>
            <span>Week window: {week_start} to {week_end}</span>
            <span>Friday checkpoint: {friday}</span>
            <span>{pending_line}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### Weekly update from Technical Architect AI Agent")
    st.info(latest_update_text)

    latest_ta_msg = _client_latest_technical_architect_message(project_id)
    if latest_ta_msg:
        st.markdown("#### Latest message from Technical Architect")
        st.success(
            f"{safe_text(latest_ta_msg.get('message_text'))}\n\n"
            f"Sent at: {safe_text(latest_ta_msg.get('created_at'))}"
        )

    render_weekly_targets_panel(
        plan,
        title="Verified weekly target list",
        expanded=True,
        client_safe=True,
        key_prefix=f"client_verified_weekly_targets_{project_id}",
    )

    info_needed = get_client_safe_information_needed(plan, latest_saved_update)
    st.info(f"Information needed from your side: {info_needed}")

    with st.expander("Message Technical Architect Agent", expanded=False):
        st.caption("Recent-first conversation. Your Technical Architect can reply from the project dashboard.")
        render_client_operations_conversation(project, report, client_account, viewer="client")

        sent_key = f"client_ops_msg_sent_{project_id}"
        if st.session_state.get(sent_key, False):
            st.success("Your message has been sent to the Technical Architect Agent.")
            if st.button("Send another message", key=f"client_ops_msg_again_{project_id}"):
                st.session_state[sent_key] = False
                st.rerun()
        else:
            with st.form(f"client_ops_message_form_{project_id}"):
                msg = st.text_area(
                    "Type your message for the Technical Architect Agent",
                    height=110,
                    placeholder="Example: Please confirm rollout priority, access details, or integration sequence.",
                )
                submitted_msg = st.form_submit_button("Send message to Technical Architect Agent", type="primary")

            if submitted_msg:
                ok, message = save_client_message_to_operations(project, report, client_account, msg)
                if ok:
                    st.session_state[sent_key] = True
                    st.rerun()
                else:
                    st.error(message)


# -----------------------------------------------------------------------------
# 2. Technical Architect dashboard: show only real open employee requests
# -----------------------------------------------------------------------------

_NO_ACTION_PHRASES = [
    "",
    "none",
    "no",
    "na",
    "n/a",
    "nil",
    "no blocker",
    "no blockers",
    "no blocker mentioned",
    "no issue",
    "no issues",
    "nothing",
    "not applicable",
    "no support needed",
    "no support required",
    "no current-week update submitted",
    "no issue mentioned",
]


def _ta_clean_text(value):
    return re.sub(r"\s+", " ", safe_text(value)).strip()


def _ta_has_meaningful_employee_request(row):
    """Only blockers, support requests, risky status, or meaningful notes need TA action."""
    if row is None:
        return False

    if hasattr(row, "to_dict"):
        row = row.to_dict()

    status = safe_text(row.get("operations_status"), "Open").strip().lower()
    if status in ["closed", "done", "resolved", "completed"]:
        return False

    progress_status = safe_text(row.get("progress_status")).strip().lower()
    if progress_status in ["blocked", "minor risk", "risk", "delayed", "behind"]:
        return True

    try:
        progress_value = safe_number(row.get("progress_percent"), 100)
        if progress_value is not None and progress_value < 60:
            return True
    except Exception:
        pass

    for field in ["hurdles", "support_needed", "notes", "operations_resolution_note"]:
        text_value = _ta_clean_text(row.get(field)).lower()
        if text_value and text_value not in _NO_ACTION_PHRASES:
            return True

    return False


def get_open_employee_project_updates(project_id=None):
    """Return only employee updates that truly need Technical Architect action."""
    try:
        updates = get_employee_project_updates(project_id=project_id)
    except Exception:
        return pd.DataFrame(columns=EMPLOYEE_PROJECT_UPDATE_COLUMNS)

    if updates is None or updates.empty:
        return pd.DataFrame(columns=EMPLOYEE_PROJECT_UPDATE_COLUMNS)

    working = updates.copy()
    rows = []

    for _, row in working.iterrows():
        if _ta_has_meaningful_employee_request(row):
            rows.append(row.to_dict())

    if not rows:
        return pd.DataFrame(columns=working.columns)

    result = pd.DataFrame(rows)
    if "created_at" in result.columns:
        result = result.sort_values("created_at", ascending=False)
    return result


def close_employee_update_action(update_row, user, closing_note):
    """Close one employee blocker/support request from Technical Architect dashboard."""
    if update_row is None:
        return False, "No employee update selected."

    if hasattr(update_row, "to_dict"):
        update_row = update_row.to_dict()

    update_id = safe_text(update_row.get("employee_update_id"))
    if not update_id:
        return False, "Employee update ID is missing."

    note = safe_text(closing_note).strip()
    if not note:
        return False, "Please add a short closing note."

    row = {column: safe_text(update_row.get(column, "")) for column in EMPLOYEE_PROJECT_UPDATE_COLUMNS}
    row["operations_status"] = "Closed"
    row["operations_done_by"] = actor_name(user)
    row["operations_done_at"] = current_timestamp()
    row["operations_resolution_note"] = note

    upsert_simple_row("employee_project_updates", "employee_update_id", EMPLOYEE_PROJECT_UPDATE_COLUMNS, row)

    try:
        append_proposal_history(
            safe_text(row.get("proposal_id")),
            user,
            "Technical Architect Closed Employee Request",
            comment=note,
            summary=(
                f"Technical Architect closed employee update/request from "
                f"{safe_text(row.get('employee_name'))} for {safe_text(row.get('week_label'))}."
            ),
        )
    except Exception:
        pass

    return True, "Employee request/update has been closed."


def render_employee_update_inbox_with_done(updates_df, user, project_id=None, key_prefix="employee_updates"):
    """Clean Technical Architect employee update section.

    Normal weekly updates like On track / 95% / no blocker are shown only as history.
    They do not appear as open requests and do not show a closing form.
    """
    if updates_df is None or updates_df.empty:
        st.success("No employee weekly updates or requests have been submitted for this project yet.")
        return

    working = updates_df.copy()
    if "created_at" in working.columns:
        working = working.sort_values("created_at", ascending=False)

    action_rows = []
    history_rows = []

    for _, row in working.iterrows():
        row_dict = row.to_dict()
        issue_text = (
            _ta_clean_text(row_dict.get("support_needed"))
            or _ta_clean_text(row_dict.get("hurdles"))
            or _ta_clean_text(row_dict.get("notes"))
        )

        history_rows.append({
            "Submitted at": safe_text(row_dict.get("created_at")),
            "Week": safe_text(row_dict.get("week_label")),
            "Employee": safe_text(row_dict.get("employee_name")),
            "Status": safe_text(row_dict.get("progress_status")),
            "Progress": (safe_text(row_dict.get("progress_percent")) + "%") if safe_text(row_dict.get("progress_percent")) else "",
            "Module": safe_text(row_dict.get("assigned_module")),
            "Note / request": issue_text or "No blocker or support request",
            "Technical Architect status": safe_text(row_dict.get("operations_status"), "Open"),
        })

        if _ta_has_meaningful_employee_request(row_dict):
            action_rows.append(row_dict)

    if action_rows:
        st.warning(f"Open employee request(s) needing Technical Architect action: {len(action_rows)}")

        labels = []
        for idx, row in enumerate(action_rows, start=1):
            issue_text = (
                _ta_clean_text(row.get("support_needed"))
                or _ta_clean_text(row.get("hurdles"))
                or _ta_clean_text(row.get("notes"))
                or safe_text(row.get("progress_status"))
            )
            labels.append(
                f"{idx}. {safe_text(row.get('created_at'))} | "
                f"{safe_text(row.get('employee_name'))} | "
                f"{safe_text(row.get('progress_status'))} | "
                f"{safe_text(row.get('progress_percent'))}% | "
                f"{safe_text(row.get('assigned_module'))} | {issue_text[:45]}"
            )

        selected_label = st.selectbox(
            "Choose employee request to review",
            labels,
            key=f"{key_prefix}_real_request_select",
        )
        selected_row = action_rows[labels.index(selected_label)]

        st.markdown("#### Selected employee request")
        c1, c2, c3 = st.columns(3)
        c1.metric("Employee", safe_text(selected_row.get("employee_name")))
        c2.metric("Status", safe_text(selected_row.get("progress_status")))
        c3.metric("Weekly progress", f"{safe_text(selected_row.get('progress_percent'))}%")

        request_text = (
            _ta_clean_text(selected_row.get("support_needed"))
            or _ta_clean_text(selected_row.get("hurdles"))
            or _ta_clean_text(selected_row.get("notes"))
            or "This update needs review because the status/progress indicates risk."
        )
        st.info(request_text)

        with st.form(f"{key_prefix}_close_real_request_{safe_text(selected_row.get('employee_update_id'))}"):
            closing_note = st.text_area(
                "Technical Architect closing note",
                height=100,
                placeholder="Example: Access shared, blocker clarified, backup assigned, or issue discussed.",
            )
            close_clicked = st.form_submit_button("Close selected request", type="primary")

        if close_clicked:
            ok, msg = close_employee_update_action(selected_row, user, closing_note)
            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

    else:
        st.success("No open employee blockers or support requests. Normal weekly updates are shown below as history only.")

    with st.expander("Recent weekly update history", expanded=False):
        if history_rows:
            st.dataframe(pd.DataFrame(history_rows), use_container_width=True, hide_index=True)
        else:
            st.info("No weekly update history available.")

# =============================================================================
# SMALL PATCH: POST-KICKOFF REQUIREMENT CHANGE + ADD MORE EMPLOYEES
# Add at the very bottom of decisiondesk_chunks/05_design_system.py
# =============================================================================

try:
    _postkick_previous_render_operations_delivery_workspace = render_operations_delivery_workspace
except Exception:
    _postkick_previous_render_operations_delivery_workspace = None


def _postkick_is_project_started(project, plan=None):
    """True only after kickoff/team allocation/delivery start."""
    if not isinstance(project, dict):
        return False

    status_text = (
        safe_text(project.get("project_status")).lower()
        + " "
        + safe_text(plan.get("approval_status") if isinstance(plan, dict) else "").lower()
    )

    if any(word in status_text for word in ["kickoff", "allocated", "in progress", "delivery plan approved", "team allocated"]):
        return True

    try:
        allocations = get_project_allocations(project.get("project_id"))
        return allocations is not None and not allocations.empty
    except Exception:
        return False


def _postkick_project_members(project_id, data=None, include_actor_id=""):
    """Return allocated project members only.

    Client is never included.
    CEO/founder is excluded.
    Actor can be excluded to avoid notifying the person who made the change.
    """
    try:
        allocations = get_project_allocations(project_id)
    except Exception:
        allocations = pd.DataFrame()

    if allocations is None or allocations.empty:
        return []

    executive_ids = set()
    try:
        executive_ids = _executive_user_ids_from_data(data)
    except Exception:
        executive_ids = set()

    actor = safe_text(include_actor_id).upper()
    members = []

    for _, row in allocations.iterrows():
        emp_id = safe_text(row.get("employee_id")).upper()
        emp_name = safe_text(row.get("employee_name")) or emp_id
        designation = safe_text(row.get("designation") or row.get("project_role")).lower()

        if not emp_id:
            continue
        if actor and emp_id == actor:
            continue
        if emp_id in executive_ids:
            continue
        if any(word in designation for word in ["ceo", "founder"]):
            continue

        members.append({
            "employee_id": emp_id,
            "employee_name": emp_name,
        })

    # unique by employee_id
    unique = {}
    for item in members:
        unique[item["employee_id"]] = item
    return list(unique.values())


def _postkick_notify_project_members(project, user, notification_type, message, data=None):
    """Notify project members only. No client notification. No CEO notification."""
    project_id = safe_text(project.get("project_id"))
    proposal_id = safe_text(project.get("proposal_id"))
    now = current_timestamp()
    members = _postkick_project_members(project_id, data=data, include_actor_id=actor_id(user))

    notified = 0
    for member in members:
        try:
            notification = {
                "notification_id": make_notification_id(),
                "employee_id": member["employee_id"],
                "project_id": project_id,
                "proposal_id": proposal_id,
                "notification_type": notification_type,
                "message": message,
                "seen": "No",
                "created_at": now,
                "seen_at": "",
            }
            upsert_simple_row(
                "employee_notifications",
                "notification_id",
                EMPLOYEE_NOTIFICATION_COLUMNS,
                notification,
            )
            notified += 1
        except Exception:
            pass

    return notified


def _postkick_get_active_projects_for_ta(focus_proposal_id=None):
    """Projects available for post-kickoff edit/add-member control."""
    try:
        projects = read_simple_table("projects", PROJECT_COLUMNS)
    except Exception:
        return pd.DataFrame(columns=PROJECT_COLUMNS)

    if projects is None or projects.empty:
        return pd.DataFrame(columns=PROJECT_COLUMNS)

    working = projects.copy()

    if focus_proposal_id and "proposal_id" in working.columns:
        working = working[working["proposal_id"].astype(str) == safe_text(focus_proposal_id)]

    if working.empty:
        return working

    active_rows = []
    for _, row in working.iterrows():
        project = row.to_dict()
        plan = get_delivery_plan_for_client_project(project.get("project_id"))
        if _postkick_is_project_started(project, plan):
            active_rows.append(project)

    if not active_rows:
        return pd.DataFrame(columns=working.columns)

    result = pd.DataFrame(active_rows)

    sort_col = "updated_at" if "updated_at" in result.columns else "created_at" if "created_at" in result.columns else "project_id"
    try:
        result = result.sort_values(sort_col, ascending=False)
    except Exception:
        pass

    return result


def save_postkick_requirement_change(project, plan, user, updated_requirement, change_note, data=None):
    """Save Technical Architect requirement change after kickoff and notify project members."""
    if not isinstance(project, dict):
        return False, "Project was not found."

    if not isinstance(plan, dict) or not safe_text(plan.get("delivery_plan_id")):
        return False, "Delivery plan was not found for this project."

    if not _postkick_is_project_started(project, plan):
        return False, "This control is available only after project kickoff/team allocation."

    updated_requirement = safe_text(updated_requirement).strip()
    change_note = safe_text(change_note).strip()

    if len(updated_requirement) < 20:
        return False, "Please enter the updated project requirement clearly."
    if not change_note:
        return False, "Please add a short reason or change summary."

    now = current_timestamp()
    project_id = safe_text(project.get("project_id"))
    proposal_id = safe_text(project.get("proposal_id"))

    previous_requirement = safe_text(plan.get("raw_requirement_text"))

    updated_plan = {column: safe_text(plan.get(column, "")) for column in DELIVERY_PLAN_COLUMNS}
    updated_plan["raw_requirement_text"] = updated_requirement
    updated_plan["updated_at"] = now

    # Keep the plan approved; this is a controlled post-kickoff requirement update.
    if not safe_text(updated_plan.get("approval_status")):
        updated_plan["approval_status"] = "Approved by Technical Architect Agent"

    upsert_simple_row(
        "delivery_plans",
        "delivery_plan_id",
        DELIVERY_PLAN_COLUMNS,
        updated_plan,
    )

    try:
        project["updated_at"] = now
        project["project_status"] = safe_text(project.get("project_status")) or "In progress"
        upsert_simple_row("projects", "project_id", PROJECT_COLUMNS, project)
    except Exception:
        pass

    message = (
        f"Project requirement updated by Technical Architect {actor_name(user)} for "
        f"{project_display_name(project=project, project_id=project_id)}. "
        f"Change summary: {change_note}. Please review the updated requirement in your project workbench."
    )

    notified_count = _postkick_notify_project_members(
        project,
        user,
        "Project Requirement Changed",
        message,
        data=data,
    )

    try:
        append_proposal_history(
            proposal_id,
            user,
            "Post-Kickoff Requirement Changed",
            comment=(
                f"Change summary: {change_note}\n\n"
                f"Previous requirement:\n{previous_requirement}\n\n"
                f"Updated requirement:\n{updated_requirement}"
            ),
            summary=(
                "Technical Architect updated the project requirement after kickoff. "
                f"{notified_count} allocated project member(s) were notified. Client and CEO were not notified."
            ),
        )
    except Exception:
        pass

    return True, f"Project requirement updated. {notified_count} project member(s) were notified. Client and CEO were not notified."


def _postkick_existing_allocated_employee_ids(project_id):
    try:
        allocations = get_project_allocations(project_id)
    except Exception:
        return set()

    if allocations is None or allocations.empty:
        return set()

    return set(allocations["employee_id"].astype(str).str.upper().tolist()) if "employee_id" in allocations.columns else set()


def render_postkick_requirement_and_team_controls(user, data=None, focus_proposal_id=None):
    """Technical Architect post-kickoff controls."""
    if role_key_for_user(user) != "operations":
        return

    projects = _postkick_get_active_projects_for_ta(focus_proposal_id=focus_proposal_id)
    if projects is None or projects.empty:
        return

    st.markdown(
        """
        <div class="dd-section-card dd-dashboard-shell">
            <div class="dd-section-title">Post-kickoff project controls</div>
            <div class="dd-section-subtitle">
                Use this only after the project has started. Requirement changes notify allocated project members only.
                Client and CEO are not notified from this control.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    labels = []
    rows = []
    for idx, (_, row) in enumerate(projects.iterrows(), start=1):
        project_id = safe_text(row.get("project_id"))
        labels.append(
            f"{idx}. {project_display_name(project=row, project_id=project_id)} | {project_id} | {safe_text(row.get('project_status'))}"
        )
        rows.append(row.to_dict())

    if not labels:
        return

    if focus_proposal_id and len(labels) == 1:
        selected_project = rows[0]
    else:
        selected_label = st.selectbox(
            "Choose active project for post-kickoff update",
            labels,
            key=f"postkick_project_select_{actor_id(user)}_{safe_text(focus_proposal_id) or 'all'}",
        )
        selected_project = rows[labels.index(selected_label)]

    project_id = safe_text(selected_project.get("project_id"))
    plan = get_delivery_plan_for_client_project(project_id)

    if not plan:
        st.info("Delivery plan is not available yet for this project.")
        return

    with st.expander("Change project requirement after kickoff", expanded=False):
        st.warning(
            "Changing the requirement after kickoff will notify allocated project members only. "
            "The client and CEO will not receive this notification."
        )

        updated_requirement = st.text_area(
            "Updated project requirement",
            value=safe_text(plan.get("raw_requirement_text")),
            height=220,
            key=f"postkick_updated_requirement_{project_id}",
        )

        change_note = st.text_area(
            "Reason / change summary for project team",
            height=90,
            placeholder="Example: Client clarified branch-wise access and dashboard priority. Update current sprint accordingly.",
            key=f"postkick_requirement_change_note_{project_id}",
        )

        if st.button(
            "Save requirement change and notify project members",
            key=f"postkick_save_requirement_change_{project_id}",
            type="primary",
        ):
            ok, msg = save_postkick_requirement_change(
                selected_project,
                plan,
                user,
                updated_requirement,
                change_note,
                data=data,
            )
            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

    with st.expander("Add more delivery employees after kickoff", expanded=False):
        st.caption(
            "This adds extra delivery employees to the active project. Existing allocated members and the new members are notified. "
            "Executives, CEO, Sales, HR, and Finance are excluded from allocation."
        )

        employees = data.get("employees", pd.DataFrame()).copy() if isinstance(data, dict) else pd.DataFrame()
        try:
            employees = filter_project_delivery_employees(employees, data)
        except Exception:
            pass

        if employees is None or employees.empty:
            st.warning("No eligible delivery employees are available.")
            return

        already_allocated = _postkick_existing_allocated_employee_ids(project_id)
        if "employee_id" in employees.columns:
            employees = employees[~employees["employee_id"].astype(str).str.upper().isin(already_allocated)]

        if employees.empty:
            st.info("All eligible delivery employees shown in the current data are already allocated to this project.")
            return

        employees["label"] = employees.apply(
            lambda r: (
                f"{r.get('employee_id')} - {r.get('employee_name')} "
                f"({r.get('designation')}, available {r.get('availability_percent', r.get('available_bandwidth', ''))}%)"
            ),
            axis=1,
        )

        selected = st.multiselect(
            "Select additional delivery employees",
            employees["label"].tolist(),
            key=f"postkick_add_people_select_{project_id}",
        )

        selected_rows = []
        for label in selected:
            emp = employees[employees["label"] == label].iloc[0].to_dict()

            c1, c2, c3 = st.columns([1, 1, 1])
            with c1:
                module = st.text_input(
                    f"Module for {emp.get('employee_name')}",
                    value=safe_text(emp.get("primary_skill")) or safe_text(emp.get("designation")),
                    key=f"postkick_module_{project_id}_{emp.get('employee_id')}",
                )
            with c2:
                role = st.text_input(
                    f"Project role for {emp.get('employee_name')}",
                    value=safe_text(emp.get("designation")),
                    key=f"postkick_role_{project_id}_{emp.get('employee_id')}",
                )
            with c3:
                allocation_percent = st.number_input(
                    f"Allocation % for {emp.get('employee_name')}",
                    min_value=5,
                    max_value=100,
                    value=40,
                    step=5,
                    key=f"postkick_alloc_pct_{project_id}_{emp.get('employee_id')}",
                )

            selected_rows.append({
                "employee_id": safe_text(emp.get("employee_id")),
                "employee_name": safe_text(emp.get("employee_name")),
                "department": safe_text(emp.get("department")),
                "designation": safe_text(emp.get("designation")),
                "project_role": role,
                "assigned_module": module,
                "responsibility_summary": (
                    f"Added after kickoff to support {module} for "
                    f"{project_display_name(project=selected_project, project_id=project_id)}. "
                    "Submit mandatory weekly progress updates and raise blockers/support needs from the employee workbench."
                ),
                "allocation_percent": str(allocation_percent),
            })

        if st.button(
            "Add selected employees and notify project team",
            key=f"postkick_add_people_button_{project_id}",
            type="primary",
        ):
            if not selected_rows:
                st.error("Select at least one additional delivery employee.")
                return

            manager_plan_text = safe_text(plan.get("operations_manager_plan") or plan.get("operations_agent_plan"))
            ok, msg = approve_delivery_plan_and_allocate(
                selected_project,
                plan,
                user,
                manager_plan_text,
                selected_rows,
            )

            if ok:
                names = ", ".join([safe_text(row.get("employee_name")) for row in selected_rows])
                note = (
                    f"Additional delivery employee(s) added to "
                    f"{project_display_name(project=selected_project, project_id=project_id)}: {names}. "
                    "Please check updated responsibilities and continue weekly updates."
                )

                notified_count = _postkick_notify_project_members(
                    selected_project,
                    user,
                    "Project Team Updated",
                    note,
                    data=data,
                )

                try:
                    append_proposal_history(
                        safe_text(selected_project.get("proposal_id")),
                        user,
                        "Post-Kickoff Team Expanded",
                        comment=note,
                        summary=f"Technical Architect added more delivery employee(s) after kickoff. {notified_count} project member(s) were notified. Client and CEO were not notified.",
                    )
                except Exception:
                    pass

                st.success(f"{msg} Project team notification sent to {notified_count} member(s). Client and CEO were not notified.")
                st.rerun()
            else:
                st.error(msg)


def render_operations_delivery_workspace(user, data, focus_proposal_id=None):
    """Existing Technical Architect workspace + post-kickoff controls."""
    if _postkick_previous_render_operations_delivery_workspace is not None:
        _postkick_previous_render_operations_delivery_workspace(user, data, focus_proposal_id=focus_proposal_id)

    render_postkick_requirement_and_team_controls(
        user,
        data=data,
        focus_proposal_id=focus_proposal_id,
    )

# =============================================================================
# SMALL PATCH: POST-KICKOFF AI REPLAN ONLY FOR PENDING WEEKS + CLEAR INPUTS
# Add at the very bottom of decisiondesk_chunks/05_design_system.py
# =============================================================================

def _postkick_current_week_number(project_id):
    """Current project week number. If project started 3 weeks ago, this returns Week 4."""
    try:
        info = get_project_week_info(project_id, datetime.now())
        return max(1, safe_int(info.get("week_number"), 1))
    except Exception:
        return 1


def _postkick_week_target_map(target_text):
    """Parse Week N target lines into {week_no: target}."""
    targets = {}
    for line in safe_text(target_text).splitlines():
        item = line.strip().lstrip("-*").strip()
        if not item:
            continue

        match = re.match(r"^Week\s*(\d+)\s*[:\-]\s*(.+)$", item, flags=re.IGNORECASE)
        if match:
            week_no = safe_int(match.group(1), 0)
            target = safe_text(match.group(2)).strip()
            if week_no > 0 and target:
                targets[week_no] = target

    return targets


def _postkick_merge_weekly_targets_for_pending_weeks(old_targets_text, new_targets_text, start_week, project_label=""):
    """Keep completed weeks unchanged and replace only current/pending weeks."""
    old_map = _postkick_week_target_map(old_targets_text)
    new_map = _postkick_week_target_map(new_targets_text)

    max_week = max(
        list(old_map.keys() or [0]) + list(new_map.keys() or [0]) + [safe_int(start_week, 1)]
    )

    lines = [
        "Technical Architect Agent - Revised Weekly Delivery Targets",
        f"Project: {safe_text(project_label) or 'Client project'}",
        f"Revision rule: Weeks before Week {safe_int(start_week, 1)} are preserved. Week {safe_int(start_week, 1)} onward is regenerated from the updated requirement.",
        "",
    ]

    for week_no in range(1, max_week + 1):
        if week_no < safe_int(start_week, 1):
            target = old_map.get(week_no) or new_map.get(week_no) or "Previously planned delivery work"
        else:
            target = new_map.get(week_no) or old_map.get(week_no) or "Continue revised delivery work based on updated requirement"
        lines.append(f"Week {week_no}: {target}")

    lines.extend([
        "",
        "Employee update rule: every allocated employee must submit weekly progress, blockers, support needs, and notes from the employee project workbench before the week closes.",
    ])

    return "\n".join(lines)


def _postkick_replace_weekly_targets_in_plan_text(plan_text, revised_targets):
    """Remove old weekly target section from plan text and append revised weekly targets."""
    text_value = safe_text(plan_text).strip()

    if not text_value:
        return revised_targets

    # Remove old target section if it exists.
    patterns = [
        r"\n\s*Technical Architect Agent\s*-\s*Weekly Delivery Targets.*$",
        r"\n\s*Technical Architect Agent\s*-\s*Revised Weekly Delivery Targets.*$",
        r"\n\s*Weekly Delivery Targets.*$",
    ]

    cleaned = text_value
    for pattern in patterns:
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE | re.DOTALL).strip()

    return cleaned.rstrip() + "\n\n" + revised_targets


def _postkick_generate_revised_ai_plan_and_targets(project, plan, updated_requirement, start_week):
    """Generate a new AI delivery plan and weekly targets, then merge only pending weeks."""
    project_id = safe_text(project.get("project_id"))
    proposal_id = safe_text(project.get("proposal_id"))

    try:
        report = get_proposal_report_by_id(proposal_id) or {}
    except Exception:
        report = {}

    if not isinstance(report, dict):
        report = {}

    report.setdefault("proposal_id", proposal_id)
    report.setdefault("analysis", {})

    project_label = project_display_name(project=project, project_id=project_id)

    old_targets_text = weekly_targets_text_from_plan(plan)

    try:
        new_full_targets_text = build_weekly_targets_for_delivery(report, updated_requirement)
    except Exception:
        new_full_targets_text = ""

    if not new_full_targets_text:
        new_full_targets_text = (
            "Technical Architect Agent - Weekly Delivery Targets\n"
            f"Project type: {safe_text(report.get('analysis', {}).get('project_type')) or project_label}\n\n"
            f"Week {safe_int(start_week, 1)}: Reconfirm updated requirement and adjust active sprint scope.\n"
            f"Week {safe_int(start_week, 1) + 1}: Continue implementation based on the updated requirement.\n"
            f"Week {safe_int(start_week, 1) + 2}: Complete revised module changes, QA, and integration checks.\n"
        )

    revised_targets = _postkick_merge_weekly_targets_for_pending_weeks(
        old_targets_text,
        new_full_targets_text,
        start_week,
        project_label=project_label,
    )

    try:
        new_plan_text = build_operations_agent_delivery_plan(report, updated_requirement)
    except Exception:
        new_plan_text = safe_text(plan.get("operations_manager_plan") or plan.get("operations_agent_plan"))

    revised_plan_text = _postkick_replace_weekly_targets_in_plan_text(new_plan_text, revised_targets)

    return revised_plan_text, revised_targets


def save_postkick_requirement_change(project, plan, user, updated_requirement, change_note, data=None):
    """Save post-kickoff requirement change and regenerate AI plan for pending weeks only."""
    if not isinstance(project, dict):
        return False, "Project was not found."

    if not isinstance(plan, dict) or not safe_text(plan.get("delivery_plan_id")):
        return False, "Delivery plan was not found for this project."

    if not _postkick_is_project_started(project, plan):
        return False, "This control is available only after project kickoff/team allocation."

    updated_requirement = safe_text(updated_requirement).strip()
    change_note = safe_text(change_note).strip()

    if len(updated_requirement) < 20:
        return False, "Please enter the updated project requirement clearly."

    if not change_note:
        return False, "Please add a short reason or change summary."

    now = current_timestamp()
    project_id = safe_text(project.get("project_id"))
    proposal_id = safe_text(project.get("proposal_id"))
    start_week = _postkick_current_week_number(project_id)

    previous_requirement = safe_text(plan.get("raw_requirement_text"))
    revised_plan_text, revised_targets = _postkick_generate_revised_ai_plan_and_targets(
        project,
        plan,
        updated_requirement,
        start_week,
    )

    updated_plan = {column: safe_text(plan.get(column, "")) for column in DELIVERY_PLAN_COLUMNS}
    updated_plan["raw_requirement_text"] = updated_requirement
    updated_plan["operations_agent_plan"] = revised_plan_text
    updated_plan["operations_manager_plan"] = revised_plan_text
    updated_plan["module_breakdown"] = revised_targets
    updated_plan["weekly_targets"] = revised_targets
    updated_plan["approval_status"] = "Approved by Technical Architect Agent - Requirement Revised After Kickoff"
    updated_plan["approved_by"] = actor_name(user)
    updated_plan["approved_at"] = now
    updated_plan["updated_at"] = now

    upsert_simple_row(
        "delivery_plans",
        "delivery_plan_id",
        DELIVERY_PLAN_COLUMNS,
        updated_plan,
    )

    try:
        project["updated_at"] = now
        project["project_status"] = safe_text(project.get("project_status")) or "In progress"
        upsert_simple_row("projects", "project_id", PROJECT_COLUMNS, project)
    except Exception:
        pass

    message = (
        f"Project requirement updated by Technical Architect {actor_name(user)} for "
        f"{project_display_name(project=project, project_id=project_id)}. "
        f"AI regenerated the delivery plan and weekly targets from Week {start_week} onward only. "
        f"Change summary: {change_note}. Please review the updated requirement and pending-week targets in your project workbench."
    )

    notified_count = _postkick_notify_project_members(
        project,
        user,
        "Project Requirement Changed",
        message,
        data=data,
    )

    try:
        append_proposal_history(
            proposal_id,
            user,
            "Post-Kickoff Requirement Changed",
            comment=(
                f"Change summary: {change_note}\n\n"
                f"Targets changed from: Week {start_week}\n\n"
                f"Previous requirement:\n{previous_requirement}\n\n"
                f"Updated requirement:\n{updated_requirement}\n\n"
                f"Revised weekly targets:\n{revised_targets}"
            ),
            summary=(
                f"Technical Architect updated the project requirement after kickoff. "
                f"AI regenerated the delivery plan and weekly targets from Week {start_week} onward. "
                f"{notified_count} allocated project member(s) were notified. Client and CEO were not notified."
            ),
        )
    except Exception:
        pass

    return True, (
        f"Update sent successfully. AI regenerated pending weekly targets from Week {start_week} onward. "
        f"{notified_count} project member(s) were notified. Client and CEO were not notified."
    )


def render_postkick_requirement_and_team_controls(user, data=None, focus_proposal_id=None):
    """Technical Architect post-kickoff controls with clear inputs after success."""
    if role_key_for_user(user) != "operations":
        return

    projects = _postkick_get_active_projects_for_ta(focus_proposal_id=focus_proposal_id)
    if projects is None or projects.empty:
        return

    st.markdown(
        """
        <div class="dd-section-card dd-dashboard-shell">
            <div class="dd-section-title">Post-kickoff project controls</div>
            <div class="dd-section-subtitle">
                Use this only after the project has started. Requirement changes regenerate AI delivery planning only for pending weeks.
                Project members are notified. Client and CEO are not notified.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    labels = []
    rows = []
    for idx, (_, row) in enumerate(projects.iterrows(), start=1):
        project_id = safe_text(row.get("project_id"))
        labels.append(
            f"{idx}. {project_display_name(project=row, project_id=project_id)} | {project_id} | {safe_text(row.get('project_status'))}"
        )
        rows.append(row.to_dict())

    if not labels:
        return

    if focus_proposal_id and len(labels) == 1:
        selected_project = rows[0]
    else:
        selected_label = st.selectbox(
            "Choose active project for post-kickoff update",
            labels,
            key=f"postkick_project_select_{actor_id(user)}_{safe_text(focus_proposal_id) or 'all'}",
        )
        selected_project = rows[labels.index(selected_label)]

    project_id = safe_text(selected_project.get("project_id"))
    plan = get_delivery_plan_for_client_project(project_id)

    if not plan:
        st.info("Delivery plan is not available yet for this project.")
        return

    success_key = f"postkick_req_success_msg_{project_id}"
    reset_counter_key = f"postkick_req_reset_counter_{project_id}"
    reset_counter = safe_int(st.session_state.get(reset_counter_key), 0)

    success_message = safe_text(st.session_state.get(success_key))
    if success_message:
        st.success(success_message)

    with st.expander("Change project requirement after kickoff", expanded=False):
        current_week = _postkick_current_week_number(project_id)

        st.warning(
            f"Changing the requirement now will preserve completed weeks and regenerate targets from Week {current_week} onward. "
            "Allocated project members will be notified. Client and CEO will not be notified."
        )

        current_requirement = safe_text(plan.get("raw_requirement_text"))
        if current_requirement:
            st.text_area(
                "Current saved requirement",
                value=current_requirement,
                height=150,
                disabled=True,
                key=f"postkick_current_requirement_readonly_{project_id}_{reset_counter}",
            )

        updated_requirement = st.text_area(
            "Updated requirement / changed requirement",
            value="",
            height=180,
            placeholder="Enter only the latest updated requirement or full corrected requirement. This field clears after successful notification.",
            key=f"postkick_updated_requirement_{project_id}_{reset_counter}",
        )

        change_note = st.text_area(
            "Reason / change summary for project team",
            value="",
            height=90,
            placeholder="Example: Client clarified branch-wise access and dashboard priority. Update current sprint accordingly.",
            key=f"postkick_requirement_change_note_{project_id}_{reset_counter}",
        )

        if st.button(
            "Save requirement change and notify project members",
            key=f"postkick_save_requirement_change_{project_id}_{reset_counter}",
            type="primary",
        ):
            ok, msg = save_postkick_requirement_change(
                selected_project,
                plan,
                user,
                updated_requirement,
                change_note,
                data=data,
            )

            if ok:
                st.session_state[success_key] = msg
                st.session_state[reset_counter_key] = reset_counter + 1
                st.rerun()
            else:
                st.error(msg)

    with st.expander("Add more delivery employees after kickoff", expanded=False):
        st.caption(
            "This adds extra delivery employees to the active project. Existing allocated members and the new members are notified. "
            "Executives, CEO, Sales, HR, and Finance are excluded from allocation."
        )

        employees = data.get("employees", pd.DataFrame()).copy() if isinstance(data, dict) else pd.DataFrame()
        try:
            employees = filter_project_delivery_employees(employees, data)
        except Exception:
            pass

        if employees is None or employees.empty:
            st.warning("No eligible delivery employees are available.")
            return

        already_allocated = _postkick_existing_allocated_employee_ids(project_id)
        if "employee_id" in employees.columns:
            employees = employees[~employees["employee_id"].astype(str).str.upper().isin(already_allocated)]

        if employees.empty:
            st.info("All eligible delivery employees shown in the current data are already allocated to this project.")
            return

        employees["label"] = employees.apply(
            lambda r: (
                f"{r.get('employee_id')} - {r.get('employee_name')} "
                f"({r.get('designation')}, available {r.get('availability_percent', r.get('available_bandwidth', ''))}%)"
            ),
            axis=1,
        )

        selected = st.multiselect(
            "Select additional delivery employees",
            employees["label"].tolist(),
            key=f"postkick_add_people_select_{project_id}",
        )

        selected_rows = []
        for label in selected:
            emp = employees[employees["label"] == label].iloc[0].to_dict()

            c1, c2, c3 = st.columns([1, 1, 1])
            with c1:
                module = st.text_input(
                    f"Module for {emp.get('employee_name')}",
                    value=safe_text(emp.get("primary_skill")) or safe_text(emp.get("designation")),
                    key=f"postkick_module_{project_id}_{emp.get('employee_id')}",
                )
            with c2:
                role = st.text_input(
                    f"Project role for {emp.get('employee_name')}",
                    value=safe_text(emp.get("designation")),
                    key=f"postkick_role_{project_id}_{emp.get('employee_id')}",
                )
            with c3:
                allocation_percent = st.number_input(
                    f"Allocation % for {emp.get('employee_name')}",
                    min_value=5,
                    max_value=100,
                    value=40,
                    step=5,
                    key=f"postkick_alloc_pct_{project_id}_{emp.get('employee_id')}",
                )

            selected_rows.append({
                "employee_id": safe_text(emp.get("employee_id")),
                "employee_name": safe_text(emp.get("employee_name")),
                "department": safe_text(emp.get("department")),
                "designation": safe_text(emp.get("designation")),
                "project_role": role,
                "assigned_module": module,
                "responsibility_summary": (
                    f"Added after kickoff to support {module} for "
                    f"{project_display_name(project=selected_project, project_id=project_id)}. "
                    "Submit mandatory weekly progress updates and raise blockers/support needs from the employee workbench."
                ),
                "allocation_percent": str(allocation_percent),
            })

        if st.button(
            "Add selected employees and notify project team",
            key=f"postkick_add_people_button_{project_id}",
            type="primary",
        ):
            if not selected_rows:
                st.error("Select at least one additional delivery employee.")
                return

            manager_plan_text = safe_text(plan.get("operations_manager_plan") or plan.get("operations_agent_plan"))
            ok, msg = approve_delivery_plan_and_allocate(
                selected_project,
                plan,
                user,
                manager_plan_text,
                selected_rows,
            )

            if ok:
                names = ", ".join([safe_text(row.get("employee_name")) for row in selected_rows])
                note = (
                    f"Additional delivery employee(s) added to "
                    f"{project_display_name(project=selected_project, project_id=project_id)}: {names}. "
                    "Please check updated responsibilities and continue weekly updates."
                )

                notified_count = _postkick_notify_project_members(
                    selected_project,
                    user,
                    "Project Team Updated",
                    note,
                    data=data,
                )

                try:
                    append_proposal_history(
                        safe_text(selected_project.get("proposal_id")),
                        user,
                        "Post-Kickoff Team Expanded",
                        comment=note,
                        summary=(
                            f"Technical Architect added more delivery employee(s) after kickoff. "
                            f"{notified_count} project member(s) were notified. Client and CEO were not notified."
                        ),
                    )
                except Exception:
                    pass

                st.success(f"{msg} Project team notification sent to {notified_count} member(s). Client and CEO were not notified.")
                st.rerun()
            else:
                st.error(msg)

# =============================================================================
# SMALL PATCH: CLEAR EMPLOYEE REQUIREMENT-CHANGE ALERT
# Add at the very bottom of decisiondesk_chunks/05_design_system.py
# =============================================================================

try:
    _reqchange_previous_render_employee_project_workbench = render_employee_project_workbench
except Exception:
    _reqchange_previous_render_employee_project_workbench = None


def _reqchange_build_full_revised_requirement(previous_requirement, change_request, change_note):
    """Merge old requirement + new change into a full revised detailed requirement."""
    previous_requirement = safe_text(previous_requirement).strip()
    change_request = safe_text(change_request).strip()
    change_note = safe_text(change_note).strip()

    fallback = (
        previous_requirement
        + "\n\nPOST-KICKOFF REQUIREMENT CHANGE APPLIED:\n"
        + f"Change summary: {change_note}\n"
        + f"New / changed requirement: {change_request}\n"
    ).strip()

    prompt = f"""
You are the Technical Architect AI Agent.

Merge the existing approved project requirement with the new post-kickoff change.

Rules:
- Preserve all unchanged old requirements.
- Apply only the new change clearly.
- Return the full revised detailed requirement.
- Do not remove existing modules unless the change explicitly says so.
- Do not mention internal cost, salary, margin, CEO, or client-private information.

Existing approved requirement:
{previous_requirement}

New change from Technical Architect:
{change_request}

Reason / change summary:
{change_note}

Return only the full revised detailed requirement.
"""

    try:
        return safe_text(ask_llm(prompt, fallback=fallback)).strip() or fallback
    except Exception:
        return fallback


def _reqchange_pending_target_preview(revised_targets, start_week, limit=6):
    """Show affected weekly targets from start_week onward."""
    try:
        target_map = _postkick_week_target_map(revised_targets)
    except Exception:
        target_map = {}

    start_week = safe_int(start_week, 1)
    rows = []

    for week_no in sorted(target_map.keys()):
        if week_no >= start_week:
            rows.append(f"Week {week_no}: {safe_text(target_map.get(week_no))}")
        if len(rows) >= limit:
            break

    if not rows:
        rows.append(f"Week {start_week} onward: Updated weekly targets are available in the project workbench.")

    return "\n".join(rows)


def _reqchange_ai_employee_change_summary(project, previous_requirement, revised_requirement, change_request, change_note, start_week):
    """Create a simple employee-friendly explanation of the change."""
    project_name = project_display_name(project=project, project_id=project.get("project_id"))

    fallback = (
        f"Project requirement changed for {project_name}.\n"
        f"Effective from Week {start_week} onward.\n"
        f"Change summary: {change_note}\n"
        f"What changed: {change_request}\n"
        "Action required: Review the updated requirement and adjust your current/pending weekly work accordingly."
    )

    prompt = f"""
You are the Technical Architect AI Agent.

Write a clear employee notification explaining a post-kickoff project requirement change.

Rules:
- Use simple language.
- Make it clear that the requirement changed.
- Mention that the change applies from Week {start_week} onward.
- Tell employees what action to take.
- Do not mention client-private details, salary, margin, CEO, or internal finance.
- Return 4 to 6 short bullet points.

Project:
{project_name}

Previous requirement:
{previous_requirement}

Updated / revised requirement:
{revised_requirement}

Technical Architect change input:
{change_request}

Reason / change summary:
{change_note}
"""

    try:
        return safe_text(ask_llm(prompt, fallback=fallback)).strip() or fallback
    except Exception:
        return fallback


def _reqchange_build_employee_notification(project, user, previous_requirement, revised_requirement, change_request, change_note, revised_targets, start_week):
    project_id = safe_text(project.get("project_id"))
    project_name = project_display_name(project=project, project_id=project_id)

    change_summary = _reqchange_ai_employee_change_summary(
        project,
        previous_requirement,
        revised_requirement,
        change_request,
        change_note,
        start_week,
    )

    target_preview = _reqchange_pending_target_preview(revised_targets, start_week)

    return (
        "IMPORTANT REQUIREMENT CHANGE - ACTION NEEDED\n\n"
        f"Project: {project_name}\n"
        f"Project ID: {project_id}\n"
        f"Changed by: Technical Architect {actor_name(user)}\n"
        f"Effective from: Week {safe_int(start_week, 1)} onward\n\n"
        "What changed:\n"
        f"{change_summary}\n\n"
        "Updated pending weekly targets:\n"
        f"{target_preview}\n\n"
        "What you should do now:\n"
        "- Open your employee project workbench.\n"
        "- Review the updated requirement and pending-week targets.\n"
        "- Adjust your current work if your module is affected.\n"
        "- Submit your next weekly update with progress/blockers/support needs.\n\n"
        "Note: Completed previous weeks are not changed."
    )


def save_postkick_requirement_change(project, plan, user, updated_requirement, change_note, data=None):
    """Save post-kickoff requirement change and notify employees clearly."""
    if not isinstance(project, dict):
        return False, "Project was not found."

    if not isinstance(plan, dict) or not safe_text(plan.get("delivery_plan_id")):
        return False, "Delivery plan was not found for this project."

    if not _postkick_is_project_started(project, plan):
        return False, "This control is available only after project kickoff/team allocation."

    change_request = safe_text(updated_requirement).strip()
    change_note = safe_text(change_note).strip()

    if len(change_request) < 20:
        return False, "Please enter the changed requirement clearly."

    if not change_note:
        return False, "Please add a short reason or change summary."

    now = current_timestamp()
    project_id = safe_text(project.get("project_id"))
    proposal_id = safe_text(project.get("proposal_id"))
    start_week = _postkick_current_week_number(project_id)

    previous_requirement = safe_text(plan.get("raw_requirement_text"))

    revised_full_requirement = _reqchange_build_full_revised_requirement(
        previous_requirement,
        change_request,
        change_note,
    )

    revised_plan_text, revised_targets = _postkick_generate_revised_ai_plan_and_targets(
        project,
        plan,
        revised_full_requirement,
        start_week,
    )

    updated_plan = {column: safe_text(plan.get(column, "")) for column in DELIVERY_PLAN_COLUMNS}
    updated_plan["raw_requirement_text"] = revised_full_requirement
    updated_plan["operations_agent_plan"] = revised_plan_text
    updated_plan["operations_manager_plan"] = revised_plan_text
    updated_plan["module_breakdown"] = revised_targets
    updated_plan["weekly_targets"] = revised_targets
    updated_plan["approval_status"] = "Approved by Technical Architect Agent - Requirement Revised After Kickoff"
    updated_plan["approved_by"] = actor_name(user)
    updated_plan["approved_at"] = now
    updated_plan["updated_at"] = now

    upsert_simple_row(
        "delivery_plans",
        "delivery_plan_id",
        DELIVERY_PLAN_COLUMNS,
        updated_plan,
    )

    try:
        project["updated_at"] = now
        project["project_status"] = safe_text(project.get("project_status")) or "In progress"
        upsert_simple_row("projects", "project_id", PROJECT_COLUMNS, project)
    except Exception:
        pass

    employee_notification = _reqchange_build_employee_notification(
        project,
        user,
        previous_requirement,
        revised_full_requirement,
        change_request,
        change_note,
        revised_targets,
        start_week,
    )

    notified_count = _postkick_notify_project_members(
        project,
        user,
        "Requirement Change - Action Needed",
        employee_notification,
        data=data,
    )

    try:
        append_proposal_history(
            proposal_id,
            user,
            "Post-Kickoff Requirement Changed",
            comment=(
                f"Change summary: {change_note}\n\n"
                f"Targets changed from: Week {start_week}\n\n"
                f"Technical Architect change input:\n{change_request}\n\n"
                f"Previous requirement:\n{previous_requirement}\n\n"
                f"Full revised requirement:\n{revised_full_requirement}\n\n"
                f"Employee notification:\n{employee_notification}\n\n"
                f"Revised weekly targets:\n{revised_targets}"
            ),
            summary=(
                f"Technical Architect updated the project requirement after kickoff. "
                f"AI regenerated the detailed requirement and weekly targets from Week {start_week} onward. "
                f"{notified_count} allocated project member(s) were clearly notified. Client and CEO were not notified."
            ),
        )
    except Exception:
        pass

    return True, (
        f"Update sent successfully. Requirement change was clearly notified to {notified_count} project member(s). "
        f"AI regenerated the detailed requirement and weekly targets from Week {start_week} onward. "
        "Input fields were cleared. Client and CEO were not notified."
    )


def _reqchange_unread_employee_requirement_notifications(employee_id):
    """Unread requirement-change notifications for employee dashboard."""
    try:
        notifications = get_employee_notifications(employee_id)
    except Exception:
        return pd.DataFrame(columns=EMPLOYEE_NOTIFICATION_COLUMNS)

    if notifications is None or notifications.empty:
        return pd.DataFrame(columns=EMPLOYEE_NOTIFICATION_COLUMNS)

    working = notifications.copy()

    if "seen" in working.columns:
        working = working[working["seen"].fillna("No").astype(str).str.lower() != "yes"]

    type_text = working["notification_type"].fillna("").astype(str).str.lower() if "notification_type" in working.columns else ""
    message_text = working["message"].fillna("").astype(str).str.lower() if "message" in working.columns else ""

    try:
        working = working[
            type_text.str.contains("requirement change", na=False)
            | message_text.str.contains("important requirement change", na=False)
            | message_text.str.contains("requirement changed", na=False)
        ]
    except Exception:
        return pd.DataFrame(columns=EMPLOYEE_NOTIFICATION_COLUMNS)

    if "created_at" in working.columns:
        working = working.sort_values("created_at", ascending=False)

    return working


def _reqchange_mark_notification_seen(notification_row):
    if notification_row is None:
        return False

    if hasattr(notification_row, "to_dict"):
        notification_row = notification_row.to_dict()

    notification_id = safe_text(notification_row.get("notification_id"))
    if not notification_id:
        return False

    row = {column: safe_text(notification_row.get(column, "")) for column in EMPLOYEE_NOTIFICATION_COLUMNS}
    row["seen"] = "Yes"
    row["seen_at"] = current_timestamp()

    try:
        upsert_simple_row("employee_notifications", "notification_id", EMPLOYEE_NOTIFICATION_COLUMNS, row)
        return True
    except Exception:
        return False


def render_employee_requirement_change_alerts(user):
    """Show requirement-change alerts clearly before normal employee workbench."""
    emp_id = safe_text(user.get("user_id")).upper()
    alerts = _reqchange_unread_employee_requirement_notifications(emp_id)

    if alerts is None or alerts.empty:
        return

    st.markdown(
        """
        <div class="dd-section-card" style="border-left: 6px solid #dc2626;">
            <div class="dd-section-title">Important project requirement change</div>
            <div class="dd-section-subtitle">
                The Technical Architect updated a project requirement after kickoff. Please read this before continuing your project work.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    labels = []
    rows = []
    for idx, (_, row) in enumerate(alerts.iterrows(), start=1):
        labels.append(
            f"{idx}. {safe_text(row.get('created_at'))} | "
            f"{safe_text(row.get('project_id'))} | "
            f"{safe_text(row.get('notification_type'))}"
        )
        rows.append(row.to_dict())

    selected_label = st.selectbox(
        "Open requirement change alert",
        labels,
        key=f"employee_requirement_change_alert_select_{emp_id}",
    )

    selected_row = rows[labels.index(selected_label)]
    st.text_area(
        "Requirement change details",
        value=safe_text(selected_row.get("message")),
        height=340,
        disabled=True,
        key=f"employee_requirement_change_alert_text_{safe_text(selected_row.get('notification_id'))}",
    )

    if st.button(
        "I have read this requirement change",
        key=f"employee_requirement_change_read_{safe_text(selected_row.get('notification_id'))}",
        type="primary",
    ):
        if _reqchange_mark_notification_seen(selected_row):
            st.success("Requirement change marked as read.")
            st.rerun()
        else:
            st.error("Could not mark this notification as read.")


def render_employee_project_workbench(user):
    """Employee workbench with requirement-change alert shown first."""
    render_employee_requirement_change_alerts(user)

    if _reqchange_previous_render_employee_project_workbench is not None:
        _reqchange_previous_render_employee_project_workbench(user)
    else:
        st.warning("Employee project workbench is unavailable.")

# =============================================================================
# FINAL PATCH: SAFE POST-KICKOFF TEAM ADD / REMOVE WITHOUT LOGOUT OR TEAM REPLACE
# Add at the very bottom of decisiondesk_chunks/05_design_system.py
# =============================================================================

REMOVED_ALLOCATION_STATUSES = [
    "removed",
    "released",
    "inactive",
    "closed",
    "completed",
    "cancelled",
    "canceled",
]


def _team_all_project_allocations(project_id):
    """Read all allocation rows for a project, including removed rows."""
    try:
        df = read_simple_table("project_allocations", PROJECT_ALLOCATION_COLUMNS)
    except Exception:
        return pd.DataFrame(columns=PROJECT_ALLOCATION_COLUMNS)

    if df is None or df.empty or "project_id" not in df.columns:
        return pd.DataFrame(columns=PROJECT_ALLOCATION_COLUMNS)

    return df[df["project_id"].astype(str) == safe_text(project_id)].copy()


def _team_active_allocation_filter(df):
    """Keep only active allocation rows."""
    if df is None or df.empty:
        return pd.DataFrame(columns=PROJECT_ALLOCATION_COLUMNS)

    working = df.copy()

    if "allocation_status" not in working.columns:
        working["allocation_status"] = "Active"

    status = working["allocation_status"].fillna("Active").astype(str).str.lower().str.strip()

    return working[~status.isin(REMOVED_ALLOCATION_STATUSES)].copy()


def get_project_allocations(project_id):
    """Override: project allocations now exclude removed employees.

    Removed employees stay in DB/history, but they no longer count as active project team.
    """
    return _team_active_allocation_filter(_team_all_project_allocations(project_id))


def get_employee_allocations(employee_id):
    """Override: employee workbench shows only active assignments."""
    try:
        allocations = read_simple_table("project_allocations", PROJECT_ALLOCATION_COLUMNS)
    except Exception:
        return pd.DataFrame(columns=PROJECT_ALLOCATION_COLUMNS)

    if allocations is None or allocations.empty or "employee_id" not in allocations.columns:
        return pd.DataFrame(columns=PROJECT_ALLOCATION_COLUMNS)

    matched = allocations[
        allocations["employee_id"].astype(str).str.upper() == safe_text(employee_id).upper()
    ].copy()

    matched = _team_active_allocation_filter(matched)

    if not matched.empty and "assigned_at" in matched.columns:
        matched = matched.sort_values("assigned_at", ascending=False)

    return matched


def _team_active_employee_ids(project_id):
    active = get_project_allocations(project_id)
    if active is None or active.empty or "employee_id" not in active.columns:
        return set()
    return set(active["employee_id"].astype(str).str.upper().tolist())


def _team_is_allowed_delivery_employee(row, data=None):
    """Extra safety check: no CEO/executive/Sales/Finance/HR allocation."""
    if row is None:
        return False

    if hasattr(row, "to_dict"):
        row = row.to_dict()

    emp_id = safe_text(row.get("employee_id") or row.get("user_id")).upper()
    designation = safe_text(row.get("designation") or row.get("employee_designation") or row.get("project_role")).lower()
    department = safe_text(row.get("department") or row.get("employee_department")).lower()
    role_value = safe_text(row.get("role")).lower()

    try:
        executive_ids = _executive_user_ids_from_data(data)
    except Exception:
        executive_ids = set()

    if not emp_id:
        return False
    if emp_id in executive_ids:
        return False
    if role_value in ["founder", "ceo", "executive"]:
        return False
    if any(word in designation for word in ["ceo", "founder", "executive", "sales", "finance", "hr"]):
        return False
    if any(word in department for word in ["sales", "finance", "hr", "business", "strategy"]):
        return False
    if "_row_has_blocked_allocation_skill" in globals() and _row_has_blocked_allocation_skill(row):
        return False

    return True


def _team_notify_employee(employee_id, project, notification_type, message):
    """Notify one employee only. Does not notify client or CEO."""
    employee_id = safe_text(employee_id).upper()
    if not employee_id:
        return False

    try:
        notification = {
            "notification_id": make_notification_id(),
            "employee_id": employee_id,
            "project_id": safe_text(project.get("project_id")),
            "proposal_id": safe_text(project.get("proposal_id")),
            "notification_type": notification_type,
            "message": message,
            "seen": "No",
            "created_at": current_timestamp(),
            "seen_at": "",
        }
        upsert_simple_row(
            "employee_notifications",
            "notification_id",
            EMPLOYEE_NOTIFICATION_COLUMNS,
            notification,
        )
        return True
    except Exception:
        return False


def _team_notify_active_members(project, notification_type, message, data=None, exclude_ids=None):
    """Notify active project members only. Client and CEO are never included."""
    project_id = safe_text(project.get("project_id"))
    exclude_ids = set([safe_text(x).upper() for x in (exclude_ids or []) if safe_text(x)])

    active = get_project_allocations(project_id)
    if active is None or active.empty:
        return 0

    notified = 0
    seen = set()

    for _, row in active.iterrows():
        row_dict = row.to_dict()
        emp_id = safe_text(row_dict.get("employee_id")).upper()

        if not emp_id or emp_id in seen or emp_id in exclude_ids:
            continue
        if not _team_is_allowed_delivery_employee(row_dict, data=data):
            continue

        if _team_notify_employee(emp_id, project, notification_type, message):
            notified += 1
            seen.add(emp_id)

    return notified


def add_project_members_after_kickoff(project, plan, user, selected_rows, data=None):
    """Append-only team addition.

    This does NOT call approve_delivery_plan_and_allocate because that function
    deletes existing project_allocations before inserting selected rows.
    """
    if not isinstance(project, dict):
        return False, "Project was not found."

    if not isinstance(plan, dict):
        return False, "Delivery plan was not found."

    if not _postkick_is_project_started(project, plan):
        return False, "Employees can be added here only after kickoff/team allocation."

    selected_rows = selected_rows or []
    if not selected_rows:
        return False, "Select at least one additional delivery employee."

    project_id = safe_text(project.get("project_id"))
    proposal_id = safe_text(project.get("proposal_id"))
    now = current_timestamp()

    active_ids_before = _team_active_employee_ids(project_id)

    added = []
    skipped_existing = []
    skipped_not_allowed = []

    for item in selected_rows:
        emp_id = safe_text(item.get("employee_id")).upper()
        emp_name = safe_text(item.get("employee_name")) or emp_id

        if not emp_id:
            skipped_not_allowed.append(emp_name)
            continue

        if emp_id in active_ids_before:
            skipped_existing.append(emp_name)
            continue

        if not _team_is_allowed_delivery_employee(item, data=data):
            skipped_not_allowed.append(emp_name)
            continue

        allocation = {
            "allocation_id": make_allocation_id(),
            "project_id": project_id,
            "proposal_id": proposal_id,
            "client_id": safe_text(project.get("client_id")),
            "employee_id": emp_id,
            "employee_name": emp_name,
            "employee_department": safe_text(item.get("department")),
            "employee_designation": safe_text(item.get("designation")),
            "project_role": safe_text(item.get("project_role")),
            "assigned_module": safe_text(item.get("assigned_module")),
            "responsibility_summary": safe_text(item.get("responsibility_summary")),
            "allocation_percent": safe_text(item.get("allocation_percent")),
            "start_date": now[:10],
            "end_date": "",
            "assigned_by": actor_name(user),
            "assigned_at": now,
            "allocation_status": "Active",
        }

        upsert_simple_row(
            "project_allocations",
            "allocation_id",
            PROJECT_ALLOCATION_COLUMNS,
            allocation,
        )

        assignment_message = (
            f"You have been added to {project_display_name(project=project, project_id=project_id)} "
            f"after project kickoff.\n\n"
            f"Role: {allocation['project_role']}\n"
            f"Module / work area: {allocation['assigned_module']}\n"
            f"Allocation: {allocation['allocation_percent']}%\n\n"
            "Please open your employee project workbench, review the current requirement, "
            "check pending weekly targets, and submit mandatory weekly updates."
        )
        _team_notify_employee(emp_id, project, "Project Assignment Added", assignment_message)

        added.append(emp_name)

    if not added:
        msg = "No new employee was added."
        if skipped_existing:
            msg += " Already active: " + ", ".join(skipped_existing) + "."
        if skipped_not_allowed:
            msg += " Not eligible for delivery allocation: " + ", ".join(skipped_not_allowed) + "."
        return False, msg

    # Keep kickoff date unchanged. Do not replace old employees.
    try:
        project["updated_at"] = now
        if not safe_text(project.get("project_status")):
            project["project_status"] = "In progress"
        upsert_simple_row("projects", "project_id", PROJECT_COLUMNS, project)
    except Exception:
        pass

    team_message = (
        f"Project team updated for {project_display_name(project=project, project_id=project_id)}.\n\n"
        f"New member(s) added: {', '.join(added)}.\n"
        "Existing employees were NOT removed. Please continue with your current assignment and weekly updates."
    )

    team_notified = _team_notify_active_members(
        project,
        "Project Team Updated",
        team_message,
        data=data,
        exclude_ids=[],
    )

    try:
        append_proposal_history(
            proposal_id,
            user,
            "Post-Kickoff Team Members Added",
            comment=team_message,
            summary=(
                f"Technical Architect added {len(added)} employee(s) after kickoff without removing existing employees. "
                f"Project team notifications sent: {team_notified}. Client and CEO were not notified."
            ),
        )
    except Exception:
        pass

    extra = ""
    if skipped_existing:
        extra += f" Already active and skipped: {', '.join(skipped_existing)}."
    if skipped_not_allowed:
        extra += f" Not eligible and skipped: {', '.join(skipped_not_allowed)}."

    return True, (
        f"Team updated successfully. Added: {', '.join(added)}. "
        f"Existing employees were not removed. {team_notified} active project member(s) were notified. "
        f"Client and CEO were not notified.{extra}"
    )


def remove_project_members_after_kickoff(project, plan, user, employee_ids_to_remove, reason, data=None, allow_remove_all=False):
    """Remove/release selected employees from active project team.

    This does not delete rows. It marks allocation_status = Removed so history remains.
    """
    if not isinstance(project, dict):
        return False, "Project was not found."

    if not isinstance(plan, dict):
        return False, "Delivery plan was not found."

    if not _postkick_is_project_started(project, plan):
        return False, "Employees can be removed here only after kickoff/team allocation."

    project_id = safe_text(project.get("project_id"))
    proposal_id = safe_text(project.get("proposal_id"))
    reason = safe_text(reason).strip()

    if not employee_ids_to_remove:
        return False, "Select at least one employee to remove from this project."

    if not reason:
        return False, "Please add a short reason for removing the selected employee(s)."

    active_allocations = get_project_allocations(project_id)
    if active_allocations is None or active_allocations.empty:
        return False, "No active project employees are available to remove."

    remove_ids = set([safe_text(x).upper() for x in employee_ids_to_remove if safe_text(x)])
    active_ids = set(active_allocations["employee_id"].astype(str).str.upper().tolist())

    if not remove_ids.intersection(active_ids):
        return False, "Selected employees are not active in this project."

    if len(remove_ids.intersection(active_ids)) >= len(active_ids) and not allow_remove_all:
        return False, "This would remove all active delivery employees. Enable the confirmation checkbox if this is intentional."

    now = current_timestamp()
    removed_names = []

    for _, row in active_allocations.iterrows():
        row_dict = row.to_dict()
        emp_id = safe_text(row_dict.get("employee_id")).upper()

        if emp_id not in remove_ids:
            continue

        emp_name = safe_text(row_dict.get("employee_name")) or emp_id
        removed_names.append(emp_name)

        updated_allocation = {
            column: safe_text(row_dict.get(column, ""))
            for column in PROJECT_ALLOCATION_COLUMNS
        }
        updated_allocation["allocation_status"] = "Removed"
        updated_allocation["end_date"] = now[:10]
        updated_allocation["responsibility_summary"] = (
            safe_text(updated_allocation.get("responsibility_summary")).strip()
            + f"\n\nRemoved from active project team by {actor_name(user)} at {now}. Reason: {reason}"
        ).strip()

        upsert_simple_row(
            "project_allocations",
            "allocation_id",
            PROJECT_ALLOCATION_COLUMNS,
            updated_allocation,
        )

        removed_message = (
            f"You have been removed from active assignment on "
            f"{project_display_name(project=project, project_id=project_id)}.\n\n"
            f"Removed by: Technical Architect {actor_name(user)}\n"
            f"Reason: {reason}\n\n"
            "You do not need to submit future weekly updates for this project unless you are assigned again."
        )
        _team_notify_employee(emp_id, project, "Project Assignment Removed", removed_message)

    if not removed_names:
        return False, "No active employee was removed."

    team_message = (
        f"Project team updated for {project_display_name(project=project, project_id=project_id)}.\n\n"
        f"Removed from active project team: {', '.join(removed_names)}.\n"
        f"Reason: {reason}\n\n"
        "Remaining members should continue their current assignments and weekly updates."
    )

    team_notified = _team_notify_active_members(
        project,
        "Project Team Updated",
        team_message,
        data=data,
        exclude_ids=[],
    )

    try:
        project["updated_at"] = now
        if not safe_text(project.get("project_status")):
            project["project_status"] = "In progress"
        upsert_simple_row("projects", "project_id", PROJECT_COLUMNS, project)
    except Exception:
        pass

    try:
        append_proposal_history(
            proposal_id,
            user,
            "Post-Kickoff Team Members Removed",
            comment=team_message,
            summary=(
                f"Technical Architect removed {len(removed_names)} employee(s) after kickoff. "
                f"Remaining active team notifications sent: {team_notified}. Client and CEO were not notified."
            ),
        )
    except Exception:
        pass

    return True, (
        f"Team updated successfully. Removed: {', '.join(removed_names)}. "
        f"Remaining active project member(s) notified: {team_notified}. Client and CEO were not notified."
    )


def _team_employee_label(row):
    emp_id = safe_text(row.get("employee_id"))
    emp_name = safe_text(row.get("employee_name"))
    role = safe_text(row.get("project_role") or row.get("designation"))
    module = safe_text(row.get("assigned_module") or row.get("primary_skill"))
    allocation = safe_text(row.get("allocation_percent"))
    return f"{emp_id} - {emp_name} | {role} | {module} | {allocation}%"


def _team_build_selected_rows_from_employees(selected_labels, employees, project, plan_id):
    selected_rows = []

    for label in selected_labels or []:
        emp = employees[employees["label"] == label].iloc[0].to_dict()

        c1, c2, c3 = st.columns([1, 1, 1])

        with c1:
            module = st.text_input(
                f"Module for {emp.get('employee_name')}",
                value=safe_text(emp.get("primary_skill")) or safe_text(emp.get("designation")),
                key=f"safe_add_module_{safe_text(project.get('project_id'))}_{plan_id}_{emp.get('employee_id')}",
            )

        with c2:
            role = st.text_input(
                f"Project role for {emp.get('employee_name')}",
                value=safe_text(emp.get("designation")),
                key=f"safe_add_role_{safe_text(project.get('project_id'))}_{plan_id}_{emp.get('employee_id')}",
            )

        with c3:
            allocation_percent = st.number_input(
                f"Allocation % for {emp.get('employee_name')}",
                min_value=5,
                max_value=100,
                value=40,
                step=5,
                key=f"safe_add_pct_{safe_text(project.get('project_id'))}_{plan_id}_{emp.get('employee_id')}",
            )

        selected_rows.append({
            "employee_id": safe_text(emp.get("employee_id")),
            "employee_name": safe_text(emp.get("employee_name")),
            "department": safe_text(emp.get("department")),
            "designation": safe_text(emp.get("designation")),
            "project_role": role,
            "assigned_module": module,
            "responsibility_summary": (
                f"Added after kickoff to support {module} for "
                f"{project_display_name(project=project, project_id=project.get('project_id'))}. "
                "Submit mandatory weekly progress updates and raise blockers/support needs from the employee workbench."
            ),
            "allocation_percent": str(allocation_percent),
        })

    return selected_rows


def render_postkick_requirement_and_team_controls(user, data=None, focus_proposal_id=None):
    """Post-kickoff controls with safe append-only add and soft remove.

    No st.rerun() is used after team update, so it will not disturb login/session state.
    """
    if role_key_for_user(user) != "operations":
        return

    projects = _postkick_get_active_projects_for_ta(focus_proposal_id=focus_proposal_id)
    if projects is None or projects.empty:
        return

    st.markdown(
        """
        <div class="dd-section-card dd-dashboard-shell">
            <div class="dd-section-title">Post-kickoff project controls</div>
            <div class="dd-section-subtitle">
                Add or remove delivery employees after kickoff without replacing the existing team.
                Client and CEO are not notified from this control.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    labels = []
    rows = []

    for idx, (_, row) in enumerate(projects.iterrows(), start=1):
        project_id = safe_text(row.get("project_id"))
        labels.append(
            f"{idx}. {project_display_name(project=row, project_id=project_id)} | {project_id} | {safe_text(row.get('project_status'))}"
        )
        rows.append(row.to_dict())

    if focus_proposal_id and len(labels) == 1:
        selected_project = rows[0]
    else:
        selected_label = st.selectbox(
            "Choose active project for post-kickoff team update",
            labels,
            key=f"safe_postkick_project_select_{actor_id(user)}_{safe_text(focus_proposal_id) or 'all'}",
        )
        selected_project = rows[labels.index(selected_label)]

    project_id = safe_text(selected_project.get("project_id"))
    plan = get_delivery_plan_for_client_project(project_id)

    if not plan:
        st.info("Delivery plan is not available yet for this project.")
        return

    plan_id = safe_text(plan.get("delivery_plan_id")) or project_id

    active_allocations = get_project_allocations(project_id)
    active_count = 0 if active_allocations is None or active_allocations.empty else len(active_allocations)

    c1, c2, c3 = st.columns(3)
    c1.metric("Project", project_display_name(project=selected_project, project_id=project_id))
    c2.metric("Active employees", active_count)
    c3.metric("Status", safe_text(selected_project.get("project_status"), "In progress"))

    # -------------------------------------------------------------------------
    # Requirement change section remains available.
    # -------------------------------------------------------------------------
    with st.expander("Change project requirement after kickoff", expanded=False):
        current_week = _postkick_current_week_number(project_id)

        st.warning(
            f"Requirement changes preserve completed weeks and regenerate targets from Week {current_week} onward. "
            "Allocated project members are notified. Client and CEO are not notified."
        )

        current_requirement = safe_text(plan.get("raw_requirement_text"))
        if current_requirement:
            st.text_area(
                "Current saved requirement",
                value=current_requirement,
                height=150,
                disabled=True,
                key=f"safe_postkick_current_requirement_{project_id}",
            )

        with st.form(f"safe_postkick_requirement_form_{project_id}", clear_on_submit=True):
            updated_requirement = st.text_area(
                "Updated requirement / changed requirement",
                height=180,
                placeholder="Enter only the latest changed requirement or full corrected requirement.",
            )
            change_note = st.text_area(
                "Reason / change summary for project team",
                height=90,
                placeholder="Example: Client clarified branch-wise access and dashboard priority. Update current sprint accordingly.",
            )
            req_clicked = st.form_submit_button("Save requirement change and notify project members", type="primary")

        if req_clicked:
            ok, msg = save_postkick_requirement_change(
                selected_project,
                plan,
                user,
                updated_requirement,
                change_note,
                data=data,
            )
            if ok:
                st.success(msg)
            else:
                st.error(msg)

    # -------------------------------------------------------------------------
    # Add employees safely: append only, no team replacement.
    # -------------------------------------------------------------------------
    with st.expander("Add more delivery employees after kickoff", expanded=False):
        st.caption(
            "This is append-only. Existing active employees remain assigned. "
            "Do not use the old delivery-plan approval button for post-kickoff additions."
        )

        employees = data.get("employees", pd.DataFrame()).copy() if isinstance(data, dict) else pd.DataFrame()

        try:
            employees = filter_project_delivery_employees(employees, data)
        except Exception:
            pass

        if employees is None or employees.empty:
            st.warning("No eligible delivery employees are available.")
        else:
            active_ids = _team_active_employee_ids(project_id)

            if "employee_id" in employees.columns:
                employees = employees[
                    ~employees["employee_id"].astype(str).str.upper().isin(active_ids)
                ].copy()

            if employees.empty:
                st.info("All eligible delivery employees in the current data are already active on this project.")
            else:
                employees["label"] = employees.apply(
                    lambda r: (
                        f"{r.get('employee_id')} - {r.get('employee_name')} "
                        f"({r.get('designation')}, available {r.get('availability_percent', r.get('available_bandwidth', ''))}%)"
                    ),
                    axis=1,
                )

                selected = st.multiselect(
                    "Select additional delivery employees",
                    employees["label"].tolist(),
                    key=f"safe_add_people_select_{project_id}",
                )

                selected_rows = _team_build_selected_rows_from_employees(
                    selected,
                    employees,
                    selected_project,
                    plan_id,
                )

                if st.button(
                    "Add selected employees without removing existing team",
                    key=f"safe_add_people_button_{project_id}",
                    type="primary",
                ):
                    ok, msg = add_project_members_after_kickoff(
                        selected_project,
                        plan,
                        user,
                        selected_rows,
                        data=data,
                    )
                    if ok:
                        st.success(msg)
                        st.info("No automatic page rerun was triggered, so your login/session is preserved.")
                    else:
                        st.error(msg)

    # -------------------------------------------------------------------------
    # Remove/release employees safely: soft remove, no delete.
    # -------------------------------------------------------------------------
    with st.expander("Remove employees from this project if necessary", expanded=False):
        st.caption(
            "This does not delete history. It marks the selected allocation as Removed, hides the project from that employee's workbench, "
            "and notifies the removed employee plus remaining active project members. Client and CEO are not notified."
        )

        active_allocations = get_project_allocations(project_id)

        if active_allocations is None or active_allocations.empty:
            st.info("No active employees are currently allocated to this project.")
        else:
            remove_options = []
            remove_map = {}

            for _, row in active_allocations.iterrows():
                row_dict = row.to_dict()
                label = _team_employee_label(row_dict)
                remove_options.append(label)
                remove_map[label] = safe_text(row_dict.get("employee_id")).upper()

            with st.form(f"safe_remove_people_form_{project_id}", clear_on_submit=True):
                selected_remove_labels = st.multiselect(
                    "Select employees to remove from active project team",
                    remove_options,
                )
                remove_reason = st.text_area(
                    "Removal reason / note",
                    height=90,
                    placeholder="Example: Module completed, employee moved to another project, replacement added, or allocation no longer needed.",
                )

                removing_all = len(selected_remove_labels) == len(remove_options) and len(remove_options) > 0
                allow_remove_all = False
                if removing_all:
                    allow_remove_all = st.checkbox(
                        "I understand this will leave the project with no active delivery employees.",
                    )

                remove_clicked = st.form_submit_button("Remove selected employees from this project", type="primary")

            if remove_clicked:
                employee_ids = [remove_map[label] for label in selected_remove_labels if label in remove_map]

                ok, msg = remove_project_members_after_kickoff(
                    selected_project,
                    plan,
                    user,
                    employee_ids,
                    remove_reason,
                    data=data,
                    allow_remove_all=allow_remove_all,
                )

                if ok:
                    st.success(msg)
                    st.info("No automatic page rerun was triggered, so your login/session is preserved.")
                else:
                    st.error(msg)

# =============================================================================
# SMALL PATCH: RELEASE BANDWIDTH WHEN EMPLOYEE IS REMOVED FROM PROJECT
# Add at the very bottom of decisiondesk_chunks/05_design_system.py
# =============================================================================

ACTIVE_BANDWIDTH_ALLOCATION_STATUSES = [
    "active",
    "assigned",
    "in progress",
    "approved",
]

REMOVED_BANDWIDTH_ALLOCATION_STATUSES = [
    "removed",
    "released",
    "inactive",
    "closed",
    "completed",
    "cancelled",
    "canceled",
]


def _bandwidth_clear_capacity_caches():
    """Make bandwidth changes visible immediately after add/remove."""
    try:
        clear_workflow_read_cache()
    except Exception:
        pass

    try:
        read_dynamic_capacity_sources.clear()
    except Exception:
        pass

    try:
        st.cache_data.clear()
    except Exception:
        pass


def _bandwidth_active_allocations_only(allocations):
    """Only active allocation rows should consume bandwidth."""
    if allocations is None or allocations.empty:
        return pd.DataFrame(columns=PROJECT_ALLOCATION_COLUMNS)

    working = allocations.copy()

    if "allocation_status" not in working.columns:
        working["allocation_status"] = "Active"

    status = working["allocation_status"].fillna("Active").astype(str).str.strip().str.lower()

    return working[
        status.isin(ACTIVE_BANDWIDTH_ALLOCATION_STATUSES)
        & ~status.isin(REMOVED_BANDWIDTH_ALLOCATION_STATUSES)
    ].copy()


def adjust_employee_availability_with_dynamic_allocations(employees, new_project_timeline_months=0):
    """Recalculate available bandwidth from active allocations only.

    Removed/released employees regain the allocation percentage immediately.
    """
    if employees is None or getattr(employees, "empty", True):
        return employees

    adjusted = employees.copy()

    if "employee_id" not in adjusted.columns:
        return adjusted

    if "availability_percent" not in adjusted.columns:
        adjusted["availability_percent"] = 100

    try:
        allocations = read_simple_table("project_allocations", PROJECT_ALLOCATION_COLUMNS)
    except Exception:
        allocations = pd.DataFrame(columns=PROJECT_ALLOCATION_COLUMNS)

    active = _bandwidth_active_allocations_only(allocations)

    if active.empty:
        adjusted["availability_percent"] = pd.to_numeric(
            adjusted["availability_percent"],
            errors="coerce",
        ).fillna(100).clip(lower=0, upper=100)

        adjusted["live_allocated_percent"] = 0
        adjusted["available_bandwidth"] = adjusted["availability_percent"].apply(lambda value: f"{safe_number(value, 0):.0f}%")
        return adjusted

    active["allocation_percent_num"] = pd.to_numeric(
        active.get("allocation_percent", 0),
        errors="coerce",
    ).fillna(0)

    used_by_employee = active.groupby(
        active["employee_id"].astype(str).str.upper()
    )["allocation_percent_num"].sum().to_dict()

    def _remaining(row):
        emp_id = safe_text(row.get("employee_id")).upper()
        base_available = safe_number(row.get("availability_percent"), 100)
        used_now = safe_number(used_by_employee.get(emp_id, 0), 0)
        return max(0, min(100, base_available - used_now))

    def _used(row):
        emp_id = safe_text(row.get("employee_id")).upper()
        return max(0, min(100, safe_number(used_by_employee.get(emp_id, 0), 0)))

    adjusted["live_allocated_percent"] = adjusted.apply(_used, axis=1)
    adjusted["availability_percent"] = adjusted.apply(_remaining, axis=1)
    adjusted["available_bandwidth"] = adjusted["availability_percent"].apply(lambda value: f"{safe_number(value, 0):.0f}%")

    return adjusted


try:
    _bandwidth_previous_add_project_members_after_kickoff = add_project_members_after_kickoff
except Exception:
    _bandwidth_previous_add_project_members_after_kickoff = None

try:
    _bandwidth_previous_remove_project_members_after_kickoff = remove_project_members_after_kickoff
except Exception:
    _bandwidth_previous_remove_project_members_after_kickoff = None


def add_project_members_after_kickoff(project, plan, user, selected_rows, data=None):
    """Add employees and refresh bandwidth immediately."""
    if _bandwidth_previous_add_project_members_after_kickoff is None:
        return False, "Add-member function is unavailable."

    ok, msg = _bandwidth_previous_add_project_members_after_kickoff(
        project,
        plan,
        user,
        selected_rows,
        data=data,
    )

    if ok:
        _bandwidth_clear_capacity_caches()
        msg += " Bandwidth has been recalculated for the added employee(s)."

    return ok, msg


def remove_project_members_after_kickoff(project, plan, user, employee_ids_to_remove, reason, data=None, allow_remove_all=False):
    """Remove employees and release their bandwidth immediately."""
    if _bandwidth_previous_remove_project_members_after_kickoff is None:
        return False, "Remove-member function is unavailable."

    ok, msg = _bandwidth_previous_remove_project_members_after_kickoff(
        project,
        plan,
        user,
        employee_ids_to_remove,
        reason,
        data=data,
        allow_remove_all=allow_remove_all,
    )

    if ok:
        _bandwidth_clear_capacity_caches()

        removed_ids = [safe_text(emp_id).upper() for emp_id in (employee_ids_to_remove or []) if safe_text(emp_id)]
        bandwidth_lines = []

        try:
            employees = data.get("employees", pd.DataFrame()).copy() if isinstance(data, dict) else pd.DataFrame()
            adjusted = adjust_employee_availability_with_dynamic_allocations(employees)

            if adjusted is not None and not adjusted.empty and "employee_id" in adjusted.columns:
                for emp_id in removed_ids:
                    matched = adjusted[adjusted["employee_id"].astype(str).str.upper() == emp_id]
                    if not matched.empty:
                        row = matched.iloc[0]
                        bandwidth_lines.append(
                            f"{safe_text(row.get('employee_name')) or emp_id}: available bandwidth now {safe_text(row.get('available_bandwidth')) or str(row.get('availability_percent')) + '%'}"
                        )
        except Exception:
            bandwidth_lines = []

        msg += " Removed employee bandwidth has been released and recalculated."

        if bandwidth_lines:
            msg += " " + " | ".join(bandwidth_lines)

    return ok, msg


# =============================================================================
# FINAL SMALL PATCH: NO RESTART / NO LOGOUT AFTER POST-KICKOFF UPDATES
# Add at the very bottom of decisiondesk_chunks/05_design_system.py
# =============================================================================

def _safe_clear_postkick_success_state(project_id, action, message):
    """Store success message without forcing logout or hard rerun."""
    key = f"postkick_success_{safe_text(project_id)}_{safe_text(action)}"
    st.session_state[key] = safe_text(message)


def _safe_show_postkick_success(project_id, action):
    key = f"postkick_success_{safe_text(project_id)}_{safe_text(action)}"
    msg = safe_text(st.session_state.get(key))
    if msg:
        st.success(msg)


def render_postkick_requirement_and_team_controls(user, data=None, focus_proposal_id=None):
    """Post-kickoff controls without forced restart/logout.

    Rules:
    - Do not call st.rerun() after requirement update, employee add, or employee remove.
    - Use clear_on_submit=True so input boxes clear automatically.
    - Keep existing login/session state untouched.
    """
    if role_key_for_user(user) != "operations":
        return

    projects = _postkick_get_active_projects_for_ta(focus_proposal_id=focus_proposal_id)
    if projects is None or projects.empty:
        return

    st.markdown(
        """
        <div class="dd-section-card dd-dashboard-shell">
            <div class="dd-section-title">Post-kickoff project controls</div>
            <div class="dd-section-subtitle">
                Update requirements, add delivery employees, or remove employees after kickoff.
                The page will not force restart after saving, so the logged-in Technical Architect session remains active.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    labels = []
    rows = []

    for idx, (_, row) in enumerate(projects.iterrows(), start=1):
        project_id = safe_text(row.get("project_id"))
        labels.append(
            f"{idx}. {project_display_name(project=row, project_id=project_id)} | "
            f"{project_id} | {safe_text(row.get('project_status'))}"
        )
        rows.append(row.to_dict())

    if not labels:
        return

    if focus_proposal_id and len(labels) == 1:
        selected_project = rows[0]
    else:
        selected_label = st.selectbox(
            "Choose active project for post-kickoff update",
            labels,
            key=f"norestart_postkick_project_select_{actor_id(user)}_{safe_text(focus_proposal_id) or 'all'}",
        )
        selected_project = rows[labels.index(selected_label)]

    project_id = safe_text(selected_project.get("project_id"))
    plan = get_delivery_plan_for_client_project(project_id)

    if not plan:
        st.info("Delivery plan is not available yet for this project.")
        return

    plan_id = safe_text(plan.get("delivery_plan_id")) or project_id

    active_allocations = get_project_allocations(project_id)
    active_count = 0 if active_allocations is None or active_allocations.empty else len(active_allocations)

    c1, c2, c3 = st.columns(3)
    c1.metric("Project", project_display_name(project=selected_project, project_id=project_id))
    c2.metric("Active employees", active_count)
    c3.metric("Status", safe_text(selected_project.get("project_status"), "In progress"))

    # -------------------------------------------------------------------------
    # Requirement update: clear inputs, no forced rerun/logout.
    # -------------------------------------------------------------------------
    _safe_show_postkick_success(project_id, "requirement")

    with st.expander("Change project requirement after kickoff", expanded=False):
        current_week = _postkick_current_week_number(project_id)

        st.warning(
            f"Requirement changes preserve completed weeks and regenerate targets from Week {current_week} onward. "
            "Allocated project members are notified. Client and CEO are not notified."
        )

        current_requirement = safe_text(plan.get("raw_requirement_text"))
        if current_requirement:
            st.text_area(
                "Current saved requirement",
                value=current_requirement,
                height=150,
                disabled=True,
                key=f"norestart_current_requirement_{project_id}",
            )

        with st.form(f"norestart_requirement_form_{project_id}", clear_on_submit=True):
            updated_requirement = st.text_area(
                "Updated requirement / changed requirement",
                height=180,
                placeholder="Enter the latest changed requirement or full corrected requirement.",
            )
            change_note = st.text_area(
                "Reason / change summary for project team",
                height=90,
                placeholder="Example: Client clarified branch-wise access and dashboard priority. Update current sprint accordingly.",
            )
            req_clicked = st.form_submit_button(
                "Save requirement change and notify project members",
                type="primary",
            )

        if req_clicked:
            ok, msg = save_postkick_requirement_change(
                selected_project,
                plan,
                user,
                updated_requirement,
                change_note,
                data=data,
            )
            if ok:
                _safe_clear_postkick_success_state(project_id, "requirement", msg)
                st.success(msg)
                st.info("Input boxes cleared. No forced restart was triggered, so your login session is preserved.")
            else:
                st.error(msg)

    # -------------------------------------------------------------------------
    # Add employees: append only, clear inputs, no forced rerun/logout.
    # -------------------------------------------------------------------------
    _safe_show_postkick_success(project_id, "add_people")

    with st.expander("Add more delivery employees after kickoff", expanded=False):
        st.caption(
            "This is append-only. Existing active employees remain assigned. "
            "The form clears after submit and does not force a page restart."
        )

        employees = data.get("employees", pd.DataFrame()).copy() if isinstance(data, dict) else pd.DataFrame()

        try:
            employees = filter_project_delivery_employees(employees, data)
        except Exception:
            pass

        if employees is None or employees.empty:
            st.warning("No eligible delivery employees are available.")
        else:
            active_ids = _team_active_employee_ids(project_id)

            if "employee_id" in employees.columns:
                employees = employees[
                    ~employees["employee_id"].astype(str).str.upper().isin(active_ids)
                ].copy()

            if employees.empty:
                st.info("All eligible delivery employees in the current data are already active on this project.")
            else:
                employees["label"] = employees.apply(
                    lambda r: (
                        f"{r.get('employee_id')} - {r.get('employee_name')} "
                        f"({r.get('designation')}, available {r.get('availability_percent', r.get('available_bandwidth', ''))}%)"
                    ),
                    axis=1,
                )

                with st.form(f"norestart_add_people_form_{project_id}", clear_on_submit=True):
                    selected = st.multiselect(
                        "Select additional delivery employees",
                        employees["label"].tolist(),
                    )

                    selected_rows = []

                    for label in selected or []:
                        emp = employees[employees["label"] == label].iloc[0].to_dict()

                        st.markdown(f"**{safe_text(emp.get('employee_name'))}**")

                        c1, c2, c3 = st.columns([1, 1, 1])

                        with c1:
                            module = st.text_input(
                                f"Module / work area",
                                value=safe_text(emp.get("primary_skill")) or safe_text(emp.get("designation")),
                                key=f"norestart_add_module_{project_id}_{emp.get('employee_id')}",
                            )

                        with c2:
                            role = st.text_input(
                                f"Project role",
                                value=safe_text(emp.get("designation")),
                                key=f"norestart_add_role_{project_id}_{emp.get('employee_id')}",
                            )

                        with c3:
                            allocation_percent = st.number_input(
                                f"Allocation %",
                                min_value=5,
                                max_value=100,
                                value=40,
                                step=5,
                                key=f"norestart_add_pct_{project_id}_{emp.get('employee_id')}",
                            )

                        selected_rows.append({
                            "employee_id": safe_text(emp.get("employee_id")),
                            "employee_name": safe_text(emp.get("employee_name")),
                            "department": safe_text(emp.get("department")),
                            "designation": safe_text(emp.get("designation")),
                            "project_role": role,
                            "assigned_module": module,
                            "responsibility_summary": (
                                f"Added after kickoff to support {module} for "
                                f"{project_display_name(project=selected_project, project_id=project_id)}. "
                                "Submit mandatory weekly progress updates and raise blockers/support needs from the employee workbench."
                            ),
                            "allocation_percent": str(allocation_percent),
                        })

                    add_clicked = st.form_submit_button(
                        "Add selected employees without removing existing team",
                        type="primary",
                    )

                if add_clicked:
                    ok, msg = add_project_members_after_kickoff(
                        selected_project,
                        plan,
                        user,
                        selected_rows,
                        data=data,
                    )
                    if ok:
                        _safe_clear_postkick_success_state(project_id, "add_people", msg)
                        st.success(msg)
                        st.info("Input boxes cleared. No forced restart was triggered, so your login session is preserved.")
                    else:
                        st.error(msg)

    # -------------------------------------------------------------------------
    # Remove employees: soft remove, clear inputs, no forced rerun/logout.
    # -------------------------------------------------------------------------
    _safe_show_postkick_success(project_id, "remove_people")

    with st.expander("Remove employees from this project if necessary", expanded=False):
        st.caption(
            "This does not delete history. It marks selected employees as Removed, releases bandwidth, "
            "and hides the project from their workbench. The form clears after submit."
        )

        active_allocations = get_project_allocations(project_id)

        if active_allocations is None or active_allocations.empty:
            st.info("No active employees are currently allocated to this project.")
        else:
            remove_options = []
            remove_map = {}

            for _, row in active_allocations.iterrows():
                row_dict = row.to_dict()
                label = _team_employee_label(row_dict)
                remove_options.append(label)
                remove_map[label] = safe_text(row_dict.get("employee_id")).upper()

            with st.form(f"norestart_remove_people_form_{project_id}", clear_on_submit=True):
                selected_remove_labels = st.multiselect(
                    "Select employees to remove from active project team",
                    remove_options,
                )

                remove_reason = st.text_area(
                    "Removal reason / note",
                    height=90,
                    placeholder="Example: Module completed, employee moved to another project, replacement added, or allocation no longer needed.",
                )

                removing_all = len(selected_remove_labels) == len(remove_options) and len(remove_options) > 0
                allow_remove_all = False

                if removing_all:
                    allow_remove_all = st.checkbox(
                        "I understand this will leave the project with no active delivery employees.",
                    )

                remove_clicked = st.form_submit_button(
                    "Remove selected employees from this project",
                    type="primary",
                )

            if remove_clicked:
                employee_ids = [
                    remove_map[label]
                    for label in selected_remove_labels
                    if label in remove_map
                ]

                ok, msg = remove_project_members_after_kickoff(
                    selected_project,
                    plan,
                    user,
                    employee_ids,
                    remove_reason,
                    data=data,
                    allow_remove_all=allow_remove_all,
                )

                if ok:
                    _safe_clear_postkick_success_state(project_id, "remove_people", msg)
                    st.success(msg)
                    st.info("Input boxes cleared. No forced restart was triggered, so your login session is preserved.")
                else:
                    st.error(msg)

# =============================================================================
# FINAL FIX: REQUIREMENT CHANGE MUST REFLECT CLEARLY IN EMPLOYEE DASHBOARD
# Add at the very bottom of decisiondesk_chunks/05_design_system.py
# =============================================================================

def _reqfix_clear_after_requirement_db_save():
    """Clear read caches only after DB save is completed."""
    try:
        clear_workflow_read_cache()
    except Exception:
        pass

    try:
        read_dynamic_capacity_sources.clear()
    except Exception:
        pass

    try:
        st.cache_data.clear()
    except Exception:
        pass


def _reqfix_latest_delivery_plan(project_id):
    """Read latest delivery plan directly so employee dashboard sees the updated requirement."""
    project_id = safe_text(project_id).strip()

    try:
        plan = get_delivery_plan_for_client_project(project_id)
        if isinstance(plan, dict) and safe_text(plan.get("delivery_plan_id")):
            return plan
    except Exception:
        pass

    try:
        plans = read_simple_table("delivery_plans", DELIVERY_PLAN_COLUMNS)
    except Exception:
        return {}

    if plans is None or plans.empty or "project_id" not in plans.columns:
        return {}

    matched = plans[plans["project_id"].astype(str) == project_id].copy()
    if matched.empty:
        return {}

    sort_col = "updated_at" if "updated_at" in matched.columns else "created_at" if "created_at" in matched.columns else None
    if sort_col:
        matched = matched.sort_values(sort_col, ascending=False)

    return matched.iloc[0].to_dict()


def _reqfix_notification_message_from_row(row):
    """Read notification text even if older code stored it in a different field."""
    if row is None:
        return ""

    if hasattr(row, "to_dict"):
        row = row.to_dict()

    for key in [
        "message",
        "notification_message",
        "message_text",
        "details",
        "description",
        "summary",
        "notification_text",
    ]:
        value = safe_text(row.get(key)).strip()
        if value:
            return value

    return ""


def _reqfix_pending_week_targets_text(revised_targets, start_week, limit=8):
    """Employee-friendly pending-week target preview."""
    try:
        target_map = _postkick_week_target_map(revised_targets)
    except Exception:
        target_map = {}

    start_week = safe_int(start_week, 1)
    lines = []

    for week_no in sorted(target_map.keys()):
        if week_no >= start_week:
            lines.append(f"Week {week_no}: {safe_text(target_map.get(week_no))}")
        if len(lines) >= limit:
            break

    if not lines:
        lines.append(f"Week {start_week} onward: Updated weekly targets are saved in the project workbench.")

    return "\n".join(lines)


def _reqfix_build_full_revised_requirement(previous_requirement, change_request, change_note):
    """Create a full revised requirement so employees do not see only a small change note."""
    previous_requirement = safe_text(previous_requirement).strip()
    change_request = safe_text(change_request).strip()
    change_note = safe_text(change_note).strip()

    fallback = (
        previous_requirement
        + "\n\nPOST-KICKOFF REQUIREMENT CHANGE:\n"
        + f"Reason / change summary: {change_note}\n"
        + f"Changed / new requirement: {change_request}\n"
    ).strip()

    prompt = f"""
You are the Technical Architect AI Agent.

Merge the existing approved project requirement with the new post-kickoff change.

Rules:
- Preserve unchanged old requirements.
- Apply the new change clearly.
- Return the full revised detailed requirement.
- Do not remove old modules unless the change explicitly says to remove them.
- Do not mention salary, margin, cost, CEO, or private internal notes.

Existing approved requirement:
{previous_requirement}

New changed requirement from Technical Architect:
{change_request}

Reason / change summary:
{change_note}

Return only the full revised detailed requirement.
"""

    try:
        result = safe_text(ask_llm(prompt, fallback=fallback)).strip()
        return result or fallback
    except Exception:
        return fallback


def _reqfix_build_employee_change_message(project, user, change_request, change_note, revised_requirement, revised_targets, start_week):
    """Build a clear employee notification. This is what appears in employee dashboard."""
    project_id = safe_text(project.get("project_id"))
    project_name = project_display_name(project=project, project_id=project_id)
    target_preview = _reqfix_pending_week_targets_text(revised_targets, start_week)

    return (
        "IMPORTANT PROJECT REQUIREMENT CHANGE - ACTION NEEDED\n\n"
        f"Project: {project_name}\n"
        f"Project ID: {project_id}\n"
        f"Changed by: Technical Architect {actor_name(user)}\n"
        f"Effective from: Week {safe_int(start_week, 1)} onward\n\n"
        "What changed:\n"
        f"{safe_text(change_request)}\n\n"
        "Why this change was made:\n"
        f"{safe_text(change_note)}\n\n"
        "Updated pending weekly targets:\n"
        f"{target_preview}\n\n"
        "What you should do now:\n"
        "- Open your employee project workbench.\n"
        "- Read the updated requirement shown there.\n"
        "- Check the revised pending-week targets.\n"
        "- Adjust your current work if your module is affected.\n"
        "- Mention progress, blockers, or support needs in your next weekly update.\n\n"
        "Note: Completed previous weeks are not changed."
    )


def _reqfix_notify_project_members(project, user, notification_type, message, data=None):
    """Notify allocated project members only. No client. No CEO."""
    project_id = safe_text(project.get("project_id"))
    proposal_id = safe_text(project.get("proposal_id"))
    now = current_timestamp()

    try:
        members = _postkick_project_members(project_id, data=data, include_actor_id=actor_id(user))
    except Exception:
        members = []

    notified = 0

    for member in members:
        employee_id = safe_text(member.get("employee_id")).upper()
        if not employee_id:
            continue

        try:
            row = {column: "" for column in EMPLOYEE_NOTIFICATION_COLUMNS}

            row["notification_id"] = make_notification_id()
            row["employee_id"] = employee_id
            row["project_id"] = project_id
            row["proposal_id"] = proposal_id
            row["notification_type"] = notification_type
            row["seen"] = "No"
            row["created_at"] = now
            row["seen_at"] = ""

            # Most current code uses "message". Keep fallbacks for older schemas.
            for msg_col in [
                "message",
                "notification_message",
                "message_text",
                "details",
                "description",
                "summary",
                "notification_text",
            ]:
                if msg_col in row:
                    row[msg_col] = message

            # If message column exists in table config but row did not get it for any reason.
            if "message" in EMPLOYEE_NOTIFICATION_COLUMNS:
                row["message"] = message

            upsert_simple_row(
                "employee_notifications",
                "notification_id",
                EMPLOYEE_NOTIFICATION_COLUMNS,
                row,
            )
            notified += 1

        except Exception:
            pass

    return notified


def save_postkick_requirement_change(project, plan, user, updated_requirement, change_note, data=None):
    """Save first, notify second, clear/read-cache third.

    The form input should clear only after this function returns success.
    """
    if not isinstance(project, dict):
        return False, "Project was not found."

    if not isinstance(plan, dict) or not safe_text(plan.get("delivery_plan_id")):
        return False, "Delivery plan was not found for this project."

    if not _postkick_is_project_started(project, plan):
        return False, "This control is available only after project kickoff/team allocation."

    change_request = safe_text(updated_requirement).strip()
    change_note = safe_text(change_note).strip()

    if len(change_request) < 20:
        return False, "Please enter the changed requirement clearly."

    if not change_note:
        return False, "Please add a short reason or change summary."

    now = current_timestamp()
    project_id = safe_text(project.get("project_id"))
    proposal_id = safe_text(project.get("proposal_id"))
    start_week = _postkick_current_week_number(project_id)

    previous_requirement = safe_text(plan.get("raw_requirement_text"))

    revised_requirement = _reqfix_build_full_revised_requirement(
        previous_requirement,
        change_request,
        change_note,
    )

    revised_plan_text, revised_targets = _postkick_generate_revised_ai_plan_and_targets(
        project,
        plan,
        revised_requirement,
        start_week,
    )

    # -------------------------------------------------------------------------
    # 1. Save updated requirement + revised plan + revised pending-week targets.
    # -------------------------------------------------------------------------
    updated_plan = {column: safe_text(plan.get(column, "")) for column in DELIVERY_PLAN_COLUMNS}
    updated_plan["raw_requirement_text"] = revised_requirement
    updated_plan["operations_agent_plan"] = revised_plan_text
    updated_plan["operations_manager_plan"] = revised_plan_text
    updated_plan["module_breakdown"] = revised_targets
    updated_plan["weekly_targets"] = revised_targets
    updated_plan["approval_status"] = "Approved by Technical Architect Agent - Requirement Revised After Kickoff"
    updated_plan["approved_by"] = actor_name(user)
    updated_plan["approved_at"] = now
    updated_plan["updated_at"] = now

    upsert_simple_row(
        "delivery_plans",
        "delivery_plan_id",
        DELIVERY_PLAN_COLUMNS,
        updated_plan,
    )

    try:
        project["updated_at"] = now
        project["project_status"] = safe_text(project.get("project_status")) or "In progress"
        upsert_simple_row("projects", "project_id", PROJECT_COLUMNS, project)
    except Exception:
        pass

    # -------------------------------------------------------------------------
    # 2. Build a clear employee notification after DB save.
    # -------------------------------------------------------------------------
    employee_message = _reqfix_build_employee_change_message(
        project,
        user,
        change_request,
        change_note,
        revised_requirement,
        revised_targets,
        start_week,
    )

    notified_count = _reqfix_notify_project_members(
        project,
        user,
        "Requirement Change - Action Needed",
        employee_message,
        data=data,
    )

    # -------------------------------------------------------------------------
    # 3. Save history after notification.
    # -------------------------------------------------------------------------
    try:
        append_proposal_history(
            proposal_id,
            user,
            "Post-Kickoff Requirement Changed",
            comment=(
                f"Effective from Week {start_week}\n\n"
                f"Change request:\n{change_request}\n\n"
                f"Change reason:\n{change_note}\n\n"
                f"Previous requirement:\n{previous_requirement}\n\n"
                f"Full revised requirement:\n{revised_requirement}\n\n"
                f"Employee notification:\n{employee_message}\n\n"
                f"Revised pending-week targets:\n{revised_targets}"
            ),
            summary=(
                f"Technical Architect updated the project requirement after kickoff. "
                f"DB updated first, then {notified_count} project member(s) were notified. "
                f"Targets changed from Week {start_week} onward. Client and CEO were not notified."
            ),
        )
    except Exception:
        pass

    # -------------------------------------------------------------------------
    # 4. Clear cache only after DB save + notification completed.
    # -------------------------------------------------------------------------
    _reqfix_clear_after_requirement_db_save()

    return True, (
        f"Update sent successfully. The revised requirement is saved and visible in employee dashboards. "
        f"Pending weekly targets were regenerated from Week {start_week} onward. "
        f"{notified_count} project member(s) were notified. Client and CEO were not notified."
    )


def _reqfix_unread_requirement_change_alerts(employee_id):
    """Get unread requirement-change alerts for the employee."""
    try:
        notifications = get_employee_notifications(employee_id)
    except Exception:
        return pd.DataFrame(columns=EMPLOYEE_NOTIFICATION_COLUMNS)

    if notifications is None or notifications.empty:
        return pd.DataFrame(columns=EMPLOYEE_NOTIFICATION_COLUMNS)

    working = notifications.copy()

    if "seen" in working.columns:
        working = working[working["seen"].fillna("No").astype(str).str.lower() != "yes"]

    if working.empty:
        return working

    type_series = working["notification_type"].fillna("").astype(str).str.lower() if "notification_type" in working.columns else pd.Series([""] * len(working), index=working.index)

    message_series = pd.Series([""] * len(working), index=working.index)
    for msg_col in [
        "message",
        "notification_message",
        "message_text",
        "details",
        "description",
        "summary",
        "notification_text",
    ]:
        if msg_col in working.columns:
            message_series = message_series + " " + working[msg_col].fillna("").astype(str).str.lower()

    working = working[
        type_series.str.contains("requirement", na=False)
        | message_series.str.contains("requirement change", na=False)
        | message_series.str.contains("requirement changed", na=False)
        | message_series.str.contains("important project requirement change", na=False)
    ]

    if "created_at" in working.columns:
        working = working.sort_values("created_at", ascending=False)

    return working


def _reqfix_mark_requirement_alert_seen(notification_row):
    if notification_row is None:
        return False

    if hasattr(notification_row, "to_dict"):
        notification_row = notification_row.to_dict()

    notification_id = safe_text(notification_row.get("notification_id"))
    if not notification_id:
        return False

    row = {column: safe_text(notification_row.get(column, "")) for column in EMPLOYEE_NOTIFICATION_COLUMNS}
    row["seen"] = "Yes"
    row["seen_at"] = current_timestamp()

    try:
        upsert_simple_row(
            "employee_notifications",
            "notification_id",
            EMPLOYEE_NOTIFICATION_COLUMNS,
            row,
        )
        return True
    except Exception:
        return False


def render_employee_requirement_change_alerts(user):
    """Employee dashboard alert that always shows latest saved requirement and targets."""
    emp_id = safe_text(user.get("user_id")).upper()
    alerts = _reqfix_unread_requirement_change_alerts(emp_id)

    if alerts is None or alerts.empty:
        return

    st.markdown(
        """
        <div class="dd-section-card" style="border-left: 6px solid #dc2626;">
            <div class="dd-section-title">Important project requirement change</div>
            <div class="dd-section-subtitle">
                The Technical Architect updated a project requirement after kickoff. Read this before continuing your project work.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    labels = []
    rows = []

    for idx, (_, row) in enumerate(alerts.iterrows(), start=1):
        labels.append(
            f"{idx}. {safe_text(row.get('created_at'))} | "
            f"{safe_text(row.get('project_id'))} | "
            f"{safe_text(row.get('notification_type'))}"
        )
        rows.append(row.to_dict())

    selected_label = st.selectbox(
        "Open requirement change alert",
        labels,
        key=f"reqfix_employee_requirement_alert_select_{emp_id}",
    )

    selected_row = rows[labels.index(selected_label)]
    project_id = safe_text(selected_row.get("project_id"))
    plan = _reqfix_latest_delivery_plan(project_id)

    message = _reqfix_notification_message_from_row(selected_row)

    if not message:
        # Fallback for older blank notification rows.
        message = (
            "IMPORTANT PROJECT REQUIREMENT CHANGE - ACTION NEEDED\n\n"
            f"Project ID: {project_id}\n\n"
            "The notification text was missing in the older row, but the latest saved project requirement is shown below. "
            "Please review the updated requirement and pending weekly targets before continuing work."
        )

    st.text_area(
        "Requirement change details",
        value=message,
        height=300,
        disabled=True,
        key=f"reqfix_requirement_change_message_{safe_text(selected_row.get('notification_id'))}",
    )

    if plan:
        updated_requirement = safe_text(plan.get("raw_requirement_text"))
        if updated_requirement:
            st.text_area(
                "Latest updated requirement now saved for this project",
                value=updated_requirement,
                height=260,
                disabled=True,
                key=f"reqfix_latest_requirement_{project_id}_{safe_text(selected_row.get('notification_id'))}",
            )

        targets_text = weekly_targets_text_from_plan(plan)
        if safe_text(targets_text):
            with st.expander("Updated weekly target list", expanded=True):
                rows_for_targets = parse_weekly_targets_to_rows(targets_text)
                if rows_for_targets:
                    st.dataframe(pd.DataFrame(rows_for_targets), use_container_width=True, hide_index=True)
                else:
                    st.text_area(
                        "Updated targets",
                        value=targets_text,
                        height=220,
                        disabled=True,
                        key=f"reqfix_latest_targets_{project_id}_{safe_text(selected_row.get('notification_id'))}",
                    )
    else:
        st.warning("Latest delivery plan could not be loaded for this project. Please contact the Technical Architect.")

    if st.button(
        "I have read this requirement change",
        key=f"reqfix_requirement_alert_read_{safe_text(selected_row.get('notification_id'))}",
        type="primary",
    ):
        if _reqfix_mark_requirement_alert_seen(selected_row):
            st.success("Requirement change marked as read.")
        else:
            st.error("Could not mark this notification as read.")


# =============================================================================
# FINAL FIX: REMOVE STALE POST-KICKOFF SUCCESS POPUPS
# Add at the very bottom of decisiondesk_chunks/05_design_system.py
# =============================================================================

def clear_postkick_temporary_success_messages():
    """Remove old post-kickoff success popups from Streamlit session state.

    These messages are only UI confirmations. They should not persist across
    login sessions, project selection changes, or later visits.
    """
    try:
        keys_to_remove = []

        for key in list(st.session_state.keys()):
            key_text = safe_text(key).lower()

            if key_text.startswith("postkick_success_"):
                keys_to_remove.append(key)

            if key_text.startswith("postkick_req_success_msg_"):
                keys_to_remove.append(key)

            if key_text.startswith("ld_postkick_success_"):
                keys_to_remove.append(key)

            if key_text.startswith("ld_success_"):
                keys_to_remove.append(key)

        for key in keys_to_remove:
            try:
                st.session_state.pop(key, None)
            except Exception:
                pass

    except Exception:
        pass


# Clear old messages immediately when this file loads.
# This removes old messages like:
# - Update sent successfully...
# - Team updated successfully. Added: Vivek Raj...
clear_postkick_temporary_success_messages()


def _safe_clear_postkick_success_state(project_id, action, message):
    """Do NOT store success messages anymore.

    Success should show only immediately after button click, not on later page visits.
    """
    clear_postkick_temporary_success_messages()
    return None


def _safe_show_postkick_success(project_id, action):
    """Disabled: do not show old saved success messages."""
    clear_postkick_temporary_success_messages()
    return None


def _ld_store_success(project_id, action, message):
    """Do NOT store success messages anymore."""
    clear_postkick_temporary_success_messages()
    return None


def _ld_show_success(project_id, action):
    """Disabled: do not show old saved success messages."""
    clear_postkick_temporary_success_messages()
    return None


# =============================================================================
# FINAL OVERRIDE: CLEAN POST-KICKOFF UI + REMOVE STALE SUCCESS POPUPS
# Paste this at the VERY BOTTOM of decisiondesk_chunks/05_design_system.py
# =============================================================================

POSTKICK_STALE_SUCCESS_PHRASES = [
    "update sent successfully",
    "team updated successfully",
    "project requirement updated",
    "requirement change was clearly notified",
    "input boxes cleared",
    "added:",
    "removed:",
    "bandwidth has been recalculated",
    "bandwidth has been released",
]

POSTKICK_STALE_KEY_PREFIXES = [
    "postkick_success_",
    "postkick_req_success_msg_",
    "ld_postkick_success_",
    "ld_success_",
]


def _final_clean_clear_stale_postkick_ui_state():
    """Remove old stored success messages from Streamlit session state."""
    try:
        for key in list(st.session_state.keys()):
            key_text = safe_text(key).lower()
            value_text = safe_text(st.session_state.get(key)).lower()

            remove_key = False

            if any(key_text.startswith(prefix) for prefix in POSTKICK_STALE_KEY_PREFIXES):
                remove_key = True

            if any(phrase in value_text for phrase in POSTKICK_STALE_SUCCESS_PHRASES):
                remove_key = True

            if remove_key:
                st.session_state.pop(key, None)
    except Exception:
        pass


# Clear old popups immediately on every app run.
_final_clean_clear_stale_postkick_ui_state()


def _safe_clear_postkick_success_state(project_id, action, message):
    """Disabled: do not store post-kickoff success messages."""
    _final_clean_clear_stale_postkick_ui_state()
    return None


def _safe_show_postkick_success(project_id, action):
    """Disabled: do not display old post-kickoff success messages."""
    _final_clean_clear_stale_postkick_ui_state()
    return None


def _ld_store_success(project_id, action, message):
    """Disabled: do not store post-kickoff success messages."""
    _final_clean_clear_stale_postkick_ui_state()
    return None


def _ld_show_success(project_id, action):
    """Disabled: do not display old post-kickoff success messages."""
    _final_clean_clear_stale_postkick_ui_state()
    return None


def _final_clean_toast(message):
    """Temporary feedback only. Nothing is stored, so it will not appear in the next login/session."""
    _final_clean_clear_stale_postkick_ui_state()
    try:
        st.toast(safe_text(message), icon="✅")
    except Exception:
        pass


def _bandwidth_clear_capacity_caches():
    """Refresh workflow/cache safely without clearing login/session-related app cache."""
    try:
        clear_workflow_read_cache()
    except Exception:
        pass

    try:
        read_dynamic_capacity_sources.clear()
    except Exception:
        pass


def _reqfix_clear_after_requirement_db_save():
    """Refresh workflow/cache safely after requirement DB save."""
    try:
        clear_workflow_read_cache()
    except Exception:
        pass

    try:
        read_dynamic_capacity_sources.clear()
    except Exception:
        pass


try:
    _final_clean_previous_approve_delivery_plan_and_allocate = approve_delivery_plan_and_allocate
except Exception:
    _final_clean_previous_approve_delivery_plan_and_allocate = None


def approve_delivery_plan_and_allocate(project, plan, user, manager_plan_text, selected_rows):
    """Safety override.

    If a project already has an active team, never replace the team.
    Route post-kickoff additions to append-only add_project_members_after_kickoff().
    """
    if not isinstance(project, dict):
        return False, "Project was not found."

    project_id = safe_text(project.get("project_id"))

    try:
        active_allocations = get_project_allocations(project_id)
        has_active_team = active_allocations is not None and not active_allocations.empty
    except Exception:
        has_active_team = False

    try:
        already_started = _postkick_is_project_started(project, plan)
    except Exception:
        already_started = has_active_team

    if already_started and has_active_team:
        return add_project_members_after_kickoff(
            project,
            plan,
            user,
            selected_rows,
            data=None,
        )

    if _final_clean_previous_approve_delivery_plan_and_allocate is None:
        return False, "Initial allocation function is unavailable."

    return _final_clean_previous_approve_delivery_plan_and_allocate(
        project,
        plan,
        user,
        manager_plan_text,
        selected_rows,
    )


def _final_clean_delivery_rows_for_ta(focus_proposal_id=None):
    """Load accepted/delivery projects for Technical Architect workspace."""
    try:
        if "_v49_delivery_rows_for_operations" in globals():
            rows = _v49_delivery_rows_for_operations(focus_proposal_id=focus_proposal_id)
            if rows is not None and not rows.empty:
                return rows
    except Exception:
        pass

    try:
        projects = read_simple_table("projects", PROJECT_COLUMNS)
    except Exception:
        return pd.DataFrame(columns=PROJECT_COLUMNS)

    if projects is None or projects.empty:
        return pd.DataFrame(columns=PROJECT_COLUMNS)

    working = projects.copy()

    if focus_proposal_id and "proposal_id" in working.columns:
        working = working[working["proposal_id"].astype(str) == safe_text(focus_proposal_id)]

    if working.empty:
        return working

    try:
        plans = read_simple_table("delivery_plans", DELIVERY_PLAN_COLUMNS)
    except Exception:
        plans = pd.DataFrame(columns=DELIVERY_PLAN_COLUMNS)

    if plans is not None and not plans.empty:
        if focus_proposal_id and "proposal_id" in plans.columns:
            plans = plans[plans["proposal_id"].astype(str) == safe_text(focus_proposal_id)]

        try:
            merged = plans.merge(
                working,
                on=["project_id", "proposal_id", "client_id"],
                how="right",
                suffixes=("", "_project"),
            )
            return merged
        except Exception:
            pass

    for col in DELIVERY_PLAN_COLUMNS:
        if col not in working.columns:
            working[col] = ""

    return working


def _final_clean_project_plan_from_row(row):
    if hasattr(row, "to_dict"):
        row = row.to_dict()

    project = {col: row.get(col, "") for col in PROJECT_COLUMNS}
    plan = {col: row.get(col, "") for col in DELIVERY_PLAN_COLUMNS}

    if not safe_text(project.get("created_at")) and safe_text(row.get("created_at_project")):
        project["created_at"] = row.get("created_at_project")

    if not safe_text(project.get("updated_at")) and safe_text(row.get("updated_at_project")):
        project["updated_at"] = row.get("updated_at_project")

    return project, plan


def _final_clean_select_project(user, rows, focus_proposal_id=None):
    if rows is None or rows.empty:
        return None

    try:
        sort_col = "updated_at_project" if "updated_at_project" in rows.columns else "updated_at" if "updated_at" in rows.columns else "created_at"
        rows = rows.sort_values(sort_col, ascending=False)
    except Exception:
        pass

    labels = []
    row_list = []

    for idx, (_, row) in enumerate(rows.iterrows(), start=1):
        project_id = safe_text(row.get("project_id"))
        project_name = safe_text(row.get("project_name")) or project_id or "Accepted client project"
        status = safe_text(row.get("approval_status")) or safe_text(row.get("project_status")) or "Waiting for review"
        created = safe_text(row.get("created_at")) or safe_text(row.get("created_at_project")) or safe_text(row.get("updated_at"))
        labels.append(f"{idx}. {project_name} | {project_id} | {status} | {created}")
        row_list.append(row)

    if not labels:
        return None

    if focus_proposal_id and len(labels) == 1:
        return row_list[0]

    selected = st.selectbox(
        "Accepted projects - recent first",
        labels,
        key=f"final_clean_ta_project_select_{actor_id(user)}_{safe_text(focus_proposal_id) or 'all'}",
    )

    return row_list[labels.index(selected)]


def _final_clean_available_employees(data, project_id):
    employees = data.get("employees", pd.DataFrame()).copy() if isinstance(data, dict) else pd.DataFrame()

    if employees is None or employees.empty:
        return pd.DataFrame()

    try:
        employees = filter_project_delivery_employees(employees, data)
    except Exception:
        pass

    if employees is None or employees.empty:
        return pd.DataFrame()

    active_ids = _team_active_employee_ids(project_id)

    if "employee_id" in employees.columns:
        employees = employees[
            ~employees["employee_id"].astype(str).str.upper().isin(active_ids)
        ].copy()

    if employees.empty:
        return employees

    employees["label"] = employees.apply(
        lambda r: (
            f"{r.get('employee_id')} - {r.get('employee_name')} "
            f"({r.get('designation')}, available "
            f"{r.get('available_bandwidth', r.get('availability_percent', ''))}%)"
        ),
        axis=1,
    )

    return employees


def _final_clean_build_selected_employee_rows(selected_labels, employees, project, default_module, default_role, allocation_percent):
    rows = []

    for label in selected_labels or []:
        matched = employees[employees["label"] == label]
        if matched.empty:
            continue

        emp = matched.iloc[0].to_dict()
        module = safe_text(default_module) or safe_text(emp.get("primary_skill")) or safe_text(emp.get("designation"))
        role = safe_text(default_role) or safe_text(emp.get("designation"))
        allocation = safe_int(allocation_percent, 40)

        rows.append({
            "employee_id": safe_text(emp.get("employee_id")),
            "employee_name": safe_text(emp.get("employee_name")),
            "department": safe_text(emp.get("department")),
            "designation": safe_text(emp.get("designation")),
            "project_role": role,
            "assigned_module": module,
            "responsibility_summary": (
                f"Assigned to support {module} for "
                f"{project_display_name(project=project, project_id=project.get('project_id'))}. "
                "Submit mandatory weekly progress updates and raise blockers/support needs from the employee workbench."
            ),
            "allocation_percent": str(allocation),
        })

    return rows


def _final_clean_render_initial_allocation(project, plan, user, data=None):
    """Show initial allocation only when there is no active team yet."""
    project_id = safe_text(project.get("project_id"))
    plan_id = safe_text(plan.get("delivery_plan_id")) or project_id

    active_allocations = get_project_allocations(project_id)

    if active_allocations is not None and not active_allocations.empty:
        return

    with st.expander("Initial delivery team allocation", expanded=False):
        st.caption("Use this only before the project team is allocated for the first time.")

        employees = _final_clean_available_employees(data or {}, project_id)

        if employees is None or employees.empty:
            st.warning("No eligible delivery employees are available for allocation.")
            return

        with st.form(f"final_clean_initial_alloc_form_{project_id}", clear_on_submit=True):
            selected = st.multiselect(
                "Select delivery employees",
                employees["label"].tolist(),
            )

            default_module = st.text_input(
                "Default module / work area",
                value="Project delivery",
            )

            default_role = st.text_input(
                "Default project role",
                value="Delivery Engineer",
            )

            allocation_percent = st.number_input(
                "Allocation % for selected employees",
                min_value=5,
                max_value=100,
                value=40,
                step=5,
            )

            manager_plan = st.text_area(
                "Technical Architect delivery plan",
                value=safe_text(plan.get("operations_manager_plan") or plan.get("operations_agent_plan")),
                height=180,
            )

            clicked = st.form_submit_button(
                "Approve delivery plan and allocate selected employees",
                type="primary",
            )

        if clicked:
            selected_rows = _final_clean_build_selected_employee_rows(
                selected,
                employees,
                project,
                default_module,
                default_role,
                allocation_percent,
            )

            if not selected_rows:
                st.error("Select at least one eligible delivery employee.")
                return

            if not safe_text(manager_plan).strip():
                st.error("Please keep or edit the delivery plan before approving.")
                return

            ok, msg = _final_clean_previous_approve_delivery_plan_and_allocate(
                project,
                plan,
                user,
                manager_plan,
                selected_rows,
            )

            if ok:
                _final_clean_toast("Initial team allocation saved.")
            else:
                st.error(msg)


def _final_clean_render_postkick_controls_for_project(project, plan, user, data=None):
    """Post-kickoff controls without sticky success popups."""
    _final_clean_clear_stale_postkick_ui_state()

    project_id = safe_text(project.get("project_id"))
    plan_id = safe_text(plan.get("delivery_plan_id")) or project_id

    active_allocations = get_project_allocations(project_id)
    active_count = 0 if active_allocations is None or active_allocations.empty else len(active_allocations)

    st.markdown(
        """
        <div class="dd-section-card dd-dashboard-shell">
            <div class="dd-section-title">Post-kickoff project controls</div>
            <div class="dd-section-subtitle">
                Update requirements, add employees, or remove employees after kickoff.
                Sticky success popups are disabled. Client and CEO are not notified from these controls.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Project", project_display_name(project=project, project_id=project_id))
    c2.metric("Active employees", active_count)
    c3.metric("Status", safe_text(project.get("project_status"), "In progress"))

    # -------------------------------------------------------------------------
    # Requirement change
    # -------------------------------------------------------------------------
    with st.expander("Change project requirement after kickoff", expanded=False):
        current_week = _postkick_current_week_number(project_id)

        st.warning(
            f"This will preserve completed weeks and regenerate pending targets from Week {current_week} onward. "
            "Allocated project members are notified. Client and CEO are not notified."
        )

        current_requirement = safe_text(plan.get("raw_requirement_text"))
        if current_requirement:
            st.text_area(
                "Current saved requirement",
                value=current_requirement,
                height=150,
                disabled=True,
                key=f"final_clean_current_req_{project_id}",
            )

        with st.form(f"final_clean_req_change_form_{project_id}", clear_on_submit=True):
            updated_requirement = st.text_area(
                "Updated requirement / changed requirement",
                height=180,
                placeholder="Enter the latest changed requirement or full corrected requirement.",
            )

            change_note = st.text_area(
                "Reason / change summary for project team",
                height=90,
                placeholder="Example: Client clarified branch-wise access and dashboard priority.",
            )

            req_clicked = st.form_submit_button(
                "Save requirement change and notify project members",
                type="primary",
            )

        if req_clicked:
            ok, msg = save_postkick_requirement_change(
                project,
                plan,
                user,
                updated_requirement,
                change_note,
                data=data,
            )

            if ok:
                _final_clean_toast("Requirement change saved and project members notified.")
            else:
                st.error(msg)

    # -------------------------------------------------------------------------
    # Add employees
    # -------------------------------------------------------------------------
    with st.expander("Add more delivery employees after kickoff", expanded=False):
        st.caption(
            "Append-only team update. Existing active employees will not be removed or replaced."
        )

        employees = _final_clean_available_employees(data or {}, project_id)

        if employees is None or employees.empty:
            st.info("All eligible delivery employees are already active on this project, or no eligible employees are available.")
        else:
            with st.form(f"final_clean_add_people_form_{project_id}", clear_on_submit=True):
                selected = st.multiselect(
                    "Select additional delivery employees",
                    employees["label"].tolist(),
                )

                default_module = st.text_input(
                    "Default module / work area for selected employees",
                    value="Project delivery support",
                )

                default_role = st.text_input(
                    "Default project role for selected employees",
                    value="Delivery Engineer",
                )

                allocation_percent = st.number_input(
                    "Allocation % for selected employees",
                    min_value=5,
                    max_value=100,
                    value=40,
                    step=5,
                )

                add_clicked = st.form_submit_button(
                    "Add selected employees without removing existing team",
                    type="primary",
                )

            if add_clicked:
                selected_rows = _final_clean_build_selected_employee_rows(
                    selected,
                    employees,
                    project,
                    default_module,
                    default_role,
                    allocation_percent,
                )

                ok, msg = add_project_members_after_kickoff(
                    project,
                    plan,
                    user,
                    selected_rows,
                    data=data,
                )

                if ok:
                    _final_clean_toast("Team updated. Existing employees were preserved.")
                else:
                    st.error(msg)

    # -------------------------------------------------------------------------
    # Remove employees
    # -------------------------------------------------------------------------
    with st.expander("Remove employees from this project if necessary", expanded=False):
        st.caption(
            "This is a soft remove. It keeps history, releases bandwidth, and hides the project from the removed employee dashboard."
        )

        active_allocations = get_project_allocations(project_id)

        if active_allocations is None or active_allocations.empty:
            st.info("No active employees are currently allocated to this project.")
        else:
            remove_options = []
            remove_map = {}

            for _, row in active_allocations.iterrows():
                row_dict = row.to_dict()
                label = _team_employee_label(row_dict)
                remove_options.append(label)
                remove_map[label] = safe_text(row_dict.get("employee_id")).upper()

            with st.form(f"final_clean_remove_people_form_{project_id}", clear_on_submit=True):
                selected_remove_labels = st.multiselect(
                    "Select employees to remove from active project team",
                    remove_options,
                )

                remove_reason = st.text_area(
                    "Removal reason / note",
                    height=90,
                    placeholder="Example: Module completed, employee moved to another project, replacement added, or allocation no longer needed.",
                )

                removing_all = len(selected_remove_labels) == len(remove_options) and len(remove_options) > 0
                allow_remove_all = False

                if removing_all:
                    allow_remove_all = st.checkbox(
                        "I understand this will leave the project with no active delivery employees.",
                    )

                remove_clicked = st.form_submit_button(
                    "Remove selected employees from this project",
                    type="primary",
                )

            if remove_clicked:
                employee_ids = [
                    remove_map[label]
                    for label in selected_remove_labels
                    if label in remove_map
                ]

                ok, msg = remove_project_members_after_kickoff(
                    project,
                    plan,
                    user,
                    employee_ids,
                    remove_reason,
                    data=data,
                    allow_remove_all=allow_remove_all,
                )

                if ok:
                    _final_clean_toast("Selected employee(s) removed and bandwidth released.")
                else:
                    st.error(msg)


def render_postkick_requirement_and_team_controls(user, data=None, focus_proposal_id=None):
    """Standalone post-kickoff control panel with no stored success popups."""
    _final_clean_clear_stale_postkick_ui_state()

    if role_key_for_user(user) != "operations":
        return

    projects = _postkick_get_active_projects_for_ta(focus_proposal_id=focus_proposal_id)

    if projects is None or projects.empty:
        return

    labels = []
    rows = []

    for idx, (_, row) in enumerate(projects.iterrows(), start=1):
        project_id = safe_text(row.get("project_id"))
        labels.append(
            f"{idx}. {project_display_name(project=row, project_id=project_id)} | "
            f"{project_id} | {safe_text(row.get('project_status'))}"
        )
        rows.append(row.to_dict())

    if not labels:
        return

    if focus_proposal_id and len(labels) == 1:
        project = rows[0]
    else:
        selected_label = st.selectbox(
            "Choose active project for post-kickoff update",
            labels,
            key=f"final_clean_postkick_project_select_{actor_id(user)}_{safe_text(focus_proposal_id) or 'all'}",
        )
        project = rows[labels.index(selected_label)]

    project_id = safe_text(project.get("project_id"))
    plan = get_delivery_plan_for_client_project(project_id)

    if not plan:
        st.info("Delivery plan is not available yet for this project.")
        return

    _final_clean_render_postkick_controls_for_project(project, plan, user, data=data)


def render_operations_delivery_workspace(user, data, focus_proposal_id=None):
    """Clean Technical Architect workspace.

    Important:
    - Does NOT call older stacked workspace wrappers.
    - Removes duplicate post-kickoff panels.
    - Removes sticky success messages.
    - Keeps initial allocation separate from post-kickoff add/remove.
    """
    _final_clean_clear_stale_postkick_ui_state()

    if role_key_for_user(user) != "operations":
        return

    st.markdown(
        """
        <div class="dd-section-card dd-dashboard-shell">
            <div class="dd-section-eyebrow">Technical Architect workspace</div>
            <div class="dd-section-title">Project delivery control center</div>
            <div class="dd-section-subtitle">
                Select an accepted project. Review week status, targets, requirement, client conversation,
                employee updates, and team controls from one clean workspace.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    rows = _final_clean_delivery_rows_for_ta(focus_proposal_id=focus_proposal_id)

    if rows is None or rows.empty:
        st.info("No accepted client projects are available yet.")
        return

    selected_row = _final_clean_select_project(user, rows, focus_proposal_id=focus_proposal_id)

    if selected_row is None:
        st.info("Select a project to open its delivery workspace.")
        return

    project, plan = _final_clean_project_plan_from_row(selected_row)
    project_id = safe_text(project.get("project_id"))
    proposal_id = safe_text(project.get("proposal_id"))

    if not project_id:
        st.warning("Selected project has no project ID.")
        return

    proposal_report = get_proposal_report_by_id(proposal_id) or {}
    active_allocations = get_project_allocations(project_id)
    all_employee_updates = get_employee_project_updates(project_id=project_id)
    open_employee_updates = get_open_employee_project_updates(project_id=project_id)

    active_count = 0 if active_allocations is None or active_allocations.empty else len(active_allocations)
    open_count = 0 if open_employee_updates is None or open_employee_updates.empty else len(open_employee_updates)

    st.markdown(
        f"""
        <div class="dd-project-card">
            <div class="dd-card-header-row">
                <div>
                    <div class="dd-card-kicker">Selected accepted project</div>
                    <div class="dd-card-title-small">{safe_text(project.get('project_name')) or safe_text(project_id)}</div>
                    <div class="dd-card-subtle">Project ID: {safe_text(project_id)}</div>
                </div>
                <div class="dd-status-pill">{safe_text(project.get('project_status')) or 'In progress'}</div>
            </div>
            <div class="dd-metric-grid">
                <div class="dd-mini-metric"><span>Delivery status</span><strong>{safe_text(plan.get('approval_status')) or 'Waiting for review'}</strong></div>
                <div class="dd-mini-metric"><span>Active employees</span><strong>{active_count}</strong></div>
                <div class="dd-mini-metric"><span>Open employee requests</span><strong>{open_count}</strong></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "_v49_project_week_status_first_panel" in globals():
        _v49_project_week_status_first_panel(
            project_id,
            project_label=project_display_name(project=project, project_id=project_id),
            key_prefix=f"final_clean_week_{project_id}",
        )
    else:
        render_project_week_status_panel(
            project_id,
            title="Current project week update status",
            expanded=True,
            client_safe=False,
            key_prefix=f"final_clean_week_{project_id}",
        )

    if safe_text(plan.get("delivery_plan_id")):
        render_weekly_targets_panel(
            plan,
            title="Weekly targets for this project",
            expanded=True,
            client_safe=False,
            key_prefix=f"final_clean_targets_{project_id}",
        )

        st.markdown("### Requirement and Technical Architect analysis")

        requirement_text = safe_text(plan.get("raw_requirement_text"))
        if requirement_text:
            with st.expander("Client requirement", expanded=True):
                st.text_area(
                    "Requirement provided by client",
                    value=requirement_text,
                    height=160,
                    disabled=True,
                    key=f"final_clean_req_{project_id}",
                )

        agent_conclusion = safe_text(plan.get("operations_agent_plan"))
        with st.expander("Technical Architect Agent conclusion", expanded=False):
            if agent_conclusion:
                st.text_area(
                    "AI delivery analysis and conclusion",
                    value=agent_conclusion,
                    height=230,
                    disabled=True,
                    key=f"final_clean_agent_plan_{project_id}",
                )
            else:
                st.info("Technical Architect Agent conclusion is not available yet.")

        st.markdown("### Client / Technical Architect conversation")
        try:
            render_client_operations_conversation(
                project,
                proposal_report,
                {
                    "client_id": project.get("client_id"),
                    "client_name": safe_text(proposal_report.get("client_name")),
                },
                viewer="operations",
                user=user,
            )
        except Exception:
            st.info("Client conversation is not available right now.")

        st.markdown("### Employee requests and weekly updates")
        render_employee_update_inbox_with_done(
            all_employee_updates,
            user,
            project_id,
            key_prefix=f"final_clean_employee_updates_{project_id}",
        )

        with st.expander("Allocated team summary", expanded=False):
            if active_allocations is None or active_allocations.empty:
                st.info("No employees are currently allocated.")
            else:
                cols = [
                    c for c in [
                        "employee_name",
                        "project_role",
                        "assigned_module",
                        "allocation_percent",
                        "allocation_status",
                    ]
                    if c in active_allocations.columns
                ]
                st.dataframe(active_allocations[cols], use_container_width=True, hide_index=True)

        _final_clean_render_initial_allocation(project, plan, user, data=data)

        if _postkick_is_project_started(project, plan):
            _final_clean_render_postkick_controls_for_project(project, plan, user, data=data)

    else:
        st.info(
            "Accepted project exists, but the client has not submitted the detailed requirement yet. "
            "Delivery plan and weekly targets will appear after client requirement submission."
        )

# # =============================================================================
# # FINAL PATCH: FLEXIBLE HR BANDWIDTH / ROLE CAPACITY MATCHING
# # Paste at the VERY BOTTOM of decisiondesk_chunks/05_design_system.py
# # =============================================================================

# def _capacity_role_aliases(role):
#     """Return flexible aliases for requirement role matching."""
#     role_text = safe_text(role).lower()

#     alias_map = {
#         "ai/ml engineer": ["ai/ml engineer", "ai ml engineer", "machine learning", "ml engineer", "ai engineer", "data scientist", "ai/ml engineer trainee"],
#         "backend developer": ["backend developer", "backend engineer", "python developer", "api developer", "server developer"],
#         "frontend developer": ["frontend developer", "frontend engineer", "react developer", "ui developer", "web developer"],
#         "full stack developer": ["full stack developer", "fullstack developer", "full stack engineer", "software engineer"],
#         "devops engineer": ["devops engineer", "cloud engineer", "deployment engineer", "site reliability", "sre"],
#         "qa engineer": ["qa engineer", "qa tester", "test engineer", "quality analyst", "quality assurance"],
#         "data engineer": ["data engineer", "etl developer", "pipeline engineer", "data pipeline", "analytics engineer"],
#         "project manager": ["project manager", "technical architect", "delivery manager", "scrum master"],
#     }

#     aliases = [role_text]

#     for key, values in alias_map.items():
#         if role_text == key or key in role_text or role_text in key:
#             aliases.extend(values)

#     clean = []
#     for item in aliases:
#         item = safe_text(item).lower().strip()
#         if item and item not in clean:
#             clean.append(item)

#     return clean


# def _capacity_employee_matches_role(employee_row, required_role):
#     """Flexible employee-role match using designation, department, skills, and role text."""
#     if employee_row is None:
#         return False

#     if hasattr(employee_row, "to_dict"):
#         employee_row = employee_row.to_dict()

#     aliases = _capacity_role_aliases(required_role)

#     fields = []
#     for col in [
#         "designation",
#         "employee_designation",
#         "department",
#         "primary_skill",
#         "skill",
#         "skills",
#         "domain",
#         "project_role",
#     ]:
#         fields.append(safe_text(employee_row.get(col)))

#     combined = " | ".join(fields).lower()

#     if not combined.strip():
#         return False

#     for alias in aliases:
#         if alias and alias in combined:
#             return True

#     required_words = [
#         word for word in re.split(r"[^a-z0-9]+", safe_text(required_role).lower())
#         if len(word) >= 3
#     ]

#     if required_words:
#         hits = sum(1 for word in required_words if word in combined)
#         return hits >= max(1, min(2, len(required_words)))

#     return False


# def build_dynamic_role_capacity(required_roles, employees, new_project_timeline_months=0):
#     """Flexible live/projected capacity by role.

#     Fix:
#     - No active Supabase allocations means workload load is 0.
#     - Employees are matched flexibly by designation/skill/department.
#     - If matching employees exist, HR should not show hiring gap only because exact designation text differs.
#     """
#     dynamic_employees = build_dynamic_employee_capacity(employees, new_project_timeline_months)
#     rows = []

#     if dynamic_employees is None or getattr(dynamic_employees, "empty", True):
#         dynamic_employees = pd.DataFrame()

#     for _, req_row in required_roles.iterrows():
#         role = safe_text(req_row.get("required_role"))
#         needed = safe_number(req_row.get("required_people"), 0)

#         if dynamic_employees.empty:
#             matching = pd.DataFrame()
#         else:
#             match_mask = dynamic_employees.apply(
#                 lambda emp_row: _capacity_employee_matches_role(emp_row, role),
#                 axis=1,
#             )
#             matching = dynamic_employees[match_mask].copy()

#         if matching.empty:
#             avg_salary = 90000
#             available_now_fte = 0.0
#             projected_available_fte = 0.0
#             active_allocated_fte = 0.0
#             avg_progress = 0.0
#             blockers = 0
#             nearest_release = ""
#             capacity_notes = "No matching employee found for this role after flexible designation/skill matching."
#         else:
#             avg_salary = safe_number(
#                 pd.to_numeric(matching.get("monthly_ctc"), errors="coerce").dropna().mean(),
#                 90000,
#             )

#             available_now_fte = (
#                 pd.to_numeric(matching.get("availability_percent", 0), errors="coerce")
#                 .fillna(0)
#                 .clip(lower=0)
#                 .sum()
#                 / 100
#             )

#             projected_available_fte = (
#                 pd.to_numeric(matching.get("projected_available_percent", matching.get("availability_percent", 0)), errors="coerce")
#                 .fillna(0)
#                 .clip(lower=0)
#                 .sum()
#                 / 100
#             )

#             active_allocated_fte = (
#                 pd.to_numeric(matching.get("live_allocated_percent", 0), errors="coerce")
#                 .fillna(0)
#                 .clip(lower=0)
#                 .sum()
#                 / 100
#             )

#             progress_values = pd.to_numeric(
#                 matching.get("avg_project_progress_percent", 0),
#                 errors="coerce",
#             ).fillna(0)
#             progress_values = progress_values[progress_values > 0]
#             avg_progress = float(progress_values.mean()) if len(progress_values) else 0.0

#             blockers = int(
#                 pd.to_numeric(matching.get("hurdle_count", 0), errors="coerce")
#                 .fillna(0)
#                 .sum()
#             )

#             release_dates = [
#                 safe_text(v)
#                 for v in matching.get("next_release_date", [])
#                 if safe_text(v)
#             ]
#             nearest_release = min(release_dates) if release_dates else ""

#             matched_names = []
#             for _, emp_row in matching.head(4).iterrows():
#                 matched_names.append(
#                     safe_text(emp_row.get("employee_name"))
#                     or safe_text(emp_row.get("employee_id"))
#                 )

#             capacity_notes = (
#                 f"Matched {len(matching)} employee(s): "
#                 + ", ".join([name for name in matched_names if name])
#                 + "."
#             )

#         rows.append({
#             "role": role,
#             "needed": round(needed, 2),
#             "available_capacity": round(projected_available_fte, 2),
#             "available_now_fte": round(available_now_fte, 2),
#             "projected_available_fte": round(projected_available_fte, 2),
#             "active_allocated_fte": round(active_allocated_fte, 2),
#             "gap": round(max(0, needed - projected_available_fte), 2),
#             "immediate_gap": round(max(0, needed - available_now_fte), 2),
#             "avg_current_project_progress_percent": round(avg_progress, 2),
#             "hurdle_or_support_request_count": blockers,
#             "nearest_release_date": nearest_release,
#             "capacity_notes": capacity_notes,
#             "avg_monthly_salary": round(avg_salary, 2),
#         })

#     return rows

# =============================================================================
# FINAL PATCH: INTERNAL AGENTS USE SUPABASE PROJECT_ALLOCATIONS FOR LIVE BANDWIDTH
# Paste at the VERY BOTTOM of decisiondesk_chunks/05_design_system.py
# =============================================================================
# Business rule:
# - Excel is static master data only: users, employees, domain, skills, designation, salary, requirement templates.
# - Supabase project_allocations is the only dynamic bandwidth source.
# - Excel availability_percent is ignored.
# - If project_allocations has no active rows, every eligible delivery employee has 100% bandwidth = 1.0 FTE.
# =============================================================================

_BWDB_PROJECT_ALLOCATION_COLUMNS = [
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

_BWDB_ACTIVE_STATUSES = {
    "active",
    "assigned",
    "in progress",
    "approved",
}

_BWDB_INACTIVE_STATUSES = {
    "removed",
    "released",
    "inactive",
    "closed",
    "completed",
    "cancelled",
    "canceled",
}


def _bwdb_norm_id(value):
    return safe_text(value).strip().upper()


def _bwdb_read_active_project_allocations():
    """Read active allocation rows from Supabase project_allocations.

    Empty table means nobody is allocated, so used bandwidth is zero.
    """
    try:
        df = read_simple_table("project_allocations", _BWDB_PROJECT_ALLOCATION_COLUMNS)
    except Exception:
        return pd.DataFrame(columns=_BWDB_PROJECT_ALLOCATION_COLUMNS)

    if df is None or df.empty:
        return pd.DataFrame(columns=_BWDB_PROJECT_ALLOCATION_COLUMNS)

    working = df.copy()

    if "allocation_status" not in working.columns:
        working["allocation_status"] = "Active"

    status = (
        working["allocation_status"]
        .fillna("Active")
        .astype(str)
        .str.strip()
        .str.lower()
    )

    working = working[
        status.isin(_BWDB_ACTIVE_STATUSES)
        & ~status.isin(_BWDB_INACTIVE_STATUSES)
    ].copy()

    if working.empty:
        return pd.DataFrame(columns=_BWDB_PROJECT_ALLOCATION_COLUMNS)

    working["employee_id_norm"] = working["employee_id"].apply(_bwdb_norm_id)

    working["allocation_percent_num"] = pd.to_numeric(
        working["allocation_percent"],
        errors="coerce",
    ).fillna(0).clip(lower=0, upper=100)

    working = working[working["employee_id_norm"] != ""].copy()

    return working


def _bwdb_used_percent_by_employee():
    """Return employee_id -> used allocation percent from Supabase only."""
    active = _bwdb_read_active_project_allocations()

    if active is None or active.empty:
        return {}

    return (
        active
        .groupby("employee_id_norm")["allocation_percent_num"]
        .sum()
        .clip(lower=0, upper=100)
        .to_dict()
    )


def _bwdb_executive_ids_from_data(data):
    ids = set()

    try:
        users = data.get("users", pd.DataFrame()) if isinstance(data, dict) else pd.DataFrame()
    except Exception:
        users = pd.DataFrame()

    if users is None or users.empty:
        return ids

    for _, row in users.iterrows():
        role = safe_text(row.get("role")).lower()
        designation = safe_text(row.get("designation")).lower()
        department = safe_text(row.get("department")).lower()
        user_id = _bwdb_norm_id(row.get("user_id") or row.get("employee_id"))

        is_executive = (
            role in ["executive", "founder", "ceo"]
            or "executive" in designation
            or "founder" in designation
            or "ceo" in designation
            or (
                "manager" in designation
                and any(word in department for word in ["sales", "finance", "hr", "human resource", "strategy"])
            )
        )

        if is_executive and user_id:
            ids.add(user_id)

    return ids


def _bwdb_is_delivery_employee(row, executive_ids=None):
    """Use Excel/static user/domain fields only to decide whether employee is delivery-eligible."""
    executive_ids = executive_ids or set()

    if hasattr(row, "to_dict"):
        row = row.to_dict()

    emp_id = _bwdb_norm_id(row.get("employee_id") or row.get("user_id"))
    role = safe_text(row.get("role")).lower()
    designation = safe_text(row.get("designation") or row.get("employee_designation")).lower()
    department = safe_text(row.get("department") or row.get("employee_department")).lower()
    domain = safe_text(row.get("domain") or row.get("primary_skill") or row.get("skills") or row.get("skill")).lower()

    if emp_id and emp_id in executive_ids:
        return False

    if role in ["executive", "founder", "ceo"]:
        return False

    if any(word in designation for word in ["executive", "founder", "ceo"]):
        return False

    if department in ["sales", "finance", "hr", "human resources", "strategy", "business strategy"]:
        return False

    blocked_domain_words = [
        "enterprise sales",
        "financial planning",
        "hr operations",
        "human resource",
        "business strategy",
    ]

    if any(word in domain for word in blocked_domain_words):
        return False

    return bool(emp_id)


def filter_project_delivery_employees(employees, data=None):
    """Delivery employee filter using static Excel/user data, then Supabase-only bandwidth."""
    if employees is None or getattr(employees, "empty", True):
        return employees

    df = employees.copy()

    if "employee_id" not in df.columns and "user_id" in df.columns:
        df["employee_id"] = df["user_id"]

    executive_ids = _bwdb_executive_ids_from_data(data)

    rows = []
    for _, row in df.iterrows():
        row_dict = row.to_dict()
        if _bwdb_is_delivery_employee(row_dict, executive_ids):
            rows.append(row_dict)

    if not rows:
        return df.iloc[0:0].copy()

    filtered = pd.DataFrame(rows)

    return build_dynamic_employee_capacity(filtered)


def build_dynamic_employee_capacity(employees, new_project_timeline_months=0):
    """Supabase-only live bandwidth calculation.

    Formula:
        base bandwidth = 100%
        used bandwidth = active project_allocations.allocation_percent
        available bandwidth = 100 - used bandwidth

    Excel availability_percent is ignored completely.
    """
    if employees is None or getattr(employees, "empty", True):
        return employees

    df = employees.copy()

    if "employee_id" not in df.columns and "user_id" in df.columns:
        df["employee_id"] = df["user_id"]

    if "employee_id" not in df.columns:
        return df

    used_by_employee = _bwdb_used_percent_by_employee()

    def _used(row):
        emp_id = _bwdb_norm_id(row.get("employee_id") or row.get("user_id"))
        return max(0.0, min(100.0, safe_number(used_by_employee.get(emp_id, 0), 0)))

    df["base_availability_percent"] = 100.0
    df["live_allocated_percent"] = df.apply(_used, axis=1)
    df["availability_percent"] = df["live_allocated_percent"].apply(
        lambda used: max(0.0, 100.0 - safe_number(used, 0))
    )
    df["projected_available_percent"] = df["availability_percent"]
    df["projected_release_percent"] = 0.0

    df["available_bandwidth"] = df["availability_percent"].apply(
        lambda value: f"{safe_number(value, 0):.0f}%"
    )

    df["active_project_count"] = df["live_allocated_percent"].apply(
        lambda value: 1 if safe_number(value, 0) > 0 else 0
    )
    df["avg_project_progress_percent"] = 0.0
    df["hurdle_count"] = 0
    df["next_release_date"] = ""

    df["capacity_notes"] = df.apply(
        lambda row: (
            "Bandwidth source: Supabase project_allocations only. "
            "Excel availability_percent ignored. "
            "Static Excel data used only for employee/user/domain/skill/salary. "
            f"Base: 100%; active allocated: {safe_number(row.get('live_allocated_percent'), 0):.0f}%; "
            f"available: {safe_number(row.get('availability_percent'), 0):.0f}%."
        ),
        axis=1,
    )

    return df


def adjust_employee_availability_with_dynamic_allocations(employees, new_project_timeline_months=0):
    """Compatibility wrapper for older code paths."""
    return build_dynamic_employee_capacity(employees, new_project_timeline_months)


def _bwdb_role_aliases(role):
    role_text = safe_text(role).lower().strip()

    alias_map = {
        "ai/ml engineer": [
            "ai/ml engineer", "ai ml engineer", "ai engineer", "ml engineer",
            "machine learning", "data scientist", "llm", "rag", "genai", "generative ai"
        ],
        "backend developer": [
            "backend developer", "backend engineer", "python developer",
            "api developer", "server developer", "fastapi", "django", "flask"
        ],
        "frontend developer": [
            "frontend developer", "frontend engineer", "react developer",
            "ui developer", "web developer", "streamlit", "angular", "vue"
        ],
        "full stack developer": [
            "full stack developer", "fullstack developer", "full stack engineer",
            "software engineer", "application developer"
        ],
        "devops engineer": [
            "devops engineer", "cloud engineer", "deployment engineer",
            "sre", "site reliability", "docker", "github", "aws", "azure", "gcp"
        ],
        "qa engineer": [
            "qa engineer", "qa tester", "test engineer", "quality analyst",
            "quality assurance", "testing"
        ],
        "data engineer": [
            "data engineer", "etl developer", "pipeline engineer",
            "analytics engineer", "data pipeline", "postgresql", "sql"
        ],
        "technical architect": [
            "technical architect", "solution architect", "architect"
        ],
        "ui/ux designer": [
            "ui designer", "ux designer", "ui/ux designer", "product designer"
        ],
    }

    aliases = [role_text]

    for key, values in alias_map.items():
        if role_text == key or key in role_text or role_text in key:
            aliases.extend(values)

    clean = []
    for item in aliases:
        item = safe_text(item).lower().strip()
        if item and item not in clean:
            clean.append(item)

    return clean


def _bwdb_employee_matches_required_role(employee_row, required_role):
    """Match required role against static Excel designation/domain/skill fields."""
    if hasattr(employee_row, "to_dict"):
        employee_row = employee_row.to_dict()

    aliases = _bwdb_role_aliases(required_role)

    fields = []
    for col in [
        "employee_name",
        "designation",
        "employee_designation",
        "department",
        "employee_department",
        "domain",
        "primary_skill",
        "skill",
        "skills",
        "project_role",
    ]:
        fields.append(safe_text(employee_row.get(col)))

    combined = " | ".join(fields).lower()

    if not combined.strip():
        return False

    for alias in aliases:
        if alias and alias in combined:
            return True

    generic_words = {
        "engineer", "developer", "specialist", "consultant",
        "senior", "junior", "trainee", "lead", "associate",
    }

    required_words = [
        word
        for word in re.split(r"[^a-z0-9]+", safe_text(required_role).lower())
        if len(word) >= 3 and word not in generic_words
    ]

    if not required_words:
        return False

    hits = sum(1 for word in required_words if word in combined)

    return hits >= 1


def _bwdb_salary_average(matching):
    if matching is None or matching.empty:
        return 90000

    for col in ["monthly_ctc", "salary", "monthly_salary", "ctc"]:
        if col in matching.columns:
            values = pd.to_numeric(matching[col], errors="coerce").dropna()
            if not values.empty:
                return safe_number(values.mean(), 90000)

    return 90000


def build_dynamic_role_capacity(required_roles, employees, new_project_timeline_months=0):
    """Role capacity used by the internal agent meeting.

    Uses:
    - Excel/static data for required role, employee identity, designation, domain, skill, salary.
    - Supabase project_allocations for live bandwidth only.

    Empty project_allocations:
    - every matching delivery employee contributes 1.0 FTE.
    """
    rows = []

    if required_roles is None or getattr(required_roles, "empty", True):
        return rows

    delivery_employees = filter_project_delivery_employees(employees, data if "data" in globals() else None)
    dynamic_employees = build_dynamic_employee_capacity(delivery_employees, new_project_timeline_months)

    if dynamic_employees is None or getattr(dynamic_employees, "empty", True):
        dynamic_employees = pd.DataFrame()

    active_allocations = _bwdb_read_active_project_allocations()
    active_allocation_count = 0 if active_allocations is None or active_allocations.empty else len(active_allocations)

    for _, req_row in required_roles.iterrows():
        role = safe_text(req_row.get("required_role"))
        needed = safe_number(req_row.get("required_people"), 0)

        if dynamic_employees.empty:
            matching = pd.DataFrame()
        else:
            match_mask = dynamic_employees.apply(
                lambda employee_row: _bwdb_employee_matches_required_role(employee_row, role),
                axis=1,
            )
            matching = dynamic_employees[match_mask].copy()

        if matching.empty:
            available_now_fte = 0.0
            projected_available_fte = 0.0
            active_allocated_fte = 0.0
            avg_salary = 90000
            capacity_notes = (
                "No matching delivery employee found in static Excel employee/user/domain/skill data for this required role. "
                "Supabase project_allocations bandwidth may be free, but role/domain match is missing."
            )
        else:
            available_now_fte = (
                pd.to_numeric(matching["availability_percent"], errors="coerce")
                .fillna(0)
                .clip(lower=0, upper=100)
                .sum()
                / 100
            )

            projected_available_fte = (
                pd.to_numeric(matching["projected_available_percent"], errors="coerce")
                .fillna(0)
                .clip(lower=0, upper=100)
                .sum()
                / 100
            )

            active_allocated_fte = (
                pd.to_numeric(matching["live_allocated_percent"], errors="coerce")
                .fillna(0)
                .clip(lower=0, upper=100)
                .sum()
                / 100
            )

            avg_salary = _bwdb_salary_average(matching)

            matched_names = []
            for _, employee_row in matching.head(6).iterrows():
                matched_names.append(
                    safe_text(employee_row.get("employee_name"))
                    or safe_text(employee_row.get("employee_id"))
                )

            if active_allocation_count == 0:
                bandwidth_note = (
                    "project_allocations has no active rows, so every matching delivery employee is treated as 100% available."
                )
            else:
                bandwidth_note = (
                    f"{active_allocation_count} active Supabase allocation row(s) were used to reduce available bandwidth."
                )

            capacity_notes = (
                f"Matched {len(matching)} delivery employee(s): "
                + ", ".join([name for name in matched_names if name])
                + ". Bandwidth source: Supabase project_allocations only; Excel availability_percent ignored. "
                + bandwidth_note
            )

        gap = round(max(0, needed - projected_available_fte), 2)
        immediate_gap = round(max(0, needed - available_now_fte), 2)
        hiring_needed = round(gap if gap > 0.30 else 0, 2)

        rows.append({
            "role": role,
            "needed": round(needed, 2),
            "available_capacity": round(projected_available_fte, 2),
            "available_now_fte": round(available_now_fte, 2),
            "projected_available_fte": round(projected_available_fte, 2),
            "active_allocated_fte": round(active_allocated_fte, 2),
            "gap": gap,
            "immediate_gap": immediate_gap,
            "hiring_needed_fte": hiring_needed,
            "avg_current_project_progress_percent": 0,
            "hurdle_or_support_request_count": 0,
            "nearest_release_date": "",
            "capacity_notes": capacity_notes,
            "avg_monthly_salary": round(avg_salary, 2),
        })

    return rows


def build_live_project_capacity_snapshot(limit=8):
    """Live capacity snapshot from Supabase project_allocations only."""
    active = _bwdb_read_active_project_allocations()

    if active is None or active.empty:
        return []

    rows = []

    grouped = active.groupby("project_id", dropna=False)

    for project_id, group in grouped:
        if len(rows) >= limit:
            break

        rows.append({
            "project_id": safe_text(project_id),
            "employee_count": int(group["employee_id_norm"].nunique()),
            "active_allocated_fte": round(
                pd.to_numeric(group["allocation_percent_num"], errors="coerce").fillna(0).sum() / 100,
                2,
            ),
            "capacity_basis": "Supabase project_allocations active allocation rows only.",
        })

    return rows


try:
    _bwdb_previous_run_external_client_decision = run_external_client_decision
except Exception:
    _bwdb_previous_run_external_client_decision = None


def run_external_client_decision(query, data):
    """Internal agent meeting entry point with corrected bandwidth basis."""
    if _bwdb_previous_run_external_client_decision is None:
        return {}

    analysis = _bwdb_previous_run_external_client_decision(query, data)

    if isinstance(analysis, dict):
        analysis["capacity_basis"] = (
            "Static Excel data is used only for employees, users, domain, skills, designation, salary, and requirement templates. "
            "Live bandwidth is calculated only from Supabase project_allocations. "
            "If project_allocations has no active rows, every matching delivery employee is treated as 100% available."
        )

        # Force wording consistency after corrected calculation.
        if safe_number(analysis.get("total_active_allocated_fte"), 0) == 0:
            if safe_number(analysis.get("total_hiring_needed_fte"), 0) <= 0.30:
                analysis["hiring_recommendation"] = (
                    "No hiring needed for the initial quotation. Supabase project_allocations shows no active bandwidth usage, "
                    "and matching delivery employees can be allocated from the current team."
                )

    return analysis
