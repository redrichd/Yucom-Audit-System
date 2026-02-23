from fastapi import APIRouter, File, UploadFile
from services.pdf_parser import audit_pdf_stream # 改用新的函數

router = APIRouter()

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """
    接收 PDF 並進行記憶體優化稽核
    """
    # 讀取檔案二進位資料
    file_content = await file.read()
    
    # 執行流式稽核 (這不會爆記憶體)
    audit_results = audit_pdf_stream(file_content)
    
    return {
        "status": "success",
        "total_errors": len(audit_results),
        "results": audit_results
    }