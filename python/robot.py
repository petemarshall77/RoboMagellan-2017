#
# MONTY III - Main Robot class
#
from threading import Thread

from logger import Logger
from powersteering import PowerSteering
from speedometer import Speedometer
from compasswitch import Compasswitch
from autopilot import Autopilot
from camera import Camera
from gps import GPS
import usb_probe
import utils

class Robot:

    def __init__(self):
        self.logger = Logger()
        self.logger.write("Robot: initializing")
        ports = usb_probe.probe()
        self.logger.write("Robot: found USB ports...")
        for port in ports:
            self.logger.write("       %s, %s" % (ports[port], port))
        self.powersteering = PowerSteering(ports['chias'], 9600, self.logger)
        self.speedometer   = Speedometer(ports['speedometer'], 9600, self.logger)
        self.compasswitch  = Compasswitch(ports['compasswitch'], 9600, self.logger)
        self.autopilot     = Autopilot(self.powersteering,
				       self.speedometer,
				       self.compasswitch,
				       self.logger)
        self.camera        = Camera(9788, self.logger)
        self.gps           = GPS(ports['gps'], 4800, self.logger)

    def initialize(self):
        self.logger.write("Robot: initializing")
        self.speedometer_thread = Thread(target = self.speedometer.run)
        self.compasswitch_thread = Thread(target = self.compasswitch.run)
        self.autopilot_thread = Thread(target = self.autopilot.run)
        self.gps_thread = Thread(target = self.gps.run)
        self.speedometer_thread.start()
        self.compasswitch_thread.start()
        self.autopilot_thread.start()
        self.gps_thread.start()

    def terminate(self):
        self.logger.write("Robot: terminating")
        self.speedometer.terminate()
        self.compasswitch.terminate()
        self.autopilot.terminate()
        self.gps.terminate()
        self.speedometer_thread.join()
        self.compasswitch_thread.join()
        self.autopilot_thread.join()
        self.gps_thread.join()

    def drive_to_waypoint(self, tgt_lat, tgt_lon, speed):
        (distance, bearing) = utils.get_distance_and_bearing(
            self.gps.latitude,
            self.gps.longitude,
            tgt_lat,
            tgt_lon)

        self.autopilot.engage()

        while distance > 7.0:
            self.autopilot.target_speed = speed
            self.autopilot.target_direction = bearing
            (distance, bearing) = utils.get_distance_and_bearing(
                self.gps.latitude,
                self.gps.longitude,
                tgt_lat,
                tgt_lon)

        self.autopilot.disengage()

    def stop(self):
        self.autopilot.disengage()
        self.powersteering.set_power(0)
                         
