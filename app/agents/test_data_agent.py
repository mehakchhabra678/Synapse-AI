from app.agents.data_agent import data_agent


result = data_agent("app/data/business_data.csv")


print("================================")
print("          DATA AGENT")
print("================================")

print("\nDataset:")
print("Rows:", result["analysis"]["rows"])
print("Columns:", result["analysis"]["columns"])

print("\nBusiness Insights:")

for i, insight in enumerate(result["insights"], 1):
    print(f"{i}. {insight}")