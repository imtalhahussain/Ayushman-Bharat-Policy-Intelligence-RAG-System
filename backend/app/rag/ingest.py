# backend/app/rag/ingest.py

import json
import os
from tqdm import tqdm

from .vector_store import (
    get_chroma_client,
    get_or_create_collection,
    embed_texts,
)

CHUNKS_FILE = os.path.join("data", "chunks", "chunks.jsonl")


def load_chunks():
    if not os.path.exists(CHUNKS_FILE):
        raise FileNotFoundError(f"Chunks file not found at: {CHUNKS_FILE}")

    chunks = []
    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            chunks.append(rec)
    return chunks


def ingest_chunks():
    print(f"Using chunks file: {CHUNKS_FILE}")

    chunks = load_chunks()
    print(f"Total chunks loaded: {len(chunks)}")

    client = get_chroma_client()

    # Optional: clear old collection
    try:
        client.delete_collection("ayushman_policies")
        print("Deleted existing collection 'ayushman_policies' (if it existed).")
    except Exception:
        print("No existing collection to delete (or delete failed, continuing).")

    collection = get_or_create_collection(client)

    print("Collection count BEFORE add:", collection.count())

    ids = []
    texts = []
    metadatas = []

    print("Preparing texts for embedding...")
    for ch in tqdm(chunks):
        ids.append(ch["id"])
        texts.append(ch["text"])
        metadatas.append({
            "source": ch.get("source"),
            "page_start": ch.get("page_start"),
            "page_end": ch.get("page_end"),
        })

    print("Embedding texts (this may take a bit)...")
    embeddings = embed_texts(texts)

    print("Adding to Chroma collection...")
    collection.add(
        ids=ids,
        embeddings=embeddings,
        metadatas=metadatas,
        documents=texts,
    )

    print("Collection count AFTER add:", collection.count())
    print("Ingestion complete! (PersistentClient should store this on disk)")


if __name__ == "__main__":
    ingest_chunks()
