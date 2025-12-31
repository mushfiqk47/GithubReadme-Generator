import argparse
import sys
import os
from src.core.config import config
from src.ingestion.github_client import GitHubClient
from src.ingestion.context_processor import ContextProcessor
from src.core.graph import create_graph

# Setup logging
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Intelligent README Generator")
    parser.add_argument("owner", help="GitHub Repository Owner")
    parser.add_argument("repo", help="GitHub Repository Name")
    parser.add_argument("--output", default="GENERATED_README.md", help="Output filename")
    
    args = parser.parse_args()
    
    # 1. Validation
    try:
        token = config.GITHUB_TOKEN
    except ValueError:
        logger.error("GITHUB_TOKEN not set. checks .env")
        sys.exit(1)
        
    if not (config.OPENAI_API_KEY or config.ANTHROPIC_API_KEY):
        logger.error("No LLM API Key set (OPENAI_API_KEY or ANTHROPIC_API_KEY).")
        sys.exit(1)

    logger.info(f"Targeting Repo: {args.owner}/{args.repo}")

    # 2. Ingestion
    client = GitHubClient()
    try:
        logger.info("Fetching repository data...")
        repo_data = client.get_repo_context(args.owner, args.repo)
    except Exception as e:
        logger.error(f"Failed to fetch repo data: {e}")
        sys.exit(1)
        
    # 3. Processing
    logger.info("Processing context...")
    repo_text = ContextProcessor.process_repo_data(repo_data)
    
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
