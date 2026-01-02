from typing import TypedDict, List, Dict, Any, Optional

class DocumentationState(TypedDict):
    """
    Main state object for the README Generator agentic workflow.
    This shared state is passed between all nodes in the graph.
    """
    # Raw Data
    repo_owner: str
    repo_name: str
    repo_data: Dict[str, Any]       # Raw data/file tree from GitHub GraphQL
    user_instructions: Optional[str] # Custom user instructions/focus areas
    
    # Analysis
    project_summary: Optional[str]            # High-level analysis/elevator pitch
    tech_stack: List[str]           # Detected technologies (e.g., "Python", "React")
    project_type: Optional[str]     # e.g., "Library", "Web App", "CLI Tool"
    
    # Planning
    table_of_contents: List[str]    # Planned sections for the README
    
    # Drafting
    draft_sections: Dict[str, str]  # Generated content per section (Key: Section Name, Value: Markdown)
    
    # Intelligence
    best_practices: Optional[List[str]]   # Suggested improvements
    vulnerabilities: Optional[List[str]]  # Potential security or performance issues
    
    # Quality Control
    review_feedback: Optional[str]            # Feedback from the Reviewer agent
    iteration: int                  # Loop counter to prevent infinite refinement
