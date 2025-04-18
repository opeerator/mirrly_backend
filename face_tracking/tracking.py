import collections
import os
import time
import sys
import cv2
import mediapipe as mp
import numpy as np
import random
from flask import Flask, Response, render_template

app = Flask(__name__)

# === Setup Head Motors ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
sys.path.append(PROJECT_ROOT)
from head_control import HeadMotors
head_motors = HeadMotors()

# === Setup MediaPipe Models ===
MODELS_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODELS_DIR, exist_ok=True)
GESTURE_MODEL = os.path.join(MODELS_DIR, "gesture_recognizer.task")
POSE_MODEL = os.path.join(MODELS_DIR, "pose_landmarker_lite.task")
FACE_MODEL = os.path.join(MODELS_DIR, "blaze_face_short_range.tflite")

# MediaPipe setup
BaseOptions = mp.tasks.BaseOptions
VisionRunningMode = mp.tasks.vision.RunningMode
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
FaceDetector = mp.tasks.vision.FaceDetector
FaceDetectorOptions = mp.tasks.vision.FaceDetectorOptions

# Global state (relative to user)
gesture_results = None
pose_results = None
face_detection_results = None
nose_positions = collections.deque(maxlen=15)
head_cooldown = 0
last_head_gesture = None
EYE_LEFT = 277
EYE_CENTER = 202
EYE_RIGHT = 139
HEAD_LEFT = 360 # 360
HEAD_RIGHT = 0 # 0
HEAD_CENTER = (HEAD_LEFT + HEAD_RIGHT) // 2
HEAD_UP = 275
HEAD_MIDDLE = 150
HEAD_DOWN = 120
EYE_ONLY_ZONE = (0.4, 0.6)
head_move_cooldown = 0
blink_cooldown = 0
HEAD_MOVE_COOLDOWN_FRAMES = 10 # NOTE: this controls how often robot checks for new head position
# 10 frame cooldown / 30 fps = check every 0.33 seconds
TOTAL_YAW_RANGE = abs(HEAD_LEFT - HEAD_RIGHT)


def process_gesture_result(result, output_image, timestamp_ms):
    global gesture_results
    gesture_results = result


def process_pose_result(result, output_image, timestamp_ms):
    global pose_results, nose_positions, head_cooldown, last_head_gesture
    pose_results = result
    if result.pose_landmarks:
        pose = result.pose_landmarks[0]
        nose = pose[0]
        nose_positions.append((nose.x, nose.y))

        if len(nose_positions) == nose_positions.maxlen and head_cooldown <= 0:
            x_vals = [x for x, _ in nose_positions]
            y_vals = [y for _, y in nose_positions]
            x_std, y_std = np.std(x_vals) * 100, np.std(y_vals) * 100
            if y_std > 1.2 and y_std > x_std * 1.5:
                last_head_gesture = "NODDING"
                head_cooldown = 15
            elif x_std > 1.2 and x_std > y_std * 1.5:
                last_head_gesture = "SHAKING"
                head_cooldown = 15
        elif head_cooldown > 0:
            head_cooldown -= 1


def process_face_result(result, output_image, timestamp_ms):
    global face_detection_results
    face_detection_results = result


def should_move_head(current, target, threshold=5):
    return abs(current - target) >= threshold


def track_face_x(face_x, cam_width=640):
    global head_move_cooldown, blink_cooldown

    norm_x = face_x / cam_width
    delta_x = norm_x - 0.5
    yaw_shift = np.interp(delta_x, [-0.5, 0.5], [90, -75])

    try:
        current_yaw = head_motors.current_pos("head_yaw")[0]
    except Exception as e:
        print(f"[WARN] Could not read head position: {e}")
        current_yaw = HEAD_CENTER

    head_target = int(current_yaw + yaw_shift)
    head_target = min(max(head_target, HEAD_RIGHT), HEAD_LEFT)

    if head_move_cooldown % 2 == 0 and EYE_ONLY_ZONE[0] <= norm_x <= EYE_ONLY_ZONE[1]:
        eye_pos = int(np.interp(norm_x, [0, 1], [EYE_LEFT, EYE_RIGHT]))
        head_motors.move("eye_self", eye_pos, speed=400)
    else:
        if head_move_cooldown == 0 and should_move_head(current_yaw, head_target):
            print("current", current_yaw)
            print("move", head_target)
            head_motors.move("head_yaw", head_target, speed=500)
            head_motors.move("eye_self", EYE_CENTER, speed=400)
            head_move_cooldown = HEAD_MOVE_COOLDOWN_FRAMES
        else:
            head_move_cooldown = max(0, head_move_cooldown - 1)
    
    if blink_cooldown == 0:
        head_motors.move("eye_brow_l", 220, 350)
        head_motors.move("eye_brow_r", 500, 350)
        time.sleep(0.3)
        head_motors.move("eye_brow_l", 350, 350)
        head_motors.move("eye_brow_r", 350, 350)
        blink_cooldown = random.randint(120,180)
    else:
        blink_cooldown = max(0, blink_cooldown-1)

# def track_face_y(face_y, cam_height=480):
#     global head_move_cooldown

#     norm_x = face_y / cam_height
#     delta_x = norm_x - 0.5
#     yaw_shift = np.interp(delta_x, [-0.5, 0.5], [90, -75])

#     try:
#         current_yaw = head_motors.current_pos("head_yaw")[0]
#     except Exception as e:
#         print(f"[WARN] Could not read head position: {e}")
#         current_yaw = HEAD_CENTER

#     head_target = int(current_yaw + yaw_shift)
#     head_target = min(max(head_target, HEAD_RIGHT), HEAD_LEFT)

#     if head_move_cooldown % 2 == 0 and EYE_ONLY_ZONE[0] <= norm_x <= EYE_ONLY_ZONE[1]:
#         eye_pos = int(np.interp(norm_x, [0, 1], [EYE_LEFT, EYE_RIGHT]))
#         head_motors.move("eye_self", eye_pos, speed=400)
#     else:
#         if head_move_cooldown == 0 and should_move_head(current_yaw, head_target):
#             print("current", current_yaw)
#             print("move", head_target)
#             head_motors.move("head_yaw", head_target, speed=500)
#             head_motors.move("eye_self", EYE_CENTER, speed=400)
#             head_move_cooldown = HEAD_MOVE_COOLDOWN_FRAMES
#         else:
#             head_move_cooldown = max(0, head_move_cooldown - 1)


def generate_frames():
    global gesture_results, pose_results, face_detection_results, last_head_gesture, head_cooldown

    gesture_options = GestureRecognizerOptions(
        base_options=BaseOptions(model_asset_path=GESTURE_MODEL),
        running_mode=VisionRunningMode.LIVE_STREAM,
        result_callback=process_gesture_result,
    )
    pose_options = PoseLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=POSE_MODEL),
        running_mode=VisionRunningMode.LIVE_STREAM,
        result_callback=process_pose_result,
    )
    face_options = FaceDetectorOptions(
        base_options=BaseOptions(model_asset_path=FACE_MODEL),
        running_mode=VisionRunningMode.LIVE_STREAM,
        result_callback=process_face_result,
    )

    with GestureRecognizer.create_from_options(
        gesture_options
    ) as gesture_recognizer, PoseLandmarker.create_from_options(
        pose_options
    ) as pose_landmarker, FaceDetector.create_from_options(
        face_options
    ) as face_detector:

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open camera")
            return

        timestamp_ms = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

            face_detector.detect_async(mp_image, timestamp_ms)

            display = frame.copy()

            if last_head_gesture and head_cooldown > 0:
                cv2.putText(
                    display,
                    f"Head: {last_head_gesture}",
                    (10, display.shape[0] - 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255, 255, 0),
                    2,
                )

            if gesture_results and gesture_results.gestures:
                for idx, gesture in enumerate(gesture_results.gestures):
                    top = gesture[0]
                    cv2.putText(
                        display,
                        f"Gesture: {top.category_name} ({top.score:.2f})",
                        (10, 30 + idx * 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 255, 0),
                        2,
                    )

            if face_detection_results and face_detection_results.detections:
                detection = face_detection_results.detections[0]  # only use first face
                bbox = detection.bounding_box
                confidence = detection.categories[0].score
                face_center_x = bbox.origin_x + (bbox.width / 2)
                face_center_y = bbox.origin_y + (bbox.height / 2)
                track_face_x(face_center_x)
                # track_face_y(face_center_y)
                cv2.rectangle(
                    display,
                    (bbox.origin_x, bbox.origin_y),
                    (bbox.origin_x + bbox.width, bbox.origin_y + bbox.height),
                    (0, 255, 255),
                    2,
                )

                # cv2.putText(
                #     display,
                #     f"Face: {confidence:.2f}",
                #     (bbox.origin_x, bbox.origin_y - 10),
                #     cv2.FONT_HERSHEY_SIMPLEX,
                #     0.6,
                #     (0, 255, 255),
                #     2,
                # )

            ret, buffer = cv2.imencode(".jpg", display)
            frame = buffer.tobytes()

            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")
            timestamp_ms += 33

        cap.release()


@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/")
def index():
    return render_template("video.html")


if __name__ == "__main__":
    head_motors.move("eye_self", EYE_CENTER, 400)
    time.sleep(0.5)
    head_motors.move("head_pitch", HEAD_MIDDLE, 1000)
    time.sleep(0.5)
    head_motors.move("head_yaw", HEAD_CENTER, 400)
    time.sleep(0.5)
    app.run(debug=False, host="0.0.0.0", port=5001)
