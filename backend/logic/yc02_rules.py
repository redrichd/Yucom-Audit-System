# backend/logic/yc02_rules.py

def check_signature_fields(page, page_number):
    errors = []
    try:
        words = page.extract_words()
        if not words:
            return errors

        # 1. 抓取關鍵標籤 Y 座標
        cg_label = next((w for w in words if "照服員" in w['text']), None)
        cl_label = next((w for w in words if "個案簽名" in w['text'] or "代理人" in w['text']), None)
        date_label = next((w for w in words if "日期" in w['text']), None)
        
        if not cg_label or not cl_label or not date_label:
            return errors

        cg_y = float(cg_label['top'])
        cl_y = float(cl_label['top'])
        date_row_y = float(date_label['top'])

        # 【關鍵修正】：動態計算簽名欄位的高度，避免掃描到底部的督導名字
        row_height = cl_y - cg_y
        client_y_bottom = cl_y + row_height + 15 # 多加 15 像素容錯，絕不碰到頁底

        # 2. 找出這頁有提供服務的「日期欄位」
        service_days = [
            w for w in words 
            if abs(float(w['top']) - date_row_y) < 10 and float(w['x0']) > float(date_label['x1'])
        ]

        def cell_has_signature(y_min, y_max, x_center):
            y_top = y_min - 5
            y_bot = y_max + 5
            # 設定緊縮的 X 軸寬度，避免碰到垂直格線或隔壁欄位
            x_min = x_center - 18
            x_max = x_center + 18

            # A. 檢查打字文字
            for w in words:
                if y_top <= float(w['top']) <= y_bot and x_min <= float(w['x0']) <= x_max:
                    if len(w['text'].strip()) > 0: return True

            # B. 檢查圖片檔 (電子印章)
            for img in page.images:
                if y_top <= float(img['top']) <= y_bot and x_min <= float(img['x0']) <= x_max:
                    return True

            # C. 檢查數位筆跡與手寫線條
            for obj_type in ["curve", "line", "rect"]:
                for obj in page.objects.get(obj_type, []):
                    obj_top = float(obj.get('top', 0))
                    obj_bot = float(obj.get('bottom', 0))
                    obj_x0 = float(obj.get('x0', 0))
                    obj_x1 = float(obj.get('x1', 0))
                    
                    width = abs(obj_x1 - obj_x0)
                    height = abs(obj_bot - obj_top)

                    # 過濾掉表格的垂直與水平格線
                    if width < 3 and height > 20: continue
                    if height < 3 and width > 20: continue
                    
                    # 如果物件有部分落入我們劃定的儲存格內，就判定為有簽名
                    if (obj_bot >= y_top and obj_top <= y_bot and 
                        obj_x1 >= x_min and obj_x0 <= x_max):
                        return True
            return False

        # 3. 逐日檢查
        for day in service_days:
            day_text = day['text']
            x_center = (float(day['x0']) + float(day['x1'])) / 2

            # 照服員簽名檢查 (您說沒問題，我們繼續保留這個邏輯)
            if not cell_has_signature(cg_y, cl_y, x_center):
                errors.append({"page": page_number, "message": f"偵測到 {day_text} 日【照服員】簽名空白"})

            # 個案簽名檢查 (y 範圍: cl_y 到 client_y_bottom，不再掃描到底部！)
            if not cell_has_signature(cl_y, client_y_bottom, x_center):
                errors.append({"page": page_number, "message": f"偵測到 {day_text} 日【個案】簽名空白"})

    except Exception as e:
        print(f"第 {page_number} 頁簽名檢查錯誤: {str(e)}")
        
    return errors