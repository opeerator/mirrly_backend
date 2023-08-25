#!/usr/bin/env python3

import time
import math
import subprocess
import multiprocessing
import pyfirmata
from pyfirmata import util
from gpiozero import Servo, AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory

def custom_range(start, end, step=1):
    if start < end:
        while start <= end:
            yield start
            start += step
    else:
        while start >= end:
            yield start
            start -= step
            
class TorsoMotors(): 
    """This class manages robot's foot motions."""

    def __init__(self):
        # Define the pins used by the motor driver
        self.PWM1 = 6
        self.PWM2 = 11
        self.PWM3 = 10
        self.PWM4 = 9
        
        # Hand pins
        # self.hs_pins = [31, 11 ,13, 15] #BOARD scheme l_hand, shoulder, r_hand, Shoulder
        self.hs_pins = [6, 17 ,27, 22] #BOARD scheme
        self.s_positions = [0, 0, 0, 0]
        self.read_positions()

        # Connect to the Arduino
        self.board = pyfirmata.Arduino('/dev/ttyACM0')  # Update the port if necessary
        it = util.Iterator(self.board)
        it.start()

        # Configure the pins # Foots
        self.M1A = self.board.get_pin(f'd:{self.PWM1}:p')
        self.M1B = self.board.get_pin(f'd:{self.PWM2}:p')
        self.M2A = self.board.get_pin(f'd:{self.PWM3}:p') 
        self.M2B = self.board.get_pin(f'd:{self.PWM4}:p')
        
        # Configure pins for # Hands 
        #GPIO.setmode(GPIO.BOARD)
        
        # Set up additional pins for servos
        #GPIO.setup(self.hs_pins, GPIO.OUT)
            
        #self.l_hand = GPIO.PWM(self.hs_pins[0], 50) # Left Hand 6.5-12
        #self.l_shoulder = GPIO.PWM(self.hs_pins[1], 50) # Left Shoulder 3-12.5
        #self.r_hand = GPIO.PWM(self.hs_pins[2], 50) # Right Hand 2.5-7.5
        #self.r_shoulder = GPIO.PWM(self.hs_pins[3], 50) # Right Shoulder 3-12.5
        
        # self.l_hand.start(0)
        # self.r_hand.start(0)
        # self.l_shoulder.start(0)
        # self.r_shoulder.start(0)
        
        # Arms Configurations GPIOZero
        """
        # Bash command to be executed
        bash_command = "sudo pigpiod"

        # Run the Bash command
        try:
            subprocess.run(bash_command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running the command: {e}")
        """
        
        self.factory = PiGPIOFactory() # For Jitter Reduction
        self.factory2 = PiGPIOFactory() # For Jitter Reduction
        self.factory3 = PiGPIOFactory() # For Jitter Reduction
        self.factory4 = PiGPIOFactory() # For Jitter Reduction

        
        self.l_hand = AngularServo(self.hs_pins[0], min_pulse_width=0.5/1000, 
                            max_pulse_width=2.5/1000, pin_factory=self.factory, initial_angle=self.s_positions[0])

        self.l_shoulder = AngularServo(self.hs_pins[1], min_pulse_width=0.5/1000, 
                            max_pulse_width=2.5/1000, pin_factory=self.factory2, initial_angle=self.s_positions[1])

        self.r_hand = AngularServo(self.hs_pins[2], min_pulse_width=0.5/1000, 
                            max_pulse_width=2.5/1000, pin_factory=self.factory3, initial_angle=self.s_positions[2])
                            
        self.r_shoulder = AngularServo(self.hs_pins[3], min_pulse_width=0.5/1000, 
                            max_pulse_width=2.5/1000, pin_factory=self.factory4,
                            min_angle= -90, max_angle= 90, initial_angle=self.s_positions[3])
        
        time.sleep(5)
        # Set the initial motor speeds
        self.speed1 = 255
        self.speed2 = 255
        
    def read_positions(self, filename="./positions.txt"):
        with open(filename, "r") as file:
            for i, line in enumerate(file):
                self.s_positions[i] = int(line.strip())

    def update_positions(self, new_positions, filename="./positions.txt"):
        self.s_positions = new_positions
        print(self.s_positions)
        with open(filename, "w") as file:
            for position in self.s_positions:
                file.write(str(position) + "\n")
        
    def arm_motion_smooth(self, servo, initial, angle, speed=0.01):
        print("initial: " + str(initial))
        print("target: " + str(angle))
        def motion_smooth():
            for i in custom_range(initial, angle):
                servo.angle = i
                time.sleep(speed)
            time.sleep(1)
            servo.value = None
            
        process = multiprocessing.Process(target=motion_smooth)
        process.start()
        # process.join()
        
    def arm_move(self, comp, angle, speed):
        self.read_positions()
        print(comp)
        if comp == "r_shoulder":
            self.arm_motion_smooth(self.r_shoulder, self.s_positions[3], angle, speed)
            self.s_positions[3] = angle
        elif comp == "l_shoulder":
            self.arm_motion_smooth(self.l_shoulder, self.s_positions[1], angle, speed)
            self.s_positions[1] = angle
        elif comp == "arm_r":
            self.arm_motion_smooth(self.r_hand, self.s_positions[2], angle, speed)
            self.s_positions[2] = angle
        elif comp == "arm_l":
            self.arm_motion_smooth(self.l_hand, self.s_positions[0], angle, speed)
            self.s_positions[0] = angle
        else:
            pass
        self.update_positions(self.s_positions)
        print("===============================")
        
    def hands_freq(self, comp, n):
        if comp == "r_shoulder":
            self.r_shoulder.ChangeFrequency(n)
        elif comp == "l_shoulder":
            self.l_shoulder.ChangeFrequency(n)
        elif comp == "arm_r":
            self.r_hand.ChangeFrequency(n)
        elif comp == "arm_l":
            self.l_hand.ChangeFrequency(n)
        elif comp == "all":
            self.l_hand.ChangeFrequency(n)
            self.r_hand.ChangeFrequency(n)
            self.l_shoulder.ChangeFrequency(n)
            self.r_shoulder.ChangeFrequency(n)
            
    def release_hands(self, comp):
        if comp == "r_shoulder":
            self.l_shoulder.stop()
        elif comp == "l_shoulder":
            self.r_shoulder.stop()
        elif comp == "arm_r":
            self.r_hand.stop()
        elif comp == "arm_l":
            self.l_hand.stop()
        elif comp == "all":
            self.l_hand.stop()
            self.r_hand.stop()
            self.l_shoulder.stop()
            self.r_shoulder.stop()
        else:
            pass
            
    def move(self, motor, speed):
        if motor == "live":
            print(speed)
            if int(speed['x']) < 80 and int(speed['x']) > -80:
                if(speed['y']) > 0:
                    print("backward")
                    self.M1A.write(float(speed['y'])/255)
                    self.M1B.write(0)
                    self.M2A.write(0)
                    self.M2B.write(float(speed['y'])/255)
                else:
                    print("forward")
                    self.M1A.write(0)
                    self.M1B.write(float(-speed['y'])/255)
                    self.M2A.write(float(-speed['y'])/255)
                    self.M2B.write(0)
            elif int(speed['y']) < 80 and int(speed['y']) > -80:
                if(speed['x']) > 0:
                    print("right")
                    self.M1A.write(0)
                    self.M1B.write(0)
                    self.M2A.write(float(speed['x'])/255)
                    self.M2B.write(0)
                else:
                    print("left")
                    self.M1A.write(0)
                    self.M1B.write(-float(speed['x'])/255)
                    self.M2A.write(0)
                    self.M2B.write(0)
            else:
                    if int(speed['x']) > 0:
                        if int(speed['y']) < 0:
                            print("top-right")
                            self.M1B.write(0)
                            self.M2B.write(0)
                            self.M1A.write(-float(speed['y'])/255)
                            self.M2A.write(float(speed['x'])/255)
                        else:
                            print("back-right")
                            self.M2A.write(0)
                            self.M2B.write(0)
                            self.M1A.write(float(speed['y'])/255)
                            self.M2A.write(float(speed['x'])/255)
                    else:
                        if int(speed['y']) < 0:
                            print("top-left")
                            self.M1A.write(0)
                            self.M2A.write(0)
                            self.M2B.write(-float(speed['y'])/255)
                            self.M1B.write(-float(speed['x'])/255)
                        else:
                            print("back-left")
                            self.M1A.write(0)
                            self.M2A.write(0)
                            self.M1B.write(float(speed['y'])/255)
                            self.M2B.write(-float(speed['x'])/255)
        if motor == "forward":
            # Set speed
            if speed != self.speed1:
                self.speed1 = int(speed)
                self.speed2 = int(speed)
            # Run the motors
            self.M1A.write(0)
            self.M1B.write(self.speed1/255)
            self.M2A.write(self.speed2/255)
            self.M2B.write(0)
        elif motor == "backward":
            # Set speed
            if speed != self.speed1:
                self.speed1 = int(speed)
                self.speed2 = int(speed)
            # Run the motors
            self.M1A.write(self.speed1/255)
            self.M1B.write(0)
            self.M2A.write(0)
            self.M2B.write(self.speed2/255)
        elif motor == "rotate_right":
            # Set speed
            if speed != self.speed1:
                self.speed1 = int(speed)
                self.speed2 = int(speed)
            # Run the motors
            self.M1A.write(0)
            self.M1B.write(0)
            self.M2A.write(self.speed1/255)
            self.M2B.write(0)
        elif motor == "rotate_left":
            # Set speed
            if speed != self.speed1:
                self.speed1 = int(speed)
                self.speed2 = int(speed)
            # Run the motors
            self.M1A.write(0)
            self.M1B.write(self.speed1/255)
            self.M2A.write(0)
            self.M2B.write(0) 
        elif motor == "rotate_left_b":
            # Set speed
            if speed != self.speed1:
                self.speed1 = int(speed)
                self.speed2 = int(speed)
            # Run the motors
            self.M1A.write(0)
            self.M1B.write(0)
            self.M2A.write(0)
            self.M2B.write(self.speed1/255)
        elif motor == "rotate_right_b":
            # Set speed
            if speed != self.speed1:
                self.speed1 = int(speed)
                self.speed2 = int(speed)
            # Run the motors
            self.M1A.write(self.speed1/255)
            self.M1B.write(0)
            self.M2A.write(0)
            self.M2B.write(0)   
    def release_motors(self):
        # Release the motors
        time.sleep(0.2) # Should be considered or it will be not work consistent
        self.M1A.write(0)
        self.M1B.write(0)
        self.M2A.write(0)
        self.M2B.write(0)
        print("release")

    def close(self):
        # Disconnect from the Arduino
        self.board.exit()

