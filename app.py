import streamlit as st
from google import genai

# 페이지 설정
st.set_page_config(
    page_title="오늘의 행운 색깔 챗봇",
    page_icon="🎨",
)

st.title("🎨 오늘의 행운 색깔 챗봇")
st.caption("Gemini 2.5 Flash Lite 기반")

# API 키 확인
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error(
        "GEMINI_API_KEY를 Streamlit Secrets에 설정해주세요."
    )
    st.stop()

# Gemini 클라이언트 생성
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Gemini 클라이언트 생성 실패: {e}")
    st.stop()

# 채팅 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "안녕하세요! 🎨\n\n"
                "생년월일, 별자리, 기분, 또는 오늘의 목표를 알려주시면 "
                "오늘의 행운 색깔을 추천해드릴게요."
            ),
        }
    ]

# 기존 메시지 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
prompt = st.chat_input("오늘의 행운 색깔을 알려줘!")

if prompt:
    # 사용자 메시지 저장
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            system_prompt = """
당신은 '오늘의 행운 색깔' 전문 챗봇입니다.

규칙:
1. 사용자의 입력을 참고하여 오늘의 행운 색깔을 추천한다.
2. 색깔 이름을 명확히 알려준다.
3. 추천 이유를 2~4문장으로 설명한다.
4. 오늘 하면 좋은 행동 1가지를 추가한다.
5. 밝고 긍정적인 톤을 유지한다.
6. 답변은 반드시 한국어로 작성한다.
"""

            conversation = []

            for msg in st.session_state.messages:
                role = "User" if msg["role"] == "user" else "Assistant"
                conversation.append(
                    f"{role}: {msg['content']}"
                )

            full_prompt = (
                system_prompt
                + "\n\n"
                + "\n".join(conversation)
            )

            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=full_prompt,
            )

            answer = response.text

            st.markdown(answer)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                }
            )

        except Exception as e:
            error_message = (
                f"오류가 발생했습니다.\n\n"
                f"에러 내용: {str(e)}"
            )

            st.error(error_message)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error_message,
                }
            )
