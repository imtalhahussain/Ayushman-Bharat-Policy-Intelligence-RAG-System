from typing import List, Dict, Any

from .vector_store import (
    get_chroma_client,
    get_or_create_collection,
    embed_texts,
)


def retrieve_top_k(query: str, k: int = 3) -> List[Dict[str, Any]]:
    """
    Returns list of dicts:
    [
      {
        "source": str,
        "page_start": int,
        "page_end": int,
        "text": str,
        "distance": float
      }, ...
    ]
    """
    client = get_chroma_client()
    collection = get_or_create_collection(client)

    query_emb = embed_texts([query])

    results = collection.query(
        query_embeddings=query_emb,
        n_results=k,
    )

    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    dists = results.get("distances", [[]])[0]

    out = []
    for doc, meta, dist in zip(docs, metas, dists):
        if not doc:
            continue
        out.append(
            {
                "source": meta.get("source"),
                "page_start": meta.get("page_start"),
                "page_end": meta.get("page_end"),
                "text": doc,
                "distance": float(dist),
            }
        )

    return out