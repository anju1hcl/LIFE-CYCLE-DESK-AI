
import json
from llm_client import ask_llm


def receptionist_understand(query: str, user=None) -> dict:
    user_context = "Not logged in"

    if user:
        user_context = (
            f"Logged in user: {user.get('employee_name')} | "
            f"Role: {user.get('role')} | "
            f"Department: {user.get('department')} | "
            f"Designation: {user.get('designation')}"
        )

    prompt = f"""
You are the AI Receptionist of a virtual IT services company.

Your job is to understand the user's intent and route them to the correct agent.

Do NOT use simple keyword matching. Understand the meaning.

Available agents and capabilities:

HR Agent:
- reporting manager
- employee profile
- attendance
- LOP / loss of pay
- leave status
- onboarding
- forms
- virtual ID
- joining status

Finance Agent:
- salary date
- in-hand salary
- salary credited amount
- salary lower than expected
- payroll discrepancy
- deductions
- LOP salary impact
- project pricing
- project cost
- profit margin

Operations Agent:
- current project
- assigned project
- project blockers
- bandwidth
- workload
- delivery risk
- project delay
- project progress

Sales Agent:
- lead qualification
- client enquiry
- new client
- project proposal
- win probability
- deal value
- sales pipeline

CEO Agent:
- company health
- business performance
- approve/reject project
- final decision
- strategy
- company-level report

User context:
{user_context}

User message:
{query}

Return ONLY valid JSON in this exact format:

{{
  "agent": "HR Agent | Finance Agent | Operations Agent | Sales Agent | CEO Agent | Receptionist",
  "intent": "short intent name",
  "confidence": 0.0,
  "reason": "short reason"
}}

Rules:
- If user says salary is lower than usual, intent is payroll_discrepancy and agent is Finance Agent.
- If user asks who reports to whom or manager, intent is reporting_manager and agent is HR Agent.
- If user asks about current workload, project, bandwidth, or blockers, agent is Operations Agent.
- If user gives a new project requirement as an external client, agent is Sales Agent with intent external_client_enquiry.
- If user mentions lead ID like L001/L002/L003, agent is CEO Agent with intent internal_project_decision.
- If user asks company performance, agent is CEO Agent.
"""

    raw = ask_llm(prompt)

    try:
        result = json.loads(raw)
    except Exception:
        result = {
            "agent": "Receptionist",
            "intent": "unknown",
            "confidence": 0.0,
            "reason": "Could not parse receptionist intent."
        }

    valid_agents = [
        "HR Agent",
        "Finance Agent",
        "Operations Agent",
        "Sales Agent",
        "CEO Agent",
        "Receptionist"
    ]

    if result.get("agent") not in valid_agents:
        result["agent"] = "Receptionist"

    return result