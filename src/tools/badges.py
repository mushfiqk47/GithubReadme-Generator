import re
from typing import Dict, Any, List

def generate_badges(repo_data: Dict[str, Any]) -> List[str]:
    """
    Analyzes repository data to strictly generate valid Shields.io badges.
    """
    badges = []
    
    # 1. License Badge
    # (Simplified check: look for LICENSE file in top level)
    # The actual graphQL data might need to be parsed deeper if we want the specific license type text
    # For now, we'll try to guess from the data context or just generic if file exists.
    # In a real app, we'd checking `object.entries` for "LICENSE".
    
    # Let's assume we have access to the file list from the simplified processing
    # A true implementation would parse the 'licenseInfo' field from GitHub API (if requested).
    # Since our query didn't request licenseInfo, we can check for file existence.
    
    # 2. CI/CD Badge
    # Check for .github/workflows/*.yml
    # This requires traversing the tree.
    
    # Implementation:
    # We will scan the processed text for hints, OR better, passing the raw tree object here is safer.
    
    # For v1, let's just return a placeholder list that the LLM *context* can use, 
    # or let the LLM do it but guided by this function if we were using tool calling.
    
    # Since the `Visualizer` node is currently LLM-driven, we will stick to that for now 
    # to avoid complex tree traversal logic in Python without the full object structure readily available.
    
    return []
