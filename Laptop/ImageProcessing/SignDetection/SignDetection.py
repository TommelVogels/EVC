# Name
# Description

#defines
USE_PI_CAMERA = 1


#include dependencies
from Debugging.Debug  import logToAll

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import imutils
import argparse

#variables

#functions
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
#camera.iso = 200
camera.awb_mode = 'off'
camera.exposure_mode = 'auto'

video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

rg, bg = (1.9, 1.2)
camera.awb_gains = (rg, bg)

camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

BlueLower = (100, 86, 6)
BlueUpper = (125, 255, 255)

RedLower = (170, 136, 130)
RedUpper = (190, 255, 255)

YellowLower = (10, 130, 130)
YellowUpper = (15, 255, 255)

left_and = cv2.imread("left_and.png",0)
stop_and = cv2.imread("stop_and.png",0)
uturn_and = cv2.imread("uturn_and.png",0)
right_and = cv2.imread("right_and.png",0)
straight_and = cv2.imread("straight_and.png",0)
 
# allow the camera to warmup
time.sleep(0.1)

def findSigns():
  logToAll("findSigns ; Find Signs ; ",2)
  
  for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):  
    stri = colordetection2(frame.array)
    rawCapture.truncate(0)
    print(str(stri))
    
  return "ok"
    
#calls


def colordetection2(frame):
	image = frame
	image = image[120:360,0:640]
	hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

	#hsv = imutils.resize(hsv, width=600)
	hsv = cv2.GaussianBlur(hsv, (11, 11), 0)
 
	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask1 = cv2.inRange(hsv, RedLower, RedUpper)
	mask2 = cv2.inRange(hsv, BlueLower, BlueUpper)
	mask3 = cv2.inRange(hsv, YellowLower, YellowUpper)
	
	mask = mask1 | mask2 | mask3
	mask = cv2.medianBlur(mask, 9)
	#mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=15)
	mask = cv2.erode(mask, None, iterations=15)
	
	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
 
	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid	q
#		c = max(cnts, key=cv2.contourArea)
		#find largests contours
		cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:3]
		for c in cnts:
			area = cv2.contourArea(c)
			if area > 1000.0:
				peri = cv2.arcLength(c, True)
				approx = cv2.approxPolyDP(c, 0.20 * peri, True)
#				cv2.drawContours(image, approx, -1, (0, 255, 0), 3)
				(x,y),radius = cv2.minEnclosingCircle(approx)
				radius = int(radius)
#				center = (int(x),int(y))
				
#				print('radius is',radius, 'x is',x, 'y is',y)
#				cv2.circle(image,center,radius,(255,255,255),2)
				yr = int(y-radius)
				xr = int(x-radius)
				yr2 = int(y+radius)
				xr2 = int(x+radius)
				y = int (y)
				x = int (x)
				if yr < 0:	
					yr = 0
				if xr < 0:
					xr = 0
				if yr2 > 480:		##possibly redundant
					yr2 = 480
				if xr2 > 640:
					xr2 = 640
					
#				print('yr is',yr, 'xr is',xr, 'yr2 is',yr2, 'xr2 is', xr2)
				
				roi = image[yr:yr2,xr:xr2]
				roi1 = mask1[yr:yr2,xr:xr2]
				roi2 = mask2[yr:yr2,xr:xr2]
				roi3 = mask3[yr:yr2,xr:xr2]
				if cv2.countNonZero(roi2) > 250:
					color = "blue"
				elif cv2.countNonZero(roi1) > 200:
					color = "red"
				elif cv2.countNonZero(roi3) > 200:
					color = "yellow"
				else:
					color = "nothing"
				##ADD PRIORITY BASED ON RADIUS
#					roi = image[50:200,50:100]
#					cv2.imwrite("derp.png", roi)
				roi = cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
				_, roi = cv2.threshold(roi,127,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
#				roi = cv2.Canny(roi,80,150,apertureSize = 3) 
				roi= cv2.resize(roi,(int(250),int(250)))
				
				result = [0,0,0,0,0]
				white = -1
				i = -1
				str = ""
				if color == "red":
					result[0] = cv2.bitwise_and(roi,stop_and)
					white2 = cv2.countNonZero(result[0])
#					print "red"
					if white2 > 11000 and white2 < 18832:
						white = white2
						i = 0
						str="stop"
				
				elif color == "blue":
					result[1] = cv2.bitwise_and(roi,right_and)
					white2 = cv2.countNonZero(result[1])
					if white2 > white and white2 > 6000 and white2 < 11018:
						white = white2
						i = 1
						str="right"
					
					result[2] = cv2.bitwise_and(roi,straight_and)
					white2 = cv2.countNonZero(result[2])
					if white2 > white and white2 > 6000 and white2 < 11097:
						white = white2
						i = 2
						str="straight"
						
					result[3] = cv2.bitwise_and(roi,left_and)
					white2 = cv2.countNonZero(result[3])
					if white2 > white and white2 > 6000 and white2 < 11016:
						white = white2
						i = 3
						str="left"
					
				elif color == "yellow":	
					result[4] = cv2.bitwise_and(roi,uturn_and)
					white2 = cv2.countNonZero(result[4])
					if white2 > white and white2 > 14500 and white2 < 20503:
						white = white2
						i = 4
						str="uturn"
				cv2.putText(image, str+repr(white), (x,y),cv2.FONT_HERSHEY_SIMPLEX,1,0xffff, 3)
				
				cv2.imshow("derp", roi)
				key = cv2.waitKey(1000) & 0xFF
				
	return str  
