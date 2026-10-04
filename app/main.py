from app.agents.agent import ask_agent


def main():
    print("=================================")
    print("       SYNAPSE-AI")
    print(" Enterprise Decision Engine")
    print("=================================")

    user_input = input("\nWhat would you like Synapse-AI to analyze?\n> ")

    result = ask_agent(user_input)

    print("\n--- SYNAPSE-AI RESPONSE ---")
    print(result)


if __name__ == "__main__":
    main()