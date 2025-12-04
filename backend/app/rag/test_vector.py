# backend/app/rag/test_vector.py

from .vector_store import (
    get_chroma_client,
    get_or_create_collection,
    embed_texts,
)
from .ingest import load_chunks  # 👈 only load_chunks, not ingest_chunks
from tqdm import tqdm


def ensure_collection_ready():
    """
    Ensure the Chroma collection has data.
    If empty, we ingest INTO THIS client/collection.
    """
    client = get_chroma_client()
    collection = get_or_create_collection(client)

    count = collection.count()
    print("Collection count BEFORE ensure:", count)

    if count == 0:
        print("Collection is empty. Ingesting chunks into this collection now...")

        chunks = load_chunks()
        print(f"Total chunks to ingest: {len(chunks)}")

        ids = []
        texts = []
        metadatas = []

        for ch in tqdm(chunks):
            ids.append(ch["id"])
            texts.append(ch["text"])
            metadatas.append({
                "source": ch.get("source"),
                "page_start": ch.get("page_start"),
                "page_end": ch.get("page_end"),
            })

        print("Embedding texts...")
        embeddings = embed_texts(texts)

        print("Adding to collection...")
        collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=texts,
        )

        print("Collection count AFTER inline ingest:", collection.count())

    return client, collection


def test_query(query: str, k: int = 3):
    client, collection = ensure_collection_ready()

    query_emb = embed_texts([query])

    results = collection.query(
        query_embeddings=query_emb,
        n_results=k,
    )

    return results


if __name__ == "__main__":
    q = input("Enter your query: ")

    res = test_query(q, k=3)

    print("\n=== RAW RESULT KEYS ===")
    print(res.keys())

    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]

    print(f"\nTotal results: {len(docs)}")

    if not docs:
        print("No documents returned, even after inline ingestion.")
    else:
        print("\nTop Chunks:")
        for i, (doc, meta) in enumerate(zip(docs, metas), start=1):
            print(f"\nRESULT {i} ------------------")
            print("Source:", meta.get("source"))
            print("Pages :", meta.get("page_start"), "-", meta.get("page_end"))
            snippet = doc[:500] + "..." if len(doc) > 500 else doc
            print("\nText Snippet:\n", snippet)
