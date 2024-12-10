import requests
import io
import base64
from PIL import Image
from config import OPENAI_ENDPOINT, OPENAI_API_KEY, DEPLOYMENT_NAME

def request_gpt(image_array):
    endpoint = f"{OPENAI_ENDPOINT}/openai/deployments/{DEPLOYMENT_NAME}/chat/completions?api-version=2024-08-01-preview"
    headers = {
        "Content-Type": "application/json",
        "api-key": OPENAI_API_KEY
    }
    
    # 이미지를 Base64로 인코딩
    image = Image.fromarray(image_array)
    buffered_io = io.BytesIO()
    image.save(buffered_io, format="png")
    base64_image = base64.b64encode(buffered_io.getvalue()).decode("utf-8")
    
    # 메세지 설정
    message_list = list()
    
    # 시스템 메세지
    message_list.append({
        "role": "system",
        "content": [{
            'type': 'text',
            'text': 'You are a bot that analyzes detected objects in photos.'
        }]
    })
    
    user_message = """
    You are a YOLO model that detects objects.
    For each object detected in this photo, give a detailed description with a probability of detection.
    Only describe the detected objects.
    """
    # 유저 메세지
    message_list.append({
        "role": "user",
        "content": [{
            'type': 'text',
            'text': user_message
        },{
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
        }]
    })

    payload = {
        "messages": message_list,
        "temperature" : 0.7,
        "top_p" : 0.95, 
        "max_tokens" : 3000
    }
    
    response = requests.post(endpoint, headers=headers, json=payload)
    if response.status_code == 200:
        response_json = response.json()
        content = response_json['choices'][0]['message']['content']
        return content
    else:
        return response.text
