import cv2

# Create a VideoCapture object to capture the video stream.
cap = cv2.VideoCapture('rtsp://admin:royal123@192.168.1.16:554/cam/realmonitor?channel=1&subtype=0')

# Create a while loop to read the frames from the video stream.
while True:
    # Read the next frame from the video stream.
    ret, frame = cap.read()

    # Check if the frame was successfully read.
    if ret:
        # Display the frame on a window.
        cv2.imshow('Video', frame)

        # Wait for 25 milliseconds to display the next frame.
        cv2.waitKey(25)
    else:
        # Break the loop if the frame was not successfully read.
        break

# Release the VideoCapture object when you are done.
cap.release()