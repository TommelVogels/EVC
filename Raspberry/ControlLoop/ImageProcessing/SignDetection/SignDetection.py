# SignDetection.py
# This file is used to convert a frame to information about the signs

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

BlueLower = (100,86,85) ##BlueLower = (100, 86, 6)
BlueUpper = (125,164,255)##BlueUpper = (125, 255, 255)
##
RedLower = (158,100,67)
RedUpper = (191,255,255)
##RedLower = (170, 136, 130)
##RedUpper = (190, 255, 255)
##
YellowLower = (10,88,95)
YellowUpper= (20,255,255)
##YellowLower = (10, 130, 130)
##YellowUpper = (15, 255, 255)




fileName =  __file__.replace("SignDetection.pyc","").replace("SignDetection.py","")

if INJECT==0:
  left_xor = cv2.imread(fileName+"/left_xor.png",0)
  stop_xor = cv2.imread(fileName+"/stop_xor.png",0)
  uturn_xor = cv2.imread(fileName+"/uturn_xor.png",0)
  right_xor = cv2.imread(fileName+"/right_xor.png",0)
  straight_xor = cv2.imread(fileName+"/straight_xor.png",0)
  circle_and_100 = cv2.imread(fileName+"/circle_and_100.png",0)

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
  
    result = colordetection2(frame) 
    i = result[0]
    stri = result[1]
    coord = result[2]
    
    t2 = time.time()
    logToAll("findSigns ; Find Signs time ;  "+ str(float(t2-t1)) + " seconds",2)
      
    logToAll("findSigns ; Find Signs time ;  "+ str(stri) + " found",0)
      
    return[i, coord]
      
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
        #print(str(stri))
    vid.release()
    cv2.destroyAllWindows()
    
  t2 = time.time()
  
  logToAll("findSigns ; Find Signs time ;  "+ float(t2-t1) + " seconds",2)
  
  return "ok"
    
#calls


def colordetection2(frame):

  sign = "none"
  image = frame
  hsv = cv2.GaussianBlur(image, (11, 11), 0)

  # construct a mask for the color "green", then perform
  # a series of dilations and erosions to remove any small
  # blobs left in the mask
  mask1 = cv2.inRange(hsv, RedLower, RedUpper)
  mask2 = cv2.inRange(hsv, BlueLower, BlueUpper)
  mask12 = mask1 | mask2
  mask12 = cv2.dilate(mask12, None, iterations=10)   #multiple dilations/erosions due to STOP-word implying 2 blobs #same for blue
  mask12 = cv2.erode(mask12, None, iterations=10)
  mask3 = cv2.inRange(hsv, YellowLower, YellowUpper)
  
  mask = mask12 | mask3
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
  prval = False
  white2 = -1
  if len(cnts) > 0:
    # find the largest contour in the mask, then use
    # it to compute the minimum enclosing circle and
    # centroid  q
    # c = max(cnts, key=cv2.contourArea)
    # find largests contours, only the biggest and thus closest are of interest
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:3]
    color = ""
    h = -1
    i = 0
    for c in cnts:
      #only continue if the area is big enough
      area = cv2.contourArea(c)
      if area > 2000.0: 
        x,y,w,h = cv2.boundingRect(c)    
        yr = y      #bounding rectangle start y
        xr = x      #bounding rectangle start x 
        yr2 = y + h #bounding rectangle end y
        xr2 = x + w #bounding rectangle end x

        #Make sure the values are not outside the image
        if yr < 0:  
          yr = 0
        if xr < 0:
          xr = 0
        if yr2 > 480:
          yr2 = 480
        if xr2 > 640:
          xr2 = 640
       
        #cut out the region of interest (roi)
        roi = mask1[yr:yr2,xr:xr2]
        
        #Try to find the color of the ROI
        #The if-else-if-else constuction is to reduce
        #computations. The order of colors is dependent
        #on some properties of the pi camera
        if cv2.countNonZero(roi) > 1000:
          color = "red"
        else:
          roi = mask2[yr:yr2,xr:xr2]
          if cv2.countNonZero(roi) > 1000:
            color = "blue"
          else:
            roi = mask3[yr:yr2,xr:xr2] 
            if cv2.countNonZero(roi) > 1000:
              color = "yellow"
            else:
              color = "nothing"
              continue
        
        #resize the roi to reduce computation
        roi= cv2.resize(roi,(int(100),int(100)))
        
        if SHOW_VIDEO:
          cv2.imshow("roi", roi)
        
        #try to find the sign
        prval = False
        white = -1
        sign = ""
        result = stop_xor
        if color == "red":
          result = cv2.bitwise_xor(roi,stop_xor) #bitwise XOR the ROI and a black/white stop image
          white2 = cv2.countNonZero(result)      #count the white pixels
      
          #at least 70% of the image should match (is white) to consider the ROI to be a stop sign
          if  white2 < (0.7*5041): 
            prval = True
            white = white2
            i = 1
            sign="stop"
            break
        
        elif color == "blue":
          #first check if the ROI is round
          #This information is needed so that we can be more focussing on the inside of the sign later on
          #(check documentation)
          check = cv2.bitwise_and(roi,circle_and_100)
          white_check = cv2.countNonZero(check)
          if white_check < (0.3*2272):                 #threshold for circle check
          
            #The ROI is rezized to 100;100 before. Depending on if we had to scale up or scale down 
            #we choose a different algorithm. Scaling up means, next to the fact that the sign is far away,
            #the quality of will be a lot lower.
            if h >= 100: #The image is scaled down, choose less compute heavy algorithm
              result = cv2.bitwise_xor(roi,right_xor)  #bitwise XOR the ROI and a black/white right image 
              white2 = cv2.countNonZero(result)        #count the white pixels
              if white2 < 1500:                        #threshold for arrowcheck
                prval = True
                white = white2
                i = 3
                sign="right"
                break
                
              #continue if a sign hasn't been found yet
              if sign == "":
                result = cv2.bitwise_xor(roi,left_xor)
                white2 = cv2.countNonZero(result)
                if white2 < 1500:
                  prval = True
                  white = white2
                  i = 2
                  sign="left"
                  break
              
              #continue if a sign hasn't been found yet              
              if sign == "":
                result = cv2.bitwise_xor(roi,straight_xor)
                white2 = cv2.countNonZero(result)
                if white2 < 1500:
                  prval = True
                  white = white2
                  i = 4
                  sign="straight"
                  break
                  
            #The image is scaled up, compare all signs and return the one that resembles the b/w image most
            else:  
              result = cv2.bitwise_xor(roi,right_xor)                        
              white2 = cv2.countNonZero(result)
              white = white2
              sign = "right"
              i = 3
              
              result = cv2.bitwise_xor(roi,left_xor)
              white2 = cv2.countNonZero(result)
              if white2 < white:
                white = white2
                sign = "left"
                i = 2
                
              result = cv2.bitwise_xor(roi,straight_xor)
              white3 = cv2.countNonZero(result)
              if white2 < white:
                white = white2
                sign="straight"
                i = 4
              
              prval = True
              break
          
        elif color == "yellow":  
          result = cv2.bitwise_xor(roi,uturn_xor)
          white2 = cv2.countNonZero(result)
          if white2 < (0.7*6772):
            prval = True
            white = white2
            i = 5
            sign="uturn"
            break

    if SHOW_VIDEO:
      if prval:
        cv2.putText(image, color+":"+sign+":"+str(h)+":"+str(white2), (x,y),cv2.FONT_HERSHEY_SIMPLEX,1,0xffff, 3)
      cv2.imshow("kak", image)
      
    
  if prval:
    return [i, sign, [x+(0.5*w), y+(0.5*h),h]]
  else:
    return [0, "", [0,0,0]]
