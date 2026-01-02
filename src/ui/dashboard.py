import streamlit as st
import time
import logging
from datetime import datetime

from src.ingestion.repo_manager import RepoManager
from src.core.workflow import ReadmeWorkflow
from src.ui.components import render_header, render_mermaid
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
    
    # Initialize History
    if 'history' not in st.session_state:
        st.session_state.history = []

    # Tabs
    tab_main, tab_history = st.tabs(["🚀 Generator", "📜 History"])

    with tab_main:
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
                
            # Narrative Status Updates
            with st.status(f"🚀 Spinnning up the team... (Brain: {config.MODEL_PLANNER})", expanded=True) as status:
                progress_bar = st.progress(0)
                
                workflow = ReadmeWorkflow()
                final_result = None
                
                # --- Execute Workflow ---
                for event in workflow.run(repo_url, custom_focus, token_budget):
                    if event.type == "status":
                        st.write(event.message)
                        status.update(label=f"🔄 {event.message}")
                        progress_bar.progress(event.progress)
                    
                    elif event.type == "log":
                        st.caption(f"ℹ️ {event.message}")
                        
                    elif event.type == "error":
                        st.error(f"❌ {event.message}")
                        status.update(label="❌ Generation Failed", state="error", expanded=True)
                        return # Stop
                        
                    elif event.type == "result":
                        final_result = event.payload
                        progress_bar.progress(100)
                        status.update(label=f"🎉 All done! Documentation generated in {event.payload['duration']:.1f}s", state="complete", expanded=False)

                if final_result:
                    final_md = final_result['markdown']
                    owner = final_result['owner']
                    repo = final_result['repo']

                    # Save to history
                    st.session_state.history.insert(0, {
                        "repo": f"{owner}/{repo}",
                        "time": datetime.now().strftime("%H:%M"),
                        "content": final_md
                    })
                    
                    # Layout for Result
                    st.balloons()
                    st.divider()
                    st.subheader("🎉 Your New README")
                    
                    # New Container: Tabs for better organization
                    tab_preview, tab_raw = st.tabs(["👁️ Live Preview", "📝 Raw Markdown"])
                    
                    with tab_preview:
                        st.info("💡 **Tip:** This is how your README will look on GitHub.")
                        # Render Visuals First
                        render_mermaid(final_md)
                        st.markdown(f'<div class="markdown-body">{final_md}</div>', unsafe_allow_html=True)
                        
                    with tab_raw:
                        st.success("⬇️ Copy this code into your README.md file.")
                        st.code(final_md, language="markdown")
                    
                    # Download Actions
                    col_a, col_b = st.columns([1, 1])
                    with col_a:
                        st.download_button("💾 Download .md File", final_md, f"{repo}_README.md", use_container_width=True, type="primary")

    with tab_history:
        if not st.session_state.history:
            st.info("No history yet. Generate a README to see it here!")
        else:
            for i, item in enumerate(st.session_state.history):
                with st.expander(f"{item['repo']} - {item['time']}"):
                    st.download_button(f"Download {item['repo']}", item['content'], f"readme_{i}.md")
                    st.markdown(item['content'])

