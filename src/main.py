import argparse
import sys
import os
import logging
from src.core.config import config
from src.core.graph import create_graph
from src.ingestion.repo_manager import RepoManager
from src.analysis.builder import ContextBuilder
from src.analysis.model_caps import ModelCapabilities

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Intelligent README Generator")
    parser.add_argument("owner", help="GitHub Repository Owner")
    parser.add_argument("repo", help="GitHub Repository Name")
    parser.add_argument("--output", default="GENERATED_README.md", help="Output filename")
    
    args = parser.parse_args()
    
    # 1. Validation
    if not config.GITHUB_TOKEN:
        logger.warning("GITHUB_TOKEN not set in .env. Rate limits may apply.")
        
    logger.info(f"Targeting Repo: {args.owner}/{args.repo}")
    repo_url = f"https://github.com/{args.owner}/{args.repo}.git"

    # 2. Ingestion (Local Clone Strategy)
    try:
        logger.info("Cloning repository...")
        repo_manager = RepoManager()
        local_path = repo_manager.clone_repo(repo_url)
    except Exception as e:
        logger.error(f"Failed to clone repo: {e}")
        sys.exit(1)
        
    # 3. Context Building
    logger.info("Mapping codebase...")
    try:
        current_model = config.MODEL_PLANNER
        max_ctx = ModelCapabilities.get_max_tokens(current_model)
        safe_budget = int(max_ctx * 0.9) # 90% budget for CLI
        
        builder = ContextBuilder(local_path)
        repo_text = builder.build_repository_map(max_tokens=safe_budget)
        token_count = builder._get_token_count(repo_text)
        logger.info(f"Context built: {token_count} tokens")
    except Exception as e:
        logger.error(f"Failed to build context: {e}")
        sys.exit(1)
    
    # 4. Graph Execution
    logger.info("Initializing Agent Graph...")
    app = create_graph()
    
    initial_state = {
        "repo_owner": args.owner,
        "repo_name": args.repo,
        "repo_data": repo_text,
        "iteration": 0,
        "visual_assets": []
    }
    
    logger.info("Running Workflow... (This may take a minute)")
    final_state = app.invoke(initial_state)
    
    # 5. Output
    draft = final_state['draft_sections'].get('full_readme', '')
    assets = final_state.get('visual_assets', [])
    
    # Append assets if not present
    assets_text = "\n\n".join(assets)
    final_content = f"{draft}\n\n<!-- Visual Assets Generated -->\n{assets_text}"
    
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(final_content)
        
    logger.info(f"Success! README generated at {args.output}")

if __name__ == "__main__":
    main()
