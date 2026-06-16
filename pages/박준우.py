import streamlit as st

st.set_page_config(
    page_title="소음 경고 도우미",
    page_icon="🔇",
    layout="centered"
)

st.title("🔇 소음 경고 도우미")
st.write("데시벨(dB)을 입력하면 소음 수준을 분석하고 조용히 해달라는 안내 문구를 제공합니다.")

# 장소별 기준
noise_limits = {
    "도서관": 40,
    "병원": 45,
    "학교": 50,
    "사무실": 55,
    "아파트": 60,
    "카페": 65
}

place = st.selectbox(
    "장소를 선택하세요",
    list(noise_limits.keys())
)

limit_db = noise_limits[place]

st.info(f"📍 {place} 권장 기준: {limit_db} dB")

db = st.number_input(
    "현재 측정된 데시벨(dB)",
    min_value=0.0,
    max_value=150.0,
    value=50.0,
    step=1.0
)


def get_warning_message(place_name, current_db, limit):
    diff = current_db - limit

    if diff <= 0:
        level = "정상"
        color = "success"
        message = (
            f"{place_name}의 권장 소음 기준을 지키고 있습니다. "
            "현재 환경은 비교적 조용한 상태입니다."
        )

    elif diff <= 10:
        level = "주의"
        color = "warning"
        message = (
            f"현재 소음이 권장 기준보다 {diff:.0f}dB 높습니다.\n\n"
            "주변 이용자를 위해 목소리를 조금 낮춰 주세요."
        )

    elif diff <= 20:
        level = "경고"
        color = "warning"
        message = (
            f"현재 소음이 권장 기준보다 {diff:.0f}dB 높습니다.\n\n"
            "대화 소리를 줄이고 조용한 환경 유지에 협조해 주세요."
        )

    else:
        level = "매우 위험"
        color = "error"
        message = (
            f"현재 소음이 권장 기준보다 {diff:.0f}dB 높습니다.\n\n"
            "소음 수준이 매우 높습니다. 즉시 소음을 줄여 주시기 바랍니다."
        )

    return level, color, message


try:
    level, color, warning_text = get_warning_message(
        place,
        db,
        limit_db
    )

    st.subheader("분석 결과")
    st.metric(
        label="소음 수준",
        value=level,
        delta=f"{db - limit_db:.0f} dB"
    )

    if color == "success":
        st.success(warning_text)
    elif color == "warning":
        st.warning(warning_text)
    else:
        st.error(warning_text)

    st.divider()

    st.subheader("📢 안내 문구")

    if db <= limit_db:
        notice = (
            f"[{place}] 현재 소음은 권장 기준 이내입니다. "
            "쾌적한 환경 유지에 감사드립니다."
        )
    else:
        notice = (
            f"[{place}] 현재 소음이 권장 기준({limit_db}dB)을 초과했습니다. "
            "주변 이용자를 위해 목소리를 낮추고 조용한 환경 유지에 협조해 주세요."
        )

    st.text_area(
        "복사하여 사용할 수 있는 안내 문구",
        value=notice,
        height=120
    )

except Exception as e:
    st.error("분석 중 오류가 발생했습니다.")
    st.exception(e)

st.divider()

st.caption(
    "※ 본 앱은 일반적인 환경 소음 기준을 참고하여 작성된 예시 도구입니다."
)
