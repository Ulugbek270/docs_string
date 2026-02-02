import re
import io

import pytesseract

from PIL import Image
import fitz
class PDFTextExtractor:
    def is_scanned_page(self, page) -> bool:
        text = page.get_text().strip()
        return len(text) < 50

    def extract_text(self, pdf_path: str) -> str:
        doc = fitz.open(pdf_path)
        full_text = ""

        for page in doc:
            if self.is_scanned_page(page):
                pix = page.get_pixmap(matrix=fitz.Matrix(3, 3), alpha=False)
                img = Image.open(io.BytesIO(pix.tobytes("png")))
                text = pytesseract.image_to_string(
                    img, lang="rus+uzb_cyrl+eng", config="--psm 6 --oem 3"
                )
            else:
                text = page.get_text()

            full_text += text + "\n\n"

        doc.close()
        return full_text

extractor = PDFTextExtractor()
text = extractor.extract_text("./doc1.pdf")
print(text)