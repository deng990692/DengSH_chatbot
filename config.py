# config.py
"""
配置管理模块，负责加载和管理环境变量
"""
import os
from dotenv import load_dotenv
import streamlit as st

# 加载.env文件
load_dotenv()

def get_supabase_config():
    """获取Supabase配置"""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        st.error("⚠️ Supabase配置未找到。请确保.env文件中包含SUPABASE_URL和SUPABASE_KEY。")
        st.stop()
    
    return url, key

def get_llm_api_key(provider="gemini"):
    """
    获取LLM API Key
    :param provider: API提供商名称(gemini/openai等)
    :return: API Key
    """
    key = os.getenv(f"{provider.upper()}_API_KEY")
    if not key:
        # 尝试从session_state获取（用户在页面中输入的key）
        key = st.session_state.get(f"{provider}_api_key")
    return key