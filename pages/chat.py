import streamlit as st
import google.generativeai as genai
from auth_utils import require_login
from config import get_llm_api_key


require_login()
st.header("LLM Chat")

# 尝试从环境变量或session_state获取API Key
api_key = get_llm_api_key("gemini")
saved_key = api_key or st.session_state.get("gemini_api_key", "")

# 允许用户在页面中输入或更新API Key
input_key = st.text_input("Gemini API Key", value=saved_key, type="password")
if input_key != saved_key:
    st.session_state["gemini_api_key"] = input_key
    api_key = input_key

if not api_key:
    st.info("Please enter Gemini API Key.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Say something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    history = "\n".join([
        f"{m['role']}: {m['content']}" for m in st.session_state.messages
    ])
    try:
        response_obj = model.generate_content([history])
        response = response_obj.text
    except Exception as e:
        response = f"❌ Error: {e}\nCheck your API Key or network."
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
