import streamlit as st
import os
import requests
from src.core.config import config
from src.core.llm_factory import LLMFactory
from langchain_core.messages import HumanMessage
from src.ui.components import render_header, ui_card

def save_env_var(key, value):
    """Save to session and .env file"""
    if not value: return
    os.environ[key] = value
    try:
        # Try to write to .env for persistence
        env_path = os.path.join(os.getcwd(), '.env')
        # Check if key exists
        content = ""
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                content = f.read()
        
        if f"{key}=" in content:
            # Simple replacement
            lines = content.split('\n')
            new_lines = []
            found = False
            for line in lines:
                if line.startswith(f"{key}="):
                    new_lines.append(f"{key}={value}")
                    found = True
                else:
                    new_lines.append(line)
            if not found: new_lines.append(f"{key}={value}")
            with open(env_path, 'w') as f:
                f.write("\n".join(new_lines))
        else:
            with open(env_path, 'a') as f:
                f.write(f"\n{key}={value}")
        
        st.toast(f"Saved {key}!", icon="💾")
    except Exception as e:
        st.error(f"Could not save to .env: {e}")

def fetch_models_for_provider(provider, api_key, base_url=None):
    """Helper to fetch models from various APIs."""
    models = []
    try:
        if provider == "openai":
            headers = {"Authorization": f"Bearer {api_key}"}
            resp = requests.get("https://api.openai.com/v1/models", headers=headers, timeout=5)
            if resp.status_code == 200:
                models = [m['id'] for m in resp.json()['data'] if 'gpt' in m['id'] or 'o1' in m['id']]
                
        elif provider == "groq":
            headers = {"Authorization": f"Bearer {api_key}"}
            resp = requests.get("https://api.groq.com/openai/v1/models", headers=headers, timeout=5)
            if resp.status_code == 200:
                models = [m['id'] for m in resp.json()['data']]
        
        elif provider == "google":
            resp = requests.get(f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}", timeout=5)
            if resp.status_code == 200:
                models = [m['name'].replace('models/', '') for m in resp.json()['models'] if 'generateContent' in m['supportedGenerationMethods']]
                
        elif provider == "openrouter":
            headers = {"Authorization": f"Bearer {api_key}"}
            resp = requests.get("https://openrouter.ai/api/v1/models", headers=headers, timeout=5)
            if resp.status_code == 200:
                models = [m['id'] for m in resp.json()['data']]
                
        elif provider == "local":
            resp = requests.get(f"{base_url}/models", timeout=2)
            if resp.status_code == 200:
                data = resp.json()
                if 'data' in data:
                    models = [m['id'] for m in data['data']]
                elif 'models' in data:
                    models = [m.get('id', m.get('name')) for m in data['models']]
                    
        models.sort()
    except Exception as e:
        st.error(f"Error fetching models: {e}")
        
    return models

def get_provider_status(provider):
    """Checks if the provider is configured (has key or is local)."""
    if provider == "local":
        return True # Assume true or check URL validity?
    
    key_var = f"{provider.upper()}_API_KEY"
    return bool(os.getenv(key_var))

def test_connection(provider):
    """Runs a test connection request."""
    with st.spinner(f"Pinging {provider}..."):
        try:
            llm = LLMFactory.get_model(os.getenv("MODEL_PLANNER", "gpt-4o"))
            resp = llm.invoke([HumanMessage(content="Reply with 'OK'.")])
            st.success(f"Connected! Response: {resp.content}")
        except Exception as e:
            st.error(f"Connection Failed: {e}")

def render_settings():
    render_header("⚙️ Configuration", "Manage your AI brains and system preferences.")

    # 1. Define Providers & their Metadata
    PROVIDERS = {
        "openai": {"icon": "🤖", "name": "OpenAI", "desc": "Industry standard. Best for reasoning (GPT-4o)."},
        "anthropic": {"icon": "🧠", "name": "Anthropic", "desc": "Huge context window. Great for large codebases (Claude 3.5)."},
        "google": {"icon": "⚡", "name": "Google", "desc": "Fast and cost-effective (Gemini 1.5 Pro)."},
        "groq": {"icon": "🚀", "name": "Groq", "desc": "Lightning fast inference (Llama 3)."},
        "openrouter": {"icon": "🔗", "name": "OpenRouter", "desc": "Aggregator for all models."},
        "local": {"icon": "🏠", "name": "Local LLM", "desc": "Privacy-focused (Ollama/LM Studio)."},
    }

    # 2. Layout: Side-by-Side (Menu | Content)
    col_menu, col_content = st.columns([1, 2.5], gap="large")

    with col_menu:
        st.subheader("AI Provider")
        
        # Format labels with status indicators
        def format_func(option):
            data = PROVIDERS[option]
            configured = get_provider_status(option)
            status = "✅" if configured else "⚪"
            return f"{status} {data['name']}"

        # Use a radio button that looks like a vertical menu
        selected_key = st.radio(
            "Select Provider",
            options=list(PROVIDERS.keys()),
            format_func=format_func,
            index=list(PROVIDERS.keys()).index(config.ACTIVE_PROVIDER) if config.ACTIVE_PROVIDER in PROVIDERS else 0,
            label_visibility="collapsed"
        )
        
        # Immediate switch logic
        if selected_key != config.ACTIVE_PROVIDER:
            save_env_var("ACTIVE_PROVIDER", selected_key)
            config.ACTIVE_PROVIDER = selected_key
            st.rerun()
            
        st.divider()
        st.caption(f"Currently Active:\n**{PROVIDERS[selected_key]['name']}**")

    with col_content:
        provider_data = PROVIDERS[selected_key]
        
        # Render the 'Active' Card
        with ui_card():
            c1, c2 = st.columns([0.1, 0.9])
            with c1: st.title(provider_data['icon'])
            with c2: 
                st.subheader(f"{provider_data['name']} Settings")
                st.caption(provider_data['desc'])
            
            st.divider()

            # Dynamic Form based on provider
            api_key = ""
            fetch_supported = False
            
            # --- INPUT SECTION ---
            if selected_key == "local":
                 st.info("Ensure your local server (e.g., LM Studio, Ollama) is running.")
                 base_url = st.text_input("Base URL", value=os.getenv("LOCAL_LLM_BASE_URL", "http://localhost:1234/v1"))
                 if st.button("💾 Save URL"):
                     save_env_var("LOCAL_LLM_BASE_URL", base_url)
                     save_env_var("USE_LOCAL_LLM", "true")
                     config.LOCAL_LLM_BASE_URL = base_url
                     config.USE_LOCAL_LLM = True
                 fetch_supported = True
                 
            else:
                # Standard API Key Providers
                env_key = f"{selected_key.upper()}_API_KEY"
                current_val = os.getenv(env_key, "")
                
                # Help links
                help_links = {
                    "openai": "[Get Key](https://platform.openai.com/api-keys)",
                    "anthropic": "[Get Key](https://console.anthropic.com/)",
                    "google": "[Get Key](https://aistudio.google.com/app/apikey)",
                    "groq": "[Get Key](https://console.groq.com/keys)",
                    "openrouter": "[Get Key](https://openrouter.ai/keys)"
                }
                
                c_input, c_btn = st.columns([3, 1], vertical_alignment="bottom")
                with c_input:
                    api_key = st.text_input(
                        "API Key", 
                        value=current_val, 
                        type="password", 
                        placeholder=f"sk-...",
                        help=f"Your key is stored locally in .env. {help_links.get(selected_key, '')}"
                    )
                with c_btn:
                    if st.button("💾 Save", key=f"save_{selected_key}", use_container_width=True):
                        save_env_var(env_key, api_key)
                        # Reflection hack for pydantic settings update
                        try:
                            # Try setting on config object if attribute exists
                             setattr(config, env_key, api_key)
                        except:
                            pass
                        st.toast("Key saved!", icon="🔒")
                
                if current_val:
                    fetch_supported = True

            # --- MODEL SELECTION ---
            if fetch_supported:
                st.markdown("### Model Selection")
                
                default_models = {
                    "openai": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "o1-preview", "o1-mini"],
                    "anthropic": ["claude-3-5-sonnet-20240620", "claude-3-opus-20240229", "claude-3-haiku-20240307"],
                    "google": ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-pro"],
                    "groq": ["llama-3.1-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768", "llama3-70b-8192"],
                    "openrouter": ["openai/gpt-4o", "anthropic/claude-3.5-sonnet", "meta-llama/llama-3.1-405b-instruct"],
                    "local": ["local-model"]
                }

                # Fetch available models
                available_models = default_models.get(selected_key, [])
                if f'{selected_key}_models' in st.session_state:
                    available_models = st.session_state[f'{selected_key}_models']

                # "Refresh" as a small icon button or link
                col_sel, col_refresh = st.columns([3, 1], vertical_alignment="bottom")
                with col_sel:
                    # Current model from config
                    current_model = os.getenv("MODEL_PLANNER", "gpt-4o")
                    
                    # Ensure current is in list
                    if current_model not in available_models:
                        available_models.insert(0, current_model)
                    
                    # Index
                    try: idx = available_models.index(current_model)
                    except: idx = 0
                    
                    new_model = st.selectbox("Active Model", available_models, index=idx)
                    
                with col_refresh:
                    fetch_key = api_key if api_key else os.getenv(f"{selected_key.upper()}_API_KEY")
                    fetch_url = base_url if selected_key == "local" else None
                    
                    if st.button("🔄 Refresh", help="Fetch latest models from API"):
                         if not fetch_key and selected_key != "local":
                             st.error("Save key first.")
                         else:
                             with st.spinner("Fetching..."):
                                 fetched = fetch_models_for_provider(selected_key, fetch_key, fetch_url)
                                 if fetched:
                                     st.session_state[f'{selected_key}_models'] = fetched
                                     st.success(f"Found {len(fetched)} models")
                                     st.rerun()

                if new_model != current_model:
                     # Save logic
                     save_env_var("MODEL_PLANNER", new_model)
                     save_env_var("MODEL_WRITER", new_model)
                     if selected_key == "local": save_env_var("LOCAL_LLM_MODEL", new_model)
                     config.MODEL_PLANNER = new_model
                     config.MODEL_WRITER = new_model
                     if selected_key == "local": config.LOCAL_LLM_MODEL = new_model
                     st.rerun()

            # --- TEST CONNECTION ---
            st.divider()
            if st.button(f"📡 Test Connection to {provider_data['name']}", use_container_width=True):
                test_connection(selected_key)