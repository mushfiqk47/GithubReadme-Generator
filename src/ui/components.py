import streamlit as st

def render_header(title: str, subtitle: str = ""):
    """
    Renders a semantic page header with consistent styling.
    """
    st.markdown(f'<h1 class="main-header">{title}</h1>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<p class="sub-header">{subtitle}</p>', unsafe_allow_html=True)

def card_container(key: str = None):
    """
    Context manager to create a styled card container.
    """
    st.markdown('<div class="ui-card">', unsafe_allow_html=True)
    # Note: Streamlit containers don't strictly nest inside the HTML above 
    # in the DOM tree in a way that inherits background perfectly if we use standard st.container() 
    # *inside* this block without closing it.
    # However, for simple visual wrapping, passing the start div here and end div later is a pattern.
    # A cleaner Streamlit way is to just use the container for layout and surrounding markdown for style.
    # We will return a container that the user can put stuff in.
    return st.container()

def end_card():
    """Closing tag for the card container strategy above."""
    st.markdown('</div>', unsafe_allow_html=True)
