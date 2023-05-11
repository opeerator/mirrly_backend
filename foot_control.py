import time
import pyfirmata

class FootMotors(): 
    """This class manages robot's foot motions."""

    def __init__(self):
        # Define the pins used by the motor driver
        self.PWM1 = 9
        self.PWM2 = 10
        self.PWM3 = 11
        self.PWM4 = 13

        # Connect to the Arduino
        self.board = pyfirmata.Arduino('/dev/ttyACM0')  # Update the port if necessary

        # Configure the pins
        self.motor1_pwm1 = self.board.get_pin(f'd:{self.PWM1}:o')
        self.motor1_pwm2 = self.board.get_pin(f'd:{self.PWM2}:p') # 0-255
        self.motor2_pwm3 = self.board.get_pin(f'd:{self.PWM3}:p') # 0-255
        self.motor2_pwm4 = self.board.get_pin(f'd:{self.PWM4}:o')

        # Set the initial motor speeds
        self.speed1 = 255
        self.speed2 = 255
        
    def move(self, motor, speed):
        if motor == "all":
            # Set speed
            if speed != self.speed1:
                self.speed1 = int(speed)
                self.speed2 = int(speed)
                self.motor1_pwm2.write(self.speed1)
                self.motor2_pwm3.write(self.speed2)
            # Run the motors
            self.motor1_pwm1.write(1)
            self.motor2_pwm4.write(1)
        elif motor == "m_1":
            if speed != self.speed1:
                self.speed1 = int(speed)
                self.motor1_pwm2.write(self.speed1)
            # Run the motors
            self.motor1_pwm1.write(1)
        elif motor == "m_2":
            if speed != self.speed2:
                self.speed2 = int(speed)
                self.motor2_pwm3.write(self.speed2)
            # Run the motors
            self.motor2_pwm4.write(1)
    
    def release_motors(self, motor):
        if motor == 'all':
            # Release the motors
            self.motor1_pwm1.write(0)
            self.motor1_pwm2.write(0)
            self.motor2_pwm3.write(0)
            self.motor2_pwm4.write(0)
        else:
            if motor == "m_1":
                self.motor1_pwm1.write(0)
            elif motor == "m_2":
                self.motor2_pwm4.write(0)
            else:
                pass

    def close(self):
        # Disconnect from the Arduino
        self.board.exit()
        
