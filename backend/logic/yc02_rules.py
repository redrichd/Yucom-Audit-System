def check_signature_fields(page, page_number):
    errors = []
    try:
        w, h = float(page.width), float(page.height)
        
        # ⚠️ 修正：pdfplumber 的格式為 (左x0, 頂top, 右x1, 底bottom)
        # 根據您的圖片，簽名欄位大約在下半部，X 軸從 150 到 550
        boxes = {
            "照服員": (150, 640, 550, 700),
            "個案": (150, 700, 550, 760)
        }

        for name, bbox in boxes.items():
            # 安全檢查，確保不會超出頁面邊界
            safe_bbox = (
                max(0, bbox[0]), max(0, bbox[1]), 
                min(w, bbox[2]), min(h, bbox[3])
            )
            
            crop = page.within_bbox(safe_bbox)
            
            # 檢查是否有文字、圖片或手寫繪圖軌跡
            has_content = (
                len(crop.extract_text() or "") > 0 or 
                len(crop.images) > 0 or 
                len(crop.objects.get("curve", [])) > 0 or
                len(crop.objects.get("line", [])) > 0
            )
            
            if not has_content:
                errors.append({"page": page_number, "message": f"偵測到【{name}】簽名欄位空白"})
                
    except Exception as e:
        print(f"第 {page_number} 頁簽名檢查錯誤: {str(e)}")
        
    return errors