import time 
import random
import sys
import os

# === Setup Head Motors ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
sys.path.append(PROJECT_ROOT)
from head_control import HeadMotors
head_motors = HeadMotors()

def blink_loop():

    while True:
        blink_speed = 350
        time.sleep(3)
        try:
            head_motors.move("eye_brow_l", 220, blink_speed)
            head_motors.move("eye_brow_r", 500, blink_speed) # close eyes (blink)
            time.sleep(0.3)
            head_motors.move("eye_brow_l", 350, blink_speed) # open eyes
            head_motors.move("eye_brow_r", 350, blink_speed) 
            time.sleep(1)
            head_motors.move("eye_self", 139, 400) # gaze left
            time.sleep(1)
            head_motors.move("eye_self", 277, 400) # gaze right
            time.sleep(1)
            head_motors.move("eye_self", 202, 400) # center gaze

        except Exception as e:
            print("Blink error:",e)

def head_movement_loop():
    while True:
        print("Centering pitch...")
        head_motors.move("head_pitch", 150, 1000)  # Center
        time.sleep(2)

        print("Centering yaw...")
        head_motors.move("head_yaw", 180, 400)  # Center
        time.sleep(2)

        print("Looking left...")
        head_motors.move("head_yaw", 0, 400)   # Turn head left
        time.sleep(2)

        print("Looking right...")
        head_motors.move("head_yaw", 360, 400)  # Turn head right
        time.sleep(2)

        print("Centering yaw...")
        head_motors.move("head_yaw", 180, 400)  # Center
        time.sleep(2)

        print("Looking up...")
        head_motors.move("head_pitch", 240, 100)  # Look up
        time.sleep(2)

        print("Looking down...")
        head_motors.move("head_pitch", 120, 1000)  # Look down
        time.sleep(2)

if __name__ == "__main__":
    print("Starting head movement loop (press Ctrl+C to stop)...")
    blink_loop()
    # head_movement_loop()

