import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="주간 소음 지수 리포트",
    page_icon="🔊",
    layout="wide"
)

st.title("🔊 주간 소음 지수 리포트")
st.write("일주일 동안의 소음 수준을 분석해보세요.")

days = ["월", "화", "수", "목", "금", "토", "일"]

st.subheader("📋 일일 소음 지수 입력 (데시벨)")

scores = []

cols = st.columns(7)

for i, day in enumerate(days):
    with cols[i]:
        value = st.number_input(
            day,
            min_value=0,
            max_value=120,
            value=50,
            step=1
        )
        scores.append(value)

try:
    df = pd.DataFrame({
        "요일": days,
        "소음지수(dB)": scores
    })

    avg_noise = round(df["소음지수(dB)"].mean(), 1)

    max_idx = df["소음지수(dB)"].idxmax()
    min_idx = df["소음지수(dB)"].idxmin()

    max_day = df.loc[max_idx, "요일"]
    max_value = df.loc[max_idx, "소음지수(dB)"]

    min_day = df.loc[min_idx, "요일"]
    min_value = df.loc[min_idx, "소음지수(dB)"]

    st.divider()

    c1, c2, c3 = st.columns(3)

    c1.metric("평균 소음", f"{avg_noise} dB")
    c2.metric("최고 소음", f"{max_day} ({max_value} dB)")
    c3.metric("최저 소음", f"{min_day} ({min_value} dB)")

    st.subheader("📈 일주일 소음 추이")

    chart_df = df.set_index("요일")
    st.line_chart(chart_df)

    st.subheader("📊 데이터")

    st.dataframe(
        df,
        use_container_width=True
    )

    st.divider()

    st.subheader("📝 자동 분석 결과")

    high_noise_days = df[df["소음지수(dB)"] >= 70]

    if avg_noise >= 70:
        st.error("⚠️ 평균 소음이 70dB 이상입니다.")

        st.write("### 충고")

        st.warning(
            """
            주변 환경이 다소 시끄러운 상태입니다.

            • 창문이나 문을 닫아 외부 소음을 줄여보세요.
            • 소음이 높은 시간대를 파악해 관리해보세요.
            • 장시간 소음 노출은 집중력 저하를 유발할 수 있습니다.
            • 조용한 휴식 시간을 확보해보세요.
            """
        )

    else:
        st.success("😊 평균 소음이 70dB 미만입니다.")

        st.write("### 칭찬")

        st.balloons()

        st.success(
            """
            훌륭합니다!

            • 전반적으로 조용한 환경을 유지했습니다.
            • 집중과 휴식에 적합한 수준입니다.
            • 현재의 생활 습관을 계속 유지해보세요.
            """
        )

    if len(high_noise_days) > 0:

        st.write("### 🔍 70dB 이상 기록한 요일")

        st.dataframe(
            high_noise_days,
            use_container_width=True
        )

except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
