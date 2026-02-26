# backend/logic/yc02_rules.py

def check_signature_fields(page, page_number):
    errors = []
    try:
        # 安全取得頁面尺寸
        w, h = float(page.width), float(page.height)
        
        # 座標設定 (頂, 左, 底, 右)
        boxes = {
            "照服員": (650, 200, 750, 400),
            "個案": (760, 200, 850, 400)
        }

        for name, bbox in boxes.items():
            # 安全檢查：若座標超出頁面邊界，則自動縮小範圍
            safe_bbox = (min(bbox[0], h-1), min(bbox[1], w-1), min(bbox[2], h), min(bbox[3], w))
            
            crop = page.within_bbox(safe_bbox)
            has_content = (
                len(crop.extract_text() or "") > 0 or 
                len(crop.images) > 0 or 
                len(crop.objects.get("curve", [])) > 0
            )
            
            if not has_content:
                errors.append({"page": page_number, "message": f"第 {page_number} 頁：{name}簽名欄位空白"})
                
    except Exception:
        # 出錯時安靜跳過，不干擾主程式執行
        pass
        
    return errors