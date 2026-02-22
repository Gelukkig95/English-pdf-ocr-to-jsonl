# streaming-ocr-to-jsonl (low-memory)

Convert a folder of PDFs into **SFT-ready JSONL** using **streaming OCR** (processes pages in small chunks so it won’t crash on large PDFs).

This repo is useful for building **English writing datasets** (e.g., fiction scene prompts) from scanned PDFs or PDF documents.

---

## Features

- Low-memory streaming OCR (no full-PDF image loading)
- Outputs instruction-style JSONL for SFT
- Chunking: N pages → 1 dataset sample
- Works on a folder of PDFs
- Instruction templates for English fiction generation

---

## Output format (JSONL)

Each line is a JSON object:

```json
{"instruction":"...","input":"...","output":""}

---

# requirements

requests
beautifulsoup4
pdf2image
pytesseract
Pillow
openai
tqdm
