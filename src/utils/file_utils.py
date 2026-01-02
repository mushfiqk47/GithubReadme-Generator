"""
Shared file reading utilities with consistent error handling.
"""
import os
import logging
from typing import Optional, List
from pathlib import Path

logger = logging.getLogger(__name__)


def safe_read_file(file_path: str, max_lines: Optional[int] = None, encoding: str = "utf-8") -> str:
    """
    Safely read a file with error handling and optional line limit.
    
    Args:
        file_path: Path to the file
        max_lines: Maximum number of lines to read (None for all)
        encoding: File encoding
    
    Returns:
        File content or empty string on error
    """
    try:
        with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
            if max_lines:
                lines = [next(f) for _ in range(max_lines)]
                return "".join(lines)
            return f.read()
    except StopIteration:
        return ""
    except Exception as e:
        logger.debug(f"Could not read {file_path}: {e}")
        return ""


def safe_write_file(file_path: str, content: str, encoding: str = "utf-8") -> bool:
    """
    Safely write content to a file with error handling.
    
    Args:
        file_path: Path to the file
        content: Content to write
        encoding: File encoding
    
    Returns:
        True if successful, False otherwise
    """
    try:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)
        return True
    except Exception as e:
        logger.error(f"Could not write to {file_path}: {e}")
        return False


def ensure_directory(dir_path: str) -> bool:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        dir_path: Path to the directory
    
    Returns:
        True if directory exists or was created
    """
    try:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Could not create directory {dir_path}: {e}")
        return False


def file_exists(file_path: str) -> bool:
    """Check if a file exists safely."""
    try:
        return Path(file_path).is_file()
    except Exception:
        return False


def is_text_file(file_path: str, max_check_size: int = 8192) -> bool:
    """
    Check if a file is likely a text file by reading a sample.
    
    Args:
        file_path: Path to the file
        max_check_size: Maximum bytes to check
    
    Returns:
        True if file appears to be text
    """
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(max_check_size)
            if not chunk:
                return True
            # Check for null bytes (binary indicator)
            if b'\x00' in chunk:
                return False
            # Try to decode as UTF-8
            try:
                chunk.decode('utf-8')
                return True
            except UnicodeDecodeError:
                return False
    except Exception:
        return False


def get_file_extension(file_path: str) -> str:
    """Get file extension without the dot."""
    return Path(file_path).suffix.lower()


def get_file_name(file_path: str) -> str:
    """Get file name without extension."""
    return Path(file_path).stem
