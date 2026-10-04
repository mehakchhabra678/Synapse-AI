from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


DOCUMENTS_PATH = Path("app/data/documents")
CHROMA_PATH = "app/data/chroma_db"

# Local embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Local ChromaDB
client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_or_create_collection(
    name="synapse_knowledge"
)


def load_documents():
    """
    Load text documents from the knowledge base.
    """

    documents = []

    for file_path in DOCUMENTS_PATH.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")

        documents.append({
            "filename": file_path.name,
            "text": text
        })

    return documents


def chunk_text(text, chunk_size=500):
    """
    Split text into simple chunks.
    """

    words = text.split()

    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


def ingest_documents():
    """
    Load, chunk, embed and store documents in ChromaDB.
    """

    documents = load_documents()

    total_chunks = 0

    for document in documents:

        chunks = chunk_text(document["text"])

        embeddings = embedding_model.encode(chunks).tolist()

        ids = [
            f"{document['filename']}_{i}"
            for i in range(len(chunks))
        ]

        metadatas = [
            {
                "source": document["filename"]
            }
            for _ in chunks
        ]

        collection.upsert(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas
        )

        total_chunks += len(chunks)

    return total_chunks


if __name__ == "__main__":

    count = ingest_documents()

    print("================================")
    print("       SYNAPSE-AI RAG")
    print("================================")

    print(f"\nDocuments ingested successfully.")
    print(f"Chunks stored: {count}")