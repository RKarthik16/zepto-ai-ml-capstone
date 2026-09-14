from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from support_assistant.config import (
    CHROMA_DIR,
    COLLECTION_NAME,
    CORPUS_DIR,
    EMBEDDING_MODEL_NAME,
)


class KnowledgeBase:
    def __init__(self):
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

        self.client = chromadb.PersistentClient(
            path=str(CHROMA_DIR)
        )

        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )

    def load_documents(self) -> list[dict]:
        documents = []

        for path in sorted(CORPUS_DIR.glob("*.md")):
            documents.append(
                {
                    "id": path.stem,
                    "source": path.name,
                    "text": path.read_text(encoding="utf-8"),
                }
            )

        if len(documents) != 8:
            raise ValueError(
                f"Expected 8 corpus documents, found {len(documents)}"
            )

        return documents

    def build_index(self) -> None:
        documents = self.load_documents()

        embeddings = self.embedding_model.encode(
            [document["text"] for document in documents],
            normalize_embeddings=True,
        ).tolist()

        self.collection.upsert(
            ids=[document["id"] for document in documents],
            documents=[document["text"] for document in documents],
            metadatas=[
                {"source": document["source"]}
                for document in documents
            ],
            embeddings=embeddings,
        )

    def retrieve(self, query: str, top_k: int = 3) -> list[dict]:
        query_embedding = self.embedding_model.encode(
            [query],
            normalize_embeddings=True,
        ).tolist()

        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )

        retrieved = []

        for index in range(len(results["ids"][0])):
            retrieved.append(
                {
                    "id": results["ids"][0][index],
                    "text": results["documents"][0][index],
                    "source": results["metadatas"][0][index]["source"],
                    "distance": results["distances"][0][index],
                }
            )

        return retrieved


if __name__ == "__main__":
    knowledge_base = KnowledgeBase()
    knowledge_base.build_index()

    print("Knowledge base created successfully.")
    print("Documents indexed:", knowledge_base.collection.count())