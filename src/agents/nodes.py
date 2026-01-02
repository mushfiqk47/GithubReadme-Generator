import json
import logging
from typing import Any, Dict
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

from src.core.state import DocumentationState
from src.core.config import config
from src.core.memory import memory  # Import persistent memory
from src.agents.prompts import (
    ARCHITECT_PROMPT, WRITER_PROMPT, VISUALIZER_PROMPT, REVIEWER_PROMPT, ENGINEERING_INSIGHTS_PROMPT
)

from src.core.llm_factory import LLMFactory

logger = logging.getLogger(__name__)

# Adapter to keep existing function signature if needed
def get_model(model_name: str):
    return LLMFactory.get_model(model_name)

def node_intelligence(state: DocumentationState) -> Dict[str, Any]:
    """
    Analyzes the codebase for engineering insights and professional quality markers.
    """
    logger.info("--- Node: Intelligence ---")
    llm = get_model(config.MODEL_PLANNER)
    repo_text = state['repo_data']
    
    messages = [
        SystemMessage(content=ENGINEERING_INSIGHTS_PROMPT),
        HumanMessage(content=f"Analyze this codebase for engineering quality:\n\n{repo_text}")
    ]
    
    response = llm.invoke(messages)
    # Store the insights to be used by the Writer
    return {
        "best_practices": [response.content]
    }

def node_architect(state: DocumentationState) -> Dict[str, Any]:
    """
    The Architect analyzes the repo data and produces a professional plan.
    """
    logger.info("--- Node: Architect ---")
    planner_llm = get_model(config.MODEL_PLANNER)
    repo_text = state['repo_data']
    insights = state.get("best_practices", [])
    user_instructions = state.get("user_instructions", "")
    
    # Load persistent user memory
    memory_context = memory.load()
    
    prompt_content = f"""Analyze this repository and design a Stripe-quality documentation plan. 

Insights found: {insights}

*** USER MEMORY (HISTORICAL PREFERENCES) ***
{memory_context}

Context:
{repo_text}"""

    if user_instructions:
        prompt_content += f"\n\n*** USER INSTRUCTIONS (PRIORITY): {user_instructions} ***"

    messages = [
        SystemMessage(content=ARCHITECT_PROMPT),
        HumanMessage(content=prompt_content)
    ]
    
    response = planner_llm.invoke(messages)
    content = response.content
    
    return {
        "project_summary": content,
        "table_of_contents": ["Hero", "Quick Start", "Features", "Architecture", "Engineering Insights", "Quality Assurance (Playwright)", "Usage", "Contributing"]
    }

def node_writer(state: DocumentationState) -> Dict[str, Any]:
    """
    The Writer drafts the high-fidelity content.
    """
    logger.info("--- Node: Writer ---")
    writer_llm = get_model(config.MODEL_WRITER)
    repo_text = state['repo_data']
    plan = state.get("project_summary", "")
    insights = "\n".join(state.get("best_practices", []))
    user_instructions = state.get("user_instructions", "")
    
    # Load persistent user memory
    memory_context = memory.load()
    
    msg = f"""Architecture Plan:
{plan}

Engineering Insights:
{insights}

*** USER MEMORY (HISTORICAL PREFERENCES) ***
{memory_context}

Codebase Context:
{repo_text}

Task: Write the full README.md. Include the Engineering Insights section."""

    if user_instructions:
        msg += f"\n\n*** USER INSTRUCTIONS (PRIORITY): {user_instructions} ***"
        
    messages = [
        SystemMessage(content=WRITER_PROMPT),
        HumanMessage(content=msg)
    ]
    
    response = writer_llm.invoke(messages)
    
    return {
        "draft_sections": {"full_readme": response.content}
    }

def node_visualizer(state: DocumentationState) -> Dict[str, Any]:
    """
    Generates high-quality badges and styled Mermaid diagrams.
    """
    logger.info("--- Node: Visualizer ---")
    planner_llm = get_model(config.MODEL_PLANNER)
    repo_text = state['repo_data']
    
    messages = [
        SystemMessage(content=VISUALIZER_PROMPT),
        HumanMessage(content=f"Repository Context:\n{repo_text}\n\nGenerate premium badges and a styled Mermaid diagram.")
    ]
    
    response = planner_llm.invoke(messages)
    
    return {
        "visual_assets": [response.content]
    }

def node_reviewer(state: DocumentationState) -> Dict[str, Any]:
    """
    The Reviewer ensures the README meets 'Principal Engineer' standards.
    """
    logger.info("--- Node: Reviewer ---")
    planner_llm = get_model(config.MODEL_PLANNER)
    draft = state['draft_sections'].get('full_readme', '')
    repo_text = state['repo_data']
    
    messages = [
        SystemMessage(content=REVIEWER_PROMPT),
        HumanMessage(content=f"Codebase Context:\n{repo_text}\n\nReview this README draft:\n\n{draft}")
    ]
    
    response = planner_llm.invoke(messages)
    feedback_text = response.content
    
    # Simple Text Parsing for Robustness with Small Models
    if "REJECT" in feedback_text.upper():
        status = "REJECT"
    else:
        status = "APPROVE"
        
    # Extract feedback cleaner if possible
    feedback = feedback_text.replace("Status:", "").replace("Feedback:", "").strip()

    iteration = state.get("iteration", 0) + 1
    
    return {
        "review_feedback": feedback,
        "iteration": iteration
    }
