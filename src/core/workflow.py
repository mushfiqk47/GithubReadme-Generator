import time
import logging
import re
from typing import Generator, Dict, Any, Optional
from datetime import datetime

from src.core.config import config
from src.core.graph import create_graph
from src.core.memory import memory
from src.ingestion.repo_manager import RepoManager
from src.analysis.builder import ContextBuilder
from src.analysis.model_caps import ModelCapabilities

logger = logging.getLogger(__name__)

class GenerationEvent:
    """Standardized event for workflow updates."""
    def __init__(self, type: str, message: str, progress: int = 0, payload: Any = None):
        self.type = type # 'status', 'log', 'result', 'error'
        self.message = message
        self.progress = progress
        self.payload = payload

class ReadmeWorkflow:
    """
    Encapsulates the end-to-end logic for generating a README.
    Shared by both CLI and Web UI to ensure consistency.
    """

    NODE_META = {
        "intelligence": {"msg": "🕵️ **Intelligence**: \"Auditing code quality...\"", "prog": 20},
        "architect": {"msg": "🏗️ **Architect**: \"Designing the blueprint...\"", "prog": 40},
        "visualizer": {"msg": "🎨 **Visualizer**: \"Sketching diagrams...\"", "prog": 60},
        "writer": {"msg": "✍️ **Writer**: \"Drafting the content...\"", "prog": 80},
        "reviewer": {"msg": "🔍 **Reviewer**: \"Reviewing for accuracy...\"", "prog": 95}
    }

    @staticmethod
    def parse_url(repo_url: str) -> tuple[str, str]:
        if "github.com" not in repo_url:
            raise ValueError("Invalid GitHub URL")
        parts = repo_url.strip().split("github.com/")[-1].split("/")
        if len(parts) < 2:
            raise ValueError("Incomplete URL format")
        return parts[0], parts[1].replace(".git", "")

    def run(self, repo_url: str, custom_focus: str = "", token_budget: int = None) -> Generator[GenerationEvent, None, None]:
        """
        Executes the generation workflow, yielding events for UI/CLI consumption.
        """
        start_time = time.time()
        
        try:
            # 1. Validation & Setup
            owner, repo = self.parse_url(repo_url)
            yield GenerationEvent("status", f"Targeting {owner}/{repo}...", 5)

            # 2. Ingestion
            yield GenerationEvent("status", "📚 Librarian: Cloning repository...", 10)
            repo_manager = RepoManager()
            local_path = repo_manager.clone_repo(f"https://github.com/{owner}/{repo}.git")

            # 3. Context Building
            if not token_budget:
                 default_limit = ModelCapabilities.get_max_tokens(config.MODEL_PLANNER)
                 token_budget = int(default_limit * 0.8)

            yield GenerationEvent("status", f"🧠 Architect: Analyzing structure (Budget: {token_budget:,} tokens)...", 15)
            builder = ContextBuilder(local_path)
            repo_text = builder.build_repository_map(max_tokens=token_budget)
            token_count = builder._get_token_count(repo_text)
            
            yield GenerationEvent("log", f"Context built: {token_count:,} tokens")

            # 4. Graph Execution
            app = create_graph()
            initial_state = {
                "repo_owner": owner, 
                "repo_name": repo, 
                "repo_data": repo_text,
                "iteration": 0, 
                "visual_assets": [],
                "project_summary": f"User Instructions: {custom_focus}" if custom_focus else None
            }
            
            final_state = initial_state
            
            for event in app.stream(initial_state):
                for key, value in event.items():
                    if key in self.NODE_META:
                        meta = self.NODE_META[key]
                        yield GenerationEvent("status", meta["msg"], meta["prog"])
                    
                    if value:
                        final_state.update(value)

            # 5. Final Assembly
            draft = final_state.get('draft_sections', {}).get('full_readme', '')
            assets = "\n\n".join(final_state.get('visual_assets', []))
            final_md = f"{draft}\n\n{assets}"
            
            duration = time.time() - start_time
            
            # 6. Memory Update
            try:
                mem_update = {
                    "last_repo": f"{owner}/{repo}",
                    "generation_count": memory.get("generation_count", 0) + 1,
                    "last_activity": datetime.now().isoformat()
                }
                if custom_focus:
                    mem_update["preferred_focus_areas"] = custom_focus
                memory.update(mem_update)
            except Exception as e:
                logger.warning(f"Memory update failed: {e}")

            # 7. Success
            result_payload = {
                "markdown": final_md,
                "owner": owner,
                "repo": repo,
                "duration": duration
            }
            yield GenerationEvent("result", "Generation Complete", 100, result_payload)

        except Exception as e:
            logger.error(f"Workflow failed: {e}", exc_info=True)
            yield GenerationEvent("error", str(e))