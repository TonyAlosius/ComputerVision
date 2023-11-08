from flask import Flask, render_template, Response
import cv2
from campus.pythonFiles import peopleCounter, faceTracking


app = Flask(__name__)
camera = cv2.VideoCapture(0)


def surveillance():
    return 0


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(faceTracking.surveillance(camera), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/mainGate')
def mainGate():
    return Response(peopleCounter.mainGateFunc(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__=='__main__':
    app.run(debug=True)