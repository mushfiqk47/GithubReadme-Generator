import os
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

def generate_badges(repo_path: str) -> List[str]:
    """
    Deterministically generates badges based on file existence.
    """
    badges = []
    
    # License
    if os.path.exists(os.path.join(repo_path, "LICENSE")):
        badges.append("[![License](https://img.shields.io/github/license/placeholder/repo?style=for-the-badge)](LICENSE)")
    
    # CI/CD
    github_workflows = os.path.join(repo_path, ".github", "workflows")
    if os.path.exists(github_workflows) and os.listdir(github_workflows):
        badges.append("[![CI](https://img.shields.io/github/actions/workflow/status/placeholder/repo/ci.yml?style=for-the-badge)](.github/workflows)")
        
    # Python
    if os.path.exists(os.path.join(repo_path, "pyproject.toml")) or os.path.exists(os.path.join(repo_path, "requirements.txt")):
        badges.append("[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)")
        
    # JavaScript/TypeScript
    if os.path.exists(os.path.join(repo_path, "package.json")):
        badges.append("[![Node](https://img.shields.io/badge/Node-18+-green?style=for-the-badge&logo=nodedotjs&logoColor=white)](https://nodejs.org)")
        
    # Docker
    if os.path.exists(os.path.join(repo_path, "Dockerfile")):
        badges.append("[![Docker](https://img.shields.io/badge/Docker-Enabled-blue?style=for-the-badge&logo=docker&logoColor=white)](Dockerfile)")

    return badges