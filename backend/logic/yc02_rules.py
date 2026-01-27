from typing import List, Dict, Any
import uuid

from collections import defaultdict

def check_signature_fields(parsed_pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    YC02-3: 檢查簽名欄位 (支援跨頁判定)
    
    Logic:
    1. Group pages by `case_id` (or `case_name` if id missing).
    2. Check each page in the group for signatures.
    3. If ANY page in the group has a valid signature, the entire group PASSES rule YC02-3.
    4. If NO page has signature, report Missing Signature (on the last page of the group).
    """
    anomalies = []
    
    # 1. Group Pages
    groups = defaultdict(list)
    for p in parsed_pages:
        # Key: group_id (Unique per record occurrence)
        key = p.get("group_id") or "unknown"
        groups[key].append(p)
        
    # 2. Process Each Group
    for group_key, pages in groups.items():
        group_has_signature = False
        
        # Check each page in this group
        for page in pages:
            words = page.get("words", [])
            page_width = float(page.get('width', 1000))
            
            non_text_objects = []
            non_text_objects.extend(page.get("rects", []))
            non_text_objects.extend(page.get("lines", []))
            non_text_objects.extend(page.get("curves", []))
            non_text_objects.extend(page.get("images", []))
            
            # Find signature label
            signature_labels = [w for w in words if "簽名" in w['text'] or "Signature" in w['text']]
            
            for label in signature_labels:
                label_x1 = float(label['x1'])
                label_top = float(label['top'])
                
                # ROI: Right side of label to End of Page
                roi_x0 = label_x1
                roi_x1 = page_width - 20 
                roi_y0 = label_top - 15  
                roi_y1 = label_top + 50 
                
                # Check Text
                found_in_page = False
                for w in words:
                    wx0 = float(w['x0'])
                    wy0 = float(w['top'])
                    if (roi_x0 < wx0 < roi_x1) and (roi_y0 < wy0 < roi_y1):
                         found_in_page = True
                         break
                
                # Check Non-Text
                if not found_in_page:
                    for obj in non_text_objects:
                        ox0 = float(obj.get('x0', 0))
                        oy0 = float(obj.get('top', 0))
                        if (roi_x0 - 20 < ox0 < roi_x1 + 20) and (roi_y0 - 20 < oy0 < roi_y1 + 20):
                             found_in_page = True
                             break
                
                if found_in_page:
                    group_has_signature = True
                    break # Break label loop
            
            if group_has_signature:
                break # Break page loop (One pass is enough for the group)
        
        # 3. Report Results
        if not group_has_signature:
            # If the whole group has no signature, flag the LAST page of the group
            last_page = pages[-1]
            anomalies.append({
                "id": str(uuid.uuid4()),
                "rule_id": "YC02-3",
                "status": "FAIL",
                "message": f"簽名欄位缺漏 (共{len(pages)}頁皆未簽名)。",
                "coordinates": {
                    "page": last_page['page'],
                    "x": 0, "y": 0, "w": 0, "h": 0 # General page error
                }
            })

    return anomalies
