import os
import subprocess
import logging
from pathlib import Path
from typing import List, Dict, Set
from concurrent.futures import ThreadPoolExecutor
from src.analysis.parser import CodeParser
from src.analysis.graph import DependencyGraph
from src.core.constants import IGNORE_DIRS, IGNORE_EXTENSIONS
from src.utils import count_tokens, truncate_tokens, safe_read_file

logger = logging.getLogger(__name__)

class ContextBuilder:
    """
    Optimized Context Builder with multi-threading and accurate token counting.
    """
    
    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        self.parser = CodeParser()
        self.graph = DependencyGraph(root_dir)

    def _collect_files(self) -> List[str]:
        """
        Collects files using 'git ls-files' if available (respects .gitignore),
        otherwise falls back to os.walk with manual ignore lists.
        """
        # 1. Try Git Method
        if os.path.exists(os.path.join(self.root_dir, ".git")):
            try:
                # Get list of tracked files, respecting .gitignore
                result = subprocess.run(
                    ["git", "ls-files"], 
                    cwd=self.root_dir, 
                    capture_output=True, 
                    text=True, 
                    encoding='utf-8',
                    errors='ignore'
                )
                if result.returncode == 0:
                    git_files = result.stdout.splitlines()
                    # Filter by extension and existence
                    final_files = []
                    for f in git_files:
                        full_path = os.path.join(self.root_dir, f)
                        if os.path.isfile(full_path):
                            if not any(f.endswith(ext) for ext in IGNORE_EXTENSIONS):
                                final_files.append(full_path)
                    if final_files:
                        logger.info(f"Using git ls-files: Found {len(final_files)} files.")
                        return final_files
            except Exception as e:
                logger.warning(f"Git ls-files failed, falling back to os.walk: {e}")

        # 2. Fallback OS Walk Method
        files = []
        for root, dirs, filenames in os.walk(self.root_dir):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            for name in filenames:
                if any(name.endswith(ext) for ext in IGNORE_EXTENSIONS):
                    continue
                files.append(os.path.join(root, name))
        return files

    def _process_file(self, f_path: str, rank: float, mode: str = "skeleton") -> str:
        """Process a single file based on mode."""
        rel_path = os.path.relpath(f_path, self.root_dir)
        try:
            if mode == "full":
                content = safe_read_file(f_path)
                if content:
                    content = truncate_tokens(content, 15000)
                    return f"--- FILE: {rel_path} (Priority: {rank:.4f}) ---\n{content}\n--- END FILE ---\n\n"
            else:
                skeleton = self.parser.parse_file(f_path)
                if skeleton and skeleton.strip():
                    return f"--- SKELETON: {rel_path} (Priority: {rank:.4f}) ---\n{skeleton}\n\n"
        except Exception as e:
            logger.debug(f"Skipping {f_path}: {e}")
        return ""

    def build_repository_map(self, max_tokens: int = 128000) -> str:
        all_files = self._collect_files()
        logger.info(f"Target Token Budget: {max_tokens} | Total Files: {len(all_files)}")
        
        ranks = self.graph.build_and_rank(all_files)
        sorted_files = sorted(all_files, key=lambda x: ranks.get(x, 0), reverse=True)
        
        current_tokens = 0
        output_parts = []
        
        header = f"# Repository Map: {os.path.basename(self.root_dir)}\nTotal Files: {len(all_files)}\n\n"
        output_parts.append(header)
        current_tokens += count_tokens(header)
        
        essential_files = {'readme.md', 'package.json', 'requirements.txt', 'pyproject.toml', 'dockerfile', 'cargo.toml', 'go.mod'}
        processed_files = set()
        
        # Pass 1: Configuration (Full)
        with ThreadPoolExecutor(max_workers=8) as executor:
            configs = [f for f in sorted_files if os.path.basename(f).lower() in essential_files]
            results = list(executor.map(lambda f: self._process_file(f, ranks.get(f, 0), "full"), configs))
            for res in results:
                if not res: continue
                tokens = count_tokens(res)
                if current_tokens + tokens < max_tokens:
                    output_parts.append(res)
                    current_tokens += tokens
                    processed_files.update(configs)

        # Pass 2: High Priority Skeletons (Concurrent)
        top_files = [f for f in sorted_files if f not in processed_files]
        with ThreadPoolExecutor(max_workers=10) as executor:
            skeletons = list(executor.map(lambda f: self._process_file(f, ranks.get(f, 0), "skeleton"), top_files))
            for res in skeletons:
                if not res: continue
                tokens = count_tokens(res)
                if current_tokens + tokens < max_tokens:
                    output_parts.append(res)
                    current_tokens += tokens
                else:
                    break

        return "".join(output_parts)
