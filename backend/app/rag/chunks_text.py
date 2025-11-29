import os
import json
import uuid

INPUT_DIR = "data/cleaned"
OUTPUT_DIR = "data/chunks"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "chunks.jsonl")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Rough char limits to target ~400–700 tokens
MAX_CHARS = 1500
MIN_CHARS = 600


def load_pages(file_path: str):
    """
    Loads cleaned pages from a JSONL file.
    Each line: { "page": int, "text": str }
    """
    pages = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            rec = json.loads(line)
            page_no = rec.get("page")
            text = rec.get("text", "").strip()
            if not text:
                continue
            pages.append({"page": page_no, "text": text})
    return pages


def make_chunks_from_pages(pages, source_name: str):
    """
    Greedy char-based chunking across pages.
    Returns list of chunk dicts.
    """
    chunks = []
    buffer = []
    buffer_len = 0
    chunk_start_page = None
    chunk_end_page = None

    for p in pages:
        page_no = p["page"]
        text = p["text"]

        if chunk_start_page is None:
            chunk_start_page = page_no

        candidate_len = buffer_len + len(text) + 1  # +1 for newline

        # If adding this page makes it too big, flush current chunk
        if buffer and candidate_len > MAX_CHARS:
            merged_text = "\n\n".join(buffer).strip()
            if merged_text:
                chunks.append({
                    "id": str(uuid.uuid4()),
                    "source": source_name,
                    "page_start": chunk_start_page,
                    "page_end": chunk_end_page,
                    "text": merged_text,
                })

            # Reset buffer
            buffer = [text]
            buffer_len = len(text)
            chunk_start_page = page_no
            chunk_end_page = page_no
        else:
            buffer.append(text)
            buffer_len = candidate_len
            chunk_end_page = page_no

    # Flush last buffer
    if buffer:
        merged_text = "\n\n".join(buffer).strip()
        if merged_text:
            chunks.append({
                "id": str(uuid.uuid4()),
                "source": source_name,
                "page_start": chunk_start_page,
                "page_end": chunk_end_page,
                "text": merged_text,
            })

    # Optionally, merge very small chunks with previous one
    merged_chunks = []
    for chunk in chunks:
        if merged_chunks and len(chunk["text"]) < MIN_CHARS:
            # Append to previous chunk
            prev = merged_chunks[-1]
            prev["text"] = prev["text"].rstrip() + "\n\n" + chunk["text"]
            prev["page_end"] = chunk["page_end"]
        else:
            merged_chunks.append(chunk)

    return merged_chunks


def process_all_files():
    all_chunks = []

    for filename in os.listdir(INPUT_DIR):
        if not filename.endswith(".jsonl"):
            continue

        input_path = os.path.join(INPUT_DIR, filename)
        source_name = filename.replace(".jsonl", "")

        print(f"Chunking: {filename}")
        pages = load_pages(input_path)
        if not pages:
            print(f" -> No pages after cleaning, skipping {filename}")
            continue

        chunks = make_chunks_from_pages(pages, source_name)
        print(f" -> Created {len(chunks)} chunks from {filename}")
        all_chunks.extend(chunks)

    # Write all chunks to single JSONL
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f_out:
        for ch in all_chunks:
            f_out.write(json.dumps(ch, ensure_ascii=False) + "\n")

    print(f"\nTotal chunks written: {len(all_chunks)}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    process_all_files()
