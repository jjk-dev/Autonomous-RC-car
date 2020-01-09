from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
 
# Load camera module
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(320, 240))
 
time.sleep(0.1)
 
# Save images
start = 1
for frame in camera.capture_continuous(rawCapture, format="bgr", se_video_port=True):
  image = frame.array

  cv2.imshow("Frame", image)
  key = cv2.waitKey(1) & 0xFF
  cv2.imwrite(str(start) + ".jpg", image)
  start = start + 1

  rawCapture.truncate(0)
 
  if key == ord("q"):
    break
  time.sleep(0.5)
