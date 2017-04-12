# MONTY III - Test the Autopilot
import time
from threading import Thread
from logger import Logger
from speedometer import Speedometer
from powersteering import PowerSteering
from compasswitch import Compasswitch
from autopilot import Autopilot
import usb_probe

logger = Logger()
ports = usb_probe.probe()

powersteering = PowerSteering(ports['chias'], 9600, logger)
speedo = Speedometer(ports['speedometer'], 9600, logger)
compasswitch = Compasswitch(ports['compasswitch'], 9600, logger)
autopilot = Autopilot(powersteering, speedo, compasswitch, logger)

speedo_thread = Thread(target=speedo.run)
speedo_thread.start()
compasswitch_thread = Thread(target=compasswitch.run)
compasswitch_thread.start()
autopilot_thread = Thread(target=autopilot.run)
autopilot_thread.start()


powersteering.delta_power(40)
autopilot.engage()
autopilot.target_speed = 1.5
autopilot.target_direction = 270
time.sleep(5)
autopilot.target_speed = 2.00
autopilot.target_direction = 180
time.sleep(5)
autopilot.target_speed = 1.5
autopilot.target_direction = 0
time.sleep(5)

speedo.terminate()
autopilot.terminate()
compasswitch.terminate()
speedo_thread.join()

autopilot_thread.join()

del logger   # force close of log file
