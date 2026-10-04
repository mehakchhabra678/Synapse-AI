def human_review(actions: list) -> dict:
    """
    Simulate human approval of AI-generated actions.
    """

    print("\n================================")
    print("         HUMAN REVIEW")
    print("================================")

    print("\nThe AI has proposed the following actions:\n")

    for i, action in enumerate(actions, 1):
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
        return {
            "status": "APPROVED",
            "message": "Human approved the proposed actions."
        }

    elif choice == "2":
        return {
            "status": "REJECTED",
            "message": "Human rejected the proposed actions."
        }

    elif choice == "3":
        modification = input("Enter modification: ")

        return {
            "status": "MODIFIED",
            "message": modification
        }

    else:
        return {
            "status": "INVALID",
            "message": "Invalid review option."
        }