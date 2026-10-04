from app.agents.data_agent import data_agent
from app.agents.risk_agent import risk_agent
from app.agents.strategy_agent import strategy_agent


# Data Agent
data_result = data_agent("app/data/business_data.csv")

# Risk Agent
risk_result = risk_agent(data_result["insights"])

# Strategy Agent
strategy_result = strategy_agent(risk_result)


print("================================")
print("       STRATEGY AGENT")
print("================================")

print("\nRisk Level:", risk_result["risk_level"])

print("\nProposed Actions:")

for i, action in enumerate(strategy_result["actions"], 1):

    print(f"\n{i}. {action['action']}")
    print("   Priority:", action["priority"])
    print("   Reason:", action["reason"])