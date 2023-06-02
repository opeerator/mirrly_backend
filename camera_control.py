from flask import Flask, render_template, Response
import cv2


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('video.html')

def generate_frames():
    camera1 = cv2.VideoCapture(0)  # Change the index to match the webcam's ID
    camera2 = cv2.VideoCapture(1)  # Change the index to match the webcam's ID

    while True:
        success1, frame1 = camera1.read()
        success2, frame2 = camera2.read()

        if not success1 or not success2:
            break

        # Process the frames if needed

        # Encode the frames to JPEG format
        ret1, buffer1 = cv2.imencode('.jpg', frame1)
        ret2, buffer2 = cv2.imencode('.jpg', frame2)

        if not ret1 or not ret2:
            break

        # Yield the frames as bytes
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer1.tobytes() + b'\r\n\r\n'
               b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer2.tobytes() + b'\r\n\r\n')

    # Release the camera resources
    camera1.release()
    camera2.release()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5001')
