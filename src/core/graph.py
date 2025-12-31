from langgraph.graph import StateGraph, END
from src.core.state import DocumentationState
from src.agents.nodes import (
    node_architect, node_writer, node_visualizer, node_reviewer, node_intelligence
)

def should_continue(state: DocumentationState):
    """
    Conditional logic to determine if we loop back or finish.
    """
    feedback = state.get("review_feedback", "")
    iteration = state.get("iteration", 0)
    
    if "REJECT" in feedback and iteration < 2:
        return "writer"
    return END

def create_graph():
    """
    Constructs the Agentic Workflow Graph.
    """
    workflow = StateGraph(DocumentationState)
    
    # 1. Add Nodes
    workflow.add_node("intelligence", node_intelligence)
    workflow.add_node("architect", node_architect)
    workflow.add_node("visualizer", node_visualizer)
    workflow.add_node("writer", node_writer)
    workflow.add_node("reviewer", node_reviewer)
    
    # 2. Add Edges
    workflow.set_entry_point("intelligence")
    workflow.add_edge("intelligence", "architect")
    workflow.add_edge("architect", "visualizer")
    workflow.add_edge("visualizer", "writer")
    workflow.add_edge("writer", "reviewer")
    
    workflow.add_conditional_edges(
        "reviewer",
        should_continue,
        {
            "writer": "writer",
            END: END
        }
    )
    
    return workflow.compile()
