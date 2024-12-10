import gradio as gr
from yolo_model import detect_object
from openai_service import request_gpt
from speech_service import request_tts
import re

def stream_webcam(image):
    return detect_object(image)

def click_capture(image):
    return image

def click_send_gpt(image_array, histories):
    content = request_gpt(image_array)
    histories.append(gr.ChatMessage(role="assistant", content=gr.Image(value=image_array)))
    histories.append(gr.ChatMessage(role="assistant", content=content))
    return histories

def change_chatbot(histories):
    content = histories[-1]['content']
    cleaned_content = re.sub(r"[^가-힣a-zA-Z0-9\s%,\.]", "", content)
    return request_tts(cleaned_content)

def create_ui():
    with gr.Blocks() as demo:
        with gr.Row():        
            webcam_input = gr.Image(label="Real-time screen", sources="webcam", width=480, height=270, mirror_webcam=False)
            output_image = gr.Image(label="Detection Screen", type="pil", interactive=False)
            output_capture_image = gr.Image(label="Screen capture", interactive=False)
        
        with gr.Row():
            capture_button = gr.Button("Capture")
            send_gpt_button = gr.Button("Send to GPT")
        
        chatbot = gr.Chatbot(label="Analysis results", type="messages")
        chatbot_audio = gr.Audio(label="GPT", interactive=False, autoplay=True)
        
        webcam_input.stream(fn=stream_webcam, inputs=[webcam_input], outputs=[output_image])
        capture_button.click(fn=click_capture, inputs=[output_image], outputs=[output_capture_image])
        send_gpt_button.click(fn=click_send_gpt, inputs=[output_capture_image, chatbot], outputs=[chatbot])
        chatbot.change(fn=change_chatbot, inputs=[chatbot], outputs=[chatbot_audio])
    
    return demo
