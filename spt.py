from gpiozero import Servo
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory
import math

factory = PiGPIOFactory()

# Right Shoulder 0 - 360 (200 front, 120 Back, when hands are down, 0, 360 are idle) # 22
# Right hand 160 - 270 (290 top, 160 down) # 27
# Left Shoulder 0 - 360 (1oo front, 280 Back, when hands are down, 0, 360 are idle) # 17
# Right hand 180 - 360 (180 top, 360 down) # 6

# Right Arm 
servo = Servo(6, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)

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
