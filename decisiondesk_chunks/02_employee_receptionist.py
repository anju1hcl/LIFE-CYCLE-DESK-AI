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
                f"Technical Architect Update: You are assigned to {p['project_name']} "
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
    external proposal is analysed, the Technical Architect/HR capacity calculation should
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


@st.cache_data(ttl=DYNAMIC_CAPACITY_CACHE_TTL_SECONDS, show_spinner=False)
def read_dynamic_capacity_sources():
    """Read live Supabase workload tables for HR/Technical Architect capacity analysis.

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


def build_live_project_capacity_snapshot(sources=None, limit=8):
    """Small readable snapshot used by HR/Technical Architect before suggesting hiring.

    It looks at live Supabase projects, allocations, delivery plans, and latest
    employee updates to describe which projects are consuming capacity, when they
    started, timeline/release expectation, and how much work is still pending.
    """
    sources = sources or read_dynamic_capacity_sources()
    projects = sources.get("projects", pd.DataFrame())
    allocations = sources.get("allocations", pd.DataFrame())
    updates = sources.get("employee_updates", pd.DataFrame())
    timeline_by_proposal = sources.get("timeline_by_proposal", {}) or {}
    if projects is None or projects.empty:
        return []

    latest_updates = _latest_employee_update_map(updates)
    rows = []
    for _, project in projects.iterrows():
        project_id = safe_text(project.get("project_id"))
        proposal_id = safe_text(project.get("proposal_id"))
        project_name = safe_text(project.get("project_name")) or project_id
        start_date = safe_text(project.get("kickoff_date")) or safe_text(project.get("created_at"))
        timeline = timeline_by_proposal.get(proposal_id.upper(), "") or timeline_by_proposal.get(proposal_id, "")
        project_allocs = pd.DataFrame()
        if allocations is not None and not allocations.empty and "project_id" in allocations.columns:
            project_allocs = allocations[allocations["project_id"].astype(str) == project_id]

        progress_values = []
        open_requests = 0
        if not project_allocs.empty:
            for _, alloc in project_allocs.iterrows():
                emp_id = safe_text(alloc.get("employee_id")).upper()
                latest = latest_updates.get((project_id.upper(), emp_id), {})
                progress = safe_number(latest.get("progress_percent"), 0)
                if progress:
                    progress_values.append(max(0, min(100, progress)))
                status = safe_text(latest.get("operations_status") or "Open").lower()
                hurdle_text = " ".join([safe_text(latest.get("hurdles")), safe_text(latest.get("support_needed")), safe_text(latest.get("notes"))]).strip()
                if hurdle_text and status != "closed":
                    open_requests += 1

        avg_progress = round(sum(progress_values) / len(progress_values), 1) if progress_values else 0
        pending_percent = round(max(0, 100 - avg_progress), 1) if progress_values else "Unknown"
        rows.append({
            "project_id": project_id,
            "project_name": project_name,
            "started_at": start_date,
            "timeline_months": timeline,
            "allocated_people": int(len(project_allocs)) if not project_allocs.empty else 0,
            "latest_progress_percent": avg_progress if progress_values else "No weekly update yet",
            "pending_percent": pending_percent,
            "open_requests": open_requests,
        })

    def sort_key(item):
        return safe_text(item.get("started_at"))
    return sorted(rows, key=sort_key, reverse=True)[:limit]


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
    """Summarise live/projected capacity by role for HR and Technical Architect."""
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
    live_project_snapshot = build_live_project_capacity_snapshot(limit=8)

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
        "capacity_basis": "Excel employee master/payroll + Supabase current projects, project start/timeline, project_allocations, delivery_plans, weekly progress, pending work, and open employee requests.",
        "live_project_capacity_snapshot": live_project_snapshot,

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

# ---------------- AI FRONT DESK ----------------

# 
def is_simple_greeting_query(query):
    """Return True for plain greetings so AI Front Desk does not over-route.

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
#                 "AI Front Desk: Thank you for sharing the project details. "
#                 "I am calling Sales, HR, Technical Architect, Finance, and CEO Agents for an internal feasibility check."
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
#                     "AI Front Desk: Welcome to Virtual Tech AI. "
#                     "I can help with your project enquiry. Please share your company name, industry, "
#                     "project requirement, expected budget, urgency, and contact details."
#                 ),
#             }

#         return {
#             "type": "general",
#             "message": (
#                 "AI Front Desk: Welcome to Virtual Tech AI. "
#                 "You can login as an employee, executive, or founder. "
#                 "If you are a client, you can tell me about your project requirement."
#             ),
#         }

#     if any(k in q for k in ["salary", "inhand", "in-hand", "pay", "credited", "salary date"]):
#         return {
#             "type": "text",
#             "message": "AI Front Desk: Connecting you to Finance Agent.\n\n"
#             + get_employee_salary_info(user, data),
#         }

#     if is_project_proposal_query(query):
#         lead_id = detect_lead_id(query)

#         if lead_id is None:
#             return {
#                 "type": "text",
#                 "message": (
#                     "AI Front Desk: I understand this is a project proposal request. "
#                     "Please mention the lead ID, for example L001, L002, or L003."
#                 ),
#             }

#         return {
#             "type": "proposal_workflow",
#             "lead_id": lead_id,
#             "message": (
#                 f"AI Front Desk: Lead {lead_id} detected. "
#                 "Starting internal AI decision meeting with Sales, HR, Technical Architect, Finance, and CEO Agents."
#             ),
#         }

#     if any(k in q for k in ["company health", "business performance", "company performance"]):
#         if user["role"] == "founder":
#             return {
#                 "type": "company_health",
#                 "message": "AI Front Desk: Connecting you to CEO Agent for company performance analysis.",
#             }

#         return {
#             "type": "text",
#             "message": "AI Front Desk: Company performance reports require Founder/CEO access.",
#         }

#     agent = receptionist_route(query)

#     return {
#         "type": "route_agent",
#         "agent": agent,
#         "message": f"AI Front Desk: Connecting you to {agent}.",
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
    """Return True for plain greetings so AI Front Desk does not over-route.

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
    AI Front Desk routes the user to the right agent.

    Important product reliability rule:
    Use deterministic routing for high-value product flows first, then use the LLM
    receptionist as a fallback. This prevents simple asks like
    "salary of the data engineer" from dying in the generic AI Front Desk fallback.
    """

    q = query.lower().strip()

    if is_simple_greeting_query(query):
        name = actor_name(user) if user else "there"
        return {
            "type": "general",
            "agent": "AI Front Desk",
            "intent": "greeting",
            "confidence": 1.0,
            "message": f"AI Front Desk: Hello {name}. Hope you are doing good today. How can I help you?",
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
                    "AI Front Desk: Company performance reports are internal company data. "
                    "Please login first so I can verify your access."
                ),
            }
        if user.get("role") == "founder":
            return {
                "type": "company_health",
                "agent": "CEO Agent",
                "intent": "company_performance",
                "message": "AI Front Desk: Connecting you to CEO Agent for company performance analysis.",
            }
        return {
            "type": "text",
            "agent": "CEO Agent",
            "intent": "company_performance",
            "message": "AI Front Desk: Company performance reports require Founder/CEO access.",
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
                    "AI Front Desk: Thank you for sharing the complete project details. "
                    "I am calling Sales, HR, Technical Architect, Finance, and CEO Agents "
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

    # 3. Do not use old lead-ID routing for the client intake workflow.
    # Any proposal-like message, even if it mentions L001/L002/L003, should be treated
    # as a new client enquiry and processed through the external-client decision room.

    # 4. Salary/payroll is a core product path, so do not leave it only to the LLM router.
    if user is not None and is_salary_related_query(query):
        return {
            "type": "route_agent",
            "agent": "Finance Agent",
            "intent": "role_salary_lookup" if is_role_salary_query(query) else "salary_info",
            "confidence": 1.0,
            "message": "AI Front Desk: Connecting you to Finance Agent.",
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
                    "AI Front Desk: Thank you. I found the company details, contact, project requirement, budget, and timeline. "
                    "I am calling Sales, HR, Technical Architect, Finance, and CEO Agents for feasibility analysis."
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

    # 6. Logged-in sales/CEO users may also enter a brand-new client requirement.
    if user is not None and looks_like_external_project:
        if is_complete_client_proposal(query):
            return {
                "type": "external_client_details_received",
                "agent": "Sales Agent",
                "intent": "external_client_details_received",
                "client_query": query,
                "message": (
                    "AI Front Desk: New client requirement detected with company/contact details. "
                    "Calling Sales, HR, Technical Architect, Finance, and CEO Agents for feasibility analysis."
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

    # 7. Ask the LLM AI Front Desk after deterministic critical routes.
    try:
        understood = receptionist_understand(query, user)
    except Exception as e:
        understood = {
            "agent": "AI Front Desk",
            "intent": "unknown",
            "confidence": 0.0,
            "reason": f"AI Front Desk understanding failed: {e}",
        }

    agent = understood.get("agent", "AI Front Desk")
    if agent in ["Operations Agent", "Operations", "Operations Executive", "Operations Manager", "Technical Architect", "Technical Architect Agent"]:
        agent = "Technical Architect Agent"
    if agent == "Receptionist":
        agent = "AI Front Desk"
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
                    "AI Front Desk: Welcome to Virtual Tech AI. "
                    "I understand you have a project requirement. Please share company name, industry, budget, timeline, urgency, and contact details."
                ),
            }

        if agent in ["HR Agent", "Finance Agent", "Technical Architect Agent", "CEO Agent"] or is_salary_related_query(query):
            return {
                "type": "login_required",
                "agent": agent if agent != "AI Front Desk" else "Finance Agent",
                "intent": intent,
                "message": (
                    "AI Front Desk: This is an internal company-data request. "
                    "Please login first so I can verify your access."
                ),
            }

        return {
            "type": "general",
            "agent": "AI Front Desk",
            "intent": intent,
            "confidence": confidence,
            "message": (
                "AI Front Desk: Welcome to Virtual Tech AI. You can login as an employee, executive, or founder. "
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
                "AI Front Desk: This looks like a new client project enquiry. "
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
                "message": "AI Front Desk: Connecting you to CEO Agent for company performance analysis.",
            }

        return {
            "type": "text",
            "agent": "CEO Agent",
            "intent": intent,
            "message": "AI Front Desk: Company performance reports require Founder/CEO access.",
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
                "AI Front Desk: I understand this is a project decision request. "
                "Please provide the full new-client requirement with project type, budget, and timeline so I can start the multi-agent decision room."
            ),
        }

    # 12. Normal agent route.
    if agent in ["HR Agent", "Finance Agent", "Technical Architect Agent", "Sales Agent", "CEO Agent"]:
        return {
            "type": "route_agent",
            "agent": agent,
            "intent": intent,
            "confidence": confidence,
            "message": f"AI Front Desk: Connecting you to {agent}.",
        }

    # 13. Last-resort deterministic fallback.
    if is_salary_related_query(query):
        return {
            "type": "route_agent",
            "agent": "Finance Agent",
            "intent": "role_salary_lookup" if is_role_salary_query(query) else "salary_info",
            "confidence": 1.0,
            "message": "AI Front Desk: Connecting you to Finance Agent.",
        }

    return {
        "type": "general",
        "agent": "AI Front Desk",
        "intent": intent,
        "confidence": confidence,
        "message": (
            "AI Front Desk: I can help route you to HR, Finance, Technical Architect, Sales, "
            "or CEO Agent. Please tell me what you need."
        ),
    }
