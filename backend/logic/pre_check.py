from typing import List, Dict, Any, Tuple
import re

def is_record_active(group_pages: List[Dict[str, Any]]) -> Tuple[bool, str]:
    """
    Check if a record group is "Active" (i.e., has been used/started).
    
    Logic:
    - Scans all pages in the group.
    - Looks for the "Date" (日期) row or similar indicators.
    - If NO day numbers (1-31) are found in the header row area, 
      the record is considered Inactive/Empty (e.g. pre-printed but unused).
      
    Returns:
        bool: True if active (should audit), False if inactive (should skip).
    """
    
    has_valid_dates = False
    date_label_found_in_group = False
    
    for page in group_pages:
        words = page.get("words", [])
        page_width = float(page.get("width", 1000))
        
        # 1. Find "日期" Label (Robust Search)
        date_label = None
        
        # Method A: Direct match
        date_label = next((w for w in words if "日期" in w['text']), None)
        
        # Method B: Split match ("日" then "期")
        if not date_label:
            sorted_words = sorted(words, key=lambda w: (float(w['top']), float(w['x0'])))
            for i, w in enumerate(sorted_words[:-1]):
                if "日" in w['text']:
                    next_w = sorted_words[i+1]
                    if "期" in next_w['text']:
                        y_diff = abs(float(w['top']) - float(next_w['top']))
                        x_diff = float(next_w['x0']) - float(w['x1'])
                        if y_diff < 10 and 0 <= x_diff < 40: # Widened x_diff
                            date_label = next_w 
                            break
        
        # Method C: Anchor by "星期" (Week) if Date label missing
        # The Date row is immediately ABOVE the Week row.
        week_label = None
        if not date_label:
             week_label = next((w for w in words if "星期" in w['text']), None)
             
        roi_defined = False
        roi_top, roi_bottom, roi_left, roi_right = 0, 0, 0, 0
        anchor_name = ""

        if date_label:
            # 2. Define ROI: Right of "日期"
            label_y_center = (float(date_label['top']) + float(date_label['bottom'])) / 2
            roi_top = label_y_center - 12  
            roi_bottom = label_y_center + 12
            roi_left = float(date_label['x1']) + 1
            roi_right = roi_left + 70
            roi_defined = True
            anchor_name = f"DateLabel({date_label['text']})"
            
        elif week_label:
            # Anchor 25px ABOVE Week label
            label_y_center = (float(week_label['top']) + float(week_label['bottom'])) / 2
            # Date row center should be approx 25-30px higher
            date_row_y = label_y_center - 25 
            
            roi_top = date_row_y - 12
            roi_bottom = date_row_y + 12
            roi_left = float(week_label['x1']) + 1
            roi_right = roi_left + 70
            roi_defined = True
            anchor_name = f"WeekLabel({week_label['text']})-OffsetUp"
        
        if roi_defined:
            date_label_found_in_group = True # matched logic
            
            # 3. Scan words in ROI
            row_text = ""
            debug_words = []
            
            # DEBUG: Print all words in the vicinity
            
            # DEBUG: Print all words in the vicinity to see alignment
            vicinity_words = []
            anchor_x = float(date_label['x1']) if date_label else float(week_label['x1'])
            
            for w in words:
                wx = (float(w['x0']) + float(w['x1'])) / 2
                wy = (float(w['top']) + float(w['bottom'])) / 2
                if abs(wy - label_y_center) < 30 and abs(wx - anchor_x) < 100:
                    vicinity_words.append(f"{w['text']}({wx:.1f},{wy:.1f})")
                
                # Check ROI intersection
                if (roi_top < wy < roi_bottom) and (roi_left < float(w['x0']) < roi_right):
                    row_text += w['text']
                    debug_words.append(w['text'])
            
            label_text = date_label['text'] if date_label else f"Week:{week_label['text']}"
            print(f"[DEBUG] Page {page.get('page')} Label: {label_text} ROI: [{roi_left:.1f}-{roi_right:.1f}, y:{roi_top:.1f}-{roi_bottom:.1f}] Extracted: '{row_text}' Vicinity: {vicinity_words}")

            # 4. Check for digits 1-31
            # Must contain digits. If it contains "星期", we might have drifted too low.
            if "星期" in row_text:
                 print(f"[DEBUG] Drifted into 'Week' row. Ignoring.")
                 continue 
            
            match = re.search(r'\b([1-9]|[12][0-9]|3[01])\b', row_text)
            if match:
                found_digit = match.group(1)
                reason = f"Active: Found date '{found_digit}' in ROI (Text: '{row_text}') on Page {page.get('page')}"
                print(f"[DEBUG_PRE_CHECK] {reason}")
                return True, reason
    
    if date_label_found_in_group:
        return False, "Inactive: Date label found but First Cell is empty."
        
    return True, "Active: Default (No Date label found)"
