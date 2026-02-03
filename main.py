import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
import subprocess
import json
from models import DocumentOutput
from pdf_text_extractor import PDFTextExtractor
app = FastAPI()


@app.get("/")
async def healthy_check():
    return {"health": "good"}


def call_ollama(pdf_text: str) -> dict:
    prompt = """Extract structured data from this Uzbek official document. Return ONLY valid JSON.

{
  "author": "name after 'Ijrochi:' (usually at bottom of document)",
  "doc_num": "document number (pattern: XXX/XX-XX-son)",
  "sender": "organization name from header in Uzbek",
  "date": "convert document date to format: DD.MM.YYYY",
  "receiver": "recipient name(s) or organization(s) listed after doc_num, before main text",
  "context": "FULL letter body from after recipients until signature block. Include all paragraphs about requirements, deadlines, instructions. Stop before 'Ilova', signatures, 'Ijrochi:'. Clean readable text only.",
  "address": "postal address from header",
  "phone_number": "phone number from document",
  "email": "email address",
  "summary": "brief summary of context in same language (Uzbek/Russian)",
  "code_doc": "code after 'Ҳужжат коди:'"
}

Context extraction rules:
- Skip fragments with /n or incomplete sentences at start
- Ignore 'Ilova X varaqda' - this counts pages, not content
- Take complete paragraphs only
- Remove page breaks, symbols like _________, excessive \\n
- Start from first full sentence after recipient section
- Stop at first footer element (Ilova/signature/Ijrochi)
- Preserve paragraph breaks with single \\n

Date examples: '2026-yil 26 yanvar' → '26.01.2026'

Return only JSON, no markdown, no explanation."""

    try:
        process = subprocess.Popen(
            ['ollama', 'run', 'qwen2.5:7b'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        full_input = f"{prompt}\n\n{pdf_text}"
        stdout, stderr = process.communicate(input=full_input, timeout=120)
        
        if process.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Ollama error: {stderr}")
        
        response = stdout.strip()
        
        # if '```' in response:
        #     parts = response.split('```')
        #     for part in parts:
        #         if part.strip().startswith('{') or part.strip().startswith('json'):
        #             response = part.replace('json', '', 1).strip()
        #             break
        
        result = json.loads(response)
        return result
        
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Invalid JSON from model: {str(e)}\nRaw: {stdout[:300]}"
        )
    except subprocess.TimeoutExpired:
        process.kill()
        raise HTTPException(status_code=504, detail="Processing timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ollama error: {str(e)}")

@app.post("/extract", response_model=DocumentOutput)
async def extract_from_pdf(file: UploadFile = File(...)):
    
    # if not file.filename.endswith('.pdf'):
    #     raise HTTPException(status_code=400, detail="Send pdf only")
    
    try:
        pdf_bytes = await file.read()
    
        extractor = PDFTextExtractor()
        pdf_text = extractor.extract_text_from_bytes(pdf_bytes)
        
        if not pdf_text or len(pdf_text) < 50:
            raise HTTPException(status_code=400, detail="PDF appears to be empty or unreadable")
        
        result = call_ollama(pdf_text)
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")


if __name__ == "__main__":
   
    uvicorn.run(app, host="0.0.0.0", port=8011, reload=True)