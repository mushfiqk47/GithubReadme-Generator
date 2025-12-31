from typing import Dict, Any, List, TypedDict

class FileNode(TypedDict):
    path: str
    content: str
    size: int

class ContextProcessor:
    """
    Responsible for filtering 'noise' files and formatting the repository data
    into a context string suitable for LLM consumption.
    """
    
    IGNORE_EXTENSIONS = {
        '.lock', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', 
        '.eot', '.ttf', '.woff', '.woff2', '.mp4', '.mp3', '.pdf', 
        '.zip', '.tar', '.gz', '.pyc', '.class'
    }
    
    IGNORE_DIRS = {
        'node_modules', 'dist', 'build', 'venv', '__pycache__', 
        '.git', '.idea', '.vscode'
    }
    
    IGNORE_FILES = {
        'package-lock.json', 'yarn.lock', 'poetry.lock', 'Cargo.lock'
    }

    @classmethod
    def should_ignore(cls, filename: str, path: str = "") -> bool:
        """Determines if a file should be ignored based on heuristics."""
        if filename in cls.IGNORE_FILES:
            return True
        
        if any(filename.endswith(ext) for ext in cls.IGNORE_EXTENSIONS):
            return True
            
        parts = path.split('/')
        if any(part in cls.IGNORE_DIRS for part in parts):
            return True
            
        return False

    @staticmethod
    def process_repo_data(repo_data: Dict[str, Any]) -> str:
        """
        Transforms raw GraphQL output into a formatted string.
        Flattens the 2-level tree from the simple query.
        """
        formatted_output = []
        
        # Meta info
        description = repo_data.get('description', 'No description found.')
        homepage = repo_data.get('homepageUrl', 'No homepage found.')
        formatted_output.append(f"# Project Description: {description}")
        formatted_output.append(f"# Homepage: {homepage}\n")
        
        files_found = 0
        
        root = repo_data.get('object', {})
        if not root:
            return "Empty repository."

        # Helper to process entries
        def process_entries(entries, current_path=""):
            nonlocal files_found
            for entry in entries:
                name = entry['name']
                obj = entry['object']
                type_ = entry['type']
                
                full_path = f"{current_path}/{name}" if current_path else name
                
                if ContextProcessor.should_ignore(name, full_path):
                    continue
                
                if type_ == 'blob':
                    # It's a file
                    if obj.get('isBinary', False):
                        continue
                        
                    content = obj.get('text', '')
                    if not content: 
                        continue

                    # Truncation logic for massive files (simple heurisitc: > 50kb)
                    size = obj.get('byteSize', 0)
                    if size > 50000:
                        lines = content.split('\n')
                        content = "\n".join(lines[:100]) + "\n...[TRUNCATED]...\n" + "\n".join(lines[-50:])
                    
                    formatted_output.append(f"--- FILE: {full_path} ---")
                    formatted_output.append(content)
                    formatted_output.append("--- END FILE ---\n")
                    files_found += 1
                
                elif type_ == 'tree':
                    # It's a directory - recurse if we have the data
                    # (The current simple GraphQL query only goes 2 levels deep depending on definition.
                    # If the data structure from recursion logic in client supports it, we traverse.)
                    if 'entries' in obj:
                        process_entries(obj['entries'], full_path)

        if 'entries' in root:
            process_entries(root['entries'])
            
        return "\n".join(formatted_output)
