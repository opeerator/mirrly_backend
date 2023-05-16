import time
import pyfirmata

class FootMotors(): 
    """This class manages robot's foot motions."""

    def __init__(self):
        # Define the pins used by the motor driver
        self.PWM1 = 6
        self.PWM2 = 11
        self.PWM3 = 10
        self.PWM4 = 9

        # Connect to the Arduino
        self.board = pyfirmata.Arduino('/dev/ttyACM0')  # Update the port if necessary

        # Configure the pins
        self.M1A = self.board.get_pin(f'd:{self.PWM1}:p')
        self.M1B = self.board.get_pin(f'd:{self.PWM2}:p')
        self.M2A = self.board.get_pin(f'd:{self.PWM3}:p') 
        self.M2B = self.board.get_pin(f'd:{self.PWM4}:p')

        # Set the initial motor speeds
        self.speed1 = 255
        self.speed2 = 255
        
    def move(self, motor, speed):
        if motor == "live":
            if speed['x'] > 0:
                if speed['y'] < 0:
                    self.M2A.write(speed['x']/255)
                else:
                    self.M1A.write(speed['x']/255)
            else:
                if speed['y'] < 0:
                    self.M1B.write(speed['x']/255)
                else:
                    self.M2B.write(speed['x']/255)
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
        if motor == 'all':
            # Release the motors
            self.M1A.write(0)
            self.M1B.write(0)
            self.M2A.write(0)
            self.M2B.write(0)

    def close(self):
        # Disconnect from the Arduino
        self.board.exit()
