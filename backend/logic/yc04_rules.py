import re

def check_ba05_1_requirements(page, page_number):
    errors = []
    try:
        words = page.extract_words()
        if not words:
            return errors
            
        food_pattern = re.compile(r'(飯|麵|粥|菜|素|葷|魚|肉|蛋|湯|地瓜|水|果|奶|餐)')

        ba05_label = next((w for w in words if "BA05-1" in w['text'] or "BA05" in w['text']), None)
        status_label = next((w for w in words if "服務執行概況" in w['text']), None)
        
        if not ba05_label or not status_label:
            return errors
            
        ba05_row_y = float(ba05_label['top'])
        status_row_y = float(status_label['top'])
        status_row_bottom = status_row_y + 120 
        
        row_content = [w for w in words if abs(float(w['top']) - ba05_row_y) < 10]
        
        for item in row_content:
            if float(item['x0']) < float(ba05_label['x1']):
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
                
                if not food_pattern.search(cell_full_text):
                    errors.append({
                        "page": page_number,
                        "message": f"BA05-1 備餐服務概況未說明菜色 (內容: {cell_full_text or '空'})"
                    })
    except Exception as e:
        print(f"YC04 檢查錯誤: {str(e)}")
        
    return errors