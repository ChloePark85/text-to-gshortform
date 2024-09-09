from crewai import Task
from agents import scriptwriter

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
        expected_output="약 300글자 분량의 과장되고 말도 안 되는 짧은 단편 소설 형식의 막장 스크립트",
        agent=scriptwriter
    )