import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="Sound Guard",
    page_icon="🔇",
    layout="centered"
)

st.title("🔇 사운드 가드: 소음 통제소")
st.write("현재 데시벨 환경을 체크하고 청각 보호를 위한 조언을 확인하세요.")

st.sidebar.header("설정")
target_limit = st.sidebar.slider("허용할 기준 데시벨 (dB)", min_value=30, max_value=100, value=65, step=5)

api_key = st.secrets.get("GEMINI_API_KEY", None)

if api_key:
    st.sidebar.success("AI 연결 성공")
    genai.configure(api_key=api_key)
else:
    st.sidebar.warning("API 키 미설정 (AI 기능 제한)")

st.subheader("🔊 현재 환경 데시벨 입력")

col1, col2, col3, col4 = st.columns(4)

if "current_db" not in st.session_state:
    st.session_state.current_db = 55

if col1.button("도서관 (40 dB)"): 
    st.session_state.current_db = 40
if col2.button("일반 카페 (65 dB)"): 
    st.session_state.current_db = 65
if col3.button("지하철 (80 dB)"): 
    st.session_state.current_db = 80
if col4.button("콘서트장 (110 dB)"): 
    st.session_state.current_db = 110

current_db = st.slider("데시벨 조절 (dB)", min_value=0, max_value=140, key="current_db")

def analyze_decibel(db):
    if db <= 40:
        return "안전", "쾌적한 수면 및 집중이 가능한 수준", "정상적인 환경이므로 특별한 조치가 필요 없습니다."
    elif db <= 60:
        return "보통", "일반적인 대화나 조용한 사무실 수준", "일상적인 소음 수준입니다. 청각에 무리가 없습니다."
    elif db <= 80:
        return "주의", "전화 벨소리나 번화가 도로 수준", "체내 스트레스가 증가할 수 있으니 주기적으로 휴식을 취하세요."
    elif db <= 100:
        return "위험", "철도변 소음이나 헤어드라이어 수준", "장시간 노출 시 난청을 유발합니다. 귀마개를 착용하세요."
    else:
        return "최고 위험", "전투기 이착륙 및 록밴드 공연 수준", "단시간 노출로도 청각 손상이 오니 즉시 대피하세요."

status_title, status_desc, basic_advice = analyze_decibel(current_db)

st.progress(min(current_db / 140, 1.0))
st.write(f"📊 현재 등급: {status_title} ({current_db} dB)")
st.write(f"💡 상황 예시: {status_desc}")

st.markdown("---")

if current_db > target_limit:
    excess = current_db - target_limit
    st.error(f"🚨 경고: 기준치({target_limit} dB)를 {excess} dB 초과했습니다!")
    st.warning(f"📢 대처 조언: {basic_advice}")
else:
    st.success(f"✅ 안전: 기준치({target_limit} dB) 이내에서 유지되고 있습니다.")
    st.info(f"📢 가이드: {basic_advice}")

st.markdown("---")

st.subheader("🤖 AI 맞춤형 소음 해결 대처 가이드")
user_situation = st.text_input(
    "구체적인 소음 상황을 입력하세요",
    placeholder="예: 아파트 윗집 발망치 소리, 옆자리 직원의 키보드 소리"
)

if st.button("AI 실시간 솔루션 받기"):
    if not api_key:
        st.error("Secrets에 GEMINI_API_KEY를 등록해야 사용 가능합니다.")
    elif not user_situation.strip():
        st.warning("상황을 입력창에 적어주세요.")
    else:
        with st.spinner("AI가 대처법을 계산 중입니다..."):
            try:
                model = genai.GenerativeModel("gemini-2.5-flash-lite")
                prompt = f"소음 상황: {user_situation}, 현재 소음 수치: {current_db} dB. 이 상황을 해결할 수 있는 정중하고 효과적인 대처 멘트와 행동 요령을 3문장 이내로 친절하게 조언해줘."
                response = model.generate_content(prompt)
                st.info("💡 AI의 맞춤형 솔루션")
                st.write(response.text)
            except Exception as e:
                st.error(f"오류가 발생했습니다: {str(e)}")
