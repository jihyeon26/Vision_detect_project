import requests
from config import SPEECH_ENDPOINT, SPEECH_API_KEY

def request_tts(text):
    headers = {
        "Ocp-Apim-Subscription-Key": SPEECH_API_KEY,
        "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "audio-16khz-128kbitrate-mono-mp3"
    }
    payload = f"""
    <speak version='1.0' xml:lang='en-US'>
        <voice xml:lang='en-US' xml:gender='Female' name='en-US-AvaMultilingualNeural'>
            {text}
        </voice>
    </speak>
    """
    response = requests.post(SPEECH_ENDPOINT, headers=headers, data=payload)
    if response.status_code == 200:
        file_name = "response_audio.mp3"
        with open(file_name, "wb") as audio_file:
            audio_file.write(response.content)
        return file_name
    return None
