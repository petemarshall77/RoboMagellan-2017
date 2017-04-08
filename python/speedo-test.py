# MONTY III - Test the speedo.py module
import time
from threading import Thread
from logger import Logger
from speedometer import Speedometer
import usb_probe

datalogger = Logger()
ports = usb_probe.probe()
speedo = Speedometer(ports['speedometer'], 9600, datalogger)
speedo_thread = Thread(target=speedo.run)
speedo_thread.start()

try:
    while(True):
        print(speedo.speed, speedo.distance)
        time.sleep(0.5)
except:
    pass
    
speedo.terminate()

speedo_thread.join()
del speedo
del datalogger
