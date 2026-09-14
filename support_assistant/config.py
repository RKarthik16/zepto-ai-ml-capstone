import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CORPUS_DIR = BASE_DIR / "corpus"
CHROMA_DIR = BASE_DIR / "chroma_db"

MOCK_LLM = os.getenv("MOCK_LLM", "1") != "0"

COLLECTION_NAME = "zepto_policy_collection"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"