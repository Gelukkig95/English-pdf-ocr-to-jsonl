import os
import json
import gc
import pytesseract
from pdf2image import convert_from_path

FICTION_INSTRUCTION = (
    "Write an English short story scene inspired by the text below. "
    "Keep a consistent point of view and tense. Use concrete sensory details. "
    "Include dialogue where it fits. End with a clear beat or hook. "
    "Length: ~800-1200 words."
)

def ocr_pdf_streaming(pdf_path, out_f, dpi=120, chunk_pages=3, lang="eng"):
    print(f"\n🧾 OCR starts: {pdf_path}")

    page = 1
    while True:
        first_page = page
        last_page = page + chunk_pages - 1

        images = convert_from_path(
            pdf_path,
            dpi=dpi,
            first_page=first_page,
            last_page=last_page,
            fmt="png"
        )
        if not images:
            break

        parts = []
        for idx, img in enumerate(images, start=first_page):
            text = pytesseract.image_to_string(img, lang=lang).strip()
            if text:
                print(f"  ✔ p{idx}: OCR ok")
                parts.append(text)
            else:
                print(f"  ❗ p{idx}: empty")

        joined = "\n".join(parts).strip()
        if joined:
            entry = {
                "instruction": FICTION_INSTRUCTION,
                "input": joined,
                "output": ""
            }
            out_f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        del images
        gc.collect()
        page += chunk_pages

def process_all_pdfs(input_folder, output_jsonl, dpi=120, chunk_pages=3, lang="eng"):
    pdfs = [f for f in os.listdir(input_folder) if f.lower().endswith(".pdf")]
    if not pdfs:
        print("No PDF files in folder:", input_folder)
        return

    os.makedirs(os.path.dirname(output_jsonl), exist_ok=True)

    print("📚 PDF files:", len(pdfs))
    with open(output_jsonl, "w", encoding="utf-8") as out_f:
        for i, pdf in enumerate(pdfs, start=1):
            pdf_path = os.path.join(input_folder, pdf)
            print(f"\n=== ({i}/{len(pdfs)}) {pdf} ===")
            ocr_pdf_streaming(pdf_path, out_f, dpi=dpi, chunk_pages=chunk_pages, lang=lang)

    print("\n All PDFs processed and saved to JSONL.")
    print("saving location:", output_jsonl)

if __name__ == "__main__":
    process_all_pdfs(
        input_folder="data/raw_pdf",                 
        output_jsonl="data/processed/pdf_dataset.jsonl",
        dpi=120,
        chunk_pages=3,
        lang="eng"
    )