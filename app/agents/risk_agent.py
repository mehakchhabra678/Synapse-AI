from app.tools.decision_engine import make_decision


def risk_agent(insights: list) -> dict:
    """
    Risk Agent.

    Evaluates business insights and produces
    an explainable risk assessment.
    """

    decision = make_decision(insights)

    return {
        "risk_score": decision["risk_score"],
        "risk_level": decision["risk_level"],
        "recommended_action": decision["recommended_action"],
        "reasons": decision["reasons"]
    }