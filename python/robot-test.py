# MONTY III robot.py test

import time
import traceback

from robot import Robot

robot = Robot()
robot.initialize()

try:
    robot.drive_to_waypoint(33.778258333333, 118.418648333333, 2.0)
    if robot.seek_cone():
        robot.stop()
        time.sleep(2)
        robot.back_up(5)

    robot.drive_to_waypoint(33.778475, 118.41908333333, 2.0)

    robot.drive_to_waypoint(33.778411666666, 118.418958333333, 2.0)
    robot.seek_cone()
    robot.stop()

except:
    robot.logger.write(traceback.format_exc())

robot.terminate()




