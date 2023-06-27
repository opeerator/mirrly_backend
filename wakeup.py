import time
from mode_config import ModeManager
from head_control import HeadMotors
from torso_control import TorsoMotors

mode_manager = ModeManager()
head_motors = HeadMotors()
torso_motors = TorsoMotors()
current_move = None

def initial_positions():
	start_head_positions = head_motors.current_pos('all')
	
	# Go to start positions - HEAD
	if start_head_positions[0] != int(807):
		head_motors.move("head_yaw", 807)
		
	if start_head_positions[0] != int(131):
		head_motors.move("head_pitch", 131)
		
	if start_head_positions[0] != int(249):
		head_motors.move("eye_brow_l", 249)
		
	if start_head_positions[0] != int(750):
		head_motors.move("eye_brow_r", 750)

	if start_head_positions[0] != int(771):
		head_motors.move("eye_self", 771)
	
		
	time.sleep
	# Go to start positions - HANDS
	torso_motors.arm_move('r_shoulder', 7) # 3-12.5
	torso_motors.arm_move('l_shoulder', 9) # 3-12.5
	torso_motors.arm_move('arm_r', 7.5) # 2.5-7.5
	torso_motors.arm_move('arm_l', 6.5) # 6.5-12


if __name__ == "__main__":
	initial_positions()
	
	time.sleep(1)


