# Name
# Description

#defines
INJECT = 0
USE_PI_CAMERA = 1
SHOW_VIDEO = 0

#include dependencies
from Debugging.Debug  import logToAll
  
import time

if INJECT==0:
  import cv2
  import numpy as np
  import imutils

import argparse
import random
import os.path
import time

#variables

#functions
# initialize the camera and grab a reference to the raw camera capture  

BlueLower = (100, 86, 6)
BlueUpper = (125, 255, 255)

RedLower = (170, 136, 130)
RedUpper = (190, 255, 255)

YellowLower = (10, 130, 130)
YellowUpper = (15, 255, 255)

fileName =  __file__.replace("SignDetection.pyc","").replace("SignDetection.py","")

if INJECT==0:
  left_nor = cv2.imread(fileName+"/left_nor.png",0)
  stop_nor = cv2.imread(fileName+"/stop_nor.png",0)
  uturn_nor = cv2.imread(fileName+"/uturn_nor.png",0)
  right_nor = cv2.imread(fileName+"/right_nor.png",0)
  straight_nor = cv2.imread(fileName+"/straight_nor.png",0)
  circle_and = cv2.imread(fileName+"/circle_and.png",0)

# allow the camera to warmup
time.sleep(0.1)

def findSigns(frame):
  logToAll("findSigns ; Find Signs ; ",2)
  
  t1 = time.time()
  
  if INJECT==1:
    rnd = random.randint(0,10)
    if rnd == 0:
      logToAll("findSigns ; stop ; ",3)
      time.sleep(0.01)
      return 1
    elif rnd == 1:
      logToAll("findSigns ; left ; ",3)
      time.sleep(0.01)
      return 2
    elif rnd == 2:
      logToAll("findSigns ; right ; ",3)
      time.sleep(0.01)
      return 3
    elif rnd == 3:
      logToAll("findSigns ; straight ; ",3)
      time.sleep(0.01)
      return 4
    elif rnd == 4:
      logToAll("findSigns ; uturn ; ",3)
      time.sleep(0.01)
      return 5
    else:
      logToAll("findSigns ; none ; ",3)
      time.sleep(0.01)
      return 0
  
  elif USE_PI_CAMERA==1:
  
    stri = colordetection2(frame) 
    t2 = time.time()
    logToAll("findSigns ; Find Signs time ;  "+ str(float(t2-t1)) + " seconds",0)
      
    logToAll("findSigns ; Find Signs time ;  "+ str(stri) + " found",0)
      
    if (stri)=="stop":
      return 1
    else:
      return 0
      
      
  else:
    videos = ['/left.mp4', '/right.mp4', '/straight.mp4', '/stop.mp4', '/uturn.mp4']
    for video in videos:
      vid = cv2.VideoCapture(fileName+video)
      key = cv2.waitKey(1) & 0xFF
      while True:
        (grabbed, image) = vid.read() ##TROEP
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
          break
        stri = colordetection2(image)
        print(str(stri))
    vid.release()
    cv2.destroyAllWindows()
    
  t2 = time.time()
  
  logToAll("findSigns ; Find Signs time ;  "+ float(t2-t1) + " seconds",2)
  
  return "ok"
    
#calls


def colordetection2(frame):

  str = "none"
  image = frame
  #image = image[120:360,0:640]
  #hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

  #hsv = imutils.resize(hsv, width=600)
  hsv = cv2.GaussianBlur(image, (11, 11), 0)
  

 
  # construct a mask for the color "green", then perform
  # a series of dilations and erosions to remove any small
  # blobs left in the mask
  mask1 = cv2.inRange(hsv, RedLower, RedUpper)
  mask_red = cv2.dilate(mask1, None, iterations=10)   #multiple dilations/erosions due to STOP-word implying 2 blobs
  mask_red = cv2.erode(mask_red, None, iterations=10)
  mask2 = cv2.inRange(hsv, BlueLower, BlueUpper)
  mask3 = cv2.inRange(hsv, YellowLower, YellowUpper)
  
  mask = mask_red | mask2 | mask3
  mask = cv2.dilate(mask, None, iterations=3)
  mask = cv2.erode(mask, None, iterations=3)


  if SHOW_VIDEO:
     cv2.imshow("asdf1", mask)
  key = cv2.waitKey(1) & 0xFF    
  
    # find contours in the mask and initialize the current
# (x, y) center of the ball
  cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)[-2]
  center = None

  # only proceed if at least one contour was found
  if len(cnts) > 0:
    # find the largest contour in the mask, then use
    # it to compute the minimum enclosing circle and
    # centroid  q
#    c = max(cnts, key=cv2.contourArea)
    #find largests contours
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:3]
    for c in cnts:
    
      area = cv2.contourArea(c)
      #print area
      if area > 2000.0:
        #peri = cv2.arcLength(c, True)
        #approx = cv2.approxPolyDP(c, 0.20 * peri, True)
#        cv2.drawContours(image, approx, -1, (0, 255, 0), 3)
        x,y,w,h = cv2.boundingRect(c)
        #(x,y),radius = cv2.minEnclosingCircle(approx)
        #radius = int(radius)
        #center = (int(x),int(y))
        
#        print('radius is',radius, 'x is',x, 'y is',y)
#        cv2.circle(image,center,radius,(255,255,255),2)
#        yr = int(y-radius)
#        xr = int(x-radius)
#        yr2 = int(y+radius)
#        xr2 = int(x+radius)
#        y = int (y)
#        x = int (x)
      
        yr = y
        xr = x
        yr2 = y + h
        xr2 = x + w


        if yr < 0:  
          yr = 0
        if xr < 0:
          xr = 0
        if yr2 > 480:    ##possibly redundant
          yr2 = 480
        if xr2 > 640:
          xr2 = 640
          
#          print('yr is',yr, 'xr is',xr, 'yr2 is',yr2, 'xr2 is', xr2)
          
#          roi = image[yr:yr2,xr:xr2]
        color = ""
        roi = mask2[yr:yr2,xr:xr2]
       # print cv2.countNonZero(roi)
        if cv2.countNonZero(roi) > 250:
          color = "blue"
        else:
          roi = mask1[yr:yr2,xr:xr2]
          
        if color == "":
          if cv2.countNonZero(roi) > 200:
            color = "red"
          else:
            roi = mask3[yr:yr2,xr:xr2]
          
        if color == "":
          if cv2.countNonZero(roi) > 200:
            color = "yellow"
          else:
            color = "nothing"
            continue
          
        
 #       roi3 = mask3[yr:yr2,xr:xr2]
 #       if cv2.countNonZero(roi2) > 250:
 #         color = "blue"
 #       elif cv2.countNonZero(roi1) > 200:
 #         color = "red"
 #       elif cv2.countNonZero(roi3) > 200:
 #         color = "yellow"
 #       else:
 #         color = "nothing"
 #         continue
        ##ADD PRIORITY BASED ON RADIUS
  #        roi = image[50:200,50:100]
  #        cv2.imwrite("derp.png", roi)
        #roi = cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
       # _, roi = cv2.threshold(roi,127,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
  #      roi = cv2.Canny(roi,80,150,apertureSize = 3) 
        roi= cv2.resize(roi,(int(250),int(250)))
        
        white = -1
        i = -1
        str = ""
        result = stop_nor
        if color == "red":
          result = cv2.bitwise_xor(roi,stop_nor)
          white2 = cv2.countNonZero(result)
          #print white2
      
          if  white2 < 22000:
            white = white2
            i = 0
            str="stop"
        
        elif color == "blue":
          #print radius
          #check if approx circle:
          check = cv2.bitwise_and(roi,circle_and)
          white_check = cv2.countNonZero(check)
          print white_check
          if white_check < 4000:        #threshold for circle check
            result = cv2.bitwise_xor(roi,right_nor)
            white2 = cv2.countNonZero(result)
            if white2 < 24000:            #threshold for arrowcheck
              white = white2
              i = 1
              str="right"
            
              result = cv2.bitwise_xor(roi,straight_nor)
              white2 = cv2.countNonZero(result)
              if white2 < white:
                white = white2
                i = 2
                str="straight"
                #print white2
                
              result = cv2.bitwise_xor(roi,left_nor)
              white2 = cv2.countNonZero(result)
              if white2 < white:
                i = 3
                str="left"
                #print white2
          
        elif color == "yellow":  
          result = cv2.bitwise_xor(roi,uturn_nor)
          white2 = cv2.countNonZero(result)
          if white2 > 4000 and white2 < 41000: #TODO: DEFINE THRESHOLD FOR YELLOW
            white = white2
            i = 4
            str="uturn"
      
        cv2.putText(image, str+repr(white), (x,y),cv2.FONT_HERSHEY_SIMPLEX,1,0xffff, 3)
        
        print (str)
      
  return str  
