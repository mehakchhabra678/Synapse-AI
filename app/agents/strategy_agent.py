from app.tools.action_engine import generate_actions


def strategy_agent(decision: dict, rag_context: str = "") -> dict:
    """
    Strategy Agent.

    Generates business actions using risk information
    and, when available, enterprise policy context.
    """

    actions = generate_actions(decision)

    # Add policy grounding to each action when RAG
    # information is available.
    if rag_context:
        for action in actions:
            action["policy_context"] = rag_context

    return {
        "actions": actions
    }