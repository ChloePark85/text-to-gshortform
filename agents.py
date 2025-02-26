from crewai import Agent
from langchain.tools import Tool
from tools import generate_script, text_to_speech, generate_image

# Tool 래핑
generate_script_tool = Tool(
    name="GenerateScript",
    func=generate_script,
    description="Generates a script based on given keywords"
)

text_to_speech_tool = Tool(
    name="TextToSpeech",
    func=text_to_speech,
    description="Converts text to speech using various voice options"
)

generate_image_tool = Tool(
    name="GenerateImage",
    func=generate_image,
    description="Generates an image based on a given text description"
)

scriptwriter = Agent(
    role="Short Story Scriptwriter",
    goal="Create engaging and over-the-top short story scripts for short-form videos based on user input",
    backstory="You are a creative and daring writer specializing in creating shocking and dramatic short stories for social media. You love to push boundaries and create narratives that are as outrageous and engaging as possible, all within a concise format.",
    verbose=True,
    tools=[generate_script_tool]
)

soundengineer = Agent(
    role="Sound Engineer",
    goal="Convert text scripts into high-quality audio using text-to-speech technology",
    backstory="You are an experienced sound engineer with a keen ear for voice modulation and audio quality. Your expertise lies in selecting the perfect voice and creating engaging audio content for short-form videos.",
    verbose=True,
    tools=[text_to_speech_tool]
)
image_generation_agent = Agent(
    role='Image Generator',
    goal='Create visually appealing images based on text descriptions',
    backstory='You are a creative AI artist with a talent for translating text into stunning visual representations.',
    verbose=True,
    allow_delegation=False,
    tools=[generate_image_tool],
)