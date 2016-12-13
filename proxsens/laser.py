import time
import picamera
import picamera.array
import cv2
import numpy as np
import math
 
#variables

with picamera.PiCamera() as camera:
 with picamera.array.PiRGBArray(camera) as stream:
  camera.capture(stream, format='bgr')
  image = stream.array
  num = (image[...,...,1] > 50)
  print "num matrix is " + str(num)
  xy_val =  num.nonzero()
  print "@@@@@@@@@@@@@@@@@@@@@"
  print "num non zero is " + str(xy_val)
  y_val = median(xy_val[0])
  print "@@@@@@@@@@@@@@@@@@@@@"
  print "y values are " + str(y_val)
  
  while True:
   pass
  
  x_val = median(xy_val[1])
 
  #dist = ((x_val - 320)**2 + (y_val - 240)**2 )**0.5 # distance of dot from center pixel
  dist = abs(x_val - 320) # distance of dot from center x_axis only
 
  print " dist from center pixel is " + str(dist)
 
  # work out distance using D = h/tan(theta)
 
  theta =0.0011450*dist + 0.0154
  tan_theta = math.tan(theta)
 
  if tan_theta > 0: # bit of error checking
   obj_dist =  int(5.33 / tan_theta)
 
  print "\033[12;0H" + "the dot is " + str(obj_dist) + "cm  away"
