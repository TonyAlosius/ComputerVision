import cv2
import os

# Path to the folder where you want to save the images
output_folder = r'C:\Users\tonya\PycharmProjects\ComputerVision\CV_Tricks\Resources\Conv_Image'

# Make sure the folder exists; create it if it doesn't
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Load a video
video_path = r'../../ComputerVision/tnev/Resources/VID-20231025-WA0025.mp4'
cap = cv2.VideoCapture(video_path)

frame_count = 0

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Construct the full file path for each image
    image_name = os.path.join(output_folder, f'frame25_{frame_count:04d}.jpg')

    # Save the frame as an image
    cv2.imwrite(image_name, frame)

    frame_count += 1

cap.release()
cv2.destroyAllWindows()
