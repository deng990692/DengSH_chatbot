import streamlit as st

st.set_page_config(page_title="DengSH Chatbot", layout="wide")

st.markdown("""
 # DengSH Chatbot
 
 欢迎使用多页面智能聊天应用！
 
 请通过页面顶部的“Select a page”或左侧菜单进入各功能页面：
 - Login/Register
 - LLM Chat
 - LLM Key Management
 
 如需扩展功能，只需在 pages/ 目录下添加新页面。
 
 > 菜单由 Streamlit 自动根据 pages/ 目录生成，无需在入口文件手动添加。
 """)
import streamlit as st

st.set_page_config(page_title="DengSH Chatbot", layout="wide")
import streamlit as st
import google.generativeai as genai
from supabase import create_client, Client


# Supabase 配置
SUPABASE_URL = "https://qxovsldqljuopljnhkbs.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF4b3ZzbGRxbGp1b3Bsam5oa2JzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk2NjQwNDgsImV4cCI6MjA3NTI0MDA0OH0.MuzXwZuf9aiX5qlXgea-DXr3K8Urnu0i7WCAD8A4jNA"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
# AIzaSyCc2c_rsd1asZq05tU4gC1C2uAm_u824k4






# 登录后才显示聊天界面，否则显示登录/注册组件



