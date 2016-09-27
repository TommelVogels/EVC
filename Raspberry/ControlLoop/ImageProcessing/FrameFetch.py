# FrameFetch.py
# This file is to initialize the Pi camera and fetch frames from items
# Auto White Balance (awb) is disabled for the camera as it would mess with the hue, saturation and value
# of the images coming out of the camera, resulting in inconsisten colors and therefore failing sign and 
# path recognition

#defines
USE_PI_CAMERA = 1 #set this to 1 to use the camera, else some stream or file can be used as input

#include dependencies
from Debugging.Debug  import logToAll
import time
import cv2

#################################################################
# Initialize the camera                                         #
# Our camera is mounted upside down and is therefore flipped    #
# NOTE the rg and bg values! These should be set because of     #
# the disabled auto white balance (awb) and should be           #
# determined using calibration. Use the provided calibration    #
# tool which can be found at: Raspberry/scripts/whitebalance.py #
#################################################################
if USE_PI_CAMERA==1:
  from picamera.array import PiRGBArray
  from picamera import PiCamera
  camera = PiCamera()
  camera.resolution = (640, 480)
  camera.awb_mode = 'off'
  camera.exposure_mode = 'auto'
  camera.hflip = True
  camera.vflip = True
  
  #USE CALIBRATION TO SET THESE VALUES
  rg, bg = (1.5, 1.5)
  camera.awb_gains = (rg, bg)
  
  camera.framerate = 8
  rawCapture = PiRGBArray(camera, size=(640, 480))

# Give the camera some time to initialize  
time.sleep(0.1)

#functions

#Get a new frame and split the image in 2 parts
# The top part will be used for sign recognition
# The bottom part will be used for line detection
def getFrame():
  t1 = time.time() 
  for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = (frame.array)
    image = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    top = image[120:360,0:640]
    bottom = image[250:480,0:640]
    rawCapture.truncate(0)
    t2 = time.time()
    logToAll("getFrame ; Get Frame ;  "+ str(float(t2-t1)) + " seconds",0)
    return [top,bottom]