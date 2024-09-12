from crewai import Task
from agents import scriptwriter, soundengineer, image_generation_agent

def create_script_task(keywords):
    return Task(
        description=f"""
        키워드: {keywords}
        
        위의 키워드를 사용하여 약 300글자 분량의 짧은 단편 소설 형식의 막장 스크립트를 작성하세요.
        다음 지침을 따라주세요:
        1. 극도로 과장되고 말도 안 되는 상황을 설정하세요.
        2. 예상치 못한 반전과 충격적인 요소를 포함하세요.
        3. 등장인물의 극단적인 반응이나 행동을 묘사하세요.
        4. 현실성은 전혀 고려하지 말고, 최대한 드라마틱하고 과장된 내용으로 만드세요.
        5. 명확한 시작, 중간, 끝 구조를 가진 이야기로 구성하세요.
        6. 대사와 묘사를 적절히 섞어 생동감 있게 표현하세요.
        
        결과는 반드시 300글자(공백 포함) 내외여야 합니다.
        """,
        agent=scriptwriter,
        expected_output="약 300글자 분량의 과장되고 말도 안 되는 짧은 단편 소설 형식의 막장 스크립트",
    )

def create_tts_task(script, voice_id):
    return Task(
        description=f"""
        주어진 스크립트를 음성으로 변환하세요.
        
        스크립트: {script}
        선택된 음성 ID: {voice_id}
        
        text_to_speech 함수를 사용하여 스크립트를 음성으로 변환하고, 생성된 오디오 파일의 경로를 반환하세요.
        """,
        agent=soundengineer,
        expected_output="생성된 오디오 파일 mp3",
    )

def generate_image_task(script):
    return Task(
        description=f"""
        주어진 스크립트를 바탕으로 이미지를 생성합니다.
        
        스크립트: {script}
        
        다음 지침을 따라주세요:
        1. 눈에 띄는 캐릭터를 표현하세요.
        2. 디자인이 멋지고 잘 설계되어야 합니다.
        3. 이미지에 대화 버블이나 텍스트를 포함하지 마세요.
        4. 이미지는 짧은 형식 비디오 썸네일에 적합해야 합니다.
        5. 시각적으로 매력적이고 매력적인 장면을 만드세요.
        
        결과로 생성된 이미지의 파일 경로를 문자열로 반환하세요.
        """,
        agent=image_generation_agent,
        expected_output="생성된 이미지 파일의 경로 (문자열)",
    )