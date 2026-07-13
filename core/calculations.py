# import pandas as pd


# def money(value):
#     return round(float(value), 2)


# def calculate_attendance_summary(attendance: pd.DataFrame, employee_id: str | None = None) -> pd.DataFrame:
#     df = attendance.copy()
#     if employee_id:
#         df = df[df["employee_id"] == employee_id]

#     grouped = df.groupby(["employee_id", "month"]).agg(
#         working_days=("day_type", lambda x: (x == "Working Day").sum()),
#         present_days=("attendance_status", lambda x: (x == "Present").sum()),
#         leave_days=("attendance_status", lambda x: (x == "Leave").sum()),
#         absent_days=("attendance_status", lambda x: (x == "Absent").sum()),
#         lop_days=("lop_flag", lambda x: (x == "Yes").sum()),
#         total_hours=("hours_worked", "sum"),
#     ).reset_index()
#     grouped["attendance_percent"] = (grouped["present_days"] / grouped["working_days"] * 100).round(2)
#     return grouped


# def calculate_lop_details(attendance: pd.DataFrame, employee_id: str | None = None) -> pd.DataFrame:
#     df = attendance.copy()
#     if employee_id:
#         df = df[df["employee_id"] == employee_id]

#     lop = df[(df["attendance_status"].isin(["Leave", "Absent"])) | (df["lop_flag"] == "Yes")].copy()
#     if lop.empty:
#         return pd.DataFrame(columns=["employee_id", "attendance_date", "month", "attendance_status", "leave_applied", "approval_status", "lop_flag", "lop_reason"])

#     def reason(row):
#         if row["lop_flag"] == "No":
#             return "Approved leave / no LOP"
#         if row["leave_applied"] == "No":
#             return "LOP because leave was not applied"
#         if str(row["approval_status"]).lower() in ["rejected", "pending"]:
#             return f"LOP because leave approval is {row['approval_status']}"
#         return "LOP marked by HR policy"

#     lop["lop_reason"] = lop.apply(reason, axis=1)
#     return lop[["employee_id", "attendance_date", "month", "attendance_status", "leave_applied", "leave_type", "approval_status", "lop_flag", "approved_by", "lop_reason"]]


# def calculate_salary_after_lop(payroll: pd.DataFrame, attendance: pd.DataFrame, employee_id: str | None = None) -> pd.DataFrame:
#     summary = calculate_attendance_summary(attendance, employee_id)
#     results = []
#     for _, row in summary.iterrows():
#         pay = payroll[payroll["employee_id"] == row["employee_id"]]
#         if pay.empty:
#             continue
#         p = pay.iloc[0]
#         per_day_salary = p["gross_salary"] / 30
#         lop_deduction = per_day_salary * row["lop_days"]
#         final_net_salary = p["net_salary"] - lop_deduction
#         results.append({
#             "employee_id": row["employee_id"],
#             "month": row["month"],
#             "gross_salary": money(p["gross_salary"]),
#             "net_salary_before_lop": money(p["net_salary"]),
#             "lop_days": int(row["lop_days"]),
#             "lop_deduction": money(lop_deduction),
#             "final_net_salary": money(final_net_salary),
#         })
#     return pd.DataFrame(results)


# def calculate_skill_gap(employees: pd.DataFrame, requirements: pd.DataFrame, project_type: str) -> pd.DataFrame:
#     req = requirements[requirements["project_type"].str.lower() == str(project_type).lower()]
#     results = []
#     for _, r in req.iterrows():
#         role = r["required_role"]
#         available = employees[(employees["designation"] == role) & (employees["current_status"] == "Active")]
#         available_capacity = available["availability_percent"].sum() / 100
#         required_people = float(r["required_people"])
#         gap = max(0, required_people - available_capacity)
#         avg_salary = employees.loc[employees["designation"] == role, "monthly_ctc"].mean()
#         if pd.isna(avg_salary):
#             avg_salary = 120000
#         hiring_cost = gap * avg_salary * float(r["estimated_months"])
#         results.append({
#             "required_role": role,
#             "required_skill": r["required_skill"],
#             "required_people": required_people,
#             "available_capacity": round(available_capacity, 2),
#             "skill_gap": round(gap, 2),
#             "estimated_hiring_cost": money(hiring_cost),
#         })
#     return pd.DataFrame(results)


# def calculate_project_finance(employees: pd.DataFrame, requirements: pd.DataFrame, project_type: str, target_margin: float = 0.40) -> dict:
#     req = requirements[requirements["project_type"].str.lower() == str(project_type).lower()]
#     duration = int(req["estimated_months"].max()) if not req.empty else 3
#     employee_cost = 0.0
#     for _, r in req.iterrows():
#         role = r["required_role"]
#         avg_salary = employees.loc[employees["designation"] == role, "monthly_ctc"].mean()
#         if pd.isna(avg_salary):
#             avg_salary = 120000
#         employee_cost += avg_salary * float(r["required_people"]) * duration
#     overhead_cost = employee_cost * 0.20
#     cloud_cost = employee_cost * 0.10
#     total_cost = employee_cost + overhead_cost + cloud_cost
#     recommended_quote = total_cost / (1 - target_margin)
#     profit = recommended_quote - total_cost
#     return {
#         "duration_months": duration,
#         "employee_cost": money(employee_cost),
#         "overhead_cost": money(overhead_cost),
#         "cloud_cost": money(cloud_cost),
#         "total_project_cost": money(total_cost),
#         "recommended_quote": money(recommended_quote),
#         "expected_profit": money(profit),
#         "profit_margin_percent": round((profit / recommended_quote) * 100, 2) if recommended_quote else 0,
#     }


# def calculate_sales_score(lead: pd.Series) -> dict:
#     score = 0
#     budget = float(lead["expected_budget"])
#     score += 25 if budget >= 7000000 else 15 if budget >= 5000000 else 8
#     score += 20 if lead["urgency"] == "High" else 10 if lead["urgency"] == "Medium" else 5
#     score += 20 if lead["existing_client"] == "Yes" else 5
#     score += 20 if lead["competition_level"] == "Low" else 10 if lead["competition_level"] == "Medium" else -10
#     score = max(0, min(score, 100))
#     return {
#         "lead_score": score,
#         "win_probability_percent": score,
#         "expected_budget": money(budget),
#         "expected_revenue_weighted": money(budget * score / 100),
#     }


# def calculate_operations_risk(projects: pd.DataFrame, assignments: pd.DataFrame) -> pd.DataFrame:
#     results = []
#     for _, p in projects.iterrows():
#         project_assignments = assignments[assignments["project_id"] == p["project_id"]]
#         avg_bandwidth = project_assignments["allocation_percent"].mean()
#         if pd.isna(avg_bandwidth):
#             avg_bandwidth = 0
#         progress_gap = max(0, float(p["expected_progress"]) - float(p["actual_progress"]))
#         timeline_risk = min(progress_gap, 25)
#         bandwidth_risk = 25 if avg_bandwidth >= 80 else 15 if avg_bandwidth >= 60 else 5
#         risk_score = timeline_risk + bandwidth_risk
#         risk_level = "High" if risk_score >= 45 else "Medium" if risk_score >= 25 else "Low"
#         results.append({
#             "project_id": p["project_id"],
#             "project_name": p["project_name"],
#             "expected_progress": p["expected_progress"],
#             "actual_progress": p["actual_progress"],
#             "progress_gap": progress_gap,
#             "average_bandwidth": round(avg_bandwidth, 2),
#             "operations_risk_score": round(risk_score, 2),
#             "risk_level": risk_level,
#         })
#     return pd.DataFrame(results)


# def calculate_project_profitability(projects: pd.DataFrame, assignments: pd.DataFrame, payroll: pd.DataFrame, expenses: pd.DataFrame) -> pd.DataFrame:
#     rows = []
#     monthly_expense = expenses["monthly_cost"].sum()
#     for _, p in projects.iterrows():
#         assigned = assignments[assignments["project_id"] == p["project_id"]]
#         employee_cost = 0.0
#         for _, a in assigned.iterrows():
#             pay = payroll[payroll["employee_id"] == a["employee_id"]]
#             if pay.empty:
#                 continue
#             employee_cost += float(pay.iloc[0]["gross_salary"]) * (float(a["allocation_percent"]) / 100) * float(p["estimated_duration_months"])
#         overhead = employee_cost * 0.20
#         allocated_expense = monthly_expense * float(p["estimated_duration_months"]) * 0.10
#         total_cost = employee_cost + overhead + allocated_expense
#         profit = float(p["project_value"]) - total_cost
#         margin = profit / float(p["project_value"]) if p["project_value"] else 0
#         rows.append({
#             "project_id": p["project_id"],
#             "project_name": p["project_name"],
#             "project_value": money(p["project_value"]),
#             "employee_cost": money(employee_cost),
#             "overhead_cost": money(overhead),
#             "allocated_company_expense": money(allocated_expense),
#             "total_project_cost": money(total_cost),
#             "profit": money(profit),
#             "profit_margin_percent": round(margin * 100, 2),
#         })
#     return pd.DataFrame(rows)


# def calculate_company_performance(data: dict) -> dict:
#     profitability = calculate_project_profitability(data["projects"], data["assignments"], data["payroll"], data["expenses"])
#     risks = calculate_operations_risk(data["projects"], data["assignments"])
#     total_revenue = float(data["projects"]["project_value"].sum())
#     total_cost = float(profitability["total_project_cost"].sum())
#     total_profit = float(profitability["profit"].sum())
#     margin = total_profit / total_revenue if total_revenue else 0
#     high_risk = int((risks["risk_level"] == "High").sum())
#     avg_util = float(data["assignments"]["allocation_percent"].mean())
#     available_people = int((data["employees"]["availability_percent"] >= 50).sum())
#     if margin >= 0.35 and high_risk == 0:
#         health = "Strong"
#     elif margin >= 0.25:
#         health = "Moderate"
#     else:
#         health = "Needs Attention"
#     return {
#         "total_revenue": money(total_revenue),
#         "total_cost": money(total_cost),
#         "total_profit": money(total_profit),
#         "company_margin_percent": round(margin * 100, 2),
#         "average_utilization_percent": round(avg_util, 2),
#         "active_projects": int((data["projects"]["status"] == "Active").sum()),
#         "high_risk_projects": high_risk,
#         "available_people": available_people,
#         "company_health": health,
#     }

import pandas as pd


# ---------------- HR CALCULATIONS ----------------

def calculate_lop(attendance: pd.DataFrame) -> pd.DataFrame:
    results = []

    for _, row in attendance.iterrows():
        leave_days = row.get("leave_days", 0)
        leave_applied = row.get("leave_applied", "No")
        leave_approved = row.get("leave_approved", "No")

        if leave_days > 0 and leave_applied == "No":
            lop_days = leave_days
            reason = "Leave not applied"
        elif leave_days > 0 and leave_applied == "Yes" and leave_approved == "No":
            lop_days = leave_days
            reason = "Leave not approved"
        else:
            lop_days = 0
            reason = "No LOP"

        results.append({
            "employee_id": row["employee_id"],
            "month": row["month"],
            "working_days": row.get("working_days", 0),
            "present_days": row.get("present_days", 0),
            "leave_days": leave_days,
            "leave_applied": leave_applied,
            "leave_approved": leave_approved,
            "lop_days": lop_days,
            "lop_reason": reason,
        })

    return pd.DataFrame(results)


def calculate_attendance_summary(attendance: pd.DataFrame, employee_id=None) -> pd.DataFrame:
    df = attendance.copy()

    if employee_id:
        df = df[df["employee_id"].astype(str).str.upper() == str(employee_id).upper()]

    summary = df.groupby("employee_id").agg({
        "attendance_percent": "mean",
        "leave_days": "sum",
        "present_days": "sum",
        "working_days": "sum",
    }).reset_index()

    summary["attendance_score"] = summary["attendance_percent"].apply(
        lambda x: "Good" if x >= 90 else "Warning" if x >= 80 else "Critical"
    )

    summary["attendance_percent"] = summary["attendance_percent"].round(2)

    return summary


def calculate_skill_gap(employees: pd.DataFrame, requirements: pd.DataFrame, project_type: str) -> pd.DataFrame:
    req = requirements[requirements["project_type"] == project_type]
    results = []

    for _, row in req.iterrows():
        role = row["required_role"]
        required_people = float(row["required_people"])
        duration = float(row["estimated_months"])

        available = employees[
            (employees["designation"] == role) &
            (employees["availability_percent"] >= 30)
        ]

        available_capacity = available["availability_percent"].sum() / 100
        gap = max(0, required_people - available_capacity)

        salary_match = employees[employees["designation"] == role]
        avg_salary = salary_match["monthly_ctc"].mean()

        if pd.isna(avg_salary):
            avg_salary = 90000

        hiring_cost = gap * avg_salary * duration

        results.append({
            "required_role": role,
            "required_people": required_people,
            "available_capacity": round(available_capacity, 2),
            "skill_gap": round(gap, 2),
            "estimated_hiring_cost": round(hiring_cost, 2),
        })

    return pd.DataFrame(results)


# ---------------- FINANCE CALCULATIONS ----------------

def calculate_salary_after_lop(payroll: pd.DataFrame, lop_df: pd.DataFrame) -> pd.DataFrame:
    results = []

    for _, lop in lop_df.iterrows():
        emp_id = lop["employee_id"]
        pay = payroll[payroll["employee_id"].astype(str).str.upper() == str(emp_id).upper()]

        if pay.empty:
            continue

        pay = pay.iloc[0]

        gross_salary = float(pay["gross_salary"])
        net_salary = float(pay["net_salary"])
        per_day_salary = gross_salary / 30

        lop_days = float(lop["lop_days"])
        lop_deduction = per_day_salary * lop_days
        final_net_salary = net_salary - lop_deduction

        results.append({
            "employee_id": emp_id,
            "month": lop["month"],
            "gross_salary": round(gross_salary, 2),
            "net_salary_before_lop": round(net_salary, 2),
            "lop_days": lop_days,
            "lop_deduction": round(lop_deduction, 2),
            "final_net_salary": round(final_net_salary, 2),
        })

    return pd.DataFrame(results)


def calculate_project_finance(
    employees: pd.DataFrame,
    requirements: pd.DataFrame,
    project_type: str,
    duration_months=None,
    target_margin=0.30
) -> dict:
    req = requirements[requirements["project_type"] == project_type]

    if req.empty:
        return {
            "error": f"No requirements found for project type: {project_type}"
        }

    if duration_months is None:
        duration_months = int(req["estimated_months"].max())

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

    employee_cost = 0
    role_costs = []

    for _, row in req.iterrows():
        role = row["required_role"]
        count = float(row["required_people"])

        matching = employees[employees["designation"] == role]

        if matching.empty:
            avg_salary = 90000
        else:
            avg_salary = matching["monthly_ctc"].mean()

        allocation = default_allocation.get(role, 0.35)

        role_cost = avg_salary * count * allocation * duration_months
        employee_cost += role_cost

        role_costs.append({
            "role": role,
            "people_required": count,
            "avg_salary": round(avg_salary, 2),
            "allocation_used": allocation,
            "duration_months": duration_months,
            "role_cost": round(role_cost, 2),
        })

    overhead = employee_cost * 0.10
    cloud_cost = employee_cost * 0.05
    software_cost = employee_cost * 0.03
    contingency = employee_cost * 0.05

    total_cost = employee_cost + overhead + cloud_cost + software_cost + contingency

    recommended_quote = total_cost / (1 - target_margin)
    expected_profit = recommended_quote - total_cost
    profit_margin = expected_profit / recommended_quote if recommended_quote else 0

    return {
        "project_type": project_type,
        "duration_months": duration_months,
        "employee_cost": round(employee_cost, 2),
        "overhead": round(overhead, 2),
        "cloud_cost": round(cloud_cost, 2),
        "software_cost": round(software_cost, 2),
        "contingency": round(contingency, 2),
        "total_project_cost": round(total_cost, 2),
        "recommended_quote": round(recommended_quote, 2),
        "expected_profit": round(expected_profit, 2),
        "profit_margin_percent": round(profit_margin * 100, 2),
        "role_cost_breakdown": role_costs,
    }


def calculate_project_profitability(
    projects: pd.DataFrame,
    assignments: pd.DataFrame,
    payroll: pd.DataFrame,
    expenses: pd.DataFrame
) -> pd.DataFrame:
    results = []
    monthly_expense = expenses["monthly_cost"].sum()

    for _, project in projects.iterrows():
        project_id = project["project_id"]
        duration = float(project["estimated_duration_months"])
        project_value = float(project["project_value"])

        project_assignments = assignments[assignments["project_id"] == project_id]
        employee_cost = 0

        for _, assignment in project_assignments.iterrows():
            emp_id = assignment["employee_id"]
            allocation = float(assignment["allocation_percent"]) / 100

            pay = payroll[payroll["employee_id"].astype(str).str.upper() == str(emp_id).upper()]

            if pay.empty:
                continue

            monthly_salary = float(pay.iloc[0]["gross_salary"])
            employee_cost += monthly_salary * allocation * duration

        overhead = employee_cost * 0.10
        cloud_cost = employee_cost * 0.05
        software_cost = employee_cost * 0.03
        allocated_company_expense = monthly_expense * duration * 0.05

        total_cost = employee_cost + overhead + cloud_cost + software_cost + allocated_company_expense

        profit = project_value - total_cost
        margin = profit / project_value if project_value else 0

        results.append({
            "project_id": project_id,
            "project_name": project["project_name"],
            "project_value": round(project_value, 2),
            "employee_cost": round(employee_cost, 2),
            "overhead": round(overhead, 2),
            "cloud_cost": round(cloud_cost, 2),
            "software_cost": round(software_cost, 2),
            "allocated_company_expense": round(allocated_company_expense, 2),
            "total_project_cost": round(total_cost, 2),
            "profit": round(profit, 2),
            "profit_margin_percent": round(margin * 100, 2),
        })

    return pd.DataFrame(results)


# ---------------- SALES CALCULATIONS ----------------

def calculate_sales_score(lead) -> dict:
    score = 0

    budget = float(lead["expected_budget"])

    if budget >= 7000000:
        score += 25
    elif budget >= 5000000:
        score += 18
    elif budget >= 3000000:
        score += 12
    else:
        score += 6

    urgency = str(lead["urgency"])

    if urgency == "High":
        score += 20
    elif urgency == "Medium":
        score += 12
    else:
        score += 6

    if str(lead["existing_client"]) == "Yes":
        score += 20
    else:
        score += 8

    competition = str(lead["competition_level"])

    if competition == "Low":
        score += 20
    elif competition == "Medium":
        score += 10
    else:
        score -= 10

    score = max(0, min(score, 100))

    return {
        "lead_score": score,
        "win_probability_percent": score,
        "expected_budget": budget,
    }


# ---------------- OPERATIONS CALCULATIONS ----------------

def calculate_operations_risk(projects: pd.DataFrame, assignments: pd.DataFrame) -> pd.DataFrame:
    results = []

    for _, project in projects.iterrows():
        project_id = project["project_id"]
        project_assignments = assignments[assignments["project_id"] == project_id]

        expected_progress = float(project["expected_progress"])
        actual_progress = float(project["actual_progress"])

        progress_gap = max(0, expected_progress - actual_progress)

        avg_bandwidth = project_assignments["allocation_percent"].mean()

        if pd.isna(avg_bandwidth):
            avg_bandwidth = 0

        timeline_risk = min(progress_gap, 25)

        if avg_bandwidth >= 80:
            bandwidth_risk = 25
        elif avg_bandwidth >= 60:
            bandwidth_risk = 15
        else:
            bandwidth_risk = 5

        risk_score = timeline_risk + bandwidth_risk

        if risk_score >= 45:
            risk_level = "High"
        elif risk_score >= 25:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        results.append({
            "project_id": project_id,
            "project_name": project["project_name"],
            "expected_progress": expected_progress,
            "actual_progress": actual_progress,
            "progress_gap": progress_gap,
            "average_bandwidth": round(avg_bandwidth, 2),
            "timeline_risk": round(timeline_risk, 2),
            "bandwidth_risk": round(bandwidth_risk, 2),
            "operations_risk_score": round(risk_score, 2),
            "risk_level": risk_level,
        })

    return pd.DataFrame(results)


def calculate_employee_bandwidth(assignments: pd.DataFrame, employee_id=None) -> pd.DataFrame:
    df = assignments.copy()

    if employee_id:
        df = df[df["employee_id"].astype(str).str.upper() == str(employee_id).upper()]

    summary = df.groupby(["employee_id", "employee_name"]).agg({
        "allocation_percent": "sum",
        "weekly_hours": "sum",
    }).reset_index()

    summary["available_bandwidth_percent"] = 100 - summary["allocation_percent"]

    summary["bandwidth_status"] = summary["allocation_percent"].apply(
        lambda x: "Overloaded" if x > 90 else "Healthy" if x >= 50 else "Available"
    )

    return summary


# ---------------- CEO CALCULATIONS ----------------

def calculate_company_performance(
    projects: pd.DataFrame,
    assignments: pd.DataFrame,
    payroll: pd.DataFrame,
    expenses: pd.DataFrame,
    employees: pd.DataFrame
) -> dict:
    profitability = calculate_project_profitability(projects, assignments, payroll, expenses)
    operations_risk = calculate_operations_risk(projects, assignments)

    total_revenue = float(projects["project_value"].sum())
    total_cost = float(profitability["total_project_cost"].sum())
    total_profit = float(profitability["profit"].sum())

    company_margin = total_profit / total_revenue if total_revenue else 0

    avg_utilization = assignments["allocation_percent"].mean()
    if pd.isna(avg_utilization):
        avg_utilization = 0

    active_projects = len(projects[projects["status"] == "Active"])
    high_risk_projects = len(operations_risk[operations_risk["risk_level"] == "High"])
    medium_risk_projects = len(operations_risk[operations_risk["risk_level"] == "Medium"])

    available_people = len(employees[employees["availability_percent"] >= 50])

    if company_margin >= 0.35 and high_risk_projects == 0:
        health = "Strong"
    elif company_margin >= 0.25 and high_risk_projects <= 1:
        health = "Moderate"
    else:
        health = "Needs Attention"

    return {
        "total_revenue": round(total_revenue, 2),
        "total_cost": round(total_cost, 2),
        "total_profit": round(total_profit, 2),
        "company_margin_percent": round(company_margin * 100, 2),
        "average_utilization_percent": round(avg_utilization, 2),
        "active_projects": active_projects,
        "high_risk_projects": high_risk_projects,
        "medium_risk_projects": medium_risk_projects,
        "available_people": available_people,
        "company_health": health,
    }