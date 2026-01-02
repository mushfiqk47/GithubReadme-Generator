import streamlit as st
import re
import base64
from contextlib import contextmanager

def render_header(title: str, subtitle: str = ""):
    """
    Renders a semantic page header with consistent styling.
    """
    st.markdown(f'<h1 class="main-header">{title}</h1>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<p class="sub-header">{subtitle}</p>', unsafe_allow_html=True)

@contextmanager
def ui_card():
    """
    Context manager to create a styled card container.
    Usage:
        with ui_card():
            st.write("Content inside card")
    """
    st.markdown('<div class="ui-card">', unsafe_allow_html=True)
    try:
        yield
    finally:
        st.markdown('</div>', unsafe_allow_html=True)

def render_mermaid(markdown_text: str):
    """
    Extracts mermaid code from markdown and renders it using mermaid.ink
    """
    pattern = r"```mermaid\n(.*?)\n```"
    matches = re.findall(pattern, markdown_text, re.DOTALL)
    
    for code in matches:
        # Encode for URL
        graph_bytes = code.encode("utf8")
        base64_bytes = base64.b64encode(graph_bytes)
        base64_string = base64_bytes.decode("ascii")
        url = f"https://mermaid.ink/img/{base64_string}"
        
        st.markdown("### 📊 Architecture Diagram")
        st.image(url, caption="Generated Architecture", use_container_width=True)
