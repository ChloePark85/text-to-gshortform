import streamlit as st
from crewai import Crew
from tasks import create_script_task, generate_image_task
from tools import text_to_speech, generate_image, add_background
from PIL import Image
from io import BytesIO
import os
import json
import re

st.set_page_config(layout="wide")

st.title("Text기반 그래픽 숏폼 생성기")

# Helper function to extract text from TaskOutput
def extract_text_from_task_output(task_output):
    if hasattr(task_output, 'output'):
        return task_output.output
    elif hasattr(task_output, 'result'):
        return task_output.result
    else:
        return str(task_output)

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
                with st.spinner("스크립트 생성 중..."):
                    task = create_script_task(keywords)
                    crew = Crew(
                        agents=[task.agent],
                        tasks=[task],
                        verbose=True
                    )
                    crew_output = crew.kickoff()
                
                # CrewOutput 객체에서 실제 스크립트 텍스트를 추출합니다.
                if crew_output.tasks_output:
                    st.session_state.generated_script = extract_text_from_task_output(crew_output.tasks_output[0])
                    st.success("스크립트가 생성되었습니다. 오른쪽 컬럼에서 확인해주세요.")
                else:
                    st.error("스크립트를 생성할 수 없습니다. 결과가 비어있습니다.")
            else:
                st.warning("키워드를 입력해주세요.")
    else:
        user_script = st.text_area("스크립트를 직접 입력하세요", height=200)
        if st.button("스크립트 저장"):
            st.session_state.generated_script = user_script
            st.success("스크립트가 저장되었습니다. 오른쪽 컬럼에서 확인해주세요.")
    
    st.header("보이스 생성 옵션")
    voice_option = st.selectbox(
        "보이스를 선택하세요",
        [
            ("pNInz6obpgDQGcFmaJgB", "Adam"),
            ("21m00Tcm4TlvDq8ikWAM", "Rachel"),
            ("7EKEe6BYL4GdiYbZHsjJ", "Dorothy")
        ],
        format_func=lambda x: x[1]
    )
    
    if st.button("보이스 생성"):
        if 'generated_script' in st.session_state:
            with st.spinner("보이스 생성 중..."):
                input_data = {
                    "text": st.session_state.generated_script,
                    "voice_id": voice_option[0]
                }
                audio_file_path = text_to_speech(json.dumps(input_data))
                st.session_state.generated_audio = audio_file_path
                st.success("오디오가 생성되었습니다. 오른쪽 컬럼에서 확인해주세요.")
        else:
            st.warning("먼저 스크립트를 생성하거나 입력해주세요.")

    st.header("이미지 생성")
    if st.button("이미지 생성"):
        if 'generated_script' in st.session_state:
            with st.spinner("이미지 생성 중..."):
                image_task = generate_image_task(st.session_state.generated_script)
                image_crew = Crew(
                    agents=[image_task.agent],
                    tasks=[image_task],
                    verbose=True
                )
                image_result = image_crew.kickoff()
                
                if image_result and image_result.tasks_output:
                    # 에이전트의 출력에서 이미지 경로 추출
                    output = str(image_result.tasks_output[0])  # 문자열로 변환
                    image_path_match = re.search(r'(generated_images/generated_image_[a-f0-9-]+\.png)', output)
                    if image_path_match:
                        image_path = image_path_match.group(1)
                        if os.path.exists(image_path):
                            st.session_state.generated_image = image_path
                            st.success("이미지가 생성되었습니다. 오른쪽 컬럼에서 확인해주세요.")
                        else:
                            st.error(f"이미지 파일을 찾을 수 없습니다: {image_path}")
                    else:
                        st.error("이미지 경로를 추출할 수 없습니다.")
                else:
                    st.error("이미지 생성에 실패했습니다.")
        else:
            st.warning("먼저 스크립트를 생성하거나 입력해주세요.")


# 오른쪽 컬럼: 결과 표시
with right_column:
    st.header("생성된 스크립트")
    if 'generated_script' in st.session_state:
        st.text_area("생성된 스크립트:", value=st.session_state.generated_script, height=300, disabled=True)
    else:
        st.write("아직 생성된 스크립트가 없습니다.")
    
    st.header("생성된 오디오")
    if 'generated_audio' in st.session_state and os.path.exists(st.session_state.generated_audio):
        st.audio(st.session_state.generated_audio, format='audio/mp3')
    else:
        st.write("생성된 오디오 파일이 없거나 찾을 수 없습니다.")

    st.header("생성된 이미지")
    if 'generated_image' in st.session_state:
        image_path = st.session_state.generated_image
        if os.path.exists(image_path):
            st.image(image_path, caption='생성된 이미지', use_column_width=True)
        else:
            st.write(f"생성된 이미지 파일을 찾을 수 없습니다: {image_path}")
    else:
        st.write("아직 생성된 이미지가 없습니다.")

# 임시 파일 정리
if st.session_state.get('generated_audio'):
    if os.path.exists(st.session_state.generated_audio):
        os.remove(st.session_state.generated_audio)