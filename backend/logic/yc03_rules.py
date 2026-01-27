from typing import List, Dict, Any
import uuid
import re

def check_ba16_1_requirements(parsed_pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    YC03-1: BA16-1 代購備註檢查
    
    規則：
    1. 偵測表格中是否包含 "BA16-1" (或 "代購或代領") 的服務項目。
    2. 若該項目當日有勾選 (或有時數)，則檢查對應的「服務執行概況」欄位。
    3. 概況欄位必須包含：
       - 金額符號或關鍵字 ($, 元, 金額)
       - 代購品項 (便當, 餐, 飯, 麵, 菜, 伙食...等)
    
    Implementation Logic:
    Since dealing with table structure in PDF is complex, we use a coordinate-based heuristic:
    1. Find "BA16-1" row.
    2. Check which columns (Days) have marks (usually "1" or checkmark) in that row.
    3. For those days, look down the column to the "服務執行概況" row.
    4. Extract text from that cell.
    5. Regex match for requirements.
    """
    anomalies = []
    
    # Keywords for validation
    money_pattern = re.compile(r'(\$|元|[0-9]+元|金額)')
    item_pattern = re.compile(r'(便當|餐|飯|麵|菜|食|購|買)')

    for page in parsed_pages:
        words = page.get("words", [])
        page_num = page.get("page")
        
        # 1. 尋找 BA16-1 關鍵字的 row
        ba16_label = next((w for w in words if "BA16-1" in w['text']), None)
        
        # 2. 尋找 "服務執行概況" row
        status_label = next((w for w in words if "服務執行概況" in w['text']), None)
        
        if not ba16_label or not status_label:
            continue
            
        # Define Row Y-coordinates
        ba16_row_y = float(ba16_label['top'])
        status_row_y = float(status_label['top'])
        status_row_bottom = status_row_y + 100 # Approx cell height
        
        # 3. 掃描 BA16-1 列，找出有勾選 (有文字 "1" 或其他標記) 的欄位 X 區間
        # 假設表格欄位是垂直對齊的
        # 我們掃描 BA16 row 附近的所有文字
        row_content = [w for w in words if abs(float(w['top']) - ba16_row_y) < 10]
        
        for item in row_content:
            # 排除 BA16-1 標籤本身與左側欄位
            if float(item['x0']) < float(ba16_label['x1']):
                continue
                
            # 若發現 "1" 或類似標記，代表該欄位當天有此服務
            if item['text'] == "1": 
                # 這是目標欄位 (Day Column)
                col_center_x = (float(item['x0']) + float(item['x1'])) / 2
                
                # 4. 在此 X 座標向下尋找對應的 "服務執行概況" 儲存格內容
                # Define cell ROI in the status row
                cell_x_range_min = col_center_x - 20 # 假設欄寬約 40~50
                cell_x_range_max = col_center_x + 20
                
                cell_text_words = [
                    w for w in words 
                    if (status_row_y < float(w['top']) < status_row_bottom) and
                       (cell_x_range_min < float(w['x0']) < cell_x_range_max)
                ]
                
                cell_full_text = "".join([w['text'] for w in cell_text_words])
                
                # 5. 驗證內容
                has_money = money_pattern.search(cell_full_text)
                has_item = item_pattern.search(cell_full_text)
                
                if not (has_money and has_item):
                    anomalies.append({
                        "id": str(uuid.uuid4()),
                        "rule_id": "YC03-1",
                        "status": "FAIL",
                        "message": f"偵測到 BA16-1 服務，但概況欄位未完整說明代購品項與金額 (目前內容: {cell_full_text or '空'})。",
                        "coordinates": {
                            "page": page_num,
                            "x": float(item['x0']), # Highlight the service checkmark first
                            "y": float(item['top']),
                            "w": float(item['x1'] - item['x0']),
                            "h": float(item['bottom'] - item['top'])
                        }
                    })

    return anomalies
