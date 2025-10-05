import streamlit as st
import google.generativeai as genai

st.header("LLM Chat")
if "user" not in st.session_state:
    st.warning("Please login first.")
    st.stop()

api_key = st.text_input("Gemini API Key", type="password")
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
