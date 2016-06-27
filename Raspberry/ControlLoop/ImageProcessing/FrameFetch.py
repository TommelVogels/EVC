# Name
# Description

#defines
USE_PI_CAMERA = 1

#include dependencies
from Debugging.Debug  import logToAll
import time
import cv2

if USE_PI_CAMERA==1:
  from picamera.array import PiRGBArray
  from picamera import PiCamera


if USE_PI_CAMERA==1: 
  camera = PiCamera()
  camera.resolution = (640, 480)
  #camera.iso = 200
  camera.awb_mode = 'off'
  camera.exposure_mode = 'auto'
  camera.hflip = True
  camera.vflip = True
  
  
  rg, bg = (1.3, 1.8)
  camera.awb_gains = (rg, bg)
  
  camera.framerate = 8
  rawCapture = PiRGBArray(camera, size=(640, 480))
  
time.sleep(0.1)

#variables

#functions

def getFrame():
  t1 = time.time()
  
  #thresholds()
  
  for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = (frame.array)
    image = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    top = image[120:360,0:640]
    bottom = image[250:480,0:640]
    rawCapture.truncate(0)
    t2 = time.time()
    logToAll("getFrame ; Get Frame ;  "+ str(float(t2-t1)) + " seconds",0)
    return [top,bottom]