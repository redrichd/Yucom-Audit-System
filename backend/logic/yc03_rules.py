import re

def check_ba16_1_requirements(page, page_number):
    errors = []
    try:
        words = page.extract_words()
        if not words:
            return errors
            
        money_pattern = re.compile(r'(\$|元|[0-9]+元|金額)')
        item_pattern = re.compile(r'(便當|餐|飯|麵|菜|食|購|買)')
        
        ba16_label = next((w for w in words if "BA16-1" in w['text']), None)
        status_label = next((w for w in words if "服務執行概況" in w['text']), None)
        
        if not ba16_label or not status_label:
            return errors
            
        ba16_row_y = float(ba16_label['top'])
        status_row_y = float(status_label['top'])
        status_row_bottom = status_row_y + 100 
        
        row_content = [w for w in words if abs(float(w['top']) - ba16_row_y) < 10]
        
        for item in row_content:
            if float(item['x0']) < float(ba16_label['x1']):
                continue
                
            if item['text'] == "1": 
                col_center_x = (float(item['x0']) + float(item['x1'])) / 2
                
                cell_x_range_min = col_center_x - 20 
                cell_x_range_max = col_center_x + 20
                
                cell_text_words = [
                    w for w in words 
                    if (status_row_y < float(w['top']) < status_row_bottom) and
                       (cell_x_range_min < float(w['x0']) < cell_x_range_max)
                ]
                
                cell_full_text = "".join([w['text'] for w in cell_text_words])
                
                if not (money_pattern.search(cell_full_text) and item_pattern.search(cell_full_text)):
                    errors.append({
                        "page": page_number,
                        "message": f"BA16-1 代購服務概況未說明品項與金額 (內容: {cell_full_text or '空'})"
                    })
    except Exception as e:
        print(f"YC03 檢查錯誤: {str(e)}")
        
    return errors