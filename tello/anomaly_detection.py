import cv2
import math
from ultralytics import YOLO
import cvzone

video = cv2.VideoCapture(0)
# frame = cv2.imread('../../ComputerVision/tello/Resources/img1.jpg')
model = YOLO('../../ComputerVision/tello/Resources/best1.pt')
className = ['knife']


while True:
    success, frame = video.read()
    results = model.predict(frame)
    print(results)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            conf = math.ceil(box.conf[0] * 100)
            print(conf)
            cls = int(box.cls[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 3)
            cvzone.putTextRect(frame, f'{conf, className[cls]}', (max(0, x1), max(0, y1)))
    cv2.imshow("Display", frame)
    cv2.waitKey(0)