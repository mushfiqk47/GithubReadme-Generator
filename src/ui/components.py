"""
Modular, accessible UI components with WCAG compliance.
"""
import streamlit as st
from typing import Optional, Callable
from contextlib import contextmanager
from src.ui.constants import COLORS, SPACING, BORDER_RADIUS, FONT_SIZES, FOCUS_STYLES


def render_header(title: str, subtitle: str = "", level: int = 1):
    """
    Renders a semantic page header with consistent styling.
    
    Args:
        title: Main heading text
        subtitle: Optional subtitle/description
        level: Heading level (1-6) for semantic HTML
    """
    tag = f"h{level}"
    st.markdown(
        f'<{tag} class="main-header">{title}</{tag}>',
        unsafe_allow_html=True
    )
    if subtitle:
        st.markdown(
            f'<p class="sub-header" role="doc-subtitle">{subtitle}</p>',
            unsafe_allow_html=True
        )


@contextmanager
def ui_card(
    title: str = "",
    icon: str = "",
    border: bool = True,
    padding: str = "lg",
    expandable: bool = False
):
    """
    Context manager to create a styled, accessible card container.
    
    Args:
        title: Optional card title
        icon: Optional icon emoji
        border: Whether to show border
        padding: Padding size from SPACING
        expandable: Whether the card can be expanded
    """
    padding_value = SPACING.get(padding, SPACING["lg"])
    border_style = f"border: 1px solid {COLORS['border_default']};" if border else ""
    icon_html = f"<span class='card-icon' aria-hidden='true'>{icon}</span> " if icon else ""
    title_html = f"<h3 class='card-title'>{icon_html}{title}</h3>" if title else ""
    
    html = f"""
    
        {title_html}
    """
    
    st.markdown(html, unsafe_allow_html=True)
    try:
        yield
    finally:
        st.markdown("</div>", unsafe_allow_html=True)


def button(
    label: str,
    on_click: Optional[Callable] = None,
    variant: str = "primary",
    icon: str = "",
    disabled: bool = False,
    help: str = "",
    use_container_width: bool = True,
    key: Optional[str] = None
) -> bool:
    """
    Accessible button with consistent styling.
    
    Args:
        label: Button text
        on_click: Callback function
        variant: 'primary', 'secondary', 'danger', 'success'
        icon: Optional icon emoji
        disabled: Whether button is disabled
        help: Tooltip text
        use_container_width: Full width button
        key: Unique key for the button
    
    Returns:
        True if button was clicked
    """
    icon_prefix = f"{icon} " if icon else ""
    full_label = f"{icon_prefix}{label}"
    
    type_map = {
        "primary": "primary",
        "secondary": "secondary",
        "danger": "secondary",  # Streamlit doesn't have danger type
        "success": "primary",
    }
    
    return st.button(
        full_label,
        on_click=on_click,
        type=type_map.get(variant, "secondary"),
        disabled=disabled,
        help=help,
        use_container_width=use_container_width,
        key=key
    )


def status_indicator(
    status: str,
    message: str = "",
    expanded: bool = False
):
    """
    Accessible status indicator with proper ARIA attributes.
    
    Args:
        status: Status type ('info', 'success', 'warning', 'error', 'loading')
        message: Status message
        expanded: Whether to show expanded view
    """
    status_map = {
        "info": ("ℹ️", st.info),
        "success": ("✅", st.success),
        "warning": ("⚠️", st.warning),
        "error": ("❌", st.error),
        "loading": ("⏳", None),
    }
    
    icon, func = status_map.get(status, ("ℹ️", st.info))
    icon_prefix = f"{icon} " if icon else ""
    
    if func and message:
        func(f"{icon_prefix}{message}")
    elif status == "loading":
        st.spinner(message)


def progress_bar(
    progress: float,
    label: str = "",
    show_percentage: bool = True
):
    """
    Accessible progress bar with ARIA attributes.
    
    Args:
        progress: Progress value (0-100)
        label: Optional label
        show_percentage: Whether to show percentage
    """
    if show_percentage:
        label_text = f"{label} ({progress:.0f}%)" if label else f"{progress:.0f}%"
    else:
        label_text = label
    
    st.progress(progress / 100)
    if label_text:
        st.caption(label_text)


def render_mermaid(markdown_text: str, caption: str = "Architecture Diagram"):
    """
    Extracts mermaid code from markdown and renders it using mermaid.ink.
    
    Args:
        markdown_text: Markdown content containing mermaid diagrams
        caption: Alt text for accessibility
    """
    import re
    import base64
    
    pattern = r"```mermaid\n(.*?)\n```"
    matches = re.findall(pattern, markdown_text, re.DOTALL)
    
    for i, code in enumerate(matches):
        graph_bytes = code.encode("utf8")
        base64_bytes = base64.b64encode(graph_bytes)
        base64_string = base64_bytes.decode("ascii")
        url = f"https://mermaid.ink/img/{base64_string}"
        
        st.markdown(f"### 📊 Architecture Diagram {i + 1}" if len(matches) > 1 else "### 📊 Architecture Diagram")
        st.image(url, caption=caption, use_container_width=True)


def input_field(
    label: str,
    value: str = "",
    placeholder: str = "",
    help_text: str = "",
    type: str = "default",
    max_chars: Optional[int] = None,
    key: Optional[str] = None
) -> str:
    """
    Accessible input field with consistent styling.
    
    Args:
        label: Field label
        value: Default value
        placeholder: Placeholder text
        help_text: Help tooltip
        type: Input type ('default', 'password')
        max_chars: Maximum character limit
        key: Unique key
    
    Returns:
        User input value
    """
    return st.text_input(
        label=label,
        value=value,
        placeholder=placeholder,
        help=help_text,
        type=type,
        max_chars=max_chars,
        key=key
    )


def text_area_field(
    label: str,
    value: str = "",
    placeholder: str = "",
    help_text: str = "",
    height: Optional[int] = None,
    max_chars: Optional[int] = None,
    key: Optional[str] = None
) -> str:
    """
    Accessible text area field.
    
    Args:
        label: Field label
        value: Default value
        placeholder: Placeholder text
        help_text: Help tooltip
        height: Height in pixels
        max_chars: Maximum character limit
        key: Unique key
    
    Returns:
        User input value
    """
    return st.text_area(
        label=label,
        value=value,
        placeholder=placeholder,
        help=help_text,
        height=height,
        max_chars=max_chars,
        key=key
    )


def select_field(
    label: str,
    options: list,
    index: int = 0,
    help_text: str = "",
    key: Optional[str] = None
) -> str:
    """
    Accessible select dropdown.
    
    Args:
        label: Field label
        options: List of options
        index: Default selected index
        help_text: Help tooltip
        key: Unique key
    
    Returns:
        Selected value
    """
    return st.selectbox(
        label=label,
        options=options,
        index=index,
        help=help_text,
        key=key
    )


def slider_field(
    label: str,
    min_value: float,
    max_value: float,
    value: float,
    step: float = 1.0,
    help_text: str = "",
    key: Optional[str] = None
) -> float:
    """
    Accessible slider input.
    
    Args:
        label: Field label
        min_value: Minimum value
        max_value: Maximum value
        value: Default value
        step: Step increment
        help_text: Help tooltip
        key: Unique key
    
    Returns:
        Selected value
    """
    return st.slider(
        label=label,
        min_value=min_value,
        max_value=max_value,
        value=value,
        step=step,
        help=help_text,
        key=key
    )


def tabs(tab_names: list, key: Optional[str] = None):
    """
    Accessible tabs with proper ARIA attributes.
    
    Args:
        tab_names: List of tab names
        key: Unique key
    
    Returns:
        List of tab context managers
    """
    return st.tabs(tab_names)


def divider():
    """Render a visual divider with semantic meaning."""
    st.markdown('<hr class="divider" aria-hidden="true">', unsafe_allow_html=True)


def spacer(height: str = "md"):
    """
    Add vertical spacing.
    
    Args:
        height: Spacing size from SPACING
    """
    height_value = SPACING.get(height, SPACING["md"])
    st.markdown(f'<div style="height: {height_value};" aria-hidden="true"></div>', unsafe_allow_html=True)
