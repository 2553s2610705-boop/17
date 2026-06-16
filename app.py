import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Gemini 사용
try:
    import google.generativeai as genai
except:
    genai = None


st.set_page_config(
    page_title="주간 소란 지수 분석기",
    page_icon="📊",
    layout="wide"
)

st.title("📊 주간 소란 지수 분석기")
st.caption("일주일 동안의 소란 지수를 분석하고 AI 피드백을 받아보세요.")

days = ["월", "화", "수", "목", "금", "토", "일"]

st.subheader("일주일 소란 지수 입력")

scores = []

cols = st.columns(7)

for i, day in enumerate(days):
    with cols[i]:
        value = st.number_input(
            day,
            min_value=0,
            max_value=100,
            value=50,
            step=1
        )
        scores.append(value)

try:
    df = pd.DataFrame({
        "요일": days,
        "소란지수": scores
    })

    avg_score = round(df["소란지수"].mean(), 1)

    max_day = df.loc[df["소란지수"].idxmax(), "요일"]
    max_value = df["소란지수"].max()

    min_day = df.loc[df["소란지수"].idxmin(), "요일"]
    min_value = df["소란지수"].min()

    st.divider()

    c1, c2, c3 = st.columns(3)

    c1.metric("평균 소란 지수", avg_score)
    c2.metric("최고 소란일", f"{max_day} ({max_value})")
    c3.metric("최저 소란일", f"{min_day} ({min_value})")

    if avg_score <= 30:
        level = "매우 안정 😊"
        color = "success"
    elif avg_score <= 60:
        level = "보통 🙂"
        color = "info"
    elif avg_score <= 80:
        level = "주의 ⚠️"
        color = "warning"
    else:
        level = "위험 🚨"
        color = "error"

    st.subheader("소란 위험도")

    if color == "success":
        st.success(level)
    elif color == "info":
        st.info(level)
    elif color == "warning":
        st.warning(level)
    else:
        st.error(level)

    st.subheader("주간 소란 지수 그래프")

    fig, ax = plt.subplots(figsize=(8, 4))

    ax.plot(
        df["요일"],
        df["소란지수"],
        marker="o"
    )

    ax.axhline(
        avg_score,
        linestyle="--",
        label=f"평균 {avg_score}"
    )

    ax.set_ylim(0, 100)
    ax.set_ylabel("소란 지수")
    ax.legend()

    st.pyplot(fig)

    st.subheader("데이터 표")
    st.dataframe(df, use_container_width=True)

    st.divider()

    st.subheader("🤖 AI 충고 / 칭찬")

    if st.button("AI 분석 실행"):

        if genai is None:
            st.error("google-generativeai 라이브러리를 불러올 수 없습니다.")
        else:

            api_key = st.secrets.get("GEMINI_API_KEY")

            if not api_key:
                st.error(
                    "GEMINI_API_KEY가 설정되지 않았습니다."
                )
            else:
                try:
                    genai.configure(api_key=api_key)

                    model = genai.GenerativeModel(
                        "gemini-2.5-flash-lite"
                    )

                    prompt = f"""
                    당신은 생활환경 분석 전문가입니다.

                    일주일 소란 지수 데이터:

                    {df.to_string(index=False)}

                    평균: {avg_score}

                    아래 형식으로 답변하세요.

                    1. 현재 상태 평가
                    2. 잘한 점 또는 칭찬
                    3. 개선 조언
                    4. 다음 주 목표

                    한국어로 친절하게 작성하세요.
                    """

                    response = model.generate_content(prompt)

                    st.success("분석 완료")

                    st.write(response.text)

                except Exception as e:
                    st.error(f"AI 분석 오류: {e}")

except Exception as e:
    st.error(f"분석 중 오류 발생: {e}")
