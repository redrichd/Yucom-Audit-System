import pdfplumber
import io
import logging
from logic.yc01_rules import check_time_overlaps
from logic.yc02_rules import check_signature_fields
from logic.static_checks import check_static_rules

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def audit_pdf_stream(pdf_bytes: bytes):
    all_errors = []
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            total_pages = len(pdf.pages)
            logger.info(f"開始分析 PDF，共 {total_pages} 頁")

            for i, page in enumerate(pdf.pages):
                page_num = i + 1
                
                # 關鍵：這裡必須統一傳入兩個參數
                all_errors.extend(check_time_overlaps(page, page_num))
                all_errors.extend(check_signature_fields(page, page_num))
                all_errors.extend(check_static_rules(page, page_num))

                if page_num % 50 == 0:
                    logger.info(f"進度：已處理 {page_num}/{total_pages} 頁")

        return all_errors
    except Exception as e:
        logger.error(f"分析中斷: {str(e)}")
        raise e