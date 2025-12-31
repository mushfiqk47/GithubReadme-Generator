import streamlit as st
import os
import requests
from src.core.config import config
from src.core.llm_factory import LLMFactory
from langchain_core.messages import HumanMessage
from src.ui.components import render_header, card_container, end_card

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

def render_settings():
    render_header("⚙️ Global Settings", "Configure your AI providers and persistent keys.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div class="ui-card">', unsafe_allow_html=True)
        st.subheader("Active Provider")
        provider_options = ["openai", "anthropic", "google", "groq", "openrouter", "local"]
        current_idx = provider_options.index(config.ACTIVE_PROVIDER) if config.ACTIVE_PROVIDER in provider_options else 0
        new_provider = st.radio("Select Engine", provider_options, index=current_idx)
        
        if new_provider != config.ACTIVE_PROVIDER:
            save_env_var("ACTIVE_PROVIDER", new_provider)
            # Update the in-memory config object so the change is reflected immediately
            config.ACTIVE_PROVIDER = new_provider
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="ui-card">', unsafe_allow_html=True)
        st.subheader(f"{new_provider.title()} Configuration")
        
        api_key = ""
        fetch_supported = False
        
        # 1. Input API Key
        if new_provider == "openai":
            api_key = st.text_input("OpenAI API Key", value=os.getenv("OPENAI_API_KEY", ""), type="password")
            if st.button("Save Key"): 
                save_env_var("OPENAI_API_KEY", api_key)
                from pydantic import SecretStr
                config.OPENAI_API_KEY = SecretStr(api_key)
            fetch_supported = True

        elif new_provider == "anthropic":
            api_key = st.text_input("Anthropic API Key", value=os.getenv("ANTHROPIC_API_KEY", ""), type="password")
            if st.button("Save Key"): 
                save_env_var("ANTHROPIC_API_KEY", api_key)
                from pydantic import SecretStr
                config.ANTHROPIC_API_KEY = SecretStr(api_key)
            st.info("Supported: claude-3-5-sonnet-20240620, claude-3-opus-20240229, claude-3-haiku-20240307")

        elif new_provider == "google":
            api_key = st.text_input("Google API Key", value=os.getenv("GOOGLE_API_KEY", ""), type="password")
            if st.button("Save Key"): 
                save_env_var("GOOGLE_API_KEY", api_key)
                from pydantic import SecretStr
                config.GOOGLE_API_KEY = SecretStr(api_key)
            fetch_supported = True
            
        elif new_provider == "groq":
            api_key = st.text_input("Groq API Key", value=os.getenv("GROQ_API_KEY", ""), type="password")
            if st.button("Save Key"): 
                save_env_var("GROQ_API_KEY", api_key)
                from pydantic import SecretStr
                config.GROQ_API_KEY = SecretStr(api_key)
            fetch_supported = True
            
        elif new_provider == "openrouter":
            api_key = st.text_input("OpenRouter API Key", value=os.getenv("OPENROUTER_API_KEY", ""), type="password")
            if st.button("Save Key"): 
                save_env_var("OPENROUTER_API_KEY", api_key)
                from pydantic import SecretStr
                config.OPENROUTER_API_KEY = SecretStr(api_key)
            fetch_supported = True

        elif new_provider == "local":
            base_url = st.text_input("Base URL", value=os.getenv("LOCAL_LLM_BASE_URL", "http://localhost:1234/v1"))
            if st.button("Save URL"): 
                save_env_var("LOCAL_LLM_BASE_URL", base_url)
                save_env_var("USE_LOCAL_LLM", "true")
                config.LOCAL_LLM_BASE_URL = base_url
                config.USE_LOCAL_LLM = True
            fetch_supported = True

        st.divider()

        # 2. Model Selection
        st.subheader("Select Model")
        current_model = os.getenv("MODEL_PLANNER", "gpt-4o")
        
        default_models = {
            "openai": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "o1-preview", "o1-mini"],
            "anthropic": ["claude-3-5-sonnet-20240620", "claude-3-opus-20240229", "claude-3-haiku-20240307"],
            "google": ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-pro"],
            "groq": ["llama-3.1-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768", "llama3-70b-8192"],
            "openrouter": ["openai/gpt-4o", "anthropic/claude-3.5-sonnet", "meta-llama/llama-3.1-405b-instruct"],
            "local": ["local-model"]
        }
        
        available_models = default_models.get(new_provider, [])
        
        if f'{new_provider}_models' in st.session_state:
            available_models = st.session_state[f'{new_provider}_models']
        
        fetch_key = api_key 
        fetch_url = None
        if not fetch_key and new_provider != "local": 
            fetch_key = os.getenv(f"{new_provider.upper()}_API_KEY")
        if new_provider == "local":
             fetch_url = os.getenv("LOCAL_LLM_BASE_URL", "http://localhost:1234/v1")
        
        if fetch_supported:
            col_a, col_b = st.columns([1, 2])
            with col_a:
                if st.button("🔄 Refresh Model List"):
                    if not fetch_key and new_provider != "local":
                        st.error("Please save API Key first.")
                    else:
                        with st.spinner("Fetching..."):
                            fetched = fetch_models_for_provider(new_provider, fetch_key, fetch_url)
                            if fetched:
                                st.session_state[f'{new_provider}_models'] = fetched
                                st.success(f"Found {len(fetched)} models")
                                st.rerun()
            
        if current_model not in available_models:
            available_models.insert(0, current_model)
            
        idx = 0
        if current_model in available_models:
             idx = available_models.index(current_model)
        
        selected_model = st.selectbox("Select Model", available_models, index=idx)
        
        if selected_model != current_model:
            save_env_var("MODEL_PLANNER", selected_model)
            save_env_var("MODEL_WRITER", selected_model)
            if new_provider == "local": save_env_var("LOCAL_LLM_MODEL", selected_model)
            
            # Update in-memory config for immediate reflection
            config.MODEL_PLANNER = selected_model
            config.MODEL_WRITER = selected_model
            if new_provider == "local": config.LOCAL_LLM_MODEL = selected_model
            
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)
        
        with st.expander("🔌 Connection Test"):
            if st.button("Run Test Request"):
                with st.spinner("Pinging AI..."):
                    try:
                        llm = LLMFactory.get_model(os.getenv("MODEL_PLANNER", "gpt-4o"))
                        resp = llm.invoke([HumanMessage(content="Reply with 'OK'.")])
                        st.success(f"Connected! Reply: {resp.content}")
                    except Exception as e:
                        st.error(f"Connection Failed: {e}")
