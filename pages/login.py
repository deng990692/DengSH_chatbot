import streamlit as st
from supabase import create_client, Client

# Supabase config (可根据实际情况调整)
SUPABASE_URL = "https://qxovsldqljuopljnhkbs.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF4b3ZzbGRxbGp1b3Bsam5oa2JzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk2NjQwNDgsImV4cCI6MjA3NTI0MDA0OH0.MuzXwZuf9aiX5qlXgea-DXr3K8Urnu0i7WCAD8A4jNA"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.header("Login / Register")
email = st.text_input("Email")
password = st.text_input("Password", type="password")
col1, col2 = st.columns(2)
with col1:
    login_clicked = st.button("Login")
with col2:
    register_clicked = st.button("Register")

if login_clicked:
    if not email or not password:
        st.warning("Please enter email and password!")
    else:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        token = getattr(res.session, "access_token", None) if hasattr(res, "session") else None
        if res.user and token:
            st.success("Login successful!")
            st.session_state["user"] = res.user
            st.session_state["access_token"] = token
            st.rerun()
        else:
            st.error(f"Login failed: {res}")

if register_clicked:
    if not email or not password:
        st.warning("Please enter email and password!")
    else:
        res = supabase.auth.sign_up({"email": email, "password": password})
        if res.user:
            st.success("Registration successful! Please check your email to activate your account.")
        else:
            st.error(f"Registration failed: {res}")
