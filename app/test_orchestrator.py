from app.agents.orchestrator import run_synapse


result = run_synapse("app/data/business_data.csv")


print("================================")
print("       SYNAPSE-AI")
print("================================")

print("\nBUSINESS INSIGHTS")

for i, insight in enumerate(result["insights"], 1):
    print(f"{i}. {insight}")


print("\nDECISION")

decision = result["decision"]

print("Risk Score:", decision["risk_score"])
print("Risk Level:", decision["risk_level"])
print("Recommended Action:", decision["recommended_action"])


print("\nPOSSIBLE ACTIONS")

for i, action in enumerate(result["actions"], 1):
    print(f"{i}. {action['action']}")
    print(f"   Priority: {action['priority']}")
    print(f"   Reason: {action['reason']}")