import streamlit as st
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
