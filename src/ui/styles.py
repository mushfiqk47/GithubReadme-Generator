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
            --text-primary: #f0f6fc;
            --text-secondary: #8b949e;
            --accent-color: #58a6ff;
            --border-color: #30363d;
            --success-color: #238636;
        }

        /* --- Base Typography --- */
        .stApp {
            background-color: var(--bg-color);
            background-image: radial-gradient(circle at top right, #1f242d 0%, #0d1117 40%);
            color: var(--text-primary);
        }
        
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            color: var(--text-primary) !important;
            letter-spacing: -0.02em;
        }
        
        p, div, label, span {
            color: var(--text-primary);
        }

        /* --- Components --- */
        
        /* Markdown Container (Readme Preview) */
        .markdown-body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
            font-size: 16px;
            line-height: 1.6;
            word-wrap: break-word;
            background-color: var(--bg-color);
            color: var(--text-primary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 32px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        }

        /* Custom Header Classes */
        .main-header { 
            font-size: 2.5rem; 
            font-weight: 800; 
            background: -webkit-linear-gradient(120deg, #58a6ff, #a371f7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
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
            border-radius: 8px; 
            font-weight: 600;
            border: 1px solid var(--border-color);
            background-color: #21262d; 
            color: var(--text-primary);
            transition: all 0.2s ease;
            box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        }
        
        .stButton > button:hover {
            border-color: var(--accent-color);
            background-color: #30363d;
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        
        .stButton > button[kind="primary"] {
            background-color: #238636;
            border-color: rgba(255,255,255,0.1);
            color: white;
            box-shadow: 0 0 15px rgba(35, 134, 54, 0.4);
        }
        
        .stButton > button[kind="primary"]:hover {
            background-color: #2ea043;
            box-shadow: 0 0 20px rgba(35, 134, 54, 0.6);
        }

        /* Custom Card Container */
        .ui-card { 
            background: rgba(22, 27, 34, 0.8); /* Glass effect */
            backdrop-filter: blur(10px);
            padding: 1.5rem; 
            border-radius: 12px; 
            border: 1px solid var(--border-color); 
            margin-bottom: 1rem; 
            box-shadow: 0 8px 32px rgba(0,0,0,0.1); 
        }
        
        .ui-card h3 {
            margin-top: 0;
            font-size: 1.25rem;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.5rem;
            margin-bottom: 1rem;
        }
        
        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #010409;
            border-right: 1px solid var(--border-color);
        }

    </style>
    """, unsafe_allow_html=True)
