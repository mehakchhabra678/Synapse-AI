from app.agents.rag_agent import rag_agent


question = (
    "What should management do when the late-order rate "
    "exceeds the investigation threshold?"
)


result = rag_agent(question)


print("================================")
print("         RAG AGENT")
print("================================")

print("\nQuestion:")
print(result["question"])

print("\nRetrieved Context:")
print(result["answer_context"])

print("\nSources:")

for source in result["sources"]:
    print("-", source)