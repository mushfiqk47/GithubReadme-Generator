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
    
    # Improved Queries with Docstring Capture
    QUERIES = {
        'python': """
            (function_definition 
                name: (identifier) @name 
                body: (block (expression_statement (string) @doc)?)) @function
            (class_definition 
                name: (identifier) @name 
                body: (block (expression_statement (string) @doc)?)) @class
        """,
        'javascript': """
            (comment) @doc
            (function_declaration name: (identifier) @name) @function
            (class_declaration name: (identifier) @name) @class
            (variable_declarator name: (identifier) @name value: [(arrow_function) (function_expression)]) @function
        """,
        'typescript': """
            (comment) @doc
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
        Parses a file and returns a skeleton string of definitions including docstrings.
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
                 return content
            
            # Execute query
            query = self.languages[lang_name].query(query_scm)
            captures = query.captures(tree.root_node)
            
            definitions = []
            last_doc = None
            
            for node, capture_name in captures:
                # Capture Docstrings
                if capture_name == 'doc':
                    last_doc = content[node.start_byte:node.end_byte].strip()
                    continue
                
                # Capture Definitions
                if capture_name in ['name', 'function', 'class', 'interface']:
                    # We usually get 'name' then the full node. Let's focus on the name for brevity.
                    if capture_name == 'name':
                        def_name = content[node.start_byte:node.end_byte]
                        parent_type = node.parent.type if node.parent else "unknown"
                        
                        line = f"{parent_type} {def_name}"
                        if last_doc:
                            # Attach the docstring if it was immediately preceding (simplistic heuristic)
                            line += f"\n  \"\"\" {last_doc[:100]}... \"\"\""
                            last_doc = None # Reset
                        
                        definitions.append(line)

            if not definitions:
                return self._fallback_read(file_path)
                
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
