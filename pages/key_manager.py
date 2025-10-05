import streamlit as st
from auth_utils import require_login


require_login()
st.header("LLM Key Management")

api_key = st.text_input("Gemini API Key", type="password", value=st.session_state.get("gemini_api_key", ""))
if st.button("Save Key"):
    st.session_state["gemini_api_key"] = api_key
    st.success("Key saved!")

# 可扩展：根据 API Key 获取可用模型列表
if api_key:
    st.write("Available models:")
    # 这里可调用 Gemini/其他服务商接口获取模型列表
    st.write(["gemini-2.5-flash", "gemini-pro", "gpt-3.5-turbo"])  # 示例
