#!/usr/bin/env python3
import os
import sys
import time
import random
import threading
import subprocess
import multiprocessing
import atexit
from flask import Flask, render_template, jsonify, Response
from flask_socketio import SocketIO, emit
from google.cloud import texttospeech
from google.oauth2 import service_account
import openai
import speech_recognition as sr
import cv2

from mode_config import ModeManager
from head_control import HeadMotors
from torso_control import TorsoMotors

mode_manager = ModeManager()
head_motors = HeadMotors()
torso_motors = TorsoMotors()
"""
#MotorTests
print("forward")
torso_motors.move('forward', 255)

time.sleep(3)
    
torso_motors.release_motors()

time.sleep(1)

print("backward")
torso_motors.move('backward', 100)

time.sleep(3)
    
torso_motors.release_motors()
time.sleep(1)

print("rotate_right")
torso_motors.move('rotate_right', 120)

time.sleep(3)
    
torso_motors.release_motors()
time.sleep(1)

print("rotate_left")
torso_motors.move('rotate_left', 200)

time.sleep(3)
    
torso_motors.release_motors()
time.sleep(1)

print("rotate_left_b")
torso_motors.move('rotate_left_b', 80)

time.sleep(3)
    
torso_motors.release_motors()
time.sleep(1)

print("rotate_right_b")
torso_motors.move('rotate_right_b', 50)

time.sleep(3)
    
torso_motors.release_motors()

print("finito")
"""



"""Hand Test"""

# Initial positions for each servo
r_shoulder_pos = 70
l_shoulder_pos = 160
arm_r_pos = 170
arm_l_pos = 80

tika = 400
jika = 118

#torso_motors.release_motors()
#torso_motors.move('forward', 255)

try:

    while True:
        head_motors.move("head_yaw", tika, 400)
        if tika == 400:
            tika = 900
        else:
            tika = 400
            
        head_motors.move("head_pitch", jika, 600)
        
        if jika == 118:
            jika = 279
        else:
            jika = 118

        # Move each servo to its respective position
        torso_motors.arm_move("arm_l", arm_l_pos, 0.01)
        torso_motors.arm_move("r_shoulder", r_shoulder_pos, 0.01)
        torso_motors.arm_move("l_shoulder", l_shoulder_pos, 0.01)
        torso_motors.arm_move("arm_r", arm_r_pos, 0.01)
        
        # Toggle positions based on current angle, adjusting each servo independently
        if r_shoulder_pos == 70:
            r_shoulder_pos = 160
        else:
            r_shoulder_pos = 70
            
        if l_shoulder_pos == 160:
            l_shoulder_pos = 60
        else:
            l_shoulder_pos = 160
            
        if arm_r_pos == 170:
            arm_r_pos = 90  # Example range for arm_r
        else:
            arm_r_pos = 170
            
        if arm_l_pos == 80:
            arm_l_pos = 160  # Example range for arm_l
        else:
            arm_l_pos = 80
            
        time.sleep(6)
        
        """
        user_angle = input("Angle: ")
        
        if user_angle.lower() == 'q':
            break
        
        number = int(user_angle)
        #torso_motors.arm_move("arm_r", number, 0.001) # 170 Down - 90 Up When screw is front 
        #torso_motors.arm_move("arm_l", number, 0.001) # 160 Up - 80 Down When screw is front 
        #torso_motors.arm_move("r_shoulder", number, 0.001) # 70 cap front - 160 cap top - 
        #torso_motors.arm_move("l_shoulder", number, 0.001) # 160 cap front - 60 cap top - 
        """
except Exception as e:
    print(e)
    torso_motors.release_motors()
    torso_motors.release_hands('all')
    head_motors.close()
    
finally:
    torso_motors.release_motors()
    torso_motors.release_hands('all')
    head_motors.close()
        