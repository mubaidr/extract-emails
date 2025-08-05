# PDF Email Extractor

Extracts emails from the **first page** of all PDFs in a folder.  
If the first page is an image, OCR is used to extract text.  
Results are saved to a CSV file.

---

## Requirements

Install [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki):

- **Linux**: `sudo apt install tesseract-ocr`
- **macOS**: `brew install tesseract`
- **Windows**: Download from GitHub and add to PATH.

---

## Install Python dependencies

Using `uv` (recommended):
```bash
uv pip install -r requirements.txt
```

Or using pip:
```bash
pip install -r requirements.txt
```

---

## Run

Put your PDFs in a folder (e.g., `RP-cvs-pdf`) and run:
```bash
python extract_emails.py RP-cvs-pdf emails.csv
```

- `RP-cvs-pdf` → folder containing PDFs  
- `emails.csv` → output CSV file with `file_name, emails`

---

## Output

`emails.csv` contains:
```
file_name,emails
file1.pdf,email1@example.com
file2.pdf,
file3.pdf,email2@example.com,email3@example.com
```
If no emails are found, the `emails` column is empty.
