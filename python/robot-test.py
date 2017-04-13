# MONTY III robot.py test

import time

from robot import Robot

robot = Robot()
robot.initialize()

try:
    robot.drive_to_waypoint(33.778127, 118.418720, 2.0)
    robot.stop()
    time.sleep(3)
    robot.drive_to_waypoint(33.778325, 118.419228, 2.0)
    robot.stop()

except:
    pass

robot.terminate()




