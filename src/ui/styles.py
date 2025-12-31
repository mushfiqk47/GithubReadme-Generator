import streamlit as st

def apply_custom_css():
    """
    Applies the global CSS styles for the application.
    Focuses on 'Cosmic Glass' aesthetic with WCAG AA compliance.
    """
    st.markdown("""
    <style>
        /* --- Global Variables --- */
        :root {
            --bg-color: #0d1117;
            --card-bg: #161b22;
            --text-primary: #f0f6fc; /* Bright white for better contrast */
            --text-secondary: #8b949e;
            --accent-color: #58a6ff;
            --border-color: #30363d;
            --success-color: #238636;
        }

        /* --- Base Typography --- */
        .stApp {
            background-color: var(--bg-color);
            color: var(--text-primary);
        }
        
        h1, h2, h3, h4, h5, h6 {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            color: var(--text-primary) !important;
        }
        
        p, div, label, span {
            color: var(--text-primary); /* Default to high contrast */
        }

        /* --- Components --- */
        
        /* Markdown Container (Readme Preview) */
        .markdown-body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
            font-size: 16px;
            line-height: 1.6; /* Improved readability */
            word-wrap: break-word;
            background-color: var(--bg-color);
            color: var(--text-primary);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 32px;
        }

        /* Custom Header Classes */
        .main-header { 
            font-size: 2.5rem; 
            font-weight: 700; 
            color: var(--accent-color) !important;
            margin-bottom: 0.5rem;
        }
        
        .sub-header { 
            font-size: 1.1rem; 
            color: var(--text-secondary) !important; 
            margin-bottom: 2rem; 
        }

        /* Streamlit Button Override */
        .stButton > button { 
            width: 100%; 
            border-radius: 6px; 
            font-weight: 600;
            border: 1px solid var(--border-color);
            background-color: #21262d; 
            color: var(--text-primary);
            transition: all 0.2s ease;
        }
        
        .stButton > button:hover {
            border-color: var(--text-secondary);
            background-color: #30363d;
        }
        
        .stButton > button[kind="primary"] {
            background-color: #238636;
            border-color: #2ea043;
            color: white;
        }

        /* Custom Card Container */
        .ui-card { 
            background: var(--card-bg); 
            padding: 1.5rem; 
            border-radius: 8px; 
            border: 1px solid var(--border-color); 
            margin-bottom: 1rem; 
            box-shadow: 0 4px 6px rgba(0,0,0,0.1); /* Subtle depth */
        }
        
        .ui-card h3 {
            margin-top: 0;
            font-size: 1.25rem;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.5rem;
            margin-bottom: 1rem;
        }

    </style>
    """, unsafe_allow_html=True)
