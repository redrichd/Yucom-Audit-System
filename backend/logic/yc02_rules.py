def check_signature_fields(page, page_number):
    """
    精準稽核範例：利用座標或表格辨識特定欄位
    """
    errors = []
    
    # 範例：提取該頁面所有的表格
    tables = page.extract_tables()
    
    for table in tables:
        # 假設您的服務紀錄單表格中，簽名通常在最後一列
        # 您可以精準判斷表格內容是否為空
        for row in table:
            if "簽名" in str(row) and (not row[-1] or row[-1].strip() == ""):
                errors.append({
                    "page": page_number,
                    "type": "簽名漏缺",
                    "message": f"第 {page_number} 頁：偵測到簽名欄位空白"
                })
    
    return errors