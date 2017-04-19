#
# MONTY III - Main Robot class
#
from threading import Thread
import time

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
        self.logger.display("Starting...")
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
        self.logger.display("Initializing...")
        self.speedometer_thread = Thread(target = self.speedometer.run)
        self.compasswitch_thread = Thread(target = self.compasswitch.run)
        self.autopilot_thread = Thread(target = self.autopilot.run)
        self.gps_thread = Thread(target = self.gps.run)
        self.camera_thread = Thread(target = self.camera.run)
        self.speedometer_thread.start()
        self.compasswitch_thread.start()
        self.autopilot_thread.start()
        self.gps_thread.start()
        self.camera_thread.start()

    def terminate(self):
        self.logger.write("Robot: terminating")
        self.logger.display("Terminating...")
        self.speedometer.terminate()
        self.compasswitch.terminate()
        self.autopilot.terminate()
        self.gps.terminate()
        self.camera.terminate()
        self.speedometer_thread.join()
        self.compasswitch_thread.join()
        self.autopilot_thread.join()
        self.gps_thread.join()
	self.camera_thread.join()

    def wait_for_start_switch(self):
        self.logger.write("Robot: waiting for start switch")
        self.logger.display("Press start")
        while self.compasswitch.start_switch == False:
            time.sleep(0.1)
        self.logger.write("Robot: start switch activated")
        self.logger.display("Go!")

    def drive_to_waypoint(self, tgt_lat, tgt_lon, speed):
        self.logger.display("Drive 2 waypoint")
        (distance, bearing) = utils.get_distance_and_bearing(
            self.gps.latitude,
            self.gps.longitude,
            tgt_lat,
            tgt_lon)

        self.autopilot.engage()

        while distance > 10.0:
            self.autopilot.target_speed = speed
            self.autopilot.target_direction = bearing
            (distance, bearing) = utils.get_distance_and_bearing(
                self.gps.latitude,
                self.gps.longitude,
                tgt_lat,
                tgt_lon)

        self.autopilot.disengage()

    def seek_cone(self):
        self.logger.write("Robot: seeking cone. Blob size %s, BlobX %s" % (self.camera.blob_size, self.camera.blob_location))
        self.logger.display("Seek Cone")
        self.autopilot.speed_engage()
        self.autopilot.target_speed = 1.0
        while self.camera.blob_size > 0:
	    self.logger.write("Robot: seek_cone; %s, %s" % (self.camera.blob_location, self.camera.blob_size))	
            if self.compasswitch.bump_switch == True:
                self.logger.write("Robot: found cone")
                self.autopilot.disengage()
                return True
            self.powersteering.set_steer((int(self.camera.blob_location) - 32) * 10)
        self.logger.write("Robot: missed cone")
        self.autopilot.disengage()
        return False

    def stop(self):
        self.autopilot.disengage()
        self.powersteering.set_power(0)
                         
    def back_up(self, delay):
        self.logger.display("Reversing")
        self.autopilot.disengage()
        self.powersteering.set_power(-90)
        self.powersteering.set_steer(0)
        time.sleep(delay)
        self.powersteering.set_power(0)
