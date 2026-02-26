# backend/logic/yc02_rules.py

def check_signature_fields(page, page_number):
    errors = []
    try:
        words = page.extract_words()
        if not words:
            return errors

        # 1. 找尋標籤位置 (動態定位 Y 座標，無懼表格伸縮)
        cg_label = next((w for w in words if "照服員" in w['text']), None)
        cl_label = next((w for w in words if "個案簽名" in w['text'] or "代理人" in w['text']), None)
        
        # 如果這頁沒有這兩個標籤，代表可能不是服務紀錄單，直接跳過
        if not cg_label or not cl_label:
            return errors

        cg_y = float(cg_label['top'])
        cl_y = float(cl_label['top'])
        page_h = float(page.height)
        cg_x1 = float(cg_label['x1'])
        cl_x1 = float(cl_label['x1'])

        def has_signature(y_min, y_max, label_x1):
            # 容錯範圍加大，允許字跡上下飄移 15 像素
            y_top = y_min - 15
            y_bot = y_max + 15
            
            # 方法 A: 檢查「打字」的文字 (若直接用鍵盤輸入名字)
            for w in words:
                if y_top <= float(w['top']) <= y_bot and float(w['x0']) > label_x1 + 5:
                    if len(w['text'].strip()) > 0:
                        return True
                        
            # 方法 B: 檢查「圖片」(貼上的印章或圖檔)
            for img in page.images:
                if y_top <= float(img['top']) <= y_bot and float(img['x0']) > label_x1:
                    return True
                    
            # 方法 C: 檢查「手寫軌跡」(數位筆跡通常儲存為 curve)
            curves = page.objects.get("curve", [])
            for c in curves:
                # 只要軌跡有一部分落在區間內就算數
                if float(c['top']) <= y_bot and float(c['bottom']) >= y_top and float(c['x0']) > label_x1:
                    return True
                    
            # 方法 D: 檢查「手寫短線」(某些簽名板會把筆跡轉成大量短線)
            lines = page.objects.get("line", [])
            short_lines = [
                l for l in lines 
                if float(l['top']) <= y_bot and float(l['bottom']) >= y_top 
                and float(l['x0']) > label_x1 
                and float(l['width']) < 100 # 排除長度大於 100 的表格格線
            ]
            if len(short_lines) > 5:  # 若有多條短線，視為手寫筆跡
                return True
                
            return False

        # 2. 執行透視掃描
        # 照服員區塊：從「照服員」的 Y 座標，掃描到「個案」的 Y 座標
        if not has_signature(cg_y, cl_y, cg_x1):
            errors.append({"page": page_number, "message": "偵測到【照服員】簽名欄位空白"})
        
        # 個案區塊：從「個案」的 Y 座標，掃描到頁面底部
        if not has_signature(cl_y, page_h, cl_x1):
            errors.append({"page": page_number, "message": "偵測到【個案】簽名欄位空白"})

    except Exception as e:
        # 出錯時記錄在 Render 後台，不讓系統崩潰
        print(f"第 {page_number} 頁簽名檢查錯誤: {str(e)}")
        
    return errors