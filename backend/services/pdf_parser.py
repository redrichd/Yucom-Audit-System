import pdfplumber
import io
import logging
from logic.yc01_rules import check_time_overlaps
from logic.yc02_rules import check_signature_fields
from logic.static_checks import check_static_rules

logger = logging.getLogger(__name__)

def audit_pdf_stream(pdf_bytes: bytes):
    all_errors = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for i, page in enumerate(pdf.pages):
            page_num = i + 1
            # 必須傳入兩個參數，解決 TypeError
            all_errors.extend(check_time_overlaps(page, page_num))
            all_errors.extend(check_signature_fields(page, page_num))
            all_errors.extend(check_static_rules(page, page_num))
    return all_errors