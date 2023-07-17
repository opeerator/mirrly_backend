import os
import sys
import time
import random
import threading
import subprocess
from google.cloud import texttospeech
from google.oauth2 import service_account
import openai
import speech_recognition as sr
import cv2

from mode_config import ModeManager
from head_control import HeadMotors
from torso_control import TorsoMotors

mode_manager = ModeManager()
head_motors = HeadMotors() # From back 970 means to right / 590 means to left
torso_motors = TorsoMotors()
current_move = None

eye_pos_checker = 0

os.environ['QT_QPA_PLATFORM'] = 'xcb'

openai.api_key = "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"

# set up the TTS client
cr = service_account.Credentials.from_service_account_file(
    'socialrobotics-381420-7add1789cf22.json')
client = texttospeech.TextToSpeechClient(credentials=cr)
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US",
    ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
)
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.LINEAR16
)

idle_v = [
    "bored",
    "friend",
    "game",
    "hungry",
    "lab",
    "see",
    "shy",
    "stare",
    "weather"
]

is_speech_playing = False  # Variable to track if speech is currently playing


def chat_bot_module(text):
    prompt = text
    model = "text-davinci-002"
    temperature = 0.5
    max_tokens = 100

    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens
    )
    print(response.choices[0].text)
    return response.choices[0].text


def say(text):
    th = threading.Thread(target=generate_speech, args=(text, ))
    th.start()
    
def play_speech(name):
    global is_speech_playing
    
    # Check if speech is already playing
    if is_speech_playing:
        return
    
    # Set is_speech_playing to True to indicate that speech is starting
    is_speech_playing = True
    
    # Amplify the sound using amixer
    subprocess.run(["amixer", "-D", "pulse", "sset", "Master", "300%"], capture_output=True)
    
    if name == "random":
        probability = 0.01
        if random.random() < probability:
            s_sound = random.choice(idle_v)
            subprocess.run(["aplay", f'tts/Daphne/{s_sound} (mp3cut.net).wav'], capture_output=True)
    else:
        # Play the amplified sound using aplay
        subprocess.run(["aplay", f'tts/Daphne/{name} (mp3cut.net).wav'], capture_output=True)
    
    # Set is_speech_playing to False to indicate that speech has finished playing
    is_speech_playing = False


def generate_speech(text):
    # set up the TTS request
    synthesis_input = texttospeech.SynthesisInput(text=text)
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )
    # save the audio to a file
    random_number = random.randint(100, 999)
    with open(f'speech_{random_number}.wav', 'wb') as out:
        out.write(response.audio_content)

    # os.system(f'aplay speech_{random_number}.wav')
    
    # Amplify the sound using amixer
    subprocess.run(["amixer", "-D", "pulse", "sset", "Master", "100%"], capture_output=True)

    # Play the amplified sound using aplay
    subprocess.run(["aplay", f'speech_{random_number}.wav'], capture_output=True)

    # Reset the sound amplification using amixer
    subprocess.run(["amixer", "-D", "pulse", "sset", "Master", "100%"], capture_output=True)

    sys.exit()



def initial_positions():
    start_head_positions = head_motors.current_pos('all')

    # Go to start positions - HEAD
    if start_head_positions[0] != int(807):
        head_motors.move("head_yaw", 807, 400)

    if start_head_positions[0] != int(131):
        head_motors.move("head_pitch", 131, 1000)

    if start_head_positions[0] != int(249):
        head_motors.move("eye_brow_l", 280, 500)

    if start_head_positions[0] != int(750):
        head_motors.move("eye_brow_r", 810, 500)

    if start_head_positions[0] != int(771):
        head_motors.move("eye_self", 771, 500)

    # Go to start positions - HANDS
    torso_motors.arm_move('r_shoulder', 7)  # 3-12.5
    torso_motors.arm_move('l_shoulder', 9)  # 3-12.5
    torso_motors.arm_move('arm_r', 7.5)  # 2.5-7.5
    torso_motors.arm_move('arm_l', 6.5)  # 6.5-12


def eye_brow_idle():
    probability = 0.07  # Probability of eye brow idle movement
    if random.random() < probability and eye_pos_checker < 800:
        head_motors.move("eye_brow_l", 280, 1000)
        head_motors.move("eye_brow_r", 850, 1000)
        time.sleep(0.2)
        head_motors.move("eye_brow_l", 509, 1000)
        head_motors.move("eye_brow_r", 596, 1000)


def eye_roll():
    probability = 0.1  # Probability of eye movement
    if random.random() < probability:
        random_value = random.randint(720, 919)
        eye_pos_checker = random_value
        head_motors.move("eye_self", random_value, 500)


def yaw_roll():
    probability = 0.1  # Probability of eye movement
    if random.random() < probability:
        random_value = random.randint(590, 970)
        random_speed = random.randint(400, 700)
        head_motors.move("head_yaw", random_value, random_speed)


def pitch_roll():
    probability = 0.1  # Probability of eye movement
    if random.random() < probability:
        random_value = random.randint(137, 237)
        random_speed = random.randint(800, 1000)
        head_motors.move("head_pitch", random_value, 1000)
        
def show_webcam1(cam_index):
    # Open the webcam
    cap = cv2.VideoCapture(cam_index)

    # Set the desired frame width and height
    frame_width = 320
    frame_height = 240

    # Set the frame size for the webcam
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    while True:
        # Read the current frame
        ret, frame = cap.read()

        # Resize the frame
        frame = cv2.resize(frame, (frame_width, frame_height))

        cv2.imshow(f'Right Eye - {cam_index}', frame)

        # Exit loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close the window
    cap.release()
    cv2.destroyAllWindows()
    
def show_webcam_output(cam_index):
    # Create a face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Set the desired frame width and height
    frame_width = 320
    frame_height = 240

    # Open the webcam
    cap = cv2.VideoCapture(cam_index)  # Assuming webcam2 is used

    # Set the frame size for the webcam
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    # Calculate the center of the frame
    frame_center_x = frame_width // 2

    # Calculate the range of yaw movement
    yaw_min = 590
    yaw_max = 970

    # Calculate the scaling factor
    scale_factor = (yaw_max - yaw_min) / frame_width

    # Initialize the previous face position
    prev_face_position = None
    is_moving = False

    while True:
        # Read the current frame
        ret, frame = cap.read()

        # Resize the frame
        frame = cv2.resize(frame, (frame_width, frame_height))

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Initialize the face center variable
        face_center_x = None

        if len(faces) > 0:
            # Select a random face from the detected faces
            selected_face = random.choice(faces)

            # Get the position of the selected face
            (x, y, w, h) = selected_face

            # Calculate the center of the selected face
            face_center_x = x + w // 2

            # Draw a rectangle around the face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Calculate the horizontal movement based on the face position relative to the frame center
        if face_center_x is not None:
            horizontal_movement = frame_center_x - face_center_x

            # Calculate the yaw movement based on the scaling factor
            yaw_movement = (-1 * int(horizontal_movement * scale_factor)) / 7
            print(f"YawMovement: {yaw_movement}")

            # Perform yaw movement based on the horizontal face movement
            try:
                current_yaw = head_motors.current_pos("head_yaw")[0]
            except:
                print("dynamixel Problem on yaw")
                continue
            new_yaw = current_yaw + yaw_movement
            yaw_change = abs(current_yaw - new_yaw)
            print(f"newYaw: {new_yaw}")
            print(f"change: {yaw_change}")
            # Check if the new yaw is within the range
            if yaw_min <= new_yaw <= yaw_max and abs(yaw_change) > 5 and is_moving == False:
                print("MOVE")
                is_moving = True
                head_motors.move("head_yaw", new_yaw, 500)
                is_moving = False

        # Display the frame
        cv2.imshow('Webcam', frame)

        # Exit loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    # Release the webcam and close the window
    cap.release()
    cv2.destroyAllWindows()




if __name__ == "__main__":
    try:
        # Webcam indexes
        webcam1_index = 0  # Index of the first webcam
        webcam2_index = 2  # Index of the second webcam

        # Create threads for each webcam
        webcam1_thread = threading.Thread(target=show_webcam1, args=(webcam1_index,))
        webcam2_thread = threading.Thread(target=show_webcam_output, args=(webcam2_index,))

        # Start the webcam threads
        webcam1_thread.start()
        webcam2_thread.start()
        """
        print(head_motors.current_pos("eye_brow"))  # Left-Right
        initial_positions()
        time.sleep(1)
        torso_motors.release_hands("all")

        time.sleep(5)
        # Wake up motion
        head_motors.move("head_pitch", 237, 500)
        head_motors.move("eye_brow_l", 509, 400)
        head_motors.move("eye_brow_r", 596, 400)
        time.sleep(5)
        head_motors.move("head_pitch", 100)
        play_speech("greeting")
        """
        while True:
            # eye_brow_idle()
            # eye_roll()
            pitch_roll()
            # yaw_roll()
            play_speech("random")

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("stopped")
        head_motors.disable_torque("all")
        torso_motors.release_motors()
        torso_motors.release_hands("all")
