import streamlit as st
from crewai import Crew
from tasks import create_script_task
from elevenlabs import generate, set_api_key
from config import ELEVENLABS_API_KEY

set_api_key(ELEVENLABS_API_KEY)

st.set_page_config(layout="wide")

st.title("막장 숏폼 비디오 스크립트 생성기")

# 두 개의 컬럼 생성
left_column, right_column = st.columns(2)

# 왼쪽 컬럼: 생성 관련 옵션
with left_column:
    st.header("스크립트 생성 옵션")
    
    script_option = st.radio("스크립트 옵션", ("키워드로 생성", "직접 입력"))
    
    if script_option == "키워드로 생성":
        keywords = st.text_input("키워드를 입력하세요 (쉼표로 구분)")
        if st.button("스크립트 생성"):
            if keywords:
                task = create_script_task(keywords)
                crew = Crew(tasks=[task])
                result = crew.kickoff()
                st.session_state.generated_script = result
            else:
                st.warning("키워드를 입력해주세요.")
    else:
        user_script = st.text_area("스크립트를 직접 입력하세요", height=200)
        if st.button("스크립트 저장"):
            st.session_state.generated_script = user_script
    
    st.header("보이스 생성 옵션")
    voice_option = st.selectbox(
        "보이스를 선택하세요",
        ("Adam", "Bella", "Charlie")
    )
    
    if st.button("보이스 생성"):
        if 'generated_script' in st.session_state:
            # 여기에 Elevenlabs API를 사용하여 음성을 생성하는 코드를 추가합니다.
            # 예시 코드:
            audio = generate(
                text=st.session_state.generated_script,
                voice=voice_option,
                model="eleven_monolingual_v1"
            )
            st.session_state.generated_audio = audio
        else:
            st.warning("먼저 스크립트를 생성하거나 입력해주세요.")

# 오른쪽 컬럼: 결과 표시
with right_column:
    st.header("생성된 스크립트")
    if 'generated_script' in st.session_state:
        st.write(st.session_state.generated_script)
    else:
        st.write("아직 생성된 스크립트가 없습니다.")
    
    st.header("생성된 오디오")
    if 'generated_audio' in st.session_state:
        st.audio(st.session_state.generated_audio, format='audio/mp3')
    else:
        st.write("아직 생성된 오디오가 없습니다.")