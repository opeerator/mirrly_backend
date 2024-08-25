#!/usr/bin/python3

# sudo apt-get install python3-setuptools
# sudo python3 setup.py install

import os
""" 
# Makes problem when running it from bash script
if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
"""
from dynamixel_sdk import * # Uses Dynamixel SDK library

MY_DXL = 'XL320'        # [WARNING] Operating Voltage : 7.4V
ADDR_TORQUE_ENABLE          = 24
ADDR_GOAL_SPEED             = 34
ADDR_GOAL_POSITION          = 30
ADDR_PRESENT_POSITION       = 36        # Default is 37
DXL_MINIMUM_POSITION_VALUE  = 0         # Refer to the CW Angle Limit of product eManual
DXL_MAXIMUM_POSITION_VALUE  = 1023      # Refer to the CCW Angle Limit of product eManual
BAUDRATE                    = 1000000   # Default Baudrate of XL-320 is 1Mbps
PROTOCOL_VERSION            = 1.0

# Factory default ID of all DYNAMIXEL is 1
DXL_ID_1                      = 1 # Yaw
DXL_ID_2                      = 2 # Pitch
DXL_ID_3                      = 3 # Left eye
DXL_ID_4                      = 4 # Right eye
DXL_ID_5                      = 5 # Eye

# ex) Windows: "COM*", Linux: "/dev/ttyUSB*", Mac: "/dev/tty.usbserial-*"
DEVICENAME                  = '/dev/ttyUSB0'

TORQUE_ENABLE               = 0     # Value for enabling the torque
TORQUE_DISABLE              = 1     # Value for disabling the torque
DXL_MOVING_STATUS_THRESHOLD = 20    # Dynamixel moving status threshold

class HeadMotors(object):
    """This class manager robot's head motion commands"""
    
    def __init__(self):
        self.dxl_yaw_range = [970, 590]         # Goal position for Yaw
        self.dxl_pitch_range = [279, 118]         # Goal position for Pitch
        self.dxl_eyes_range = [268, 221]         # Goal position for eye
        
        self.moving = False

        # Initialize PortHandler instance
        # Set the port path
        # Get methods and members of PortHandlerLinux or PortHandlerWindows
        self.portHandler = PortHandler(DEVICENAME)

        # Initialize PacketHandler instance
        # Set the protocol version
        # Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
        self.packetHandler = PacketHandler(PROTOCOL_VERSION)

        # Open port
        if self.portHandler.openPort():
            print("Succeeded to open the port")
        else:
            print("Failed to open the port")
            print("Press any key to terminate...")
            getch()
            quit()

        # Set port baudrate
        if self.portHandler.setBaudRate(BAUDRATE):
            print("Succeeded to change the baudrate")
        else:
            print("Failed to change the baudrate")
            print("Press any key to terminate...")
            getch()
            quit()

        # Enable Dynamixel Torque
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, DXL_ID_1, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
        dxl_comm_result_2, dxl_error_2 = self.packetHandler.write1ByteTxRx(self.portHandler, DXL_ID_2, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
        dxl_comm_result_3, dxl_error_3 = self.packetHandler.write1ByteTxRx(self.portHandler, DXL_ID_3, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
        dxl_comm_result_4, dxl_error_4 = self.packetHandler.write1ByteTxRx(self.portHandler, DXL_ID_4, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
        dxl_comm_result_5, dxl_error_5 = self.packetHandler.write1ByteTxRx(self.portHandler, DXL_ID_5, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)

        # if dxl_comm_result != COMM_SUCCESS:
        #     print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        # elif self.dxl_error != 0:
        #     print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        # else:
        #     print("Dynamixel has been successfully connected")
            
    def move(self, component, g_pos, speed=1000):
        # A function to move the robot from server commands
        # Move Component
        dxl_comm_result = None
        dxl_error = None
        dxl_comm_result_2 = None
        dxl_error_2 = None
        
        # Wait for last move
        while self.moving == True:
            pass
        
        self.moving == True
        if component == "head_yaw":
            # Setting speed
            self.packetHandler.write2ByteTxRx(self.portHandler, DXL_ID_1, ADDR_GOAL_SPEED, int(speed))
            # Setting goal position
            dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, DXL_ID_1, ADDR_GOAL_POSITION, int(g_pos))
        elif component == "head_pitch":
            # Setting speed
            self.packetHandler.write2ByteTxRx(self.portHandler, DXL_ID_2, ADDR_GOAL_SPEED, int(speed))
            dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, DXL_ID_2, ADDR_GOAL_POSITION, int(g_pos))
        elif component == "eye_brow":
            # Setting speed
            self.packetHandler.write2ByteTxRx(self.portHandler, DXL_ID_3, ADDR_GOAL_SPEED, int(speed))
            self.packetHandler.write2ByteTxRx(self.portHandler, DXL_ID_4, ADDR_GOAL_SPEED, int(speed))
            dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, DXL_ID_3, ADDR_GOAL_POSITION, int(g_pos))
            dxl_comm_result_2, dxl_error_2 = self.packetHandler.write2ByteTxRx(self.portHandler, DXL_ID_4, ADDR_GOAL_POSITION, g_pos)
        elif component == "eye_brow_l":
            # Setting speed
            self.packetHandler.write2ByteTxRx(self.portHandler, DXL_ID_3, ADDR_GOAL_SPEED, int(speed))
            dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, DXL_ID_3, ADDR_GOAL_POSITION, int(g_pos))
        elif component == "eye_brow_r":
            # Setting speed
            self.packetHandler.write2ByteTxRx(self.portHandler, DXL_ID_4, ADDR_GOAL_SPEED, int(speed))
            dxl_comm_result_2, dxl_error_2 = self.packetHandler.write2ByteTxRx(self.portHandler, DXL_ID_4, ADDR_GOAL_POSITION, g_pos)
        elif component == "eye_self":
            # Setting speed
            self.packetHandler.write2ByteTxRx(self.portHandler, DXL_ID_5, ADDR_GOAL_SPEED, int(speed))
            dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, DXL_ID_5, ADDR_GOAL_POSITION, int(g_pos))
        else:
            pass
        self.moving == False
        
        
        if dxl_comm_result != None:
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                return "success_1"
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
                return "failed_1"
            
        if dxl_comm_result_2 != None:
            if dxl_comm_result_2 != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result_2))
                return "success_2"
            elif dxl_error_2 != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error_2))
                return "failed_2"

    def current_pos(self, component):
        if component == "all":
            dxl_present_position, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, DXL_ID_1, ADDR_PRESENT_POSITION)
            dxl_present_position_2, dxl_comm_result_2, dxl_error_2 = self.packetHandler.read2ByteTxRx(self.portHandler, DXL_ID_2, ADDR_PRESENT_POSITION)
            dxl_present_position_3, dxl_comm_result_3, dxl_error_3 = self.packetHandler.read2ByteTxRx(self.portHandler, DXL_ID_3, ADDR_PRESENT_POSITION)
            dxl_present_position_4, dxl_comm_result_4, dxl_error_4 = self.packetHandler.read2ByteTxRx(self.portHandler, DXL_ID_4, ADDR_PRESENT_POSITION)
            dxl_present_position_5, dxl_comm_result_5, dxl_error_5 = self.packetHandler.read2ByteTxRx(self.portHandler, DXL_ID_5, ADDR_PRESENT_POSITION)
        elif component == "head_yaw":
            dxl_present_position, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, DXL_ID_1, ADDR_PRESENT_POSITION)
        elif component == "head_pitch":
            dxl_present_position, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, DXL_ID_2, ADDR_PRESENT_POSITION)
        elif component == "eye_brow":
            dxl_present_position, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, DXL_ID_3, ADDR_PRESENT_POSITION)
            dxl_present_position_2, dxl_comm_result_2, dxl_error_2 = self.packetHandler.read2ByteTxRx(self.portHandler, DXL_ID_4, ADDR_PRESENT_POSITION)
        elif component == "eye_self":
            dxl_present_position, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, DXL_ID_5, ADDR_PRESENT_POSITION)
        else:
            pass
        
        positions = []
        if component == "all":
            positions.append(dxl_present_position)
            positions.append(dxl_present_position_2)
            positions.append(dxl_present_position_3)
            positions.append(dxl_present_position_4)
            positions.append(dxl_present_position_5)
        elif component == "eye_brow":
            positions.append(dxl_present_position)
            positions.append(dxl_present_position_2)
        else:
            positions.append(dxl_present_position)
            
        return positions
            
    def disable_torque(self, component):
        if component == "all":
            dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, DXL_ID_1, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
            dxl_comm_result_2, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, DXL_ID_2, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
            dxl_comm_result_3, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, DXL_ID_3, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
            dxl_comm_result_4, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, DXL_ID_4, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
            dxl_comm_result_5, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, DXL_ID_5, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)

        elif component == "head_yaw":
            dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, DXL_ID_1, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
        elif component == "head_pitch":
            dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, DXL_ID_2, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
        elif component == "eye_brow":
            dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, DXL_ID_3, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
            dxl_comm_result_2, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, DXL_ID_4, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
        elif component == "eye_self":
            dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, DXL_ID_5, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
        else:
            pass
        
        # if dxl_comm_result != COMM_SUCCESS:
        #     print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        # elif dxl_error != 0:
        #     print("%s" % packetHandler.getRxPacketError(dxl_error))
        
    def close(self):
        # Close port
        self.portHandler.closePort()
