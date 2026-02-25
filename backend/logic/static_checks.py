def check_static_rules(page, page_number):
    """
    修正後的靜態規則，現在可以正確接收頁碼參數
    """
    errors = []
    text = page.extract_text() or ""
    
    # 範例：檢查是否有特定關鍵字
    if "悠康事業有限公司" not in text and page_number == 1:
        errors.append({
            "page": page_number,
            "type": "標題錯誤",
            "message": f"第 {page_number} 頁：找不到悠康機構標題"
        })
        
    return errors