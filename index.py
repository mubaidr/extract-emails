import os
import re
import csv
import pytesseract
from pdf2image import convert_from_path
from PyPDF2 import PdfReader

def extract_text_first_page(pdf_path):
    # Extract text from first page using PyPDF2
    with open(pdf_path, "rb") as f:
        reader = PdfReader(f)
        text = reader.pages[0].extract_text() if reader.pages else ""

    # If no text, fallback to OCR
    if not text.strip():
        images = convert_from_path(pdf_path, first_page=1, last_page=1)
        text = pytesseract.image_to_string(images[0])
    return text

def extract_emails(text):
    return re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)

def extract_phone_numbers(text):
    # Matches various phone number formats, including international and local
    phone_pattern = re.compile(r"""
        (?:\+?\d{1,3}[\s-]?)?            # country code
        (?:\(?\d{2,4}\)?[\s-]?)?        # area code
        \d{3,4}[\s-]?\d{3,4}            # main number
    """, re.VERBOSE)
    # Filter out numbers that are too short (e.g., less than 7 digits)
    numbers = [n.strip() for n in phone_pattern.findall(text) if len(re.sub(r'\D', '', n)) >= 7]
    return numbers

def process_pdfs(input_dir, output_csv):
    files = [f for f in os.listdir(input_dir) if f.lower().endswith(".pdf")]
    total = len(files)

    rows = []
    for idx, file in enumerate(files, start=1):
        path = os.path.join(input_dir, file)
        text = extract_text_first_page(path)
        emails = extract_emails(text)
        phones = extract_phone_numbers(text)
        rows.append([
            file,
            ", ".join(emails) if emails else "",
            ", ".join(phones) if phones else ""
        ])
        print(f"[{idx}/{total}] Processed: {file}")

    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["file_name", "emails", "phone_numbers"])
        writer.writerows(rows)

    print(f"\nDone! Extracted emails and phone numbers saved to {output_csv}")

# Example usage
process_pdfs("RP-cvs-pdf", "emails.csv")
