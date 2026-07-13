from io import BytesIO
import pandas as pd


def generate_proposal_report(result: dict) -> BytesIO:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        pd.DataFrame([result["lead"]]).to_excel(writer, sheet_name="Lead", index=False)
        pd.DataFrame([result["sales_result"]]).to_excel(writer, sheet_name="Sales Agent", index=False)
        result["hr_result"].to_excel(writer, sheet_name="HR Agent", index=False)
        result["operations_existing_risk"].to_excel(writer, sheet_name="Operations Agent", index=False)
        pd.DataFrame([result["finance_result"]]).to_excel(writer, sheet_name="Finance Agent", index=False)
        pd.DataFrame([{
            "new_project_risk": result["new_project_risk"],
            "risk_score": result["risk_score"],
            "ceo_decision": result["ceo_decision"],
            "internal_meeting_report": result["llm_report"],
        }]).to_excel(writer, sheet_name="CEO Decision", index=False)
    output.seek(0)
    return output
