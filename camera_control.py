#!/usr/bin/env python3

from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

def get_camera(camera_index):
    camera = cv2.VideoCapture(camera_index)
    while True:
        success, frame = camera.read()
        if success:
            yield frame
        else:
            break
    camera.release()

def generate_frames(camera):
    for frame in camera:
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed_left_eye')
def video_feed_0():
    camera = get_camera(0)
    return Response(generate_frames(camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_feed_right_eye')
def video_feed_1():
    camera2 = get_camera(2)
    return Response(generate_frames(camera2),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
                    
@app.route('/left_eye')
def left_eye_render():
    return render_template('video.html')
    
@app.route('/right_eye')
def right_eye_render():
    return render_template('video2.html')


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5001)
