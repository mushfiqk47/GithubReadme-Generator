import streamlit as st
import os
import sys
from dotenv import load_dotenv

# Hot-reload .env
load_dotenv(override=True)

# Fix Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.config import config
from src.ui.styles import apply_custom_css
from src.ui.dashboard import render_dashboard
from src.ui.settings import render_settings

# Page Config
st.set_page_config(
    page_title="Intelligent README Generator",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Styles
apply_custom_css()

# Navigation
if 'page' not in st.session_state:
    st.session_state.page = 'home'

def navigate_to(page):
    st.session_state.page = page
    st.rerun()

with st.sidebar:
    st.title("IRG")
    st.caption(f"v{config.VERSION if hasattr(config, 'VERSION') else '2.0'}")
    st.markdown("---")
    
    if st.button("🏠 Generator", use_container_width=True, type="primary" if st.session_state.page == 'home' else "secondary"):
        navigate_to('home')
    
    if st.button("⚙️ Settings", use_container_width=True, type="primary" if st.session_state.page == 'settings' else "secondary"):
        navigate_to('settings')

if st.session_state.page == 'home':
    render_dashboard()
else:
    render_settings()
