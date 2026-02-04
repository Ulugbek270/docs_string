import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from src.schemas.response import Response_Json
from src.scripts.pdf_text_extractor import PDFTextExtractor
import logging
from src.scripts.call_ollama import call_ollama

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.post("/extract", response_model=Response_Json)
async def extract_from_pdf(file: UploadFile = File(...)):

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Send pdf only")

    try:
        pdf_bytes = await file.read()

        extractor = PDFTextExtractor()
        pdf_text = extractor.extract_text_from_bytes(pdf_bytes)

        if not pdf_text or len(pdf_text) < 50:
            raise HTTPException(
                status_code=400, detail="PDF appears to be empty or unreadable"
            )

        result = call_ollama(pdf_text)

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.info(e)
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

