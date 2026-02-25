def check_time_overlaps(page, page_number):
    """
    檢查時間重疊規則 (YC01)
    """
    errors = []
    # 這裡放入原本的稽核邏輯，傳入的 page 是 pdfplumber 的頁面物件
    # 範例：
    # text = page.extract_text()
    # if "某個錯誤條件" in text:
    #     errors.append({
    #         "page": page_number,
    #         "type": "時間重疊",
    #         "message": f"第 {page_number} 頁偵測到服務時間重疊"
    #     })
    return errors