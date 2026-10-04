from app.agents.data_agent import data_agent
from app.agents.risk_agent import risk_agent


# Data Agent
data_result = data_agent("app/data/business_data.csv")

# Risk Agent
risk_result = risk_agent(data_result["insights"])


print("================================")
print("          RISK AGENT")
print("================================")

print("\nRisk Score:", risk_result["risk_score"])
print("Risk Level:", risk_result["risk_level"])

print("\nRecommended Action:")
print(risk_result["recommended_action"])

print("\nRisk Reasons:")

for reason in risk_result["reasons"]:
    print("-", reason)