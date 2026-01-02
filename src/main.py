import argparse
import sys
import logging
from src.core.config import config
from src.core.workflow import ReadmeWorkflow

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Intelligent README Generator")
    parser.add_argument("owner", help="GitHub Repository Owner")
    parser.add_argument("repo", help="GitHub Repository Name")
    parser.add_argument("--output", default="GENERATED_README.md", help="Output filename")
    parser.add_argument("--focus", default="", help="Custom instructions/focus area")
    
    args = parser.parse_args()
    
    # 1. Validation
    if not config.GITHUB_TOKEN:
        logger.warning("GITHUB_TOKEN not set. Rate limits may apply.")
        
    repo_url = f"https://github.com/{args.owner}/{args.repo}.git"
    workflow = ReadmeWorkflow()
    final_result = None

    print(f"\n🚀 Starting generation for {args.owner}/{args.repo}...\n")

    # 2. Execution
    try:
        for event in workflow.run(repo_url, custom_focus=args.focus):
            if event.type == "status":
                print(f"[{event.progress}%] {event.message}")
            elif event.type == "log":
                logger.info(event.message)
            elif event.type == "error":
                logger.error(event.message)
                sys.exit(1)
            elif event.type == "result":
                final_result = event.payload
                print(f"\n✅ Done in {final_result['duration']:.1f}s")

    except KeyboardInterrupt:
        print("\n🛑 Operation cancelled by user.")
        sys.exit(130)

    # 3. Output
    if final_result:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(final_result['markdown'])
            
        logger.info(f"Success! README generated at {args.output}")

if __name__ == "__main__":
    main()
