import os
import re
import networkx as nx
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class DependencyGraph:
    """
    Builds a dependency graph of the repository and calculates PageRank.
    """
    
    # Simple RegEx for imports - robust enough for MVP
    # Python: from x import y, import x
    # JS/TS: import x from 'y', require('y')
    PATTERNS = {
        '.py': [
            r'^\s*from\s+([\w\.]+)\s+import',
            r'^\s*import\s+([\w\.]+)'
        ],
        '.js': [
            r'import\s+.*\s+from\s+[\'"](.+)[\'"]',
            r'require\s*\([\'"](.+)[\'"]\)'
        ],
        '.ts': [
            r'import\s+.*\s+from\s+[\'"](.+)[\'"]',
            r'require\s*\([\'"](.+)[\'"]\)'
        ],
        '.tsx': [r'import\s+.*\s+from\s+[\'"](.+)[\'"]'],
        '.jsx': [r'import\s+.*\s+from\s+[\'"](.+)[\'"]']
    }

    def __init__(self, root_dir: str):
        self.root_dir = root_dir

    def _resolve_path(self, current_file: str, import_str: str) -> str:
        """
        Resolves import string to absolute file path.
        Handles relative imports.
        """
        # Naive resolution
        current_dir = os.path.dirname(current_file)
        
        # 1. Relative import
        if import_str.startswith('.'):
            # Resolve relative
            target = os.path.normpath(os.path.join(current_dir, import_str))
            
            # Try extensions
            for ext in ['.py', '.js', '.ts', '.tsx', '.jsx']:
                if os.path.exists(target + ext):
                    return target + ext
                if os.path.exists(os.path.join(target, 'index' + ext)):
                     return os.path.join(target, 'index' + ext)
            
            if os.path.exists(target):
                 return target
                 
        # 2. Absolute/Library import - We skip external libs for now, 
        # but if it matches a path in root, we might track it.
        # For this version, we focus on internal relative imports for the graph structure.
        return None

    def _extract_imports(self, file_path: str) -> List[str]:
        ext = os.path.splitext(file_path)[1]
        patterns = self.PATTERNS.get(ext, [])
        if not patterns:
            return []
            
        imports = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                for p in patterns:
                    matches = re.finditer(p, content, re.MULTILINE)
                    for m in matches:
                        imports.append(m.group(1))
        except Exception:
            pass
        return imports

    def build_and_rank(self, files: List[str]) -> Dict[str, float]:
        """
        Builds the graph and returns PageRank scores.
        """
        G = nx.DiGraph()
        
        # Add all files as nodes
        for f in files:
            G.add_node(f)
            
        # Add edges
        for f in files:
            raw_imports = self._extract_imports(f)
            for imp in raw_imports:
                resolved = self._resolve_path(f, imp)
                if resolved and resolved in files: # Only internal links
                    G.add_edge(f, resolved)
        
        try:
            ranks = nx.pagerank(G, alpha=0.85)
            # Normalize? NetworkX returns sum=1.
            return ranks
        except Exception as e:
            logger.warning(f"PageRank failed: {e}")
            # Fallback: uniform rank
            return {f: 1.0 for f in files}
