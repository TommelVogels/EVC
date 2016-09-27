# PathRecognition.py
# This file is used to convert a video frame to information about the path

#defines
USE_PI_CAMERA = 1           #set this to 1 to use the camera, else some stream or file can be used as input
SHOW_VIDEO = 0              #define if the program shows the user a frame with information about the path recognition
TilesLower = (0,0,20)       #lower threshold (hue, saturation, value) used for filtering useful data from the frame
TilesUpper = (255,255,100)  #upper threshold (hue, saturation, value) used for filtering useful data from the frame

#include dependencies
import cv2
import numpy 
import math
from Debugging.Debug  import logToAll

#include dependencies
from Debugging.Debug  import logToAll
import random
import time

#variables
destination = 0
current = 0

#functions

def findPath(frame): # Is this even used?
  t1 = time.time()
  stri = hough(frame)
  t2 = time.time()
  return stri

#From all the lines that are found by the houghline function we would like to 
#substract the most interesting one at the right (if present)
#Please see the documentation 
def findClosestRightLineAngle(lines, middle):
  for x in range(0, len(lines)):
    x1=lines[x][0]
    y1=lines[x][1]
    x2=lines[x][2]
    y2=lines[x][3]
    if (x1>=middle or x2>=middle) and x1!=x2  and abs(y2-y1)>20:
      if y1>50 or y2>50:
        if ((x2-x1)**2+(y2-y1)**2)**0.5>0:
          angle = math.atan(float((y2-y1))/float((x2-x1)))*(180/numpy.pi)
          if ((x2-x1)>=0 and (y2-y1)>=0) or ((x2-x1)<0 and (y2-y1)<0):
            angle=angle
          elif (y2-y1)<0 and (x2-x1)>=0:
            angle=180+angle
          return [x1,y1,x2,y2,angle]
  return [0,0,0,0,1000]

#From all the lines that are found by the houghline function we would like to 
#substract the most interesting horizontal one (if present)
#Please see the documentation 
def findHorizontalLine(lines):
  lineData = [0,0,0,0,1000000]
  maxY=0
  for x in range(0, len(lines)):
    x1=lines[x][0]
    y1=lines[x][1]
    x2=lines[x][2]
    y2=lines[x][3]
    if x1!=x2  and abs(y2-y1)<20:
      if y1>0 or y2>0:
        if ((x2-x1)**2+(y2-y1)**2)**0.5>0:
          if maxY<y2:
           maxY=y2
           lineData = [x1,y1,x2,y2,240-y2]
          if maxY<y1:
           maxY=y1
           lineData = [x1,y1,x2,y2,240-y1]
  return lineData

# Get the distance to the right line
def findClosestRightLineDistance(lines, middle):
  for x in range(0, len(lines)):
    x1=lines[x][0]
    y1=lines[x][1]
    x2=lines[x][2]
    y2=lines[x][3]
    if (x1>=middle or x2>=middle) and x1!=x2 and abs(y2-y1)>20:
      if y1>50 or y2>50:
        if ((x2-x1)**2+(y2-y1)**2)**0.5>0:
          p1=numpy.array([x1,y1])
          p2=numpy.array([x2,y2])
          p3=numpy.array([-100000,80])
          p4=numpy.array([100000,80])
          x=seg_intersect(p1,p2,p3,p4)
          c=numpy.polyfit([x1,y1],[x2,y2],1)
          x=x[0]-320
          return [x1,y1,x2,y2,x]
  return [0,0,0,0,1000000]

# Get the angle of the left line
def findClosestLeftLineAngle(lines, middle):
  for x in range(len(lines)-1, 0, -1):
    x1=lines[x][0]
    y1=lines[x][1]
    x2=lines[x][2]
    y2=lines[x][3]
    if (x1<=middle or x2<=middle) and x1!=x2 and abs(y2-y1)>20:
      if y1>50 or y2>50:
        if ((x2-x1)**2+(y2-y1)**2)**0.5>0:
          angle = math.atan(float((y2-y1))/float((x2-x1)))*(180/numpy.pi)
          if ((x2-x1)>=0 and (y2-y1)>=0) or ((x2-x1)<0 and (y2-y1)<0):
            angle=angle
          elif (y2-y1)<0 and (x2-x1)>=0:
            angle=180+angle
          return [x1,y1,x2,y2,angle]
  return [0,0,0,0,1000]

# Get the distance to the left line
def findClosestLeftLineDistance(lines, middle):
  for x in range(len(lines)-1, 0, -1):
    x1=lines[x][0]
    y1=lines[x][1]
    x2=lines[x][2]
    y2=lines[x][3]
    if (x1<=middle or x2<=middle) and x1!=x2  and abs(y2-y1)>20:
      if y1>50 or y2>50:
        if ((x2-x1)**2+(y2-y1)**2)**0.5>0:
          p1=numpy.array([x1,y1])
          p2=numpy.array([x2,y2])
          p3=numpy.array([-100000,80])
          p4=numpy.array([100000,80])
          x=seg_intersect(p1,p2,p3,p4)
          c=numpy.polyfit([x1,y1],[x2,y2],1)
          x=320-x[0]
          return [x1,y1,x2,y2,x]
  return [0,0,0,0,1000000]   

def perp( a ) :
    b = numpy.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b

# line segment a given by endpoints a1, a2
# line segment b given by endpoints b1, b2
# return 
def seg_intersect(a1,a2, b1,b2) :
    da = a2-a1
    db = b2-b1
    dp = a1-b1
    dap = perp(da)
    denom = numpy.dot( dap, db)
    num = numpy.dot( dap, dp )
    return (num / denom.astype(float))*db + b1     

def sortBy(item):
  return item[0]
    
def hough(frame):
    if SHOW_VIDEO:
      image = frame.copy()
    else: 
      image = frame

    mask_tiles = cv2.inRange(image, TilesLower, TilesUpper)

    mask = cv2.erode(mask_tiles, None, iterations=2)
    mask = cv2.medianBlur(mask,9)
    mask = cv2.dilate(mask, None, iterations=2)
    edges = cv2.Canny(mask,50,150,apertureSize = 3)
    
    if SHOW_VIDEO:
        cv2.imshow("Frame", mask_tiles)
    key = cv2.waitKey(1) & 0xFF
    
    lines = cv2.HoughLinesP(edges,4,numpy.pi/180,50,1,75,30) #(edges,1,2*numpy.pi/180,120,90,1)
    
    RightDistance=[0,0,0,0,1000000]
    RightAngle=[0,0,0,0,0]
    LeftDistance=[0,0,0,0,1000000]
    LeftAngle=[0,0,0,0,0]
    b=[0,0,0,0,0]
    horizontalLine=[0,0,0,0,1000000]
    
    lines2 = []
    
    if lines is not None:
      ignorelist = []
      
      for x in range(0, len(lines)):
       lines2.append(lines[x][0])
       
      
      lines2 = sorted(lines2, key=sortBy, reverse=False)

      RightDistance=findClosestRightLineDistance(lines2, 640/2)
      RightAngle=findClosestRightLineAngle(lines2, 640/2)
      
      LeftDistance=findClosestLeftLineDistance(lines2, 640/2)
      LeftAngle=findClosestLeftLineAngle(lines2, 640/2)
      
      horizontalLine = findHorizontalLine(lines2)
      
      if RightAngle[4]>90 or RightAngle[4]==0:
       #angle greater than 90 drop
       print("Dropping Right Line")
       RightDistance[4]=1000000
      
      if LeftAngle[4]<90  or LeftAngle[4]==0:
       #left angle less than 90 drop
       print("Dropping Left Line")
       LeftDistance[4]=1000000
      
      if SHOW_VIDEO:
        cv2.line(image,(RightDistance[0],RightDistance[1]),(RightDistance[2],RightDistance[3]),(0,255,0),5)
        cv2.line(image,(LeftDistance[0],LeftDistance[1]),(LeftDistance[2],LeftDistance[3]),(255,0,0),5)
        cv2.line(image,(horizontalLine[0],horizontalLine[1]),(horizontalLine[2],horizontalLine[3]),(255,255,0),5)
        cv2.line(image,(0,80),(640,80),(255,0,0),5)
      
        for x in range(0, len(lines2)):
          x1=lines2[x][0]
          y1=lines2[x][1]
          x2=lines2[x][2]
          y2=lines2[x][3]

          cv2.line(image,(x1,y1),(x2,y2),(0,0,255),2)

    if SHOW_VIDEO:
      cv2.imshow('frame',image)
    cv2.waitKey(1)

    return {"RightLine":[RightDistance[0],RightDistance[1],RightDistance[2],RightDistance[3],RightDistance[4],RightAngle[4]],"LeftLine":[LeftDistance[0],LeftDistance[1],LeftDistance[2],LeftDistance[3],LeftDistance[4],LeftAngle[4]],"horizontalLine":[horizontalLine[0],horizontalLine[1],horizontalLine[2],horizontalLine[3],horizontalLine[4]]}
  
def setup_trackbars(range_filter):
    cv2.namedWindow("Trackbars", 0)

    for i in ["MIN", "MAX"]:
        v = 0 if i == "MIN" else 255

        for j in range_filter:
            cv2.createTrackbar("%s_%s" % (j, i), "Trackbars", v, 255, callback)
      
def get_trackbar_values(range_filter):
    values = []

    for i in ["MIN", "MAX"]:
        for j in range_filter:
            v = cv2.getTrackbarPos("%s_%s" % (j, i), "Trackbars")
            values.append(v)

    return values
  
def callback(value):
    pass
  
def thresholds():
  setup_trackbars("HSV")
  
  for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    image = image[120:360,0:640]

    # grab the current frame
    hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    v1_min, v2_min, v3_min, v1_max, v2_max, v3_max = get_trackbar_values("HSV")
    thresh = cv2.inRange(hsv, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))
    
    rawCapture.truncate(0)

  cv2.destroyAllWindows()
  return 