from fastapi import APIRouter, File, UploadFile
from typing import List

router = APIRouter()

from services.pdf_parser import parse_pdf_bytes
from logic.yc01_rules import check_time_overlaps
from logic.yc02_rules import check_signature_fields
from logic.static_checks import check_static_rules
from logic.time_checks import check_time_rules
from logic.content_checks import check_content_rules
import io

from starlette.concurrency import run_in_threadpool

from logic.pre_check import is_record_active
from collections import defaultdict
import uuid

@router.post("/upload", tags=["Audit"])
async def upload_pdf(file: UploadFile = File(...)):
    """
    接收 PDF 檔案並進行記憶體中分析 (不存硬碟)。
    """
    # 讀取檔案內容為 bytes (Memory-only)
    file_content = await file.read()
    
    # 1. Parse PDF (Run in threadpool to avoid blocking event loop)
    parsed_pages = await run_in_threadpool(parse_pdf_bytes, io.BytesIO(file_content))
    
    # 2. Pre-check: Filter out Inactive/Empty Record Groups
    # Group by group_id first
    groups = defaultdict(list)
    for p in parsed_pages:
        gid = p.get("group_id") or "unknown"
        groups[gid].append(p)
        
    active_pages = []
    
    # Store debug info to return even if active
    debug_results = []
    
    for gid, pages in groups.items():
        is_active, reason = is_record_active(pages)
        if is_active:
            active_pages.extend(pages)
            # Add a system info/debug message to help user understand WHY it's active
            # We add it to the first page of the group
            page_num = pages[0]['page'] if pages else 0
            debug_results.append({
                "rule_id": "SYS-DEBUG",
                "severity": "INFO", 
                "status": "PASS",
                "id": str(uuid.uuid4()), # Add unique ID just in case
                "message": f"[System] {reason}", 
                "page": page_num,
                "group_id": gid,
                "coordinates": { # Add dummy coordinates to prevent Frontend Crash
                    "page": page_num,
                    "x": 0.0,
                    "y": 0.0,
                    "w": 0.0,
                    "h": 0.0
                }
            })
    
    # If no pages are active, we can return early or just pass empty list
    # The rules will mostly likely return empty results for empty input.
    
    # If no pages are active, we can return early or just pass empty list
    # The rules will mostly likely return empty results for empty input.
    
    # 3. Run Audit Logic (Comprehensive) on ACTIVE pages only
    results = []
    if active_pages:
        results.extend(check_time_overlaps(active_pages)) # YC01-8 Overlap
        results.extend(check_signature_fields(active_pages)) # YC01-3/4, YC02-3 Signature
        results.extend(check_static_rules(active_pages)) # YC01-5/6/7/8 Static
        results.extend(check_time_rules(active_pages)) # YC02-5, YC04-7 Time
        results.extend(check_content_rules(active_pages)) # YC01-10, YC03-1, YC04-1 Notes
    
    return {
        "record_meta": {
            "file_name": file.filename,
            "total_pages": len(parsed_pages), # Show total parsed
            "active_pages": len(active_pages), # Show how many were actually checked
            "upload_timestamp": 0 # Mock timestamp
        },
        "audit_results": results
    }
    

@router.get("/status", tags=["System"])
def get_status():
    return {"status": "backend_ready", "version": "0.1.0"}
