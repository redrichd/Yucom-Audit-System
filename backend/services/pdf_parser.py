import pdfplumber
import io
import logging
from logic.yc01_rules import check_time_overlaps
from logic.yc02_rules import check_signature_fields
from logic.static_checks import check_static_rules

# 設定日誌以利在 Render Logs 觀察進度
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def audit_pdf_stream(pdf_bytes: bytes):
    """
    流式稽核：一次只讀一頁進入記憶體，稽核完畢即釋放。
    """
    all_errors = []
    
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            total_pages = len(pdf.pages)
            logger.info(f"開始流式稽核，總計 {total_pages} 頁")

            for i, page in enumerate(pdf.pages):
                page_num = i + 1
                
                # --- 在此處呼叫各個規則檢查 ---
                # 我們直接把 page 物件傳進去，這樣規則內就能辨識座標與表格
                
                # 1. 檢查時間重疊 (YC01)
                all_errors.extend(check_time_overlaps(page, page_num))
                
                # 2. 檢查簽名欄位 (YC02)
                all_errors.extend(check_signature_fields(page, page_num))
                
                # 3. 檢查其他靜態規則
                all_errors.extend(check_static_rules(page, page_num))

                # 每處理 20 頁回報一次進度，避免 Render 認為程式當掉
                if page_num % 20 == 0:
                    logger.info(f"進度：已完成 {page_num}/{total_pages} 頁稽核...")

        logger.info("全數稽核完成")
        return all_errors

    except Exception as e:
        logger.error(f"稽核過程中發生錯誤: {str(e)}")
        raise e