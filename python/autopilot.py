# MONTY III Autopilot

# The autopilot uses the speed and direction data (from speedometer.py and
# compassbump.py) to enable the robot to maintain a steady course and speed.
#
# Note that at some times, it will be preferable to set speed (well, power,
# actually) and steering directly through Powersteering. The autopilot
# therefore should be engaged and disengaged as necessary.
#
import time
import utils

class Autopilot:

    def __init__(self, powersteering, speedometer, compasswitch, logger):
        self.logger = logger
        self.logger.write("Autopilot: starting")
        self.powersteering = powersteering
        self.compasswitch = compasswitch
        self.speedo = speedometer
        self._running = False
        self.target_speed = 0
        self.target_direction = 0
        self.speed_engaged = False
        self.steer_engaged = False

    def run(self):
        self._running = True
        self.logger.write("Autopilot: running")

        while (self._running == True):
            if self.speed_engaged == True:
                if self.target_speed > self.speedo.speed:
		    delta_value = int((self.target_speed - self.speedo.speed)
                                      * 2)
                    self.logger.write("Autopilot: speed = %f, increasing power"
                                      % self.speedo.speed)
                    self.powersteering.delta_power(delta_value)
                else:
		    delta_value = int((self.target_speed - self.speedo.speed)
                                      * 2)
                    self.logger.write("Autopilot: speed = %f, decreasing power"
                                      % self.speedo.speed)
                    self.powersteering.delta_power(delta_value)
            if self.steer_engaged == True:
                delta_angle = int(utils.delta_angle(self.target_direction,
                                                    self.compasswitch.heading))
		self.logger.write(
                    "Autopilot: target: %d, compass = %d, delta = %d"
                    % (self.target_direction,
                       self.compasswitch.heading,
                       delta_angle))
                self.powersteering.set_steer(delta_angle * 4)

	    time.sleep(0.25)

    def terminate(self):
        self.logger.write("Autopilot: terminated")
        self._running = False

    def engage(self):
        self.logger.write("Autopilot: engaged")
        self.steer_engaged = True
        self.speed_engaged = True

    def disengage(self):
        self.logger.write("Autopilot: disengaged")
        self.steer_engaged = False
        self.speed_engaged = False

    def speed_engage(self):
        self.logger.write("Autopilot: speed engaged")
        self.speed_engaged = True
