from typing import List, Dict, Any
import uuid
import re

def check_ba05_1_requirements(parsed_pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    YC04-1: BA05-1 備餐菜色檢查
    
    規則：
    1. 偵測表格中是否包含 "BA05-1" (或 "餐食照顧", "備餐") 的服務項目。
    2. 若該項目當日有勾選 (標記 "1")，則檢查對應的「服務執行概況」欄位。
    3. 概況欄位必須包含菜色關鍵字，例如：
       - 飯, 麵, 粥, 菜, 地瓜, 湯, 魚, 肉, 蛋, 水 (煮水)
       - 或其他常見食物描述
    
    Implementation Logic:
    (Same heuristic column/row scan as YC03-1)
    """
    anomalies = []
    
    # Keywords for food items
    food_pattern = re.compile(r'(飯|麵|粥|菜|素|葷|魚|肉|蛋|湯|地瓜|水|果|奶|餐)')

    for page in parsed_pages:
        words = page.get("words", [])
        page_num = page.get("page")
        
        # 1. 尋找 BA05-1 關鍵字的 row
        ba05_label = next((w for w in words if "BA05-1" in w['text'] or "BA05" in w['text']), None)
        
        # 2. 尋找 "服務執行概況" row
        status_label = next((w for w in words if "服務執行概況" in w['text']), None)
        
        if not ba05_label or not status_label:
            continue
            
        # Define Row Y-coordinates
        ba05_row_y = float(ba05_label['top'])
        status_row_y = float(status_label['top'])
        status_row_bottom = status_row_y + 120 # Approx cell height (allow slightly taller)
        
        # 3. 掃描 BA05-1 列
        row_content = [w for w in words if abs(float(w['top']) - ba05_row_y) < 10]
        
        for item in row_content:
            if float(item['x0']) < float(ba05_label['x1']):
                continue
                
            # 若發現 "1"
            if item['text'] == "1": 
                # Target column
                col_center_x = (float(item['x0']) + float(item['x1'])) / 2
                
                # 4. 向下尋找對應的 "服務執行概況"
                cell_x_range_min = col_center_x - 20 
                cell_x_range_max = col_center_x + 20
                
                cell_text_words = [
                    w for w in words 
                    if (status_row_y < float(w['top']) < status_row_bottom) and
                       (cell_x_range_min < float(w['x0']) < cell_x_range_max)
                ]
                
                cell_full_text = "".join([w['text'] for w in cell_text_words])
                
                # 5. 驗證內容
                has_food = food_pattern.search(cell_full_text)
                
                if not has_food:
                    anomalies.append({
                        "id": str(uuid.uuid4()),
                        "rule_id": "YC04-1",
                        "status": "FAIL",
                        "message": f"偵測到 BA05-1 備餐服務，但概況欄位未說明菜色 (如: 飯, 菜, 肉, 魚, 煮水)。",
                        "coordinates": {
                            "page": page_num,
                            "x": float(item['x0']),
                            "y": float(item['top']),
                            "w": float(item['x1'] - item['x0']),
                            "h": float(item['bottom'] - item['top'])
                        }
                    })

    return anomalies
