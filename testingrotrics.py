from pydexarm import Dexarm
import time
import serial

port = 'COM4'
dexarm = Dexarm(port)
# dexarm._send_cmd("M1112\n")
print('initialised')

# print(dexarm.get_current_position())

# dexarm.go_home()
# dexarm._send_cmd("M894 X0 Y300 Z0\n")
# dexarm._send_cmd("G1 X50")

# dexarm.move_to(0 , 300 , -127)
# dexarm.soft_gripper_pick()

# dexarm.move_to((200, 200, 100))
# dexarm.move_to(50, 300, -50)
# dexarm.air_picker_pick()
# dexarm.move_to(50, 300, 0)
# dexarm.move_to(-50, 300, 0)
# dexarm.move_to(-50, 300, -50)
# dexarm.air_picker_place()
# 
dexarm.go_home()
# dexarm.move_to((-310, 0, 50), feedrate = 10000)
# print('this is the initial position')
# print(dexarm.get_current_position())
# dexarm.fast_move_to((-350, 200, 50), feedrate = 10000)

# while dexarm.get_current_position()[:3] != (100, 300, 50):
#     print('dexarm in motion')
#     print(dexarm.get_current_position())

# print(dexarm.get_current_position())

# dexarm.move_to((-200, 0, 50), feedrate = 100000)

# dexarm.move_rail(0)
# dexarm.move_to((-114, 313 , 0))
# print(dexarm.get_current_position())
# dexarm.soft_gripper_place()
# dexarm.move_rail(0)
dexarm.soft_gripper_nature()
# print(dexarm.get_current_position())

# dexarm.sliding_rail_init()
# dexarm.move_rail(200, feedrate = 4500)
# dexarm.conveyor_belt_forward(speed = 500)

# dexarm._send_cmd("G01 E200 F4000\n")

# dexarm.conveyor_belt_stop()

# time.sleep(10)
# dexarm.go_home()
# dexarm.soft_gripper_pick()
# dexarm.soft_gripper_nature()
# dexarm.move_to((10, 310, -30))
# dexarm.move_to((53, 408, 0))
# dexarm.move_to((53, 408, -30))
# dexarm.move_rail(0)
# dexarm.fast_move_to((400,0,-77))
# dexarm._send_cmd("M1002\n")
