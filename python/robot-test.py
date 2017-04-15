# MONTY III robot.py test

import time
import traceback

from robot import Robot

robot = Robot()
robot.initialize()

try:
    robot.drive_to_waypoint(33.77817333333, 118.41868333333, 2.0)
    robot.seek_cone()
    robot.stop()
    time.sleep(3)
    robot.drive_to_waypoint(33.778341666666, 118.418971666666, 2.0)
    robot.seek_cone()
    robot.stop()

except:
    robot.logger.write(traceback.format_exc())

robot.terminate()




