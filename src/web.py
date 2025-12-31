import streamlit as st
import os
import sys
from dotenv import load_dotenv

# Hot-reload .env file so changes take effect immediately
load_dotenv(override=True)

# Fix Path to allow imports from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.config import config
from src.ui.styles import apply_custom_css
from src.ui.dashboard import render_dashboard
from src.ui.settings import render_settings

# Page Config
st.set_page_config(
    page_title="Intelligent README Generator",
    page_icon="📝",
    layout="wide"
)

# Apply Styles
apply_custom_css()

# --- Session State ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

def navigate_to(page):
    st.session_state.page = page
    st.rerun()

# --- Navigation ---
with st.sidebar:
    st.markdown("### Navigation")
    if st.button("🏠 Home", use_container_width=True, type="primary" if st.session_state.page == 'home' else "secondary"):
        navigate_to('home')
    if st.button("⚙️ Settings", use_container_width=True, type="primary" if st.session_state.page == 'settings' else "secondary"):
        navigate_to('settings')
    
    st.divider()
    st.caption(f"Active: **{config.ACTIVE_PROVIDER.upper()}**")
    if 'token_usage' in st.session_state:
        st.progress(min(st.session_state['token_usage'] / 100000, 1.0))
        st.caption(f"{st.session_state['token_usage']} Estimated Tokens")

# --- Router ---
if st.session_state.page == 'home':
    render_dashboard()
else:
    render_settings()
