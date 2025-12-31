import streamlit as st
import os
import time
import logging
from src.ingestion.repo_manager import RepoManager
from src.analysis.builder import ContextBuilder
from src.core.graph import create_graph
from src.ui.components import render_header
from src.analysis.model_caps import ModelCapabilities

logger = logging.getLogger(__name__)

def render_dashboard():
    render_header("🧙‍♂️ Intelligent README Generator", "Agentic documentation for your codebase.")
    
    with st.container():
        repo_url = st.text_input("GitHub Repository URL", placeholder="https://github.com/owner/repo")
        
    if st.button("🚀 Generate Documentation", type="primary", use_container_width=True):
        if not repo_url:
            st.error("Please enter a URL")
            return
            
        start_time = time.time()
        try:
            if "github.com" not in repo_url: raise ValueError("Invalid URL")
            parts = repo_url.strip().split("github.com/")[-1].split("/")
            owner, repo = parts[0], parts[1].replace(".git", "")
            
            with st.status("🤖 Orchestrating AI Agents...", expanded=True) as status:
                # 1. Ingestion
                st.write("📥 **Librarian**: Cloning & Indexing repository...")
                repo_manager = RepoManager()
                local_path = repo_manager.clone_repo(f"https://github.com/{owner}/{repo}.git")
                
                # 2. Context Building
                current_model = os.getenv("MODEL_PLANNER", "gpt-4o")
                max_ctx = ModelCapabilities.get_max_tokens(current_model)
                safe_budget = int(max_ctx * 0.8) 
                
                st.write(f"🧠 **Architect**: Mapping codebase (Budget: {safe_budget:,} tokens)...")
                builder = ContextBuilder(local_path)
                repo_text = builder.build_repository_map(max_tokens=safe_budget)
                
                # Token Metrics
                actual_tokens = builder._get_token_count(repo_text)
                st.write(f"📊 **Context Size**: {actual_tokens:,} tokens / {safe_budget:,} limit")
                
                # 3. Agent Execution
                st.write("✍️ **Writer**: Drafting high-fidelity documentation...")
                app = create_graph()
                final_state = app.invoke({
                    "repo_owner": owner, "repo_name": repo, "repo_data": repo_text,
                    "iteration": 0, "visual_assets": []
                })
                
                draft = final_state['draft_sections'].get('full_readme', '')
                assets = "\n\n".join(final_state.get('visual_assets', []))
                final_md = f"{draft}\n\n{assets}"
                
                duration = time.time() - start_time
                status.update(label=f"✅ Documentation Ready! (Processed in {duration:.1f}s)", state="complete", expanded=False)
                
            # Layout for Result
            st.divider()
            col_a, col_b = st.columns([4, 1])
            with col_a:
                st.subheader("📄 Generated README")
            with col_b:
                st.download_button("💾 Download .md", final_md, f"{repo}_README.md", use_container_width=True)
            
            st.markdown(f'<div class="markdown-body">{final_md}</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ Generation Failed: {e}")
            logger.error(f"Error in dashboard: {e}", exc_info=True)
