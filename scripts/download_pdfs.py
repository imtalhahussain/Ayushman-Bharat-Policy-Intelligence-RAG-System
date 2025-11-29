# scripts/load_pdfs.py

import fitz 
import json
import os

PDF_DIR = "data/pdfs/"
OUTPUT_DIR = "data/extracted/"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    pages = []

    for page_number, page in enumerate(doc):
        text = page.get_text("text")
        pages.append({
            "page": page_number + 1,
            "text": text
        })
    
    return pages

def process_all_pdfs():
    for filename in os.listdir(PDF_DIR):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(PDF_DIR, filename)
            print(f"Processing: {filename}")

            pages = extract_text_from_pdf(pdf_path)
            
            output_path = os.path.join(
                OUTPUT_DIR,
                filename.replace(".pdf", ".jsonl")
            )

            with open(output_path, "w", encoding="utf-8") as f:
                for page in pages:
                    f.write(json.dumps(page, ensure_ascii=False) + "\n")

            print(f"Saved → {output_path}")

if __name__ == "__main__":
    process_all_pdfs()
