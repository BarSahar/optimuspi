from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
from numpy import *
import math
 
#variables
loop = 1
dot_dist = 0

#vc = cv2.VideoCapture(0)

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

#if vc.isOpened(): # try to get the first frame
#    rval, frame = vc.read()
 
#else:
#    rval = False
#    #print "failed to open Camera"
 
#if rval == 1 :
while loop == 1:
 #rval, frame = vc.read()
 frame = rawCapture
 #key = cv2.waitKey(20)
 #if key == 27: # exit on ESC
 #    loop = 0
 num = (frame[...,...,1] > 236)
 xy_val =  num.nonzero()
 
 y_val = median(xy_val[0])
 #x_val = median(xy_val[1])
            
 print (xy_val)
 input("Press Enter to continue...")
            
 #dist = ((x_val - 320)**2 + (y_val - 240)**2 )**0.5 # distance of dot from center pixel
 dist = abs(y_val - 240) # distance of dot from center y_axis only
 
 print " dist from center pixel is " + str(dist)
 
 # work out distance using D = h/tan(theta)
 
 theta =0.0011450*dist + 0.0154
 tan_theta = math.tan(theta)
 
 if tan_theta > 0: # bit of error checking
  obj_dist =  int(5.33 / tan_theta)
 
  print "\033[12;0H" + "the dot is " + str(obj_dist) + "cm  away"
#elif rval == 0:
#        print " webcam error "
