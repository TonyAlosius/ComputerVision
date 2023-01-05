import cv2
# mediapipe developed by google to detect eye movements
import mediapipe as mp
import pyautogui
# VideoCapture(Camera = 0)
cam = cv2.VideoCapture(0)
# Landmarks = 478 landmarks and each identify different parts of the face
# FaceMesh() - Landmarks on Face which looks like a mesh
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
# Scaling the cursor with the screen
screen_w, screen_h = pyautogui.size()
# Infinite Loop inorder to fetch Continues frames of video
while True:
    _, frame = cam.read()
    # Flipping to avoid Mirroring
    frame = cv2.flip(frame, 1)
    # Converting from BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmarks_pts = output.multi_face_landmarks
    # print(landmarks_pts)
    frame_h, frame_w, _ = frame.shape
    if landmarks_pts:
        # Since we need to detect only one face that's the first face
        # landmarks_pts[0].landmark Single face from the multiple faces
        landmarks = landmarks_pts[0].landmark
        # id = index
        for id, landmark in enumerate(landmarks[474:478]):
            # Setting up with our Display resolution
            # landmark.x * frame_w
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            # Detect the Face using circle(where, centre(x,y), radius, color(rgb))
            cv2.circle(frame, (x,y), 3,(0,255,0))
            # print(x,y)
            if id == 1:
                # id may be 0,1,2,3
                # Scaling with the Screen
                screen_x = screen_w / frame_w * x
                screen_y = screen_h / frame_h * y
                pyautogui.moveTo(screen_x, screen_y)
        left = [landmarks[145], landmarks[159]]
        for landmark in left:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255))

        if (left[0].y - left[1].y) < 0.004:
            pyautogui.click()
            pyautogui.sleep(1)
    # Shows the Live Video Tab
    cv2.imshow('Eye C)ontrolled Mouse', frame)
    cv2.waitKey(1)