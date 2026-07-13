
def render_dynamic_skill_gap_table(analysis):
    """Render HR/Technical Architect skill-gap/capacity details safely.

    Some recent Technical Architect UI cleanup versions still call this function from the
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
        "🛠️ Technical Architect AI Agent",
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
        st.markdown("#### Technical Architect AI Agent basis")
        st.write(summaries.get("operations") or "Technical Architect summary unavailable.")
        o1, o2, o3 = st.columns(3)
        o1.metric("Requested Timeline", f"{analysis['timeline_months']} months")
        o2.metric("Timeline Risk", analysis["timeline_risk"])
        o3.metric("Resource Gap", f"{analysis['total_skill_gap']} FTE")
        st.caption("Technical Architect checks delivery feasibility, timeline risk, blockers, and dependency planning.")

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

    HR should never appear to recommend a quote/timeline. Technical Architect should never appear
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




def render_ceo_project_lifecycle_dashboard(report, user=None, data=None):
    """CEO lifecycle view after a proposal has moved into delivery.

    Once the client has accepted and Technical Architect has started/allocation exists,
    CEO should not see the old quotation-editing decision room. The quote stage
    is closed. CEO should see project delivery state, allocated internal team,
    and employee-side weekly progress/request status.
    """
    proposal_id = safe_text(report.get("proposal_id"))
    project = get_project_for_proposal(proposal_id)
    if not project:
        # Fallback to the proposal view if no live project exists yet.
        render_external_client_report(report, user=user, compact=False)
        return

    project_id = safe_text(project.get("project_id"))
    project_name = safe_text(project.get("project_name")) or project_id or "Accepted client project"
    plan = get_delivery_plan_for_client_project(project_id)
    allocations = get_project_allocations(project_id)
    all_updates = get_employee_project_updates(project_id=project_id)
    open_updates = get_open_employee_project_updates(project_id=project_id)

    st.markdown(
        """
        <div class="dd-section-card dd-dashboard-shell">
            <div class="dd-section-eyebrow">CEO lifecycle view</div>
            <div class="dd-section-title">Project is already kicked off</div>
            <div class="dd-section-subtitle">
                Quotation and executive decision stage is closed. This view focuses on live delivery,
                allocated internal team, and weekly progress from employees.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    client_response = safe_text(report.get("client_response"), "Accept Proposal")
    quote = report.get("ceo_final_quote") or report.get("recommended_quote") or report.get("analysis", {}).get("recommended_quote")
    timeline = report.get("ceo_final_timeline_months") or report.get("timeline_months") or report.get("analysis", {}).get("timeline_months")

    closed_updates = all_updates.copy() if all_updates is not None and not all_updates.empty else pd.DataFrame()
    if not closed_updates.empty and "operations_status" in closed_updates.columns:
        closed_updates = closed_updates[closed_updates["operations_status"].astype(str).str.lower().eq("closed")]
    progress_summary = get_client_safe_project_progress(project_id)

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Delivery status", safe_text(plan.get("approval_status") if plan else project.get("project_status"), "In progress"))
    c2.metric("Weekly progress", progress_summary.get("weekly_progress_percent") or "Not updated")
    c3.metric("Allocated employees", 0 if allocations.empty else len(allocations))
    c4.metric("Open blockers / requests", 0 if open_updates.empty else len(open_updates))
    c5.metric("Closed blockers / requests", 0 if closed_updates.empty else len(closed_updates))

    with st.expander("Commercial summary / latest quotation", expanded=False):
        q1, q2 = st.columns(2)
        q1.metric("Latest approved quotation", money_text(quote) if quote else "Available in quotation")
        q2.metric("Approved timeline", f"{safe_text(timeline)} month(s)" if safe_text(timeline) else "Available in quotation")
        quotation = safe_text(report.get("client_quotation"))
        if quotation:
            st.text_area("Latest quotation sent", value=quotation, height=180, disabled=True, key=f"ceo_live_quote_{proposal_id}")

    st.markdown("### Project delivery snapshot")
    st.markdown(
        f"""
        <div class="dd-project-card">
            <div class="dd-card-header-row">
                <div>
                    <div class="dd-card-kicker">Live project</div>
                    <div class="dd-card-title-small">{project_name}</div>
                    <div class="dd-card-subtle">Project ID: {project_id}</div>
                </div>
                <div class="dd-status-pill">Team work going on</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    req = safe_text(plan.get("raw_requirement_text") if plan else "")
    if req:
        with st.expander("Client requirement", expanded=False):
            st.text_area("Requirement provided by client", value=req, height=140, disabled=True, key=f"ceo_live_req_{project_id}")

    conclusion = safe_text(plan.get("operations_agent_plan") if plan else "")
    if conclusion:
        with st.expander("Technical Architect AI Agent conclusion", expanded=False):
            st.text_area("AI delivery analysis and conclusion", value=conclusion, height=180, disabled=True, key=f"ceo_live_ops_plan_{project_id}")

    st.markdown("### Allocated team and weekly progress")
    if allocations.empty:
        st.info("Technical Architect has not allocated employees to this project yet.")
    else:
        rows = []
        updates_by_emp = {}
        if all_updates is not None and not all_updates.empty:
            working_updates = all_updates.copy()
            if "created_at" in working_updates.columns:
                working_updates = working_updates.sort_values("created_at", ascending=False)
            for _, upd in working_updates.iterrows():
                emp_id = safe_text(upd.get("employee_id")).upper()
                if emp_id and emp_id not in updates_by_emp:
                    updates_by_emp[emp_id] = upd

        for _, alloc in allocations.iterrows():
            emp_id = safe_text(alloc.get("employee_id")).upper()
            upd = updates_by_emp.get(emp_id)
            operations_status = safe_text(upd.get("operations_status"), "Open") if upd is not None else "No update yet"
            rows.append({
                "Employee": safe_text(alloc.get("employee_name")),
                "Department": safe_text(alloc.get("employee_department")),
                "Project role": safe_text(alloc.get("project_role")),
                "Module / work area": safe_text(alloc.get("assigned_module")),
                "Latest weekly status": safe_text(upd.get("progress_status"), "No update yet") if upd is not None else "No update yet",
                "Weekly progress": (safe_text(upd.get("progress_percent")) + "%") if upd is not None and safe_text(upd.get("progress_percent")) else "Not updated",
                "Request status": operations_status,
                "Last update": safe_text(upd.get("created_at"), "") if upd is not None else "",
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    if all_updates is not None and not all_updates.empty:
        with st.expander("Employee blockers / request status", expanded=False):
            working = all_updates.copy()
            if "created_at" in working.columns:
                working = working.sort_values("created_at", ascending=False)
            visible = []
            for _, upd in working.iterrows():
                issue = safe_text(upd.get("support_needed")).strip() or safe_text(upd.get("hurdles")).strip() or safe_text(upd.get("notes")).strip() or "No blocker mentioned"
                visible.append({
                    "Received": safe_text(upd.get("created_at")),
                    "Employee": safe_text(upd.get("employee_name")),
                    "Status": safe_text(upd.get("progress_status")),
                    "Progress": (safe_text(upd.get("progress_percent")) + "%") if safe_text(upd.get("progress_percent")) else "",
                    "Module": safe_text(upd.get("assigned_module")),
                    "Blocker / request": issue,
                    "Technical Architect status": safe_text(upd.get("operations_status"), "Open"),
                })
            st.dataframe(pd.DataFrame(visible), use_container_width=True, hide_index=True)
    else:
        st.success("No employee blockers or requests recorded for this project.")

    st.caption("CEO can monitor delivery here. Quotation editing is disabled because the project has already moved into delivery.")

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
            "Technical Architect AI Agent Delivery Opinion",
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



def proposal_has_ceo_quote_sent(report):
    """True when CEO has already generated/sent the client quotation.

    After this point Sales/HR/Finance should not see department-decision input
    forms. The proposal decision stage is closed for non-CEO roles; they get a
    compact read-only lifecycle view instead.
    """
    if not isinstance(report, dict):
        return False
    return bool(
        safe_text(report.get("client_quotation")).strip()
        or safe_text(report.get("ceo_final_decision")).strip()
        or safe_text(report.get("ceo_decided_at")).strip()
        or safe_text(report.get("quotation_sent")).strip().lower() == "yes"
    )


def proposal_is_in_delivery_stage(report):
    """True when the accepted proposal has moved beyond quotation into delivery."""
    if not isinstance(report, dict):
        return False
    status_text = safe_text(report.get("workflow_status")).lower()
    return bool(
        safe_text(report.get("project_id")).strip()
        or safe_text(report.get("project_created")).strip().lower() == "yes"
        or "kickoff" in status_text
        or "delivery" in status_text
        or "team allocated" in status_text
        or get_project_for_proposal(report.get("proposal_id")) is not None
    )


def render_post_ceo_readonly_lifecycle_view(report, user=None, compact=False):
    """Compact dropdown-first view for Sales/HR/Finance after CEO quotation.

    This prevents long scrolling decision-room pages and prevents executives from
    submitting department opinions after CEO has already sent the quote. Each role
    sees only role-safe lifecycle status and optional details selected from one
    dropdown.
    """
    role_key = role_key_for_user(user) or "executive"
    analysis = report.get("analysis", {}) if isinstance(report, dict) else {}
    proposal_id = safe_text(report.get("proposal_id"))
    project = get_project_for_proposal(proposal_id)
    project_id = safe_text(project.get("project_id") if project else report.get("project_id"))
    plan = get_delivery_plan_for_client_project(project_id) if project_id else {}
    allocations = get_project_allocations(project_id) if project_id else pd.DataFrame()
    updates = get_employee_project_updates(project_id=project_id) if project_id else pd.DataFrame()
    open_updates = get_open_employee_project_updates(project_id=project_id) if project_id else pd.DataFrame()

    role_titles = {
        "sales": "Sales lifecycle status",
        "finance": "Finance lifecycle status",
        "hr": "HR resource lifecycle status",
    }
    role_subtitles = {
        "sales": "CEO quotation has already been sent. Sales can view quotation and client status; decision inputs are closed.",
        "finance": "CEO quotation has already been sent. Finance can view commercial status; decision inputs are closed.",
        "hr": "CEO quotation has already been sent. HR can view resource/allocation status; decision inputs are closed.",
    }

    st.markdown(
        f"""
        <div class=\"dd-section-card dd-dashboard-shell\">
            <div class=\"dd-section-eyebrow\">Read-only lifecycle view</div>
            <div class=\"dd-section-title\">{role_titles.get(role_key, 'Lifecycle status')}</div>
            <div class=\"dd-section-subtitle\">{role_subtitles.get(role_key, 'CEO quotation is already sent. This is now a read-only lifecycle status view.')}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    quote = report.get("ceo_final_quote") or report.get("recommended_quote") or analysis.get("recommended_quote")
    timeline = report.get("ceo_final_timeline_months") or report.get("timeline_months") or analysis.get("timeline_months")
    client_response = safe_text(report.get("client_response"), "Awaiting client response")
    delivery_status = safe_text(plan.get("approval_status") if isinstance(plan, dict) else "") or safe_text(project.get("project_status") if project else "") or safe_text(report.get("workflow_status"), "Quotation sent")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Latest quote", money_text(quote) if quote else "Available")
    m2.metric("Timeline", f"{safe_text(timeline)} month(s)" if safe_text(timeline) else "Available")
    m3.metric("Client status", client_response or "Awaiting response")
    m4.metric("Delivery status", delivery_status)

    if project_id:
        st.caption(f"Project: {project_display_name(project=project or {}, project_id=project_id)}")

    if role_key == "hr":
        h1, h2 = st.columns(2)
        h1.metric("Allocated employees", 0 if allocations.empty else len(allocations))
        h2.metric("Open employee requests", 0 if open_updates.empty else len(open_updates))
    elif role_key in ["sales", "finance"]:
        st.caption("Team and employee-level delivery details are handled by Technical Architect/HR. This view keeps your dashboard compact and role-safe.")

    detail_options = ["Overview"]
    if safe_text(report.get("client_quotation")).strip():
        detail_options.append("Latest quotation sent")
    if role_key == "hr" and not allocations.empty:
        detail_options.append("Allocated resource view")
    if role_key == "hr" and updates is not None and not updates.empty:
        detail_options.append("Employee weekly progress")
    detail_options.append("Proposal audit summary")

    selected = st.selectbox(
        "Choose what to view",
        detail_options,
        key=f"post_ceo_detail_{proposal_id}_{role_key}",
    )

    if selected == "Overview":
        st.info("The proposal decision stage is closed because CEO quotation has already been sent. No department decision is needed now.")
        if proposal_is_in_delivery_stage(report):
            st.success("Project delivery has started. Use the role-specific details dropdown only if you need more information.")
        else:
            st.caption("Awaiting client response or delivery kickoff.")

    elif selected == "Latest quotation sent":
        st.text_area(
            "Latest client quotation",
            value=safe_text(report.get("client_quotation")),
            height=220,
            disabled=True,
            key=f"post_ceo_quote_{proposal_id}_{role_key}",
        )

    elif selected == "Allocated resource view":
        rows = []
        for _, alloc in allocations.iterrows():
            rows.append({
                "Employee": safe_text(alloc.get("employee_name")),
                "Department": safe_text(alloc.get("employee_department")),
                "Project role": safe_text(alloc.get("project_role")),
                "Module / work area": safe_text(alloc.get("assigned_module")),
                "Allocation %": safe_text(alloc.get("allocation_percent")),
                "Status": safe_text(alloc.get("allocation_status"), "Active"),
            })
        if rows:
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        else:
            st.info("No allocated employees found for this project yet.")

    elif selected == "Employee weekly progress":
        working = updates.copy() if updates is not None and not updates.empty else pd.DataFrame()
        if working.empty:
            st.info("No employee weekly updates submitted yet.")
        else:
            if "created_at" in working.columns:
                working = working.sort_values("created_at", ascending=False)
            rows = []
            for _, upd in working.iterrows():
                rows.append({
                    "Updated": safe_text(upd.get("created_at")),
                    "Employee": safe_text(upd.get("employee_name")),
                    "Status": safe_text(upd.get("progress_status")),
                    "Weekly progress": (safe_text(upd.get("progress_percent")) + "%") if safe_text(upd.get("progress_percent")) else "",
                    "Module": safe_text(upd.get("assigned_module")),
                    "Request status": safe_text(upd.get("operations_status"), "Open"),
                })
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    elif selected == "Proposal audit summary":
        rows = []
        for dept_key, label in PROPOSAL_DEPARTMENT_LABELS.items():
            item = report.get("decisions", {}).get(dept_key, {})
            rows.append({
                "Department": label,
                "Decision": item.get("decision") or "Not required after CEO quote",
                "By": item.get("decided_by") or "",
                "Updated At": item.get("decided_at") or "",
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        st.caption("This audit summary is read-only. Use the inbox only for active items.")

def render_external_client_report(report, user=None, compact=False):
    analysis = report["analysis"]
    role_key = role_key_for_user(user)
    if (
        not compact
        and role_key in ["sales", "finance", "hr"]
        and proposal_has_ceo_quote_sent(report)
    ):
        render_post_ceo_readonly_lifecycle_view(report, user=user, compact=compact)
        return

    st.markdown(
        """
        <div class="dd-section-card">
            <div class="dd-section-title">Client proposal decision room</div>
            <div class="dd-section-subtitle">
                Shared view for Sales, HR, Technical Architect, Finance, and CEO. Agent analysis is generated first; human executives then review and approve.
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
        linked_project = get_project_for_proposal(report.get("proposal_id"))
        project_label = project_display_name(
            project=linked_project or {},
            project_id=report.get("project_id"),
            proposal_id=report.get("proposal_id"),
            fallback=analysis.get("project_type", "Project"),
        )
        label = (
            f"{idx}. {updated} | {project_label} | {report.get('workflow_status', 'Pending')} | "
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
                "Project": project_display_name(project=get_project_for_proposal(report.get("proposal_id")) or {}, project_id=report.get("project_id"), proposal_id=report.get("proposal_id"), fallback=analysis.get("project_type")),
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
            or safe_text(selected_report.get("project_created")).strip().lower() == "yes"
            or "delivery" in safe_text(selected_report.get("workflow_status")).lower()
            or "kickoff" in safe_text(selected_report.get("workflow_status")).lower()
            or "team allocated" in safe_text(selected_report.get("workflow_status")).lower()
            or get_project_for_proposal(selected_report.get("proposal_id")) is not None
        )
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
        st.info("This is now a delivery-readiness item, not a department-decision item. Old Sales/Finance/HR/CEO review details are hidden.")
        render_operations_delivery_workspace(user, data or {}, focus_proposal_id=selected_report.get("proposal_id"))
    elif is_ceo_live_project_item:
        render_ceo_project_lifecycle_dashboard(selected_report, user=user, data=data or {})
    else:
        render_external_client_report(selected_report, user=user, compact=False)

    # The old "mark reviewed without decision" shortcut is intentionally removed.
    # Executives should either submit/update their role opinion or leave the item
    # visible in the inbox until a real action is taken.


def render_all_proposals_board(user):
    if role_key_for_user(user) is None:
        return
    with st.expander("Proposal audit overview", expanded=False):
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
                "Technical Architect": report.get("decisions", {}).get("operations", {}).get("decision") or "Pending",
                "CEO Final": report.get("decisions", {}).get("ceo", {}).get("decision") or "Pending",
                "Quote Sent": report.get("quotation_sent", "No"),
                "Last Updated": report.get("last_updated_at"),
            })
        board = pd.DataFrame(rows)
        st.dataframe(board, use_container_width=True, hide_index=True)
        st.caption("Read-only overview of proposal decisions, quotations, and client responses. Use the update inbox above for active action items.")


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
