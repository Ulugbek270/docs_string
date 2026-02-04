import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
import subprocess
import json
from src.models.response import Response_Json
from src.scripts.pdf_text_extractor import PDFTextExtractor
import logging
from src.scripts.call_ollama import call_ollama
from src.routers import auth, extract


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
async def healthy_check():
    return {"health": "good"}


app.include_router(auth.app)
app.include_router(extract.app)

# if __name__ == "__main__":
   
#     uvicorn.run(app, host="0.0.0.0", port=8011, reload=True)