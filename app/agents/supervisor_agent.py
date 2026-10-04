import os

from google import genai
from dotenv import load_dotenv


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def supervisor_agent(user_question: str) -> dict:
    """
    Supervisor Agent.

    Development mode:
        Uses deterministic routing to avoid Gemini API calls.

    Production mode:
        Uses Gemini to select specialized agents.
    """

    app_mode = os.getenv("APP_MODE", "development")

    # ==========================================
    # DEVELOPMENT MODE
    # ==========================================

    if app_mode == "development":

        question = user_question.lower()

        selected_agents = []
        selected_agents.append("RAG_AGENT")

# Enterprise policy context is always available



        # RAG Agent
        if any(word in question for word in [
            "policy",
            "procedure",
            "according to",
            "company rule",
            "guideline"
        ]):
            selected_agents.append("RAG_AGENT")

        # Data Agent
        if any(word in question for word in [
            "data",
            "revenue",
            "orders",
            "customers",
            "cost",
            "trend",
            "increase",
            "decrease",
            "performance",
            "late"
        ]):
            selected_agents.append("DATA_AGENT")

        # Risk Agent
        if any(word in question for word in [
            "risk",
            "late",
            "problem",
            "issue",
            "decline",
            "deterioration"
        ]):
            selected_agents.append("RISK_AGENT")

        # Strategy Agent
        if any(word in question for word in [
            "what should",
            "what do",
            "action",
            "recommend",
            "improve",
            "solve"
        ]):
            selected_agents.append("STRATEGY_AGENT")

        # Remove duplicates while preserving order
        selected_agents = list(dict.fromkeys(selected_agents))

        # Fallback
        if not selected_agents:
            selected_agents = [
                "DATA_AGENT",
                "RAG_AGENT",
                "RISK_AGENT",
                "STRATEGY_AGENT"
            ]

        print("Supervisor: DEVELOPMENT MODE")
        print("Supervisor: selected agents =", selected_agents)

        return {
            "question": user_question,
            "selected_agents": selected_agents
        }

    # ==========================================
    # PRODUCTION MODE — GEMINI
    # ==========================================

    prompt = f"""
You are the Supervisor Agent of Synapse-AI,
an enterprise decision intelligence system.

Your job is to decide which specialized agents
should participate in answering the user's question.

Available agents:

1. DATA_AGENT
   - Analyzes business datasets
   - Identifies trends and operational indicators

2. RAG_AGENT
   - Retrieves relevant enterprise policies
   - Provides knowledge-grounded context

3. RISK_AGENT
   - Evaluates business risk using data insights

4. STRATEGY_AGENT
   - Generates possible business actions

User question:

{user_question}

Return ONLY the agent names that should participate.

Possible names:
DATA_AGENT
RAG_AGENT
RISK_AGENT
STRATEGY_AGENT

Return them as a comma-separated list.
"""

    print("Supervisor: calling gemini-3.8-flash")

    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt,
        generation_config={
            "thinking_level": "low",
            "max_output_tokens": 100
        }
    )

    response_text = interaction.output_text

    if not response_text:
        raise RuntimeError(
            "Gemini Supervisor returned an empty response."
        )

    agents = [
        agent.strip()
        for agent in response_text.split(",")
        if agent.strip()
    ]

    return {
        "question": user_question,
        "selected_agents": agents
    }