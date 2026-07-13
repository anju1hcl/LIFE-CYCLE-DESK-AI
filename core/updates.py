from core.auth import role_name
from core.calculations import calculate_attendance_summary, calculate_lop_details, calculate_salary_after_lop, calculate_company_performance, calculate_project_profitability, calculate_operations_risk


def user_specific_updates(user: dict, data: dict) -> list[str]:
    role = role_name(user)
    emp_id = user["user_id"]
    updates = []

    if role == "Founder":
        perf = calculate_company_performance(data)
        updates.append(f"CEO Update: Company health is {perf['company_health']} with {perf['company_margin_percent']}% margin.")
        if perf["high_risk_projects"]:
            updates.append(f"CEO Update: {perf['high_risk_projects']} project(s) need delivery attention.")
        updates.append("CEO Update: New proposal workflow is ready for approval decisions.")

    elif role == "HR Executive":
        lop = calculate_lop_details(data["attendance"])
        pending_lop = lop[lop["lop_flag"] == "Yes"]
        onboarding = data["onboarding"]
        pending_onboarding = onboarding[onboarding["onboarding_status"] != "Completed"]
        updates.append(f"HR Update: {len(pending_lop)} LOP/absence records need review.")
        updates.append(f"HR Update: {len(pending_onboarding)} new joinee onboarding record(s) are pending.")

    elif role == "Finance Executive":
        salary_impact = calculate_salary_after_lop(data["payroll"], data["attendance"])
        deductions = salary_impact["lop_deduction"].sum() if not salary_impact.empty else 0
        profitability = calculate_project_profitability(data["projects"], data["assignments"], data["payroll"], data["expenses"])
        updates.append(f"Finance Update: Total LOP deduction impact this period is INR {round(deductions, 2)}.")
        updates.append(f"Finance Update: {len(profitability)} active project profitability records are ready for review.")

    elif role == "Operations Executive":
        risks = calculate_operations_risk(data["projects"], data["assignments"])
        high = risks[risks["risk_level"] == "High"]
        updates.append(f"Operations Update: {len(high)} high-risk project(s) found.")
        updates.append("Operations Update: Employee bandwidth and blockers are ready for review.")

    elif role == "Sales Executive":
        leads = data["leads"]
        new_leads = leads[leads["status"].isin(["New", "Qualified", "Proposal Sent"])]
        updates.append(f"Sales Update: {len(new_leads)} open lead(s) need follow-up.")
        updates.append("Sales Update: New proposal workflow can generate price and CEO decision instantly.")

    elif role == "New Joinee":
        onboarding = data["onboarding"]
        rec = onboarding[onboarding["employee_id"] == emp_id]
        if not rec.empty:
            row = rec.iloc[0]
            if row["forms_submitted"] != "Yes":
                updates.append("HR Update: Your onboarding forms are still pending.")
            if row["virtual_id_created"] != "Yes":
                updates.append("HR Update: Your virtual ID card is not created yet.")
            if row["laptop_issued"] != "Yes":
                updates.append("HR Update: Your laptop is not yet issued.")

    elif role == "Employee":
        my_assignments = data["assignments"][data["assignments"]["employee_id"] == emp_id]
        for _, a in my_assignments.iterrows():
            project = data["projects"][data["projects"]["project_id"] == a["project_id"]]
            if not project.empty:
                p = project.iloc[0]
                if p["actual_progress"] < p["expected_progress"]:
                    updates.append(f"Operations Update: {p['project_name']} is behind schedule. Please report blockers if any.")
        my_att = calculate_attendance_summary(data["attendance"], emp_id)
        if not my_att.empty and (my_att["attendance_percent"] < 90).any():
            updates.append("HR Update: Your attendance is below 90% in at least one month.")

    elif role == "External Client":
        client = data["clients"][data["clients"]["client_user_id"] == emp_id]
        if not client.empty:
            client_id = client.iloc[0]["client_id"]
            projects = data["projects"][data["projects"]["client_id"] == client_id]
            updates.append(f"Client Update: {len(projects)} project(s) are visible in your workspace.")

    if not updates:
        updates.append("No pending HR or operational updates. Have a good day.")
    return updates
