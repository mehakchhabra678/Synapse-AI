from app.tools.data_analyzer import analyze_dataset
from app.tools.insight_engine import generate_insights
from app.tools.decision_engine import make_decision
from app.tools.action_engine import generate_actions
from app.tools.human_review import human_review

# Step 1: Analyze data
result = analyze_dataset("app/data/business_data.csv")


# Step 2: Generate insights
insights = generate_insights(result)


# Step 3: Make decision
decision = make_decision(insights)


# Step 4: Generate possible actions
actions = generate_actions(decision)


print("================================")
print("       SYNAPSE-AI ENGINE")
print("================================")

print("\nBUSINESS INSIGHTS")

for i, insight in enumerate(insights, 1):
    print(f"{i}. {insight}")


print("\nDECISION")

print("Risk Score:", decision["risk_score"])
print("Risk Level:", decision["risk_level"])
print("Recommended Action:", decision["recommended_action"])


print("\nREASONS")

for reason in decision["reasons"]:
    print("-", reason)


print("\nPOSSIBLE ACTIONS")

for i, action in enumerate(actions, 1):
    print(f"\n{i}. {action['action']}")
    print("   Priority:", action["priority"])
    print("   Reason:", action["reason"])

review = human_review(actions)

print("\n================================")
print("       FINAL HUMAN DECISION")
print("================================")

print("Status:", review["status"])
print("Message:", review["message"])