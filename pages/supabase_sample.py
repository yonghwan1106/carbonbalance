import streamlit as st
from supabase import create_client, Client
import os

# 환경 변수에서 Supabase 설정 가져오기
supabase_url = st.secrets["supabase_url"]
supabase_key = st.secrets["supabase_key"] 

# Supabase 클라이언트 생성
supabase: Client = create_client(supabase_url, supabase_key)

# 스트림릿 앱 UI
st.title("Supabase 연동 예제")

# 데이터 입력 폼
with st.form("data_form"):
    name = st.text_input("이름")
    age = st.number_input("나이", min_value=0, max_value=150)
    submit_button = st.form_submit_button("데이터 저장")

    if submit_button:
        # Supabase에 데이터 삽입
        data, count = supabase.table("users").insert({"name": name, "age": age}).execute()
        st.success(f"데이터가 성공적으로 저장되었습니다!")

# 저장된 데이터 표시
st.subheader("저장된 데이터")
response = supabase.table("users").select("*").execute()
st.table(response.data)
