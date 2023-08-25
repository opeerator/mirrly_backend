from gpiozero import Servo, AngularServo
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory
import math

factory = PiGPIOFactory()

# Right Shoulder Plate Top 90, Plate Front 0, Plate Down -90
# Right hand 160 - 270 (290 top, 160 down) # 27
# Left Shoulder 0 - 360 (1oo front, 280 Back, when hands are down, 0, 360 are idle) # 17
# Left hand 180 - 360 (180 top, 360 down) # 6

# Right Arm -10 (Top) to 90 (Down)
"""

servo = Servo(27, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)

try:
	while True:
		for i in range(180, 360):
			servo.value = math.sin(math.radians(i))
			print("degree: " + str(i))
			print("Servo Value: " + str(servo.value))
			sleep(0.01)

	servo.value = None
except KeyboardInterrupt:
	print("stopped by me!")
	servo.value = None
"""
# Plate Top -90, Plate Front 0, Plate Down 90

servo = AngularServo(17, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)
servo.source_delay = 0.05

max_i = 40

servo.angle = -90

"""
def custom_range(start, end, step=1):
    if start < end:
        while start <= end:
            yield start
            start += step
    else:
        while start >= end:
            yield start
            start -= step
            
while True:
	for i in custom_range(int(servo.angle), max_i):
		servo.angle = i
		print(i)
		sleep(0.01)
"""
sleep(1)
