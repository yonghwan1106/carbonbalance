import streamlit as st
from supabase import create_client, Client

def get_supabase_client() -> Client:
    url: str = st.secrets["supabase_url"]
    key: str = st.secrets["supabase_key"]
    return create_client(url, key)
