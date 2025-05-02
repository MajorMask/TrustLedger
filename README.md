# TrustLedger Backend

This is a Flask-based backend for OCR, translation, and watermarking of documents. It extracts text from images, translates it from Hungarian to English, and reconstructs the document with a watermark.

## Features
- Extract text from images using Tesseract OCR.
- Translate text from Hungarian to English using MarianMT.
- Reconstruct the document with the same design and add a watermark.
<img width="1097" alt="image" src="https://github.com/user-attachments/assets/e4b891a6-860e-4894-84d0-6785467028e3" />

## Requirements
- Python 3.10+
- Flask
- Transformers
- Torch
- Pillow
- Pytesseract

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/TrustLedger.git
   cd TrustLedger

   brew install tesseract
   brew install tesseract-lang
   export TESSDATA_PREFIX=/opt/homebrew/share/tessdata
   brew install poppler  # Required for pdf2image on macOS
