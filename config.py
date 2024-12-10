import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경 변수 가져오기
OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")

SPEECH_ENDPOINT = os.getenv("SPEECH_ENDPOINT")
SPEECH_API_KEY = os.getenv("SPEECH_API_KEY")
