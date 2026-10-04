from app.rag.retriever import retrieve_documents


def rag_agent(question: str) -> dict:
    """
    RAG Agent.

    Retrieves relevant enterprise knowledge for a question.
    No LLM call yet.
    """

    results = retrieve_documents(question)

    if not results:
        return {
            "question": question,
            "answer_context": "",
            "sources": []
        }

    context_parts = []
    sources = []

    for result in results:

        context_parts.append(result["content"])

        if result["source"] not in sources:
            sources.append(result["source"])

    context = "\n\n".join(context_parts)

    return {
        "question": question,
        "answer_context": context,
        "sources": sources
    }