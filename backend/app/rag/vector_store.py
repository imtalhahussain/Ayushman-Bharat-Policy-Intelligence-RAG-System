import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# ---- Paths ----
BASE_DIR = os.path.abspath(os.getcwd())
CHROMA_DIR = os.path.join(BASE_DIR, "data", "chroma")

print(f"[vector_store] BASE_DIR   = {BASE_DIR}")
print(f"[vector_store] CHROMA_DIR = {CHROMA_DIR}")

# ---- Embeddings ----
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ---- Vector Store (singleton) ----
vectorstore = Chroma(
    persist_directory=CHROMA_DIR,
    embedding_function=embeddings,
)
