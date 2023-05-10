import serial
import time

# Define the serial port
serial_port = '/dev/ttyUSB0'  # Update with the correct port

# Initialize the serial connection
arduino = serial.Serial(serial_port, 9600, timeout=1)

# Wait for the Arduino to initialize
time.sleep(2)

# Function to control the motors
def control_motors(motor1_speed, motor2_speed):
    command = f'{motor1_speed},{motor2_speed}\n'
    arduino.write(command.encode())

# Example usage
control_motors(200, -200)  # Set motor1 speed to 200 and motor2 speed to -200

# Close the serial connection
arduino.close()