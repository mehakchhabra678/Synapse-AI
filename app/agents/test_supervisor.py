from app.agents.supervisor_agent import supervisor_agent


question = (
    "Late orders have increased significantly. "
    "What should management do according to company policy?"
)


result = supervisor_agent(question)


print("================================")
print("       SUPERVISOR AGENT")
print("================================")

print("\nUser Question:")
print(result["question"])

print("\nSelected Agents:")

for agent in result["selected_agents"]:
    print("-", agent)