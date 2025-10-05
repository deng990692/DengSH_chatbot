# auth_utils.py
import streamlit as st
from supabase import create_client, Client
import extra_streamlit_components as stx
import time

# 从环境变量获取Supabase配置
from config import get_supabase_config

SUPABASE_URL, SUPABASE_KEY = get_supabase_config()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Cookie管理器
def get_cookie_manager():
    """获取或创建Cookie管理器"""
    if "cookie_manager" not in st.session_state:
        st.session_state.cookie_manager = stx.CookieManager()
    return st.session_state.cookie_manager

def save_token(token):
    """保存token到cookie，有效期30天"""
    cookie_manager = get_cookie_manager()
    expires_at = int(time.time()) + 30 * 24 * 60 * 60  # 30天后过期
    cookie_manager.set("auth_token", token, expires_at=expires_at)

def clear_token():
    """清除cookie中的token"""
    cookie_manager = get_cookie_manager()
    cookie_manager.delete("auth_token")

def restore_login():
    """
    每个页面顶部调用，自动用token校验并恢复登录状态。
    优先从session_state获取登录状态，其次从URL参数获取token。
    """
    try:
        # 如果已经登录且token有效，直接返回True
        if st.session_state.get("logged_in") and st.session_state.get("access_token"):
            try:
                supabase.auth.get_user(st.session_state["access_token"])
                return True
            except:
                pass
        
        # 尝试从URL参数获取token
        token = st.query_params.get("token")
        if token:
            try:
                # 验证token
                user_response = supabase.auth.get_user(token)
                if user_response and user_response.user:
                    # 保存登录状态
                    st.session_state["access_token"] = token
                    st.session_state["user"] = user_response.user
                    st.session_state["logged_in"] = True
                    return True
            except:
                # token无效，清除URL参数
                del st.query_params["token"]
        
        # 登录失效，清除所有状态
        st.session_state.pop("access_token", None)
        st.session_state.pop("user", None)
        st.session_state.pop("logged_in", None)
        return False
            
    except Exception as e:
        # 发生错误，清除所有状态
        if "token" in st.query_params:
            del st.query_params["token"]
        st.session_state.clear()
        return False

def require_login():
    """
    页面顶部调用，检查登录状态和token有效性。
    未登录则提示并停止页面。
    """
    # 先检查session_state中的登录状态
    if st.session_state.get("logged_in") and st.session_state.get("access_token"):
        try:
            # 验证token是否有效
            supabase.auth.get_user(st.session_state["access_token"])
            return True
        except:
            # token无效，清除状态
            st.session_state.clear()
    
    # 尝试恢复登录
    if not restore_login():
        st.warning("⚠️ Please login to continue")
        st.info("💡 Click the 'Login/Register' page in the sidebar to get started")
        st.stop()
    
    return True

def get_current_user():
    """获取当前登录用户"""
    if "user" in st.session_state:
        return st.session_state["user"]
    return None
