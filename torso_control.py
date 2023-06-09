import time
import pyfirmata
from pyfirmata import util
import RPi.GPIO as GPIO


class TorsoMotors(): 
    """This class manages robot's foot motions."""

    def __init__(self):
        # Define the pins used by the motor driver
        self.PWM1 = 6
        self.PWM2 = 11
        self.PWM3 = 10
        self.PWM4 = 9
        
        # Hand pins
        self.hs_pins = [31, 11 ,13, 15] #BOARD scheme

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
        GPIO.setmode(GPIO.BOARD)
        
        # Set up additional pins for servos
        GPIO.setup(self.hs_pins, GPIO.OUT)
            
        self.l_hand = GPIO.PWM(self.hs_pins[0], 50) # Left Hand 6.5-12
        self.l_shoulder = GPIO.PWM(self.hs_pins[1], 50) # Left Shoulder 3-12.5
        self.r_hand = GPIO.PWM(self.hs_pins[2], 50) # Right Hand 2.5-7.5
        self.r_shoulder = GPIO.PWM(self.hs_pins[3], 50) # Right Shoulder 3-12.5
         
        # self.l_hand.start(0)
        # self.r_hand.start(0)
        # self.l_shoulder.start(0)
        # self.r_shoulder.start(0)
        
        # Set the initial motor speeds
        self.speed1 = 255
        self.speed2 = 255
        
    def arm_move(self, comp, angle):
        if comp == "r_shoulder":
            print(GPIO.input(11))
            self.r_shoulder.start(0)
            self.r_shoulder.ChangeDutyCycle(angle)
            print("right shoulder")
        elif comp == "l_shoulder":
            self.l_shoulder.start(0)
            self.l_shoulder.ChangeDutyCycle(angle)
            print("left shoulder")
        elif comp == "arm_r":
            self.r_hand.start(0)
            self.r_hand.ChangeDutyCycle(angle)
            print("right arm")
        elif comp == "arm_l":
            self.l_hand.start(0)
            self.l_hand.ChangeDutyCycle(angle)
            print("left arm")
        else:
            pass
        
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
    def release_motors(self, motor):
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

