# Name
# Description

#defines
USE_PI_CAMERA = 1

#include dependencies

#variables

#functions

def findPath():

if USE_PI_CAMERA==1:
  
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
      properline = hough(frame.array)
      rawCapture.truncate(0)
      print(str(stri))

#calls
    
  
def hough(frame):

    image = frame
    image = image[250:480,0:640]
    hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    hsv = cv2.GaussianBlur( hsv, (5, 5), 0 )
    mask_tiles = cv2.inRange(hsv, TilesLower, TilesUpper)
    
    mask = cv2.erode(mask_tiles, None, iterations=2)
    #mask = cv2.dilate(mask, None, iterations=2)
    edges = cv2.Canny(mask,50,150,apertureSize = 3)
    
    cv2.imshow("Frame", edges)
    key = cv2.waitKey(1) & 0xFF
    
    #lines = cv2.HoughLines(edges,1,np.pi/180,100)
    lines = cv2.HoughLinesP(edges,2,2*np.pi/180,50,1,120,5) #(edges,1,2*np.pi/180,120,90,1)
    
    if lines is not None:
    
      for x in range(0, len(lines)):
        for x1,y1,x2,y2 in lines[x]:
          cv2.line(image,(x1,y1),(x2,y2),(0,255,0),2) 
    
    

    
    cv2.imshow('frame',image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

  return properline