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
        num = (image[...,...,1] > 200)
        xy_val =  num.nonzero()
        y_val = median(xy_val[0])
        print "y values are " + str(y_val)
 
        dist = abs(y_val - 240) # distance of dot from center y_axis only
        #save the dists of all..... stuff
        np.savetxt('yvals', y_val , delimiter=',')
        np.savetxt('dists1', dist , delimiter=',')
        print " dist from center pixel is " + str(dist)
 
        # work out distance using D = h/tan(theta)
 
        #theta =0.0011450*dist + 0.0154
        #tan_theta = math.tan(theta)
 
        #if tan_theta > 0: # bit of error checking
        #    obj_dist =  int(5.33 / tan_theta)
 
        #print "\033[12;0H" + "the dot is " + str(obj_dist) + "cm  away"
