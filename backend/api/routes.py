from fastapi import APIRouter, File, UploadFile
from services.pdf_parser import audit_pdf_stream

router = APIRouter()

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_content = await file.read()
    results = audit_pdf_stream(file_content)
    
    return {
        "status": "success",
        "results": results
    }