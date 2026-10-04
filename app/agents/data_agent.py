from app.tools.data_analyzer import analyze_dataset
from app.tools.insight_engine import generate_insights


def data_agent(file_path: str) -> dict:
    """
    Data Agent.

    Analyzes business data and produces business insights.
    """

    analysis = analyze_dataset(file_path)

    insights = generate_insights(analysis)

    return {
        "analysis": analysis,
        "insights": insights
    }