# MONTY III - Test the camera.py module
import time
from threading import Thread
from logger import Logger
from camera import Camera

datalogger = Logger()
camera = Camera(9788, datalogger)
camera_thread = Thread(target=camera.run)
camera_thread.start()

try:
  while True:
    print(camera.blob_location, camera.blob_size)
    time.sleep(2)

except:
  pass

camera.terminate()

camera_thread.join()
del camera
del datalogger
