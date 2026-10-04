from langgraph.types import Command

from app.graph.workflow import synapse_graph


initial_state = {
    "file_path": "app/data/business_data.csv",
    "user_question": (
        "What should management do when late orders "
        "increase significantly?"
    )
}


# ==========================================
# CONFIGURATION
# ==========================================

config = {
    "configurable": {
        "thread_id": "synapse-test-1"
    }
}


# ==========================================
# START WORKFLOW
# ==========================================

result = synapse_graph.invoke(
    initial_state,
    config=config
)


# ==========================================
# HUMAN REVIEW INTERRUPT
# ==========================================

if "__interrupt__" in result:

    interrupt_data = result["__interrupt__"][0].value

    print("\n================================")
    print("       HUMAN REVIEW REQUIRED")
    print("================================")

    print("\nThe AI has proposed the following actions:\n")

    for i, action in enumerate(
        interrupt_data["actions"],
        1
    ):
        print(f"{i}. {action['action']}")
        print(f"   Priority: {action['priority']}")
        print(f"   Reason: {action['reason']}")
        print()

    print("Review Options:")
    print("1 - Approve")
    print("2 - Reject")
    print("3 - Modify")

    choice = input("\nEnter your choice: ")

    if choice == "1":

        human_decision = {
            "status": "APPROVED",
            "message": "Human approved the proposed actions."
        }

    elif choice == "2":

        human_decision = {
            "status": "REJECTED",
            "message": "Human rejected the proposed actions."
        }

    elif choice == "3":

        modification = input(
            "Enter modification: "
        )

        human_decision = {
            "status": "MODIFIED",
            "message": modification
        }

    else:

        human_decision = {
            "status": "INVALID",
            "message": "Invalid review option."
        }


    # ======================================
    # RESUME GRAPH
    # ======================================

    result = synapse_graph.invoke(
        Command(resume=human_decision),
        config=config
    )


# ==========================================
# FINAL OUTPUT
# ==========================================

print("\n================================")
print("       SYNAPSE-AI MAS")
print("================================")


print("\nSELECTED AGENTS")
print(result.get("selected_agents"))


print("\nDATA INSIGHTS")

for insight in result.get("insights", []):
    print("-", insight)


print("\nRAG SOURCES")

for source in result.get("rag_sources", []):
    print("-", source)


print("\nRISK")

if "risk" in result:

    print(
        "Score:",
        result["risk"]["risk_score"]
    )

    print(
        "Level:",
        result["risk"]["risk_level"]
    )


print("\nSTRATEGY")

for action in result.get("actions", []):

    print(f"\n- {action['action']}")
    print("  Priority:", action["priority"])
    print("  Reason:", action["reason"])

    if "policy_context" in action:
        print("  Policy Context: AVAILABLE")


print("\nFINAL HUMAN DECISION")

print(
    result.get(
        "human_decision",
        "No human decision recorded."
    )
)