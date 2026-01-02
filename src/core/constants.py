from typing import Set

IGNORE_DIRS: Set[str] = {
    'node_modules', 'dist', 'build', 'venv', '__pycache__', 
    '.git', '.idea', '.vscode', '.repo_cache', 'intelligent_readme_generator.egg-info',
    '.pytest_cache', 'coverage', 'site-packages', 'target', 'bin', 'obj'
}

IGNORE_EXTENSIONS: Set[str] = {
    '.lock', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', 
    '.eot', '.ttf', '.woff', '.woff2', '.mp4', '.mp3', '.pdf', 
    '.zip', '.tar', '.gz', '.pyc', '.class', '.exe', '.dll', '.bin',
    '.so', '.dylib', '.jar', '.war', '.ear', '.psd', '.ai', '.sketch'
}

IGNORE_FILES: Set[str] = {
    'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml', 'poetry.lock', 
    'Cargo.lock', 'gemfile.lock', 'composer.lock', 'mix.lock'
}
