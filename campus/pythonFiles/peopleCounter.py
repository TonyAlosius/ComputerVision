import cv2
from ultralytics import YOLO
import numpy as np
import cvzone
import math
from campus.pythonFiles.sort import *


def mainGateFunc():
    cap = cv2.VideoCapture("static/Image/main_gate.mp4")
    model = YOLO("../Yolo_Weights/yolov8l.pt")

    # Finding the Co-Ordinates of the line
    # def mouse_callback(event, x, y):
    #     if event == cv2.EVENT_LBUTTONDOWN:
    #         print(f"Clicked at (x, y): ({x}, {y})")
    # cv2.namedWindow("Image")
    # cv2.setMouseCallback("Image", mouse_callback)

    # w_prop_id = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # h_prop_id = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
    # cv2.resizeWindow("Video", 1280, 720)

    classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
                  "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
                  "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
                  "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
                  "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
                  "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
                  "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
                  "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
                  "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
                  "teddy bear", "hair drier", "toothbrush"
                  ]

    tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)
    mask = cv2.imread('static/Image/mask.png')
    limitsUp = [1060, 240, 1261, 715]
    totalCountUp = []

    while True:
        success, img = cap.read()
        resize = cv2.resize(img, (1280, 720))
        imgRegion = cv2.bitwise_and(resize, mask)
        imgGraphics = cv2.imread("static/Image/graphics.png", cv2.IMREAD_UNCHANGED)
        resize = cvzone.overlayPNG(resize, imgGraphics, (0, 0))
        results = model(imgRegion, stream=True)
        detections = np.empty((0, 5))

        for r in results:
            boxes = r.boxes
            for box in boxes:
                # x1, y1 represent the top-left corner of the bounding box
                # x2, y2 represent the bottom-right corner of the bounding box.
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w, h = x2 - x1, y2 - y1
                conf = math.ceil((box.conf[0] * 100)) / 100
                cls = int(box.cls[0])
                currentClass = classNames[cls]
                if currentClass == "person" and conf > 0.3:
                    currentArray = np.array([x1, y1, x2, y2, conf])
                    detections = np.vstack((detections, currentArray))
                    # cvzone.cornerRect(resize, (x1, y1, w, h))
                    # cvzone.putTextRect(resize, f'{classNames[cls]}{conf}', (max(0, x1), max(0, y1)), scale=1, thickness=1)

        cv2.line(resize, (limitsUp[0], limitsUp[1]), (limitsUp[2], limitsUp[3]), (0, 0, 255), 5)

        resultsTracker = tracker.update(detections)
        for result in resultsTracker:
            x1, y1, x2, y2, id = result
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            # print(result)
            cvzone.cornerRect(resize, (x1, y1, w, h), l=9, rt=2, colorR=(255, 0, 255))
            cvzone.putTextRect(resize, f' {int(id)}', (max(0, x1), max(35, y1)),
                               scale=2, thickness=3, offset=10)
            cx, cy = x1 + w // 2, y1 + h // 2
            # print((cx, cy), id)
            cv2.circle(resize, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

            if limitsUp[0] < cx < limitsUp[2] and 400 < cy < 660:
                print("Entered")
                if totalCountUp.count(id) == 0:
                    totalCountUp.append(id)
                    cv2.line(resize, (limitsUp[0], limitsUp[1]), (limitsUp[2], limitsUp[3]), (0, 255, 0), 5)
            # print(totalCountUp)

        cv2.putText(resize, str(len(totalCountUp)), (200, 90), cv2.FONT_HERSHEY_PLAIN, 5, (139, 195, 75), 7)

        ret, buffer = cv2.imencode('.jpg', resize)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')