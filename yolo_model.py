from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFont
import platform

# YOLO 모델 초기화
model = YOLO('yolov8n.pt').to('cpu')

def detect_object(origin_image):
    """
    YOLO 모델을 사용하여 이미지에서 객체를 감지합니다.
    
    Args:
        origin_image (numpy.ndarray): 원본 이미지 배열.

    Returns:
        PIL.Image: 감지된 객체에 박스와 라벨이 추가된 이미지.
    """
    # 이미지 복사 및 PIL 이미지로 변환
    image = origin_image.copy()
    image = Image.fromarray(image)
    draw = ImageDraw.Draw(image)
    
    # YOLO 모델 실행
    response = model(origin_image)
    
    # 폰트 설정
    font_size = 15
    if platform.system() == "Darwin":  # macOS
        font = ImageFont.truetype("AppleGothic.ttf", size=font_size)
    elif platform.system() == "Windows":  # Windows
        font = ImageFont.truetype("malgun.ttf", size=font_size)
    else:  # 기타 (Linux 등)
        font = ImageFont.load_default()
    
    # 감지된 객체 그리기
    for result in response:
        label_list = result.names
        box_list = result.boxes.xyxy.cpu().numpy()
        confidences_list = result.boxes.conf.cpu().numpy()
        class_id_list = result.boxes.cls.cpu().numpy()
        
        for index, box in enumerate(box_list):
            x1, y1, x2, y2 = map(int, box)  # 바운딩 박스 좌표
            confidences = confidences_list[index]  # 신뢰도
            class_id = class_id_list[index]  # 클래스 ID
            label = label_list[class_id]  # 클래스 라벨
            
            # 박스 및 라벨 추가
            draw.rectangle((x1, y1, x2, y2), outline=(255, 217, 8), width=2)
            draw.text((x1 + 5, y1 + 5), text=f"{label} ({confidences*100:.2f}%)", fill=(255, 217, 0), font=font)
    
    return image
