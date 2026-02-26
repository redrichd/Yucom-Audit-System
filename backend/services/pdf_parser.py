# backend/services/pdf_parser.py
import pdfplumber
import io
import logging

# 匯入規則
from logic.yc01_rules import check_time_overlaps
from logic.yc02_rules import check_signature_fields
from logic.static_checks import check_static_rules

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def audit_pdf_stream(pdf_bytes: bytes):
    all_errors = []
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            total = len(pdf.pages)
            logger.info(f"🚀 開始稽核任務：共 {total} 頁")

            for i, page in enumerate(pdf.pages):
                page_num = i + 1
                # 這行會在 Render Logs 即時跳出進度
                logger.info(f"📊 [進度] 稽核中: 第 {page_num} / {total} 頁...")

                try:
                    # 執行各項檢查
                    all_errors.extend(check_time_overlaps(page, page_num))
                    all_errors.extend(check_signature_fields(page, page_num))
                    all_errors.extend(check_static_rules(page, page_num))
                except Exception as page_err:
                    # 關鍵：若某一頁出錯，跳過它並繼續下一頁，不讓整個分析失敗
                    logger.error(f"❌ 第 {page_num} 頁處理發生錯誤（已跳過）: {str(page_err)}")
                    continue

        logger.info(f"✅ 稽核完成！共發現 {len(all_errors)} 項異常")
        return all_errors
    except Exception as e:
        logger.error(f"🚨 嚴重錯誤: {str(e)}")
        raise e