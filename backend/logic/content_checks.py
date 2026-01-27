from typing import List, Dict, Any
from .yc03_rules import check_ba16_1_requirements
from .yc04_rules import check_ba05_1_requirements
# Import other content checks here

def check_content_rules(parsed_pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    整合內容檢查規則 (YC01-10, BA series)
    """
    results = []
    # Reuse existing implementations
    results.extend(check_ba16_1_requirements(parsed_pages))
    results.extend(check_ba05_1_requirements(parsed_pages))
    
    # Add generic empty note check for BA13, BA14 if needed
    
    return results
