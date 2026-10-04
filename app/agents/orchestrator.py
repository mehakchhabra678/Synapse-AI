from app.tools.data_analyzer import analyze_dataset
from app.tools.insight_engine import generate_insights
from app.tools.decision_engine import make_decision
from app.tools.action_engine import generate_actions


def run_synapse(file_path: str) -> dict:
    """
    Main Synapse-AI orchestration pipeline.

    No Gemini/API call is made here.
    """

    # 1. Analyze business data
    analysis = analyze_dataset(file_path)

    # 2. Generate business insights
    insights = generate_insights(analysis)

    # 3. Assess risk and make a decision
    decision = make_decision(insights)

    # 4. Generate possible actions
    actions = generate_actions(decision)

    return {
        "analysis": analysis,
        "insights": insights,
        "decision": decision,
        "actions": actions
    }