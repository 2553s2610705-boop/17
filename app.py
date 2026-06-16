import streamlit as st
import pandas as pd

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
st.write("일주일 동안의 소란 지수를 입력하고 분석 결과를 확인해보세요.")

days = ["월", "화", "수", "목", "금", "토", "일"]

scores = []

st.subheader("소란 지수 입력 (0~100)")

cols = st.columns(7)

for i, day in enumerate(days):
    with cols[i]:
        score = st.number_input(
            day,
            min_value=0,
            max_value=100,
            value=50,
            step=1
        )
        scores.append(score)

df = pd.DataFrame({
    "요일": days,
    "소란지수": scores
})

avg_score = round(df["소란지수"].mean(), 1)

max_day = df.loc[df["소란지수"].idxmax(), "요일"]
max_score = df["소란지수"].max()

min_day = df.loc[df["소란지수"].idxmin(), "요일"]
min_score = df["소란지수"].min()

st.divider()

c1, c2, c3 = st.columns(3)

c1.metric("평균", avg_score)
c2.metric("최고", f"{max_day} ({max_score})")
c3.metric("최저", f"{min_day} ({min_score})")

if avg_score <= 30:
    st.success("매우 안정 😊")
elif avg_score <= 60:
    st.info("보통 🙂")
elif avg_score <= 80:
    st.warning("주의 ⚠️")
else:
    st.error("위험 🚨")

st.subheader("📈 주간 소란 지수 그래프")

chart_df = df.set_index("요일")
st.line_chart(chart_df)

st.subheader("📋 데이터")

st.dataframe(
    df,
    use_container_width=True
)

st.divider()

st.subheader("🤖 AI 충고 또는 칭찬")

if st.button("AI 분석 실행"):

    if genai is None:
        st.error("AI 라이브러리를 불러올 수 없습니다.")
    else:

        try:
            api_key = st.secrets["GEMINI_API_KEY"]

            genai.configure(api_key=api_key)

            model = genai.GenerativeModel(
                "gemini-2.5-flash-lite"
            )

            prompt = f"""
            일주일 소란 지수 데이터

            {df.to_string(index=False)}

            평균 소란 지수: {avg_score}

            아래 형식으로 답변하세요.

            1. 현재 상태 평가
            2. 칭찬할 점
            3. 개선할 점
            4. 다음 주 목표

            한국어로 친절하게 작성하세요.
            """

            response = model.generate_content(prompt)

            st.write(response.text)

        except KeyError:
            st.error("Secrets에 GEMINI_API_KEY가 없습니다.")

        except Exception as e:
            st.error(f"AI 분석 오류: {e}")
