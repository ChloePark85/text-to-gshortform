import json
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from config import ELEVENLABS_API_KEY, OPENAI_API_KEY
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import uuid

client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.9)

prompt_template = PromptTemplate(
    input_variables=["keywords"],
    template="""
    키워드: {keywords}
    
    위의 키워드를 사용하여 약 300글자 분량의 짧은 단편 소설 형식의 막장 스크립트를 작성하세요.
    극도로 과장되고 말도 안 되는 상황, 예상치 못한 반전, 충격적인 요소를 포함하세요.
    등장인물의 극단적인 반응이나 행동을 묘사하고, 현실성은 전혀 고려하지 말고 최대한 드라마틱하게 만드세요.
    명확한 시작, 중간, 끝 구조를 가진 이야기로 구성하고, 대사와 묘사를 적절히 섞어 생동감 있게 표현하세요.
    
    결과는 반드시 300글자(공백 포함) 내외여야 합니다.
    """
)

script_chain = LLMChain(llm=llm, prompt=prompt_template)

def generate_script(keywords: str) -> str:
    """주어진 키워드를 기반으로 300글자 내외의 막장 단편 소설 스크립트를 생성합니다."""
    try:
        result = script_chain.run(keywords)
        # 결과가 300글자를 초과하면 잘라냅니다.
        if len(result) > 300:
            result = result[:297] + "..."
        return result
    except Exception as e:
        return f"스크립트 생성 중 오류 발생: {str(e)}"

def text_to_speech(input_str: str) -> str:
    """주어진 텍스트와 voice_id를 받아 음성으로 변환하고 파일 경로를 반환합니다."""
    try:
        # input_str은 JSON 형식의 문자열로, text와 voice_id를 포함합니다.
        input_dict = json.loads(input_str)
        text = input_dict['text']
        voice_id = input_dict['voice_id']

        response = client.text_to_speech.convert(
            voice_id=voice_id,
            output_format="mp3_22050_32",
            text=text,
            model_id="eleven_turbo_v2_5",
            voice_settings=VoiceSettings(
                stability=0.0,
                similarity_boost=1.0,
                style=0.0,
                use_speaker_boost=True,
            ),
        )

        save_file_path = f"{uuid.uuid4()}.mp3"

        with open(save_file_path, "wb") as f:
            for chunk in response:
                if chunk:
                    f.write(chunk)

        return save_file_path
    except Exception as e:
        return f"음성 생성 중 오류 발생: {str(e)}"