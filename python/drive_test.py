#!/usr/bin/python

# Robomagellan 2016
#

# Import all the things
import time, sys
from usb_probe import probe
from logger import Logger
from powersteering import *

#========================================================
#Main program starts here
#========================================================
def main():
    # Start logging
    datalog = Logger()

    # Check the USB ports
    ports = probe()
    for port in ports:
        datalog.write("Drivetest: found USB: %s --> %s" % (port, ports[port]))

    # Open the power/steering serial port 
    power_steering = PowerSteering(ports['chias'], 9600, datalog)
    time.sleep(3)

    # Here we go...
    instructions = [[0, 100, 3],     # Steer, power, time
                    [-300, 100, 3],
                    [0, 100, 3],
                    [300, 100, 3]]
    try:
        power_steering.set_steer_and_pwr(0, 50)
        time.sleep(3)
        power_steering.set_steer_and_pwr(-300, 50)
        time.sleep(3)
        power_steering.set_steer_and_pwr(0, 50)
        time.sleep(3)
        power_steering.set_steer_and_pwr(300, 50)
        time.sleep(3)

        power_steering.stop()
        time.sleep(3)

        power_steering.set_power(50)
        time.sleep(3)
        power_steering.set_steer(300)
        time.sleep(3)

        power_steering.stop()

    except Exception as e:
        datalog.write("RoboMagellan: an exception occured.")
        datalog.write(e)
        power_steering.stop()

    # Start the compass serial port
    #compass = Compass(compass_port_name, 9600, datalog)

    # Start the GPS serial port
    #gps = GPS(GPS_port_name, 4800, datalog)

    # Set the Arduino to Drive Mode by sending control string
    #power_steering.set_mode_drive()
    #time.sleep(5)

    #compass_thread = CompassThread(compass, datalog)
    #compass_thread.start()

    #gps_thread = GPSThread(gps, datalog)
    #gps_thread.start()

    #camera = Camera(datalog)
    #camera_thread = CameraThread(camera, datalog)
    #camera_thread.start()

    #robot = Robot(power_steering, compass, gps, camera, datalog)

    #try:
    #    gps.get_GPS()
    #    datalog.write("Armed and Ready - Press Button")
    #    while compass.get_bump_switch_state() == False:
    #        pass
    #    datalog.write("Go!!!")
    #    dec12course(robot)

    #except KeyboardInterrupt:
    #    pass

    #========================================================
    #Main program stops here
    #========================================================
    #robot.stop_driving()
    #power_steering.set_mode_stop()

    #compass_thread.join()
    #gps_thread.join()
    #camera_thread.join()
    #time.sleep(5)
        datalog.write('RoboMagellan: Done.')
        del datalog


if __name__ == "__main__":
    main()
