import pdfplumber
from typing import List, Dict, Any

def parse_pdf_bytes(file_bytes: bytes) -> List[Dict[str, Any]]:
    """
    Parse PDF bytes using pdfplumber to extraction text and coordinates.
    Returns a list of page objects with text and layout info.
    """
    import uuid
    parsed_pages = []
    current_case_id = None
    current_case_name = None
    current_group_id = str(uuid.uuid4()) # Start with a default group
    
    with pdfplumber.open(file_bytes) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            # Extract words with bounding boxes
            words = page.extract_words()
            
            # Extract raw text for easier regex matching (optional)
            raw_text = page.extract_text() or ""
            
            # Simple metadata extraction for grouping
            case_id = ""
            case_name = ""
            
            # Regex to find Case ID (e.g., FX123456) and Name
            import re
            img_id_match = re.search(r'個案編號\s*[:：]\s*([A-Za-z0-9]+)', raw_text)
            img_name_match = re.search(r'個案姓名\s*[:：]\s*(\S+)', raw_text)
            
            if img_id_match:
                case_id = img_id_match.group(1)
                # Found a header! This marks the start of a NEW record group.
                # Even if case_id is same as previous, it's a new sheet (e.g. different week).
                current_group_id = str(uuid.uuid4())
                current_case_id = case_id
            
            if img_name_match:
                case_name = img_name_match.group(1)
                current_case_name = case_name
                
            # If no header found, we stay in the current_group_id (continuation)
            # and inherit context
            if not case_id and current_case_id:
                case_id = current_case_id
            
            if not case_name and current_case_name:
                case_name = current_case_name

            parsed_pages.append({
                "page": page_num,
                "width": float(page.width),
                "height": float(page.height),
                "words": words, # List of {text, x0, top, x1, bottom}
                "raw_text": raw_text,
                "rects": page.rects,
                "lines": page.lines,
                "curves": page.curves,
                "images": page.images,
                "case_id": case_id,
                "case_name": case_name,
                "group_id": current_group_id 
            })
            
    return parsed_pages
