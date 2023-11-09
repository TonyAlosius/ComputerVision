from ultralytics import YOLO

model = YOLO('yolov8n.pt')
results = model.predict('../../ComputerVision/CV_Tricks/Resources/1.jpg', save = True)
print(results)