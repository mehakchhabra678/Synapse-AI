from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt

from app.graph.state import SynapseState

from app.agents.data_agent import data_agent
from app.agents.rag_agent import rag_agent
from app.agents.risk_agent import risk_agent
from app.agents.strategy_agent import strategy_agent
from app.agents.supervisor_agent import supervisor_agent
from app.tools.human_review import human_review



# ==========================================
# SUPERVISOR
# ==========================================

def supervisor_node(state: SynapseState):
    result = supervisor_agent(state["user_question"])

    return {
        "selected_agents": result["selected_agents"]
    }


# ==========================================
# DATA AGENT
# ==========================================

def data_node(state: SynapseState):
    result = data_agent(state["file_path"])

    return {
        "analysis": result["analysis"],
        "insights": result["insights"]
    }


# ==========================================
# RAG AGENT
# ==========================================

def rag_node(state: SynapseState):
    result = rag_agent(state["user_question"])

    return {
        "rag_context": result["answer_context"],
        "rag_sources": result["sources"]
    }


# ==========================================
# RISK AGENT
# ==========================================

def risk_node(state: SynapseState):
    result = risk_agent(state["insights"])

    return {
        "risk": result
    }


# ==========================================
# STRATEGY AGENT
# ==========================================

def strategy_node(state: SynapseState):
    result = strategy_agent(
        state["risk"],
        state.get("rag_context", "")
    )

    return {
        "actions": result["actions"]
    }

# ==========================================
# HUMAN REVIEW
# ==========================================

def human_review_node(state: SynapseState):
    """
    Pause the graph and request human approval.
    """

    decision = interrupt({
        "type": "human_review",
        "actions": state["actions"],
        "message": "Please review the proposed actions."
    })

    return {
        "human_decision": decision
    }

# ==========================================
# SUPERVISOR ROUTING
# ==========================================

def route_from_supervisor(state: SynapseState):

    selected_agents = state.get("selected_agents", [])

    routes = []

    # RAG can run independently
    if "RAG_AGENT" in selected_agents:
        routes.append("rag_agent")

    # DATA starts the main analytical chain
    if "DATA_AGENT" in selected_agents:
        routes.append("data_agent")

    return routes


# ==========================================
# BUILD GRAPH
# ==========================================

builder = StateGraph(SynapseState)

builder.add_node("supervisor_agent", supervisor_node)

builder.add_node("data_agent", data_node)
builder.add_node("rag_agent", rag_node)
builder.add_node("risk_agent", risk_node)
builder.add_node("strategy_agent", strategy_node)
builder.add_node("human_review",human_review_node)

# ==========================================
# START
# ==========================================

builder.add_edge(
    START,
    "supervisor_agent"
)


# ==========================================
# SUPERVISOR → INITIAL AGENTS
# ==========================================

builder.add_edge(
    "supervisor_agent",
    "rag_agent"
)


# ==========================================
# AGENT DEPENDENCIES
# ==========================================

# ==========================================
# AGENT DEPENDENCIES
# ==========================================

# RAG → DATA
builder.add_edge(
    "rag_agent",
    "data_agent"
)

# DATA → RISK
builder.add_edge(
    "data_agent",
    "risk_agent"
)

# RISK → STRATEGY
builder.add_edge(
    "risk_agent",
    "strategy_agent"
)

# STRATEGY → END
# STRATEGY → HUMAN REVIEW
builder.add_edge(
    "strategy_agent",
    "human_review"
)

# HUMAN REVIEW → END
builder.add_edge(
    "human_review",
    END
)
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()

synapse_graph = builder.compile(
    checkpointer=checkpointer
)