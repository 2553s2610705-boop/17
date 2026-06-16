Python
import streamlit as st
import google.generativeai as genai

# 1. 페이지 레이아웃 및 기본 설정
st.set_page_config
    page_title="사운드 가드 (Sound Guard)",
    page_icon="🔇",
    layout="centered"

# UI 가독성을 위한 커스텀 스타일 정의
st.markdown("""
    <style>
    .title-text { font-size: 2.3rem; font-weight: bold; text-align: center; color: #1E88E5; }
    .subtitle-text { text-align: center; color: #555; margin-bottom: 2rem; }
    .alert-box { padding: 20px; border-radius: 10px; background-color: #FFF3CD; border-left: 5px solid #FFC107; margin-top: 15px; }
    .danger-box { padding: 20px; border-radius: 10px; background-color: #F8D7DA; border-left: 5px solid #DC3545; margin-top: 15px; }
    </style>
""", unsafe_index=True)

st.markdown("<div class='title-text'>🔇 사운드 가드: 소음 경고 & 조언 통제소</div>", unsafe_index=True)
st.markdown("<div class='subtitle-text'>현재 데시벨 환경을 체크하고 청각 보호를 위한 올바른 조언을 확인하세요!</div>", unsafe_index=True)

# 2. 사이드바 - 허용 기준치 설정 및 Secrets API 키 검증
st.sidebar.header("⚙️ 소음 기준 제어판")
target_limit = st.sidebar.slider("⚠️ 허용할 기준 데시벨 (dB) 설정", min_value=30, max_value=100, value=65, step=5)

# Streamlit Secrets로부터 API Key 가져오기 예외 처리
api_key = st.secrets.get("GEMINI_API_KEY", None)

if api_key:
    st.sidebar.success("✅ Gemini AI 모듈 로드 완료")
    genai.configure(api_key=api_key)
else:
    st.sidebar.warning("🔒 AI 기능을 사용하려면 Secrets 설정을 완료하세요.")

# 3. 소음 입력 섹션 (퀵 프리셋 버튼 기능 제공)
st.subheader("🔊 현재 환경 데시벨 입력")
col1, col2, col3, col4 = st.columns(4)

# 프리셋 기본값 핸들링을 위한 세션 상태 세팅
if "current_db" not in st.session_state:
    st.session_state.current_db = 55

if col1.button("📚 도서관 (40 dB)"): st.session_state.current_db = 40
if col2.button("☕ 일반 카페 (65 dB)"): st.session_state.current_db = 65
if col3.button("🚇 지하철 내부 (80 dB)"): st.session_state.current_db = 80
if col4.button("🎸 콘서트장 (110 dB)"): st.session_state.current_db = 110

# 실시간 데시벨 미세 조절 슬라이더
current_db = st.slider("직접 데시벨을 조절해 보세요 (dB)", min_value=0, max_value=140, key="current_db")

# 4. 데시벨별 기본 정보 및 상태 분류 함수
def analyze_decibel(db):
    if db <= 40:
        return "🟢 안전 (쾌적)", "쾌적한 수면 및 집중이 가능한 수준입니다.", "정상적인 환경이므로 특별한 조치가 필요 없습니다. 유지해 주세요! ✨"
    elif db <= 60:
        return "🔵 보통 (무난)", "일반적인 대화나 조용한 사무실 수준입니다.", "일상적인 소음 수준입니다. 장시간 노출되어도 청각에 무리가 없습니다. ☕"
    elif db <= 80:
        return "🟡 주의 (시끄러움)", "전화 벨소리나 번화가 도로 수준의 소음입니다.", "체내 스트레스 호르몬이 증가할 수 있습니다. 2~3시간마다 조용한 곳에서 휴식을 취하세요. 🎧"
    elif db <= 100:
        return "🟠 위험 (소음 공해)", "철도변 소음이나 헤어드라이어 장시간 사용 수준입니다.", "8시간 이상 노출 시 소음성 난청을 유발합니다. 귀마개를 착용하거나 자리를 피하세요! ❌"
    else:
        return "🔴 폭발적 위험 (청각 손상)", "전투기 이착륙 소리 및 록밴드 공연장 전면 수준입니다.", "단시간 노출로도 청각 세포가 영구 손상될 수 있습니다. 즉시 대피하거나 소음 차단 헤드폰을 쓰세요! 🚨"

status_title, status_desc, basic_advice = analyze_decibel(current_db)

# 위험도 시각화 미터기
st.progress(min(current_db / 140, 1.0))
st.write(f"📊 **현재 소음 등급:** {status_title} ({current_db} dB)")
st.write(f"💡 _상황 예시: {status_desc}_")

st.markdown("---")

# 5. 기준치 초과에 따른 경고글 및 조언 출력
if current_db > target_limit:
    excess = current_db - target_limit
    st.markdown("<div class='danger-box'>", unsafe_index=True)
    st.error(f"🚨 **[초과 고지] 설정하신 기준치({target_limit} dB)를 {excess} dB 초과했습니다!**")
    st.markdown(f"**📢 올바른 가이드 및 조언:**\n\n> {basic_advice}")
    st.markdown("</div>", unsafe_index=True)
else:
    st.markdown("<div class='alert-box'>", unsafe_index=True)
    st.success(f"✅ 환경 안정성 통과! 설정 기준치({target_limit} dB) 이내에서 안전하게 통제되고 있습니다.")
    st.write(f"**안내:** {basic_advice}")
    st.markdown("</div>", unsafe_index=True)

st.markdown("---")

# 6. AI 기능: 상황 최적화 맞춤형 조언 솔루션 (Gemini 2.5 Flash-lite)
st.subheader("🤖 AI 맞춤형 소음 해결 대처 가이드")
st.write("소음이 발생하는 구체적인 상황을 입력하시면, 인공지능이 최적의 대처 멘트와 방안을 처방해 드립니다.")

user_situation = st.text_input(
    "예시: 아파트 윗집의 발망치 소리, 옆자리 직원의 키보드 타건음 등",
    placeholder="현재 스트레스를 유발하는 소음 상황을 적어주세요."
)

if st.button("🔥 AI 실시간 맞춤 솔루션 받기"):
    if not api_key:
        st.error("AI 기능을 활용하시려면 Streamlit 자격 증명(Secrets)에 `GEMINI_API_KEY`를 등록해야 합니다.")
    elif not user_situation.strip():
        st.warning("구체적인 소음 상황을 입력창에 적어주세요!")
    else:
        with st.spinner("Gemini AI가 상황에 맞는 최적의 대처법을 계산 중입니다..."):
            try:
                # 지정된 경량 모델 활용
                model = genai.GenerativeModel("gemini-2.5-flash-lite")
                
                # 명확한 페르소나와 제약을 부여한 프롬프트
                prompt = f"""
                역할: 소음 제어 전문가 및 청각 보호 어드바이저
                현재 주변 소음 수치: {current_db} dB (사용자 설정 기준치: {target_limit} dB)
                사용자 소음 상황: {user_situation}
                
                위 조건들을 고려해서 이 소음 환경을 지혜롭고 단호하게 해결할 수 있는 맞춤형 조언을 제공해줘.
                다음 내용을 포함해야 해:
                1. 현재 데시벨 수준이 해당 장소에서 정당한지 판단
                2. 상대방에게 정중하면서도 똑부러지게 요청할 수 있는 실제 대화 예시문 1개
                3. 사용자의 청각 보호를 위한 행동 요령
                
                말투는 명확하고 친절하면서 위트있게 3문장 내외로 요약해서 가독성 좋게 출력해줘. 이모지도 섞어줘.
                """
                
                response = model.generate_content(prompt)
                
                st.info("💡 사운드 가드 AI의 맞춤형 솔루션 안내")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"API 호출 중 예기치 못한 오류가 발생했습니다: {e}")
