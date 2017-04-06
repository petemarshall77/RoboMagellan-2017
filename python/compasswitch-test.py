# MONTY III - Test the compasswitch.py module
import time, math
from threading import Thread
from logger import Logger
from compasswitch import Compasswitch
import usb_probe

datalogger = Logger()
ports = usb_probe.probe()
print(ports)
compasswitch = Compasswitch(ports['compasswitch'], 9600, datalogger)
compasswitch_thread = Thread(target=compasswitch.run)
compasswitch_thread.start()

try:
  while True:
    print(compasswitch.compassX, compasswitch.compassY, compasswitch.heading,
            compasswitch.bump_switch, compasswitch.start_switch)
    time.sleep(1)

except:
  pass

compasswitch.terminate()

compasswitch_thread.join()
del compasswitch
del datalogger
