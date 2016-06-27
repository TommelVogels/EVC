from picamera.array import PiRGBArray
from picamera import PiCamera
#import picamera.array
#from skimage import morphology
import time
import cv2
import numpy as np
import imutils
import argparse
#from matplotlib import pyplot as plt


def hough(avg1):

  

  image = frame.array
  image = image[240:480,0:640]
  cv2.accumulateWeighted(image,avg1,0.1)   
  res1 = cv2.convertScaleAbs(avg1)
  
  image = image - res1
  #gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
  #image2 = cv2.threshold(image, 0, 255, 0)
  image2 = cv2.Canny(image,50,150,apertureSize = 3)
  
  #fgmask = fgbg.apply(image)
  gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
  edges = cv2.Canny(gray,50,150,apertureSize = 3)
  lines = cv2.HoughLines(edges,1,np.pi/180,200,80)

  if lines is not None:
    for x in range(0,len(lines)):
      for rho,theta in lines[x]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0+1000*(-b))
        y1 = int(y0+1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0-1000*(a))
        
        cv2.line(image,(x1,y1),(x2,y2),(0,0,255),2)
  return res1
  
def contours():
  image = frame.array
  gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
  #gray = cv2.bilateralFilter(gray,11,17,17) #blur
  edges = cv2.Canny(gray,50,150)
  (_, contours, _) = cv2.findContours(edges.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
  #contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10] #prune amount of contours, may be nice
  cv2.drawContours(image, contours, -1, (0, 255, 0), 3)
  return image
  
def circles():
  imgleft = cv2.imread('left.jpg',1) #2k*2k
  imgleft = cv2.cvtColor(imgleft,cv2.COLOR_BGR2GRAY)
  #imgleft = cv2.Canny(imgleft,50,150,apertureSize = 3)


  image = frame.array
  gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
  gray = cv2.GaussianBlur( gray, (5, 5), 0 )
#  edges = cv2.Canny(gray,50,150,apertureSize = 3)
#  edges = cv2.Laplacian(gray,cv2.CV_8U)
#  edges = cv2.Sobel(gray,cv2.CV_8U,1,0,ksize=5)  
  copy = image.copy()
  circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1.5,50,3,200,100,20, 200) #hough_gradient, resolution(performance),mindistance,max amount of circles,?, circle precision(higher is more precise),minsize,maxsize
  
  if circles is not None:
  # convert the (x, y) coordinates and radius of the circles to integers
    circles = np.round(circles[0, :]).astype("int")
 
  # loop over the (x, y) coordinates and radius of the circles
    for (x, y, r) in circles:
      # draw the circle in the output image, then draw a rectangle
      # corresponding to the center of the circle
      cv2.circle(image, (x, y), r, (0, 255, 0), 4)
      cv2.rectangle(image, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
      

      roi = gray[y-r:y+r,x-r:x+r]
#      roi= cv2.resize(roi,(int(2000),int(2000)))

      cv2.imwrite("derp.png", roi)
      
            
      #roi = cv2.Canny(roi,50,150,apertureSize = 3)
  
  
  
      hist1 = cv2.calcHist([imgleft],[0],None,[256],[0,256])
      hist2 = cv2.calcHist([roi],[0],None,[256],[0,256])
  
      compare = cv2.compareHist(hist1, hist2, 1)  
      
      print compare
      
      
      
      
  return image
  
  
def robotcircles():
#IMAGE READING/FILTER
  imgleft = cv2.imread('left_small.jpg',1) #2k*2k
  imgleft = cv2.GaussianBlur( imgleft, (5, 5), 0 )
  imgleft = cv2.cvtColor(imgleft,cv2.COLOR_BGR2GRAY)
  ret,th1 = cv2.threshold(imgleft,127,255,0)
  (_, contours, _) = cv2.findContours(th1.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
  
#  imgleft = cv2.Canny(imgleft,50,150,apertureSize = 3)

  image = frame.array    
  image2 = np.array(image)  #CHANGE METHOD OF CONVERSION?
  image2[image2 >= 150] = 255
  image2[image2 < 80]=0
  

#  n = 2    # Number of levels of quantization
#
#  indices = np.arange(0,256)   # List of all colors 
#
#  divider = np.linspace(0,255,n+1)[1] # we get a divider
#
#  quantiz = np.int0(np.linspace(0,255,n)) # we get quantization colors
#
#  color_levels = np.clip(np.int0(indices/divider),0,n-1) # color levels 0,1,2..
#
#  palette = quantiz[color_levels] # Creating the palette
#
#  im2 = palette[image]  # Applying palette on image
#
#  image = cv2.convertScaleAbs(im2) # Converting image back to uint8

  gray = cv2.cvtColor(image2,cv2.COLOR_BGR2GRAY)
  gray = cv2.GaussianBlur( gray, (5, 5), 0 )
#  gray = cv2.equalizeHist(gray)
#  ret,th2 = cv2.threshold(gray,127,255,0)
  

#  equ = cv2.equalizeHist(img)

  edges = cv2.Canny(gray,50,150,apertureSize = 3)
#  edges = cv2.Laplacian(gray,cv2.CV_8U)
#  edges = cv2.Sobel(gray,cv2.CV_8U,1,0,ksize=5)
#  print "kak"

  (_, contours, _) = cv2.findContours(edges.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
  contours = sorted(contours, key = cv2.contourArea, reverse = True)[:20] #prune amount of contours, may be nice
  
  for contour in contours:
#    approxRect = cv2.approxPolyDP(contour, cv2.arcLength(contour, True)*0.05, True)
    
    
#    if approxRect.size == 4:
    area = cv2.contourArea(contour)
    if area > 10000.0:
      cv2.drawContours(image, contour, -1, (0, 255, 0), 3)
      (x,y),radius = cv2.minEnclosingCircle(contour)
      radius = int(radius)
      center = (int(x),int(y))
      cv2.circle(image,center,radius,(255,255,255),2)
      #print area
      
      roi = edges[y-radius:y+radius,x-radius:x+radius]
      roi= cv2.resize(roi,(int(256),int(256)))  #RESIZE TO x,ySIZE
      cv2.imwrite("derp.png", roi)
#      hist1 = cv2.calcHist([imgleft],[0],None,[256],[0,256])
#      hist2 = cv2.calcHist([roi],[0],None,[256],[0,256])
    
#      compare = cv2.compareHist(hist1, hist2, 1)  
      
#      print compare
      
      
  return edges  
  
def testfetchcontours():
#IMAGE READING/FILTER
  image = cv2.imread('left_small.jpg',1) #256x256?
#  imgleft = cv2.GaussianBlur( image, (5, 5), 0 )
  imgleft = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
  ret,thresh = cv2.threshold(imgleft,127,255,0)
#  canny = cv2.Canny(th1,80,150,apertureSize = 3) 
  (_, contours, _) = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #SIMPLE vs NONE: show key, or all contourpoints
  contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10] #prune amount of contours, may be nice
  
  for contour in contours:
  #  approxRect = cv2.approxPolyDP(contour, cv2.arcLength(contour, True)*0.05, True)
    
    
  #  if approxRect.size == 4:
#    area = cv2.contourArea(contour)
#    if area > 100.0:
    cv2.drawContours(image, contour, -1, (0, 255, 0), 3)
    (x,y),radius = cv2.minEnclosingCircle(contour)
    radius = int(radius)
    center = (int(x),int(y))
      #cv2.circle(image,center,radius,(255,255,255),2)
      #print area
      
      
    
    cv2.imshow("derp", image)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
      break
    
    image2 = frame.array
      
  return image2
  
def colordetection():

  image = frame.array
  

  boundaries = [
    ([17, 15, 50], [70, 70, 250]),
    ([15, 50, 15], [70, 250, 70]),
    ([40, 15, 15], [250, 100, 100]),
#    ([103, 86, 65], [145, 133, 128])
]

  for (lower, upper) in boundaries:
    lower = np.array(lower,dtype ="uint8")
    upper = np.array(upper, dtype = "uint8")
    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask = mask)
    
    cv2.imshow("images", np.hstack([image, output]))
    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    if key == ord("q"):
      break

  return image
  
  
def colordetection2():
  image = frame.array
  image = image[120:360,0:640]
  hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

  #hsv = imutils.resize(hsv, width=600)
  hsv = cv2.GaussianBlur(hsv, (11, 11), 0)
 
  # construct a mask for the colors, then perform
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
      if area > 1000.0:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.20 * peri, True)
#        cv2.drawContours(image, approx, -1, (0, 255, 0), 3)
        (x,y),radius = cv2.minEnclosingCircle(approx)
        radius = int(radius)
#        center = (int(x),int(y))
        
#        print('radius is',radius, 'x is',x, 'y is',y)
#        cv2.circle(image,center,radius,(255,255,255),2)
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
        if yr2 > 480:    ##possibly redundant
          yr2 = 480
        if xr2 > 640:
          xr2 = 640
          
#        print('yr is',yr, 'xr is',xr, 'yr2 is',yr2, 'xr2 is', xr2)
        
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
#          roi = image[50:200,50:100]
#          cv2.imwrite("derp.png", roi)
        roi = cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
        _, roi = cv2.threshold(roi,127,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
#        roi = cv2.Canny(roi,80,150,apertureSize = 3) 
        roi= cv2.resize(roi,(int(250),int(250)))
        
        result = [0,0,0,0,0]
        white = -1
        i = -1
        str = ""
        if color == "red":
          result[0] = cv2.bitwise_and(roi,stop_and)
          white2 = cv2.countNonZero(result[0])
#          print "red"
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
        
        #print (i)
        
        
        
        cv2.imshow("derp", roi)
        key = cv2.waitKey(1000) & 0xFF
        
        
    
    
  #    ((x, y), radius) = cv2.minEnclosingCircle(c)
  #    M = cv2.moments(c)
  #    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
  #
  #    # only proceed if the radius meets a minimum size
  #    if radius > 50:
  #      # draw the circle and centroid on the frame,
  #      # then update the list of tracked points
  #      cv2.circle(image, (int(x), int(y)), int(radius),
  #        (0, 255, 255), 2)
  #      cv2.circle(image, center, 5, (0, 0, 255), -1)
  
  # update the points queue
#  pts.appendleft(center)
  
#  if i == -1:
#    return roi
#  else:
#    return result[i]
  return image
  
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
  image = frame.array
  hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
  v1_min, v2_min, v3_min, v1_max, v2_max, v3_max = get_trackbar_values("HSV")
  thresh = cv2.inRange(hsv, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))
    #cv2.imshow("Original", image)
  cv2.imshow("Thresh", thresh)
  return image

  
def colordetection_video():
  camera = cv2.VideoCapture("video.h264.640.MKV")
  while True:
  # grab the current frame
    (grabbed, image) = camera.read()
 
    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if not grabbed:
      print("not grabbed")
      break
    image = imutils.resize(image, width=480)
    hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    #hsv = imutils.resize(hsv, width=480)
    #hsv = cv2.GaussianBlur(hsv, (11, 11), 0)
  
    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask1 = cv2.inRange(hsv, RedLower, RedUpper)
    mask2 = cv2.inRange(hsv, BlueLower, BlueUpper)
    mask3 = cv2.inRange(hsv, YellowLower, YellowUpper)
    
    mask = mask1 | mask2 | mask3
    mask = cv2.erode(mask, None, iterations=4)
    mask = cv2.dilate(mask, None, iterations=4)
  
    
      # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
      cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
  
    # only proceed if at least one contour was found
    if len(cnts) > 0:
      # find the largest contour in the mask, then use
      # it to compute the minimum enclosing circle and
      # centroid    
      #c = max(cnts, key=cv2.contourArea)
      #find largests contours
      cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:3]
      for c in cnts:
      
        area = cv2.contourArea(c)
        if area > 1000.0:
          cv2.drawContours(image, c, -1, (0, 255, 0), 3)
          (x,y),radius = cv2.minEnclosingCircle(c)
          radius = int(radius)
          center = (int(x),int(y))
          cv2.circle(image,center,radius,(255,255,255),2)  

    cv2.imshow('frame',image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
  
  camera.release()
  cv2.destroyAllWindows()

  return
  
def surf():
  
  surf = cv2.xfeatures2d.SURF_create(400)
  imgleft = cv2.imread('left_small.jpg',1) #256x256?
  imgleft = cv2.GaussianBlur( imgleft, (5, 5), 0 )
  imgleft = cv2.cvtColor(imgleft,cv2.COLOR_BGR2GRAY)
  
  kp1, des1 = surf.detectAndCompute(imgleft,None)
  image = frame.array
  image = cv2.GaussianBlur( image, (5, 5), 0 )
  image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
#  surf.upright = True

  kp2, des2 = surf.detectAndCompute(image,None)

  
  FLANN_INDEX_KDTREE = 0
#  index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
#  search_params = dict(checks=50)   # or pass empty dictionary
  
#  flann = cv2.FlannBasedMatcher(index_params,search_params)
  
#  matches = flann.knnMatch(des1,des2,k=2)

  bf = cv2.BFMatcher()
  matches = bf.knnMatch(des1, des2, k=2)
  
  # Need to draw only good matches, so create a mask
  matchesMask = [[0,0] for i in xrange(len(matches))]
  
  # ratio test as per Lowe's paper
  for i,(m,n) in enumerate(matches):
    if m.distance < 0.7*n.distance:
      matchesMask[i]=[1,0]
  
  draw_params = dict(matchColor = (0,255,0),
          singlePointColor = (255,0,0),
          matchesMask = matchesMask,
          flags = 0)
  
  img3 = cv2.drawMatchesKnn(imgleft,kp1,image,kp2,matches,None,**draw_params)
    
  return img3
  
  
  
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
#camera.iso = 200
camera.awb_mode = 'off'
camera.exposure_mode = 'auto'


rg, bg = (1.3, 1.8)
camera.awb_gains = (rg, bg)
      
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
#fgbg = cv2.createBackgroundSubtractorMOG()

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
setup_trackbars("HSV")

#colordetection_video()
 
# capture frames from the camera
x = 0

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
  
  if not x:
    tstimage = frame.array
    tstimage = tstimage[240:480,0:640]
    avg1 = np.float32(tstimage) 
    x = 1
  
#  image = hough(avg1)
#  image = contours()
#  image = circles()
#  image = robotcircles()
#  image = testfetchcontours()
#  image = colordetection()
#  image = surf()
#  image = colordetection2()
  image = thresholds()
  
  # grab the raw NumPy array representing the image, then initialize the timestamp    
#  lines = cv2.HoughLinesP(edges, 1, np.pi / 4, 2, None, 10, 1)
#  lines = cv2.HoughLinesP(edges,1,np.pi/180,10,150,10)

#  if lines is not None:
#    for x in range(0, len(lines)):
#      for x1,y1,x2,y2 in lines[x]:
#        cv2.line(image,(x1,y1),(x2,y2),(0,255,0),2)
#
  
  #lines = cv2.HoughLinesP(edges, 1, np.pi/180,100,50,100)
#  lines = cv2.HoughLinesP(edges, 1, np.pi/360, 50, 30, 100)
#
#  for line in lines[0]:
#    pt1 = (line[0],line[1])
#    pt2 = (line[2],line[3])
#    cv2.line(image, pt1, pt2, (0,0,255), 2)
  
#  lines = cv2.HoughLines(edges, 1, np.pi/6,1)
#  

  
#  img = frame.array
#  img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#  
#  size = np.size(img)
#  skel = np.zeros(img.shape,np.uint8)
#   
#  ret,img = cv2.threshold(img,127,255,0)
#  element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
#  done = False
   
#  while( not done):
#    eroded = cv2.erode(img,element)
#    temp = cv2.dilate(eroded,element)
#    temp = cv2.subtract(img,temp)
#    skel = cv2.bitwise_or(skel,temp)
#    img = eroded.copy()
#   
#    zeros = size - cv2.countNonZero(img)
#    if zeros==size:
#      done = True
  
#  im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
#  im = cv2.threshold(im, 0, 255, 0)
#  im = morphology.skeletonize(im > 0)

  
#  gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
#  edges = cv2.Canny(gray,50,150,apertureSize = 3)
#  
#  lines = cv2.HoughLines(edges,1,np.pi/180,75)
#
#  if lines is not None:
#    for x in range(0,len(lines)):
#      for rho,theta in lines[x]:
#        a = np.cos(theta)
#        b = np.sin(theta)
#        x0 = a*rho
#        y0 = b*rho
#        x1 = int(x0+1000*(-b))
#        y1 = int(y0+1000*(a))
#        x2 = int(x0 - 1000*(-b))
#        y2 = int(y0-1000*(a))
#        
#        cv2.line(image,(x1,y1),(x2,y2),(0,0,255),2)
  # show the frame
  #roi = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)

  
  cv2.imshow("Frame", image)
  key = cv2.waitKey(1) & 0xFF
 
  # clear the stream in preparation for the next frame
  rawCapture.truncate(0)
 
  # if the `q` key was pressed, break from the loop
  if key == ord("q"):
    break