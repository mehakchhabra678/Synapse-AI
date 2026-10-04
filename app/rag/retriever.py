import chromadb
from sentence_transformers import SentenceTransformer


CHROMA_PATH = "app/data/chroma_db"

# Load the embedding model only when it is actually needed
_embedding_model = None


def get_embedding_model():
    global _embedding_model

    if _embedding_model is None:
        print("RAG: Loading embedding model...")
        _embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    return _embedding_model


client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_collection(
    name="synapse_knowledge"
)


def retrieve_documents(
    query: str,
    top_k: int = 3
) -> list:

    embedding_model = get_embedding_model()

    query_embedding = embedding_model.encode(
        [query]
    ).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )

    retrieved_documents = []

    for i, document in enumerate(
        results["documents"][0]
    ):

        retrieved_documents.append({
            "content": document,
            "source": results["metadatas"][0][i]["source"],
            "distance": results["distances"][0][i]
        })

    return retrieved_documents