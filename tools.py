import json
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from config import ELEVENLABS_API_KEY, OPENAI_API_KEY
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import uuid
import requests
from PIL import Image
from io import BytesIO
from openai import OpenAI
import os

elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
openai_client = OpenAI(api_key=OPENAI_API_KEY)

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

        response = elevenlabs_client.text_to_speech.convert(
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

        save_file_path = os.path.join(os.getcwd(), f"{uuid.uuid4()}.mp3")
        with open(save_file_path, "wb") as f:
            for chunk in response:
                if chunk:
                    f.write(chunk)

        if os.path.exists(save_file_path):
            return save_file_path
        else:
            return "오디오 파일 생성 실패"
    except Exception as e:
        return f"음성 생성 중 오류 발생: {str(e)}"
    
def generate_image(prompt: str) -> str:
    """
    DALL-E를 사용하여 주어진 프롬프트에 기반한 이미지를 생성합니다.
    """
    # 프롬프트를 더 일반적이고 중립적으로 수정
    prompt = f"""Create a stylish illustration featuring an attractive character based on the following scene: {prompt}. 
Key points:
- The character should be visually appealing and well-designed
- Use a sophisticated illustration style
- Do not include any speech bubbles or text in the image
- The image should be suitable for a short-form video thumbnail
- Focus on creating a visually striking and engaging scene
"""
    
    response = openai_client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

    image_url = response.data[0].url
    image_response = requests.get(image_url)
    image = Image.open(BytesIO(image_response.content))
        
    # 이미지를 2:3 비율로 조정
    width, height = image.size
    new_height = int(width * 3 / 2)
    
    # 새 이미지 생성 (검은색 배경)
    new_image = Image.new('RGB', (width, new_height), color='black')
    
    # 원본 이미지를 새 이미지의 중앙에 붙여넣기
    paste_y = (new_height - height) // 2
    new_image.paste(image, (0, paste_y))
    
    # 이미지를 파일로 저장
    save_dir = "generated_images"
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, f"generated_image_{uuid.uuid4()}.png")
    new_image.save(save_path)
    
    print(f"Debug - Generated image path: {save_path}")  # 디버그 출력
    return save_path

def add_background(image, target_ratio=2/3):
    """이미지에 검은색 배경을 추가하여 2:3 비율로 만듭니다."""
    width, height = image.size
    new_height = int(width / target_ratio)
    result = Image.new('RGB', (width, new_height), color='black')
    paste_y = (new_height - height) // 2
    result.paste(image, (0, paste_y))
    
    return result