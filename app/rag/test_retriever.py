from app.rag.retriever import retrieve_documents


query = "What should management do when late orders exceed the investigation threshold?"


results = retrieve_documents(query)


print("================================")
print("       RAG RETRIEVAL TEST")
print("================================")

print("\nQuery:")
print(query)

print("\nRetrieved Information:")

for i, result in enumerate(results, 1):

    print(f"\n--- Result {i} ---")

    print("Source:", result["source"])

    print("Distance:", round(result["distance"], 4))

    print("Content:")
    print(result["content"])
    