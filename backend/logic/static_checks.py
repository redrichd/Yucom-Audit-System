from typing import List, Dict, Any
import uuid

from collections import defaultdict

def check_static_rules(parsed_pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    實作 YC01 系列靜態欄位檢查 (支援跨頁判定):
    - YC01-5: 身心狀況 (Header Row Check)
    - YC01-7: TOCC/體溫 (Check numeric/text presence)
    """
    anomalies = []
    
    # 1. Group Pages
    groups = defaultdict(list)
    for p in parsed_pages:
        key = p.get("group_id") or "unknown"
        groups[key].append(p)

    for group_key, pages in groups.items():
        # Check Temp in Whole Group
        group_has_temp = False
        
        for page in pages:
            # More robust check: use raw_text instead of words list
            # This handles cases where '體溫' might be split or merged differently in tokenization
            raw_text = page.get("raw_text", "")
            if "體溫" in raw_text:
                 group_has_temp = True
                 break
        
        if not group_has_temp:
             # Report ALL pages in group
             page_nums = [str(p['page']) for p in pages]
             page_range = ", ".join(page_nums)
             
             # Use the first page for coordinate anchor
             p0 = pages[0]
             
             anomalies.append({
                "id": str(uuid.uuid4()),
                "rule_id": "YC01-7",
                "status": "WARN",
                "message": f"未偵測到 '體溫' 欄位，請檢核這些頁面: {page_range}。",
                "coordinates": {
                    "page": p0['page'], 
                    "x": 0, "y": 0, "w": 0, "h": 0
                }
            })
            
        # YC01-5 Body Status can be added similarly here

    return anomalies
