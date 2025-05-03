from fastapi import FastAPI, UploadFile, File, Query
import cv2
import numpy as np
from ultralytics import YOLO
from paddleocr import PaddleOCR
from typing import List, Dict, Any


app = FastAPI()

# Load YOLOv8 and PaddleOCR models
object_detection_model = YOLO("yolov8n.pt")
ocr = PaddleOCR(use_angle_cls=True, lang="en")

# COCO Class Names Mapping
COCO_CLASSES = {
    0: "person", 1: "bicycle", 2: "car", 3: "motorcycle", 4: "airplane",
    5: "bus", 6: "train", 7: "truck", 8: "boat", 9: "traffic light",
    10: "fire hydrant", 11: "stop sign", 12: "parking meter", 13: "bench",
    14: "bird", 15: "cat", 16: "dog", 17: "horse", 18: "sheep",
    19: "cow", 20: "elephant", 21: "bear", 22: "zebra", 23: "giraffe",
    24: "backpack", 25: "umbrella", 26: "handbag", 27: "tie", 28: "suitcase",
    29: "frisbee", 30: "skis", 31: "snowboard", 32: "sports ball", 33: "kite",
    34: "baseball bat", 35: "baseball glove", 36: "skateboard", 37: "surfboard", 38: "tennis racket",
    39: "bottle", 40: "wine glass", 41: "cup", 42: "fork", 43: "knife",
    44: "spoon", 45: "bowl", 46: "banana", 47: "apple", 48: "sandwich",
    49: "orange", 50: "broccoli", 51: "carrot", 52: "hot dog", 53: "pizza",
    54: "donut", 55: "cake", 56: "chair", 57: "couch", 58: "potted plant",
    59: "bed", 60: "dining table", 61: "toilet", 62: "TV", 63: "laptop",
    64: "mouse", 65: "remote", 66: "keyboard", 67: "cell phone", 68: "microwave",
    69: "oven", 70: "toaster", 71: "sink", 72: "refrigerator", 73: "book",
    74: "clock", 75: "vase", 76: "scissors", 77: "teddy bear", 78: "hair drier",
    79: "toothbrush"
}

def preprocess_image_for_ocr(image: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def recognize_handwritten_text(image: np.ndarray) -> str:
    image = preprocess_image_for_ocr(image)
    predictions = ocr.ocr(image)

    # Extract detected text
    text_result = []
    for line in predictions:
        for word in line:
            text_result.append(word[1][0])

    return " ".join(text_result)

def detect_objects(image: np.ndarray) -> Dict[str, Any]:
    results = object_detection_model(image) 
    boxes = results[0].boxes.data.cpu().numpy()

    detected_objects = []
    detected_class_names = set()

    for box in boxes:
        x1, y1, x2, y2, confidence, class_id = box
        class_name = COCO_CLASSES.get(int(class_id), "Unknown")
        detected_class_names.add(class_name)

        detected_objects.append({
            "class_name": class_name
        })

    # Summary of detected classes
    detected_classes_string = ", ".join(detected_class_names)

    return {
        "detected_objects": detected_objects,
        "summary": f"Detected objects: {detected_classes_string}"
    }

@app.post("/process/")
async def process_image(
    mode: str = Query(..., enum=["object_detection", "handwriting"]),
    file: UploadFile = File(...)
):
    """Process an image using either object detection or handwriting recognition."""
    contents = await file.read()
    image = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    if mode == "object_detection":
        result = detect_objects(image)
    elif mode == "handwriting":
        result = {"recognized_text": recognize_handwritten_text(image)}
    else:
        return {"error": "Invalid mode. Choose 'object_detection' or 'handwriting'."}

    return {"mode": mode, "result": result}
