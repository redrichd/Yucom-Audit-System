# backend/logic/yc02_rules.py

def check_signature_fields(page, page_number):
    """
    優化版：同時檢查文字與圖像物件，防止手寫簽名誤判
    """
    errors = []
    
    # 1. 定義簽名欄位的座標 (這裡需要根據 YUCOM 表格實際位置微調)
    # 範例座標：[頂, 左, 底, 右]
    caregiver_box = (650, 200, 750, 400) # 照服員簽名區
    client_box = (760, 200, 850, 400)    # 個案簽名區

    def is_box_blank(bbox):
        # 裁剪該區域
        crop = page.within_bbox(bbox)
        
        # 檢查該區域是否包含：文字 OR 圖片 OR 繪圖路徑
        has_text = len(crop.extract_text() or "") > 0
        has_images = len(crop.images) > 0
        has_drawings = len(crop.objects.get("curve", [])) > 0 or len(crop.objects.get("line", [])) > 0
        
        # 只要有任何一樣，就代表「不空白」
        return not (has_text or has_images or has_drawings)

    # 執行稽核
    if is_box_blank(caregiver_box):
        errors.append({"page": page_number, "message": f"第 {page_number} 頁：偵測到照服員簽名欄位空白"})
        
    if is_box_blank(client_box):
        errors.append({"page": page_number, "message": f"第 {page_number} 頁：偵測到個案簽名欄位空白"})

    return errors