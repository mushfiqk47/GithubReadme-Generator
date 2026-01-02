import os
import tempfile
import logging
import shutil
import stat
from git import Repo # type: ignore
from pathlib import Path

logger = logging.getLogger(__name__)

def remove_readonly(func, path, exc_info):
    """
    Error handler for shutil.rmtree.
    If the error is due to an access error (read only file),
    it attempts to add write permission and then retries.
    If the error is for another reason it re-raises the error.
    """
    # Clear the readonly bit and reattempt the removal
    os.chmod(path, stat.S_IWRITE)
    func(path)

class RepoManager:
    """
    Manages local cloning and updates of git repositories.
    Implements 'Strategy B' from the architecture report (Local Processing).
    """

    def __init__(self, base_dir: str = None):
        # Use a localized cache dir in the user's project if possible, or temp
        # For now, let's use a .cache directory in the project root to persist across runs nicely
        if base_dir:
             self.base_dir = Path(base_dir)
        else:
             # Default to .repo_cache in the current working directory
             self.base_dir = Path(os.getcwd()) / ".repo_cache"
        
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def clear_cache(self):
        """
        Removes the entire cache directory to free space or reset state.
        """
        if self.base_dir.exists():
            # onerror is required on Windows for read-only git files
            shutil.rmtree(self.base_dir, onerror=remove_readonly)
            self.base_dir.mkdir(parents=True, exist_ok=True)
            logger.info("Repository cache cleared.")

    def clone_repo(self, url: str) -> str:
        """
        Clones or updates a repository in the local cache.
        """
        try:
            parts = url.strip("/").split("/")
            if "github.com" not in url:
                 raise ValueError("Only GitHub URLs supported")
            
            owner = parts[-2]
            name = parts[-1].replace(".git", "")
            target_path = self.base_dir / owner / name
            
            if target_path.exists():
                logger.info(f"Updating repository {owner}/{name}...")
                repo = Repo(target_path)
                origin = repo.remotes.origin
                origin.pull()
                return str(target_path)
            
            logger.info(f"Cloning {url} to {target_path}...")
            Repo.clone_from(url, target_path, depth=1)
            
            return str(target_path)
            
        except Exception as e:
            logger.error(f"Git operation failed: {e}")
            if "target_path" in locals() and target_path.exists():
                return str(target_path) # Fallback to existing if pull fails (offline)
            raise
