# MONTY III - Test the gps.py module
import time
from threading import Thread
from logger import Logger
from gps import GPS
import usb_probe

datalogger = Logger()
ports = usb_probe.probe()
print(ports)
gps = GPS(ports['gps'], 4800, datalogger)
gps_thread = Thread(target=gps.run)
gps_thread.start()

try:
  while True:
    print("Got fix?", gps.got_fix())
    print(gps.latitude, gps.longitude)
    time.sleep(2)

except:
  pass

gps.terminate()

gps_thread.join()
del gps
del datalogger
