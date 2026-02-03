import uvicorn
import pytesseract
# from pdf_string import PDFTextExtractor
import fitz
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import subprocess
import json
import io
import pytesseract
from PIL import Image
import tempfile
import os
class PDFTextExtractor:
    def is_scanned_page(self, page) -> bool:
        text = page.get_text().strip()
        return len(text) < 50

    def extract_text_from_bytes(self, pdf_bytes: bytes) -> str:
        # Save bytes to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(pdf_bytes)
            tmp_path = tmp_file.name
        
        try:
            doc = fitz.open(tmp_path)
            full_text = ""

            for page in doc:
                if self.is_scanned_page(page):
                    # Use OCR for scanned pages
                    pix = page.get_pixmap(matrix=fitz.Matrix(3, 3), alpha=False)
                    img = Image.open(io.BytesIO(pix.tobytes("png")))
                    text = pytesseract.image_to_string(
                        img, lang="rus+uzb_cyrl+eng", config="--psm 6 --oem 3"
                    )
                else:
                    # Extract text directly
                    text = page.get_text()

                full_text += text + "\n\n"

            doc.close()
            return full_text.strip()
        
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
