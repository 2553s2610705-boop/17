import streamlit as st
import math
import struct
import io
import wave

# 1. 페이지 기본 설정 및 다크 테마 레이아웃
st.set_page_config(page_title="🚨 EMERGENCY SYSTEM", layout="centered")

# 2. 커스텀 CSS injection (메인 버튼을 거대한 3D 빨간색 버튼으로 변경)
st.markdown("""
    <style>
    /* 전체 배경을 어두운 통제실 느낌으로 전환 */
    .stApp {
        background-color: #0f0f11;
    }
    /* 메인 타이틀 스타일링 */
    .main-title {
        color: #ff3333;
        text-align: center;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        letter-spacing: 3px;
        margin-top: 80px;
        margin-bottom: 60px;
        text-shadow: 0 0 10px rgba(255, 51, 51, 0.5);
    }
    /* 오직 메인 화면의 버튼만 타겟팅하여 거대한 비상 버튼으로 커스텀 */
    div.stButton > button {
        background: linear-gradient(135deg, #e60000 0%, #990000 100%) !important;
        color: white !important;
        border: 4px solid #ff4b4b !important;
        border-radius: 50% !important;
        width: 220px !important;
        height: 220px !important;
        font-size: 26px !important;
        font-weight: bold !important;
        letter-spacing: 1px;
        box-shadow: 0 0 30px rgba(255, 75, 75, 0.6), inset 0 0 15px rgba(0,0,0,0.6) !important;
        transition: all 0.1s ease-in-out !important;
        display: block;
        margin: 0 auto !important;
        cursor: pointer;
    }
    /* 버튼에 마우스를 올렸을 때 (Hover Effect) */
    div.stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 45px rgba(255, 75, 75, 0.9), inset 0 0 10px rgba(0,0,0,0.4) !important;
        background: linear-gradient(135deg, #ff1a1a 0%, #b30000 100%) !important;
    }
    /* 버튼을 클릭했을 때 (Active Effect) */
    div.stButton > button:active {
        transform: scale(0.95);
        box-shadow: 0 0 15px rgba(255, 75, 75, 0.4) !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🚨 EMERGENCY ALERT</h1>", unsafe_allow_html=True)

# 3. 짧고 강렬한 경고 알람음(Siren) 실시간 생성 함수
def generate_intense_alarm():
    sample_rate = 44100
    duration = 1.5  # 1.5초간 지속되는 짧고 강렬한 사운드
    num_samples = int(sample_rate * duration)
    
    buffer = io.BytesIO()
    with wave.open(buffer, 'wb') as wav:
        wav.setnchannels(1)      # 모노 오디오
        wav.setsampwidth(2)      # 16비트 해상도
        wav.setframerate(sample_rate)
        
        for i in range(num_samples):
            t = float(i) / sample_rate
            
            # 주파수가 850Hz와 1200Hz 사이를 빠르게 요동치는 강렬한 사이렌 효과
            frequency = 1025 + 175 * math.sin(2 * math.pi * 9 * t)
            
            # 기본 사인파(Sine wave) 생성
            sine_value = math.sin(2 * math.pi * frequency * t)
            
            # 소리를 더 날카롭고 강렬하게 만들기 위해 배음(Harmonics) 추가 및 디스토션 효과 부여
            harsh_value = 0.7 * sine_value + 0.3 * (1.0 if sine_value > 0 else -1.0)
            
            # 오디오 클리핑 방지 및 볼륨 조절
            final_value = max(-1.0, min(1.0, harsh_value)) * 0.8
            
            # 바이너리 데이터로 패킹
            packed_sample = struct.pack('<h', int(final_value * 32767))
            wav.writeframes(packed_sample)
            
    buffer.seek(0)
    return buffer.read()

# 4. 레이아웃 제어 및 버튼 구동 매커니즘
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    try:
        # 다른 문구 없이 직관적인 텍스트만 버튼 내부에 배치
        if st.button("PUSH\nTO ALERT"):
            # 버튼 클릭 시 즉시 경고음 생성 및 자동 재생(autoplay)
            alarm_sound = generate_intense_alarm()
            st.audio(alarm_sound, format="audio/wav", autoplay=True)
    except Exception as e:
        # 혹시 모를 오디오 버퍼 예외 처리
        st.sidebar.error(f"Audio System Error: {e}")
