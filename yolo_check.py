import cv2
import numpy as np
from ultralytics import YOLO
from paddleocr import PaddleOCR

image_path = "OIP.jpeg"  # Replace with a real image

# ✅ Test YOLO
try:
    model = YOLO("yolov8n.pt")
    image = cv2.imread(image_path)
    results = model(image)
    print("✅ YOLO works!")
except Exception as e:
    print(f"❌ YOLO Error: {e}")

# ✅ Test PaddleOCR
try:
    ocr = PaddleOCR(use_angle_cls=True, lang="en")
    results = ocr.ocr(image)
    print("✅ PaddleOCR works!")
except Exception as e:
    print(f"❌ PaddleOCR Error: {e}")
