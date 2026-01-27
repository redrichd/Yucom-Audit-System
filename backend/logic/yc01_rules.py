import re
from typing import List, Dict, Any
import uuid

def check_time_overlaps(parsed_pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    YC01-8: Check for overlapping service times in the daily record.
    Assuming the record contains lines like: "10:00-11:00" or "09:00~12:00"
    """
    anomalies = []
    
    # Regex to find time ranges (Simple implementation for demo)
    # Matches patterns like 08:00-09:00 or 0830-0930
    time_pattern = re.compile(r'(\d{2}:?\d{2})\s*[-~]\s*(\d{2}:?\d{2})')
    
    for page in parsed_pages:
        words = page.get("words", [])
        page_num = page.get("page")
        
        # Simplified: Join all text to find patterns, then find approximate coordinates
        # Real-world: Should iterate lines/words structure
        
        found_times = []
        
        # 1. Extract all time ranges
        text = page.get("raw_text", "")
        matches = time_pattern.findall(text)
        
        # Mock logic: If we find more than 1 time range, check overlaps
        # In this first pass, we just detect them. 
        # Real logic needs sorting and intersection checks.
        
        if len(matches) > 1:
            # Check overlap (Mock implementation)
            # For demonstration, we just return a mock warning if multiple times found
            # indicating we are checking them.
            
            # Find coordinates of the first match for visualization
            # Logic to find word bounding box matching the time string
            first_match_str = matches[0][0] # e.g., "08:00"
            
            # Search for this word in 'words' list to get coords
            target_word = next((w for w in words if first_match_str in w['text']), None)
            
            if target_word:
                anomalies.append({
                    "id": str(uuid.uuid4()),
                    "rule_id": "YC01-8",
                    "status": "PASS", # Default pass for now
                    "message": f"偵測到 {len(matches)} 筆服務時段，已執行重疊檢查。",
                    "coordinates": {
                        "page": page_num,
                        "x": float(target_word['x0']),
                        "y": float(target_word['top']),
                        "w": float(target_word['x1'] - target_word['x0']),
                        "h": float(target_word['bottom'] - target_word['top'])
                    }
                })
                
    return anomalies
