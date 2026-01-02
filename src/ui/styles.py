"""
WCAG AA compliant styles with semantic structure and accessibility.
"""
import streamlit as st
from src.ui.constants import COLORS, SPACING, BORDER_RADIUS, FONT_SIZES, FOCUS_STYLES


def apply_custom_css():
    """
    Applies global CSS styles with WCAG AA compliance.
    Features:
    - Proper color contrast ratios (4.5:1 for normal text, 3:1 for large text)
    - Semantic HTML structure
    - Accessible focus states
    - Responsive design
    """
    st.markdown(f"""
    <style>
        /* --- CSS Custom Properties for Theming --- */
        :root {{
            /* Colors */
            --bg-primary: {COLORS['bg_primary']};
            --bg-secondary: {COLORS['bg_secondary']};
            --bg-tertiary: {COLORS['bg_tertiary']};
            --bg-sidebar: {COLORS['bg_sidebar']};
            
            --text-primary: {COLORS['text_primary']};
            --text-secondary: {COLORS['text_secondary']};
            --text-muted: {COLORS['text_muted']};
            
            --accent-blue: {COLORS['accent_blue']};
            --accent-purple: {COLORS['accent_purple']};
            --accent-green: {COLORS['accent_green']};
            --accent-green-hover: {COLORS['accent_green_hover']};
            --accent-red: {COLORS['accent_red']};
            --accent-yellow: {COLORS['accent_yellow']};
            
            --border-default: {COLORS['border_default']};
            --border-focus: {COLORS['border_focus']};
            
            /* Spacing */
            --spacing-xs: {SPACING['xs']};
            --spacing-sm: {SPACING['sm']};
            --spacing-md: {SPACING['md']};
            --spacing-lg: {SPACING['lg']};
            --spacing-xl: {SPACING['xl']};
            
            /* Border Radius */
            --radius-sm: {BORDER_RADIUS['sm']};
            --radius-md: {BORDER_RADIUS['md']};
            --radius-lg: {BORDER_RADIUS['lg']};
            
            /* Typography */
            --font-size-base: {FONT_SIZES['base']};
            --font-size-lg: {FONT_SIZES['lg']};
            --font-size-xl: {FONT_SIZES['xl']};
            --font-size-2xl: {FONT_SIZES['2xl']};
            --font-size-3xl: {FONT_SIZES['3xl']};
        }}

        /* --- Base Styles --- */
        .stApp {{
            background-color: var(--bg-primary);
            background-image: radial-gradient(circle at top right, #1f242d 0%, var(--bg-primary) 40%);
            color: var(--text-primary);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
        }}
        
        /* --- Typography (WCAG AA Compliant) --- */
        h1, h2, h3, h4, h5, h6 {{
            color: var(--text-primary) !important;
            letter-spacing: -0.02em;
            font-weight: 700;
            margin-top: 0;
        }}
        
        h1 {{ font-size: var(--font-size-3xl); }}
        h2 {{ font-size: var(--font-size-2xl); }}
        h3 {{ font-size: var(--font-size-xl); }}
        h4 {{ font-size: var(--font-size-lg); }}
        
        p, div, label, span {{
            color: var(--text-primary);
        }}
        
        .stMarkdown {{
            color: var(--text-primary);
        }}
        
        /* --- Semantic Header Classes --- */
        .main-header {{
            font-size: var(--font-size-3xl);
            font-weight: 800;
            background: linear-gradient(120deg, var(--accent-blue), var(--accent-purple));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: var(--spacing-sm);
            line-height: 1.2;
        }}
        
        .sub-header {{
            font-size: var(--font-size-lg);
            color: var(--text-secondary) !important;
            margin-bottom: var(--spacing-xl);
            font-weight: 400;
        }}
        
        /* --- Accessible Focus States --- */
        *:focus-visible {{
            outline: {FOCUS_STYLES['outline']};
            outline-offset: {FOCUS_STYLES['outline_offset']};
        }}
        
        /* --- Button Styles (WCAG AA Contrast) --- */
        .stButton > button {{
            width: 100%;
            border-radius: var(--radius-md);
            font-weight: 600;
            font-size: var(--font-size-base);
            padding: var(--spacing-sm) var(--spacing-md);
            border: 1px solid var(--border-default);
            background-color: var(--bg-tertiary);
            color: var(--text-primary);
            transition: all {SPACING['md']} ease;
            box-shadow: 0 1px 2px rgba(0,0,0,0.1);
            cursor: pointer;
        }}
        
        .stButton > button:hover:not(:disabled) {{
            border-color: var(--accent-blue);
            background-color: var(--bg-secondary);
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}
        
        .stButton > button:focus-visible {{
            outline: {FOCUS_STYLES['outline']};
            outline-offset: {FOCUS_STYLES['outline_offset']};
            box-shadow: {FOCUS_STYLES['box_shadow']};
        }}
        
        .stButton > button:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}
        
        .stButton > button[kind="primary"] {{
            background-color: var(--accent-green);
            border-color: rgba(255,255,255,0.1);
            color: white;
            box-shadow: 0 0 15px rgba(35, 134, 54, 0.4);
        }}
        
        .stButton > button[kind="primary"]:hover:not(:disabled) {{
            background-color: var(--accent-green-hover);
            box-shadow: 0 0 20px rgba(35, 134, 54, 0.6);
        }}
        
        /* --- Card Component --- */
                    .ui-card {{
                        background: transparent;
                        backdrop-filter: none;
                        -webkit-backdrop-filter: none;
                        padding: 0;
                        border-radius: 0;
                        border: none;
                        margin-bottom: 0;
                        box-shadow: none;
                    }}
        
        .ui-card h3 {{
            margin-top: 0;
            font-size: var(--font-size-xl);
            border-bottom: 1px solid var(--border-default);
            padding-bottom: var(--spacing-sm);
            margin-bottom: var(--spacing-md);
            color: var(--text-primary);
        }}
        
        .ui-card .card-icon {{
            font-size: var(--font-size-xl);
            margin-right: var(--spacing-xs);
        }}
        
        /* .ui-card .card-content removed */
        
        /* --- Markdown Body (Theme-matched Preview) --- */
        .markdown-body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
            font-size: 16px;
            line-height: 1.6;
            word-wrap: break-word;
            background-color: {COLORS['bg_secondary']};
            color: {COLORS['text_primary']};
            border: 1px solid {COLORS['border_default']};
            border-radius: {BORDER_RADIUS['lg']};
            padding: 32px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.25);
        }}
        
        .markdown-body h1,
        .markdown-body h2,
        .markdown-body h3,
        .markdown-body h4,
        .markdown-body h5,
        .markdown-body h6 {{
            color: {COLORS['text_primary']} !important;
            margin-top: 24px;
            margin-bottom: 12px;
            font-weight: 700;
        }}
        
        .markdown-body h1 {{ font-size: 2em; border-bottom: 1px solid {COLORS['border_default']}; padding-bottom: 0.3em; }}
        .markdown-body h2 {{ font-size: 1.6em; border-bottom: 1px solid {COLORS['border_default']}; padding-bottom: 0.2em; }}
        .markdown-body h3 {{ font-size: 1.3em; }}
        .markdown-body h4 {{ font-size: 1.1em; }}
        .markdown-body h5 {{ font-size: 1em; }}
        .markdown-body h6 {{ font-size: 0.95em; color: {COLORS['text_secondary']}; }}
        
        .markdown-body p {{
            margin-top: 0;
            margin-bottom: 16px;
            color: {COLORS['text_secondary']};
        }}
        
        .markdown-body a {{
            color: {COLORS['accent_blue']};
            text-decoration: none;
        }}
        
        .markdown-body a:hover {{
            text-decoration: underline;
        }}
        
        .markdown-body ul,
        .markdown-body ol {{
            margin-top: 0;
            margin-bottom: 16px;
            padding-left: 2em;
        }}
        
        .markdown-body li {{ margin-top: 4px; }}
        .markdown-body li + li {{ margin-top: 6px; }}
        
        .markdown-body blockquote {{
            margin: 0 0 16px;
            padding: 0 1em;
            color: {COLORS['text_secondary']};
            border-left: 4px solid {COLORS['accent_blue']};
            background: {COLORS['bg_tertiary']};
        }}
        
        .markdown-body code {{
            padding: 0.2em 0.4em;
            margin: 0;
            font-size: 85%;
            font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, Liberation Mono, monospace;
            background-color: {COLORS['bg_tertiary']};
            border-radius: 6px;
            color: {COLORS['text_primary']};
        }}
        
        .markdown-body pre {{
            padding: 16px;
            overflow: auto;
            font-size: 90%;
            line-height: 1.45;
            background-color: {COLORS['bg_tertiary']};
            border: 1px solid {COLORS['border_default']};
            border-radius: 10px;
            margin-top: 0;
            margin-bottom: 16px;
        }}
        
        .markdown-body pre code {{
            background-color: transparent;
            border-width: 0;
            border-radius: 0;
            padding: 0;
            margin: 0;
            font-size: 100%;
            word-break: normal;
            white-space: pre;
        }}
        
        .markdown-body table {{
            display: block;
            width: max-content;
            max-width: 100%;
            overflow: auto;
            margin-top: 0;
            margin-bottom: 16px;
            border-spacing: 0;
            border-collapse: collapse;
        }}
        
        .markdown-body table th {{
            font-weight: 600;
            background-color: {COLORS['bg_tertiary']};
            color: {COLORS['text_primary']};
        }}
        
        .markdown-body table th,
        .markdown-body table td {{
            padding: 8px 12px;
            border: 1px solid {COLORS['border_default']};
        }}
        
        .markdown-body table tr {{
            background-color: {COLORS['bg_secondary']};
            border-top: 1px solid {COLORS['border_default']};
        }}
        
        .markdown-body table tr:nth-child(2n) {{
            background-color: {COLORS['bg_tertiary']};
        }}
        
        .markdown-body hr {{
            height: 1px;
            padding: 0;
            margin: 24px 0;
            background-color: {COLORS['border_default']};
            border: 0;
        }}
        
        .markdown-body img {{
            max-width: 100%;
            box-sizing: content-box;
            background-color: transparent;
        }}
        
        .markdown-body .task-list-item {{
            list-style-type: none;
        }}
        
        .markdown-body .task-list-item label {{
            display: flex;
            align-items: center;
        }}
        
        .markdown-body .task-list-item input[type="checkbox"] {{
            margin: 0 0.4em 0 0;
            vertical-align: middle;
        }}
        
        /* --- Sidebar Styling --- */
        section[data-testid="stSidebar"] {{
            background-color: var(--bg-sidebar);
            border-right: 1px solid var(--border-default);
        }}
        
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {{
            color: var(--text-primary) !important;
        }}
        
        /* --- Input Fields --- */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select {{
            background-color: var(--bg-tertiary);
            color: var(--text-primary);
            border: 1px solid var(--border-default);
            border-radius: var(--radius-md);
        }}
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus,
        .stSelectbox > div > div > select:focus {{
            border-color: var(--accent-blue);
            outline: {FOCUS_STYLES['outline']};
            outline-offset: {FOCUS_STYLES['outline_offset']};
        }}
        
        /* --- Progress Bar --- */
        .stProgress > div > div > div > div {{
            background-color: var(--accent-green);
        }}
        
        /* --- Tabs --- */
        .stTabs [data-baseweb="tab-list"] {{
            gap: var(--spacing-md);
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background-color: var(--bg-tertiary);
            border-radius: var(--radius-md) var(--radius-md) 0 0;
            padding: var(--spacing-sm) var(--spacing-md);
            color: var(--text-secondary);
        }}
        
        .stTabs [aria-selected="true"] {{
            background-color: var(--bg-secondary);
            color: var(--text-primary);
            border-bottom: 2px solid var(--accent-blue);
        }}
        
        /* --- Divider --- */
        .divider {{
            border: none;
            border-top: 1px solid var(--border-default);
            margin: var(--spacing-lg) 0;
        }}
        
        /* --- Expander --- */
        .streamlit-expanderHeader {{
            background-color: var(--bg-tertiary);
            border-radius: var(--radius-md);
            padding: var(--spacing-sm) var(--spacing-md);
            color: var(--text-primary);
        }}
        
        .streamlit-expanderContent {{
            background-color: var(--bg-secondary);
            border-radius: 0 0 var(--radius-md) var(--radius-md);
            padding: var(--spacing-md);
        }}
        
        /* --- Status Messages --- */
        .stAlert {{
            border-radius: var(--radius-md);
            border: 1px solid var(--border-default);
        }}
        
        /* --- Responsive Design --- */
        @media (max-width: 768px) {{
            .main-header {{
                font-size: var(--font-size-2xl);
            }}
            
            .markdown-body {{
                padding: var(--spacing-md);
            }}
        }}
        
        /* --- Accessibility: Skip to Content --- */
        .skip-to-content {{
            position: absolute;
            top: -40px;
            left: 0;
            background: var(--accent-blue);
            color: white;
            padding: var(--spacing-sm) var(--spacing-md);
            z-index: 100;
            transition: top 0.3s;
        }}
        
        .skip-to-content:focus {{
            top: 0;
        }}
        
        /* --- Reduced Motion --- */
        @media (prefers-reduced-motion: reduce) {{
            *,
            *::before,
            *::after {{
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }}
        }}
    </style>
    """, unsafe_allow_html=True)
