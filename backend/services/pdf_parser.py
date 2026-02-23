import pdfplumber
import io
import logging

# 設定日誌以利在 Render Logs 中觀察進度
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_pdf_bytes(pdf_bytes: bytes):
    """
    以分頁讀取並立即釋放資源的方式解析 PDF，
    專為記憶體受限環境（如 Render Free Tier）優化。
    """
    extracted_data = []
    
    try:
        # 使用 io.BytesIO 將二進位資料轉為類文件物件
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            total_pages = len(pdf.pages)
            logger.info(f"開始解析 PDF，總計 {total_pages} 頁")

            for i, page in enumerate(pdf.pages):
                # 1. 提取純文字（文字字串遠比頁面物件輕量）
                text = page.extract_text()
                
                # 2. 封裝成簡單的字典
                page_info = {
                    "page_number": i + 1,
                    "content": text if text else "",
                    # 如果有需要提取表格，可以在此處執行，但會增加記憶體消耗
                    # "tables": page.extract_tables() 
                }
                
                extracted_data.append(page_info)
                
                # 3. 每 50 頁在 Logs 紀錄一次進度，確認後端沒死機
                if (i + 1) % 50 == 0:
                    logger.info(f"已處理 {i + 1} / {total_pages} 頁...")

                # 在 loop 的下一步，目前的 'page' 物件會被 Python 垃圾回收機制標記為可釋放
                # 因為我們已經將需要的文字存入 extracted_data，不再引用 page 物件

        logger.info("PDF 解析完成")
        return extracted_data

    except Exception as e:
        logger.error(f"解析 PDF 時發生錯誤: {str(e)}")
        raise e