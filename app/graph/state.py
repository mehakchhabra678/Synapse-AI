from typing import TypedDict


class SynapseState(TypedDict, total=False):

    file_path: str
    user_question: str
    selected_agents: list

    analysis: dict
    insights: list

    rag_context: str
    rag_sources: list

    risk: dict
    actions: list

    human_decision: dict