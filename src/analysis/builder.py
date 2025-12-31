import os
import logging
import tiktoken
from pathlib import Path
from typing import List, Dict, Set
from concurrent.futures import ThreadPoolExecutor
from src.analysis.parser import CodeParser
from src.analysis.graph import DependencyGraph

logger = logging.getLogger(__name__)

class ContextBuilder:
    """
    Optimized Context Builder with multi-threading and accurate token counting.
    """
    
    IGNORE_DIRS = {
        'node_modules', 'dist', 'build', 'venv', '__pycache__', 
        '.git', '.idea', '.vscode', '.repo_cache', 'intelligent_readme_generator.egg-info'
    }
    
    IGNORE_EXTENSIONS = {
        '.lock', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', 
        '.eot', '.ttf', '.woff', '.woff2', '.mp4', '.mp3', '.pdf', 
        '.zip', '.tar', '.gz', '.pyc', '.class', '.exe', '.dll', '.bin'
    }

    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        self.parser = CodeParser()
        self.graph = DependencyGraph(root_dir)
        try:
            self.encoder = tiktoken.get_encoding("cl100k_base")
        except:
            self.encoder = None

    def _get_token_count(self, text: str) -> int:
        if self.encoder:
            return len(self.encoder.encode(text, disallowed_special=()))
        return len(text) // 4

    def _collect_files(self) -> List[str]:
        files = []
        for root, dirs, filenames in os.walk(self.root_dir):
            dirs[:] = [d for d in dirs if d not in self.IGNORE_DIRS]
            for name in filenames:
                if any(name.endswith(ext) for ext in self.IGNORE_EXTENSIONS):
                    continue
                files.append(os.path.join(root, name))
        return files

    def _process_file(self, f_path: str, rank: float, mode: str = "skeleton") -> str:
        """Process a single file based on mode."""
        rel_path = os.path.relpath(f_path, self.root_dir)
        try:
            if mode == "full":
                with open(f_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if len(content) > 15000: content = content[:15000] + "\n... [TRUNCATED]"
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
        current_tokens += self._get_token_count(header)
        
        essential_files = {'readme.md', 'package.json', 'requirements.txt', 'pyproject.toml', 'dockerfile', 'cargo.toml', 'go.mod'}
        processed_files = set()
        
        # Pass 1: Configuration (Full)
        with ThreadPoolExecutor(max_workers=8) as executor:
            configs = [f for f in sorted_files if os.path.basename(f).lower() in essential_files]
            results = list(executor.map(lambda f: self._process_file(f, ranks.get(f, 0), "full"), configs))
            for res in results:
                if not res: continue
                tokens = self._get_token_count(res)
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
                tokens = self._get_token_count(res)
                if current_tokens + tokens < max_tokens:
                    output_parts.append(res)
                    current_tokens += tokens
                else:
                    break

        return "".join(output_parts)
