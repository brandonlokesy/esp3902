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
# dexarm.go_home()
# dexarm.move_to((100, 300, 50))
# dexarm.move_to((-100, 300, 50))
# dexarm.move_to(0 , 300 , -122)
# dexarm.soft_gripper_place()

# dexarm.sliding_rail_init()
# dexarm.conveyor_belt_forward(speed = 500)

# dexarm._send_cmd("G01 E400 F4000\n")

# dexarm.conveyor_belt_stop()

# time.sleep(10)
dexarm.go_home()
# dexarm.move_to((-80, 350, 0))
# dexarm.move_rail(0)
# dexarm.fast_move_to((400,0,-77))
# dexarm._send_cmd("M1002\n")
