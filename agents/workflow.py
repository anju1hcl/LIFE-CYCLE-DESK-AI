from llm_client import ask_llm
from core.calculations import (
    calculate_sales_score,
    calculate_skill_gap,
    calculate_project_finance,
    calculate_operations_risk,
    calculate_company_performance,
)
from core.calculations import calculate_company_performance

def run_new_project_proposal_workflow(data: dict, lead_id: str) -> dict | None:
    lead_row = data["leads"][data["leads"]["lead_id"] == lead_id]
    if lead_row.empty:
        return None

    lead = lead_row.iloc[0]
    project_type = lead["project_type"]

    sales_result = calculate_sales_score(lead)
    hr_result = calculate_skill_gap(data["employees"], data["requirements"], project_type)
    finance_result = calculate_project_finance(data["employees"], data["requirements"], project_type)
    operations_risk = calculate_operations_risk(data["projects"], data["assignments"])

    hiring_needed = float(hr_result["skill_gap"].sum()) if not hr_result.empty else 0
    avg_existing_risk = float(operations_risk["operations_risk_score"].mean()) if not operations_risk.empty else 0
    risk_score = 25
    if avg_existing_risk >= 45:
        risk_score = 70
    elif hiring_needed > 1:
        risk_score = 50
    elif avg_existing_risk >= 25:
        risk_score = 40

    new_project_risk = "High" if risk_score >= 65 else "Medium" if risk_score >= 40 else "Low"

    profit_margin = finance_result["profit_margin_percent"]
    win_probability = sales_result["win_probability_percent"]

    if profit_margin >= 30 and win_probability >= 50 and risk_score <= 60:
        decision = "Approved"
    elif profit_margin >= 25 and risk_score <= 70:
        decision = "Approved with Conditions"
    else:
        decision = "Rejected"

    fallback_report = f"""
Internal AI Meeting Report

Sales Agent: Lead score is {sales_result['lead_score']} with win probability {win_probability}%.
HR Agent: Total hiring gap is {hiring_needed} FTE equivalent.
Operations Agent: Current operating risk is {new_project_risk} with risk score {risk_score}.
Finance Agent: Recommended quote is INR {finance_result['recommended_quote']} with expected margin {profit_margin}%.
CEO Agent: Decision is {decision}.

This workflow replaces manual Sales, HR, Operations, Finance and CEO review meetings by generating a decision-ready report in seconds.
"""

    prompt = f"""
You are the CEO Agent preparing an internal decision meeting report.
Use the calculations below. Do not invent numbers.

Lead: {lead.to_dict()}
Sales Agent Calculation: {sales_result}
HR Agent Skill Gap: {hr_result.to_dict(orient='records')}
Operations Agent Risk: average existing risk {avg_existing_risk}, new project risk {new_project_risk}, risk score {risk_score}
Finance Agent Calculation: {finance_result}
CEO Decision: {decision}

Write a concise professional internal meeting report with sections:
1. Business problem
2. Sales analysis
3. HR capacity analysis
4. Operations risk analysis
5. Finance quote and profitability
6. CEO decision
7. Conditions / next steps
8. Time saved versus manual multi-department meetings
"""
    llm_report = ask_llm(prompt, fallback=fallback_report)

    return {
        "lead": lead.to_dict(),
        "sales_result": sales_result,
        "hr_result": hr_result,
        "operations_existing_risk": operations_risk,
        "finance_result": finance_result,
        "risk_score": risk_score,
        "new_project_risk": new_project_risk,
        "ceo_decision": decision,
        "llm_report": llm_report,
    }


# def run_company_health_workflow(data: dict) -> dict:
#     performance = calculate_company_performance(data)
#     fallback = f"Company health is {performance['company_health']}. Revenue INR {performance['total_revenue']}, profit INR {performance['total_profit']}, margin {performance['company_margin_percent']}%."
#     prompt = f"""
# You are CEO Agent. Explain this company performance in a concise executive format:
# {performance}
# Include health, profitability, operations utilization, risks, and CEO recommendations.
# """
#     return {"performance": performance, "llm_response": ask_llm(prompt, fallback=fallback)}
def run_company_health_workflow(data):
    performance = calculate_company_performance(
        data["projects"],
        data["assignments"],
        data["payroll"],
        data["expenses"],
        data["employees"]
    )

    prompt = f"""
You are the CEO Agent.

Analyze this company performance:

{performance}

Give:
1. Company health summary
2. Financial interpretation
3. Operations interpretation
4. Hiring/resource concern
5. CEO recommendation
"""

    llm_response = ask_llm(prompt)

    return {
        "performance": performance,
        "llm_response": llm_response
    }