import os
import json
import re

# Input: raw extracted pages from load_pdfs.py
INPUT_DIR = "data/extracted"
# Output: cleaned pages
OUTPUT_DIR = "data/cleaned"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def clean_page_text(text: str) -> str:
    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove very common "Page X of Y" or "Page X" style lines
    lines = text.split("\n")
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()

        # Skip empty lines early
        if not stripped:
            cleaned_lines.append("")
            continue

        # Skip pure page markers
        if re.match(r"^page\s*\d+(\s*of\s*\d+)?$", stripped, re.IGNORECASE):
            continue
        if re.match(r"^\d{1,4}$", stripped):  # lines that are only numbers
            continue

        cleaned_lines.append(stripped)

    text = "\n".join(cleaned_lines)

    # Collapse multiple blank lines to max 2
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Collapse multiple spaces
    text = re.sub(r"[ \t]{2,}", " ", text)

    # Strip leading/trailing whitespace
    text = text.strip()

    return text


def process_file(input_path: str, output_path: str) -> None:
    with open(input_path, "r", encoding="utf-8") as f_in, \
         open(output_path, "w", encoding="utf-8") as f_out:

        for line in f_in:
            if not line.strip():
                continue

            record = json.loads(line)
            raw_text = record.get("text", "")
            cleaned_text = clean_page_text(raw_text)

            # Skip completely empty pages after cleaning
            if not cleaned_text:
                continue

            record["text"] = cleaned_text
            f_out.write(json.dumps(record, ensure_ascii=False) + "\n")


def process_all():
    for filename in os.listdir(INPUT_DIR):
        if not filename.endswith(".jsonl"):
            continue

        in_path = os.path.join(INPUT_DIR, filename)
        out_path = os.path.join(OUTPUT_DIR, filename)

        print(f"Cleaning: {filename}")
        process_file(in_path, out_path)
        print(f" -> Saved cleaned file: {out_path}")


if __name__ == "__main__":
    process_all()
