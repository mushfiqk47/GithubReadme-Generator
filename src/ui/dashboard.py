import streamlit as st
import os
import time
import logging
from src.ingestion.repo_manager import RepoManager
from src.analysis.builder import ContextBuilder
from src.core.graph import create_graph
from src.ui.components import render_header, ui_card
from src.analysis.model_caps import ModelCapabilities
from src.core.config import config

logger = logging.getLogger(__name__)

def render_dashboard():
    # --- Sidebar Controls ---
    with st.sidebar:
        st.divider()
        st.subheader("🛠️ Utilities")
        if st.button("🗑️ Clear Repo Cache", help="Deletes downloaded repositories to free space"):
            RepoManager().clear_cache()
            st.toast("Cache cleared successfully!", icon="🧹")

    render_header("👋 Welcome to IRG", "I'm your AI documentation specialist. Let's build a stunning README for your project.")
    
    with st.container():
        col1, col2 = st.columns([3, 1])
        with col1:
            repo_url = st.text_input("Project Repository", placeholder="Paste your GitHub link here (e.g., https://github.com/owner/repo)")
        with col2:
            st.write("") # Spacer
            st.write("") # Spacer
            if st.button("🎲 Try Example", help="Use a demo repository"):
                repo_url = "https://github.com/mushfiqk47/intelligent-readme-generator"
                st.rerun()
                
        # Advanced Configuration
        with st.expander("⚙️ Advanced Controls", expanded=False):
            c1, c2 = st.columns([2, 1])
            with c1:
                custom_focus = st.text_area("Custom Focus / Instructions", placeholder="e.g. 'Focus heavily on the API endpoints' or 'Ignore the legacy folder'")
            with c2:
                # Dynamic default based on model
                default_limit = ModelCapabilities.get_max_tokens(config.MODEL_PLANNER)
                token_budget = st.slider("Context Budget (Tokens)", 
                                         min_value=10000, 
                                         max_value=200000, 
                                         value=int(default_limit * 0.8), 
                                         step=5000,
                                         help="Higher budget = more file context, but slower generation.")

    if st.button("✨ Start Magic", type="primary", use_container_width=True):
        if not repo_url:
            st.warning("👈 Please paste a GitHub URL first so I know what to document!")
            return
            
        start_time = time.time()
        try:
            if "github.com" not in repo_url: 
                raise ValueError("I can currently only work with GitHub links. Please make sure it's a valid https://github.com/... URL.")
            
            parts = repo_url.strip().split("github.com/")[-1].split("/")
            if len(parts) < 2:
                 raise ValueError("The URL seems incomplete. It should look like owner/repo.")
            owner, repo = parts[0], parts[1].replace(".git", "")
            
            # Narrative Status Updates
            with st.status(f"🚀 Spinnning up the team... (Brain: {config.MODEL_PLANNER})", expanded=True) as status:
                
                # 1. Ingestion
                st.write("📚 **Librarian**: \"Checking out the library... cloning your code now.\"")
                repo_manager = RepoManager()
                local_path = repo_manager.clone_repo(f"https://github.com/{owner}/{repo}.git")
                
                # 2. Context Building
                st.write(f"🧠 **Architect**: \"Analyzing the structure... (Budget: {token_budget:,} tokens)\"")
                builder = ContextBuilder(local_path)
                repo_text = builder.build_repository_map(max_tokens=token_budget)
                
                # Token Metrics
                actual_tokens = builder._get_token_count(repo_text)
                st.caption(f"   *Read {actual_tokens:,} tokens of context.*")
                
                # 3. Agent Execution (Streaming)
                app = create_graph()
                initial_state = {
                    "repo_owner": owner, 
                    "repo_name": repo, 
                    "repo_data": repo_text,
                    "iteration": 0, 
                    "visual_assets": [],
                    # Inject custom instructions into the context if present
                    "project_summary": f"User Instructions: {custom_focus}" if custom_focus else None
                }
                
                final_state = initial_state
                
                # Node-to-Message Mapping
                NODE_MESSAGES = {
                    "intelligence": "🕵️ **Intelligence**: \"Auditing code quality and performance...\"",
                    "architect": "🏗️ **Architect**: \"Designing the blueprint and table of contents...\"",
                    "visualizer": "🎨 **Visualizer**: \"Sketching diagrams and generating badges...\"",
                    "writer": "✍️ **Writer**: \"Drafting the content chapter by chapter...\"",
                    "reviewer": "🔍 **Reviewer**: \"Reviewing for accuracy and tone...\""
                }

                for event in app.stream(initial_state):
                    for key, value in event.items():
                        if key in NODE_MESSAGES:
                            st.write(NODE_MESSAGES[key])
                            # Update status label to show current activity
                            status.update(label=f"🔄 Working: {key.title()} Agent...")
                        
                        # Merge the state update
                        if value:
                            final_state.update(value)
                        else:
                            logger.warning(f"Received empty update from node: {key}")

                draft = final_state.get('draft_sections', {}).get('full_readme', '')
                assets = "\n\n".join(final_state.get('visual_assets', []))
                final_md = f"{draft}\n\n{assets}"
                
                duration = time.time() - start_time
                status.update(label=f"🎉 All done! Documentation generated in {duration:.1f}s", state="complete", expanded=False)
                
            # Layout for Result
            st.balloons()
            st.divider()
            
            st.subheader("Your New README")
            st.info("💡 **Tip:** You can edit the text below or download it directly.")
            
            col_a, col_b = st.columns([1, 1])
            with col_a:
                st.download_button("💾 Download README.md", final_md, f"{repo}_README.md", use_container_width=True, type="primary")
            
            with st.expander("👁️ View Raw Markdown"):
                 st.code(final_md, language="markdown")

            st.markdown(f'<div class="markdown-body">{final_md}</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"😅 Oops! Something went wrong: {e}")
            logger.error(f"Error in dashboard: {e}", exc_info=True)
