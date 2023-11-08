import face_recognition
import cv2
import numpy as np


def surveillance(camera):
    # Load a sample picture and learn how to recognize it.
    tony_image = face_recognition.load_image_file("static/Image/tony.jpg")
    tony_face_encoding = face_recognition.face_encodings(tony_image)[0]

    # Load a second sample picture and learn how to recognize it.
    sriram_image = face_recognition.load_image_file("static/Image/sriram.jpg")
    sriram_face_encoding = face_recognition.face_encodings(sriram_image)[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = [
        tony_face_encoding,
        sriram_face_encoding
    ]
    known_face_names = [
        "Tony",
        "Sriram"
    ]
    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)


            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
