import cv2
import cvzone
from ultralytics import YOLO
import math
import time
import requests
import numpy as np
import imutils

# Live Stream URL
# WA0004
video = cv2.VideoCapture('../../ComputerVision/tnev/Resources/VID-20231025-WA0004.mp4')
# url = "http://192.168.168.91:8080/shot.jpg"
# video = cv2.VideoCapture('rtsp://admin:royal123@192.168.1.16:554/cam/realmonitor?channel=1&subtype=0')
# video = cv2.VideoCapture(0)
model = YOLO('weights/best.pt')

className = ['ambulance']

while True:
    # img_resp = requests.get(url)
    # img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    # frame = cv2.imdecode(img_arr, -1)
    # frame = imutils.resize(frame, width=1000, height=1800)

    success, frame = video.read()
    results = model.predict(frame)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            conf = math.ceil(box.conf[0] * 100)
            cls = int(box.cls[0])
            if conf > 85:
                seconds = time.time()
                local_time = time.ctime(seconds)
                local_time = local_time.replace(" ", "_")
                local_time = local_time.replace(":", "_")
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 3)
                cvzone.putTextRect(frame, f'{conf, className[cls]}', (max(0, x1), max(0, y1)))
                cv2.imwrite(f"liveCapture/{local_time}.jpg", frame)
    cv2.imshow("Display", frame)
    cv2.waitKey(1)
