import os
from typing import List, Dict, Any
import logging
from tree_sitter_languages import get_language, get_parser

logger = logging.getLogger(__name__)

class CodeParser:
    """
    Uses Tree-sitter to parse code and extract high-level definitions (skeletons).
    """

    SUPPORTED_LANGUAGES = {
        '.py': 'python',
        '.js': 'javascript',
        '.jsx': 'javascript',
        '.ts': 'typescript',
        '.tsx': 'typescript',
        '.go': 'go',
        '.rs': 'rust',
        '.java': 'java',
        '.cpp': 'cpp',
        '.c': 'c',
    }
    
    # S-expressions for queries
    QUERIES = {
        'python': """
            (function_definition name: (identifier) @name) @function
            (class_definition name: (identifier) @name) @class
        """,
        'javascript': """
            (function_declaration name: (identifier) @name) @function
            (class_declaration name: (identifier) @name) @class
            (variable_declarator name: (identifier) @name value: [(arrow_function) (function_expression)]) @function
        """,
        'typescript': """
            (function_declaration name: (identifier) @name) @function
            (class_declaration name: (identifier) @name) @class
            (interface_declaration name: (type_identifier) @name) @interface
            (variable_declarator name: (identifier) @name value: [(arrow_function) (function_expression)]) @function
        """
    }

    def __init__(self):
        self.parsers = {}
        self.languages = {}

    def _get_parser(self, lang_name: str):
        if lang_name not in self.parsers:
            try:
                self.parsers[lang_name] = get_parser(lang_name)
                self.languages[lang_name] = get_language(lang_name)
            except Exception as e:
                logger.warning(f"Could not load parser for {lang_name}: {e}")
                return None
        return self.parsers.get(lang_name)

    def parse_file(self, file_path: str) -> str:
        """
        Parses a file and returns a skeleton string of definitions.
        If parsing fails or language not supported, returns first 50 lines.
        """
        ext = os.path.splitext(file_path)[1]
        lang_name = self.SUPPORTED_LANGUAGES.get(ext)
        
        if not lang_name:
            return self._fallback_read(file_path)

        parser = self._get_parser(lang_name)
        if not parser:
            return self._fallback_read(file_path)

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            tree = parser.parse(bytes(content, "utf8"))
            query_scm = self.QUERIES.get(lang_name)
            
            if not query_scm:
                 # If no query defined, just return the whole file for now (or fallback)
                 return content
            
            # Execute query
            query = self.languages[lang_name].query(query_scm)
            captures = query.captures(tree.root_node)
            
            # Build skeleton
            # This is a simplified approach: we just list the names found.
            # A better approach (Full Skeleton) requires reconstructing the text with bodies removed.
            # detailed in 2.2.1 of the report.
            
            definitions = []
            for node, capture_name in captures:
                # Get the name of the definition
                name_node = node
                # The query puts @name on the identifier, and @class/@function on the whole node.
                # However, captures return both. We want the full text of the signature ideally,
                # or just "class Foo"
                
                # Let's simplify: Just extract the text of the line where the node starts
                start_point = node.start_point
                if hasattr(start_point, 'row'):
                    start_line = start_point.row
                else:
                    start_line = start_point[0]
                # end_line = node.end_point.row
                
                # Fetch the line from content
                lines = content.split('\n')
                if start_line < len(lines):
                    definitions.append(f"{capture_name}: {lines[start_line].strip()}")
            
            if not definitions:
                return self._fallback_read(file_path) # No definitions found, maybe just script
                
            return "\n".join(definitions)

        except Exception as e:
            logger.error(f"Error parsing {file_path}: {e}")
            return self._fallback_read(file_path)

    def _fallback_read(self, file_path: str) -> str:
        """Reads first 100 lines as fallback."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = [next(f) for _ in range(100)]
            return "".join(lines)
        except StopIteration:
            return "" # empty file
        except Exception:
            return ""
