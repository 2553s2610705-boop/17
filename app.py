import streamlit as st
import random

colors = [
    "빨간색 ❤️",
    "파란색 💙",
    "초록색 💚",
    "노란색 💛",
    "보라색 💜",
    "주황색 🧡",
    "핑크색 🩷",
    "하늘색 🩵"
]

st.title("🎨 오늘의 행운 색깔")

if st.button("행운 색깔 확인하기"):
    lucky_color = random.choice(colors)
    st.success(f"오늘의 행운 색깔은 {lucky_color} 입니다!")
