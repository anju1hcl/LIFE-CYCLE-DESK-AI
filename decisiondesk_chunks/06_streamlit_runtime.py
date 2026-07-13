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
    """Scroll only to the intended UI section, not always to the AI Front Desk chat."""
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
    elif target == "dashboard_result":
        selector = "#dd-dashboard-result"
        block = "start"
    elif target == "selected_update_dashboard":
        selector = "#dd-selected-update-dashboard"
        block = "start"
    elif target == "reviewed_item_detail":
        selector = "#dd-reviewed-item-detail"
        block = "start"
    elif target == "selected_project_detail":
        selector = "#dd-selected-project-detail"
        block = "start"
    elif target == "ta_project_week_detail":
        selector = "#dd-ta-selected-week-project-detail"
        block = "start"
    elif target == "frontdesk_answer":
        selector = "#dd-frontdesk-latest-answer"
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
                let attempts = 0;
                function findTarget() {{
                    if ({target!r} === 'chat') {{
                        const messages = doc.querySelectorAll('[data-testid="stChatMessage"]');
                        return messages.length ? messages[messages.length - 1] : null;
                    }}
                    return doc.querySelector({selector!r});
                }}
                function scrollWhenReady() {{
                    attempts += 1;
                    const targetNode = findTarget();
                    if (targetNode) {{
                        targetNode.scrollIntoView({{behavior: 'smooth', block: {block!r}}});
                    }} else if (attempts < 18) {{
                        setTimeout(scrollWhenReady, 140);
                    }}
                }}
                scrollWhenReady();
            }}, 80);
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
                <div class="dd-muted-small">Virtual Tech AI is a Bangalore-based company providing AI and data solutions. This workspace manages proposals, approvals, delivery, resources, and updates.</div></div>
                <div class="dd-chip">AI Front Desk open</div>
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
                # Testing fix: start a fresh AI Front Desk chat after login.
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
                st.success(f"AI Front Desk: Identity verified. Welcome {user['employee_name']}.")
                st.rerun()
            else:
                st.error("AI Front Desk: Invalid employee ID or secret key.")

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
        st.caption("Use only when setting up Supabase or repairing workflow tables.")
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
            "AI Front Desk chat",
        ]
    elif role == "founder":
        options = [
            "Choose dashboard item...",
            "Executive update inbox",
            "All proposal board",
            "Live company performance",
            "AI Front Desk chat",
        ]
    elif role == "executive":
        options = [
            "Choose dashboard item...",
            "Executive update inbox",
            "All proposal board",
        ]
        if role_key == "operations":
            options.append("Technical Architect delivery workspace")
        options.append("AI Front Desk chat")
    else:
        options = ["Choose dashboard item...", "AI Front Desk chat"]

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

    dashboard_memory_key = f"_dd_last_dashboard_selection_{actor_id(user)}"
    previous_dashboard_selection = st.session_state.get(dashboard_memory_key)
    if (
        previous_dashboard_selection is not None
        and selected != previous_dashboard_selection
        and selected != "Choose dashboard item..."
    ):
        request_page_scroll("dashboard_result")
    st.session_state[dashboard_memory_key] = selected

    if selected == "Choose dashboard item...":
        st.info("Choose a dashboard item from the dropdown above.")
        return selected

    st.markdown('<div id="dd-dashboard-result"></div>', unsafe_allow_html=True)

    if selected == "My project workbench":
        render_employee_project_workbench(user)
    elif selected == "Executive update inbox":
        render_pending_proposal_notifications(user, data)
    elif selected == "All proposal board":
        render_all_proposals_board(user)
    elif selected == "Live company performance":
        render_company_performance_dashboard(data)
    elif selected == "Technical Architect delivery workspace":
        render_operations_delivery_workspace(user, data)
    elif selected == "AI Front Desk chat":
        # Keep logged-in Front Desk clean: the chat input remains available below
        # without an extra static instruction panel.
        pass

    run_pending_page_scroll()
    return selected


def auto_scroll_to_chat_response():
    """Scroll to the latest AI Front Desk answer after a real message is submitted."""
    request_page_scroll("frontdesk_answer")
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

# Keep AI Front Desk available for front-desk visitors and logged-in employees/executives.
# It is not shown inside the client portal. Normal dashboard/login clicks do not scroll here;
# chat scrolling is triggered only after a real chat message is submitted.
should_show_receptionist_chat = (
    st.session_state.client_user is None
)

if should_show_receptionist_chat:
    if st.session_state.user is None:
        st.divider()


    # ---------------- AI FRONT DESK CHAT ----------------

    if st.session_state.user is None:
        render_chat_intro()

        with st.expander("Sample prompts", expanded=False):
            st.markdown(
                """
                - `Company name is EduSmart, contact edu@example.com, we need an AI chatbot for students and staff with login, role-based access, document upload, FAQs, admin dashboard, reports, notifications, and cloud deployment. Budget 40 lakhs, timeline 8 months`
                - `Company name is DataNova, contact 9876543210, we need a data pipeline with API ingestion, ETL jobs, validation, PostgreSQL storage, dashboards, scheduled reports, alerts, and cloud deployment. Budget 15 lakhs, timeline 3 months`
                - `When will my salary be credited?`
                - `Why is my salary less this month?`
                - `Show company performance`
                """
            )

    if st.session_state.user is None:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
    else:
        render_ai_frontdesk_history_dropdown(st.session_state.messages)

    query = None if st.session_state.client_user else st.chat_input("Type your request to the AI Front Desk...")

    if query:
        st.session_state.messages.append({"role": "user", "content": query})

        with st.chat_message("user"):
            st.write(query)

        st.markdown('<div id="dd-frontdesk-latest-answer"></div>', unsafe_allow_html=True)
        with st.chat_message("assistant"):
            reply = handle_receptionist_query(query, st.session_state.user, data)

            st.write(reply["message"])

            if reply["type"] == "external_client_details_received":
                st.success("AI Front Desk: External client details received. Calling internal agents now...")

                client_query = reply.get("client_query", query)
                external_result = run_external_client_decision(client_query, data)
                report = save_latest_external_client_report(client_query, external_result)
                st.session_state.pending_client_proposal_text = ""

                if report.get("proposal_id"):
                    st.success(
                        "Your proposal has been received. Our internal LifecycleDesk AI meeting analysis is complete, "
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

                    st.subheader("Technical Architect AI Agent Risk Calculation")
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

                elif reply["agent"] == "Technical Architect AI Agent":
                    latest_report = get_latest_external_client_report()
                    if latest_report and any(x in query.lower() for x in ["client", "proposal", "latest", "requirement", "decision"]):
                        render_external_client_report(latest_report, user=st.session_state.user, compact=False)
                    else:
                        result = answer_with_sql_agent(query, st.session_state.user, data, "Technical Architect AI Agent")
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
