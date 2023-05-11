import time
import pyfirmata

# Define the pins used by the motor driver
PWM1 = 9
PWM2 = 10
PWM3 = 11
PWM4 = 13

# Connect to the Arduino
board = pyfirmata.Arduino('/dev/ttyACM1')  # Update the port if necessary

# Configure the pins
motor1_pwm1 = board.get_pin(f'd:{PWM1}:o')
motor1_pwm2 = board.get_pin(f'd:{PWM2}:o')
motor2_pwm3 = board.get_pin(f'd:{PWM3}:o')
motor2_pwm4 = board.get_pin(f'd:{PWM4}:o')

# Set the initial motor speeds
speed1 = 255
speed2 = 200

# Run the motors
motor1_pwm1.write(1)
motor1_pwm2.write(0)
motor2_pwm3.write(1)
motor2_pwm4.write(0)

# Function to control motor speed using software PWM
def set_motor_speed(motor_pwm1, motor_pwm2, speed):
    for i in range(speed):
        motor_pwm1.write(1)
        motor_pwm2.write(0)
        time.sleep(0.001)
        motor_pwm1.write(0)
        motor_pwm2.write(1)
        time.sleep(0.001)

# Set the motor speeds using software PWM
set_motor_speed(motor1_pwm1, motor1_pwm2, speed1)
set_motor_speed(motor2_pwm3, motor2_pwm4, speed2)

# Wait for 5 seconds
time.sleep(5)

# Release the motors
motor1_pwm1.write(0)
motor1_pwm2.write(0)
motor2_pwm3.write(0)
motor2_pwm4.write(0)

# Disconnect from the Arduino
board.exit()

