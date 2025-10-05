import streamlit as st
from supabase import create_client, Client
from auth_utils import restore_login
from config import get_supabase_config
import time

# 从环境变量获取Supabase配置
SUPABASE_URL, SUPABASE_KEY = get_supabase_config()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# 登录状态管理
def is_logged_in():
    """检查是否已登录，同时尝试恢复登录状态"""
    # 已有登录状态，验证token
    if st.session_state.get("logged_in") and st.session_state.get("access_token"):
        try:
            supabase.auth.get_user(st.session_state["access_token"])
            return True
        except:
            pass
            
    # 尝试恢复登录
    return restore_login()

if is_logged_in():
    user = st.session_state["user"]
    email = getattr(user, "email", "")
    
    # 显示欢迎信息
    st.success(f"Welcome back, {email}!")
    
    def handle_logout():
        # 清除URL参数和session state
        if "token" in st.query_params:
            del st.query_params["token"]
        # 清除所有session状态
        st.session_state.clear()
        # 显示退出消息
        st.toast("Successfully logged out!")
        st.rerun()
        
    st.button("Logout", on_click=handle_logout)
else:
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
            try:
                # 登录获取session
                auth_response = supabase.auth.sign_in_with_password({"email": email, "password": password})
                if hasattr(auth_response, "session") and auth_response.session:
                    session = auth_response.session
                    
                    # 存储登录信息到session_state
                    st.session_state["user"] = auth_response.user
                    st.session_state["access_token"] = session.access_token
                    st.session_state["logged_in"] = True  # 添加登录状态标记
                    
                    # 设置URL参数保存token
                    st.query_params["token"] = session.access_token
                    
                    # 显示成功消息
                    st.success(f"Login successful! Welcome {auth_response.user.email}!")
                    time.sleep(1)  # 等待消息显示
                    st.rerun()
                else:
                    st.error("Login failed: Invalid response from server")
            except Exception as e:
                st.error(f"Login error: {str(e)}")

    if register_clicked:
        if not email or not password:
            st.warning("Please enter email and password!")
        else:
            res = supabase.auth.sign_up({"email": email, "password": password})
            if res.user:
                st.success("Registration successful! Please check your email to activate your account.")
            else:
                st.error(f"Registration failed: {res}")
