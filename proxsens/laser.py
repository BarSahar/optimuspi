import time
import picamera
import picamera.array
import cv2
import numpy as np
import math
import distConst

#Calibration Constants 

#DistConsts = np.loadtxt()

#Calibration
def getLaserDistArr():
    with picamera.PiCamera() as camera:
        with picamera.array.PiRGBArray(camera) as stream:
            camera.capture(stream, format='bgr')
            image = stream.array
            num = (image[...,...,1] > 200)
            y_vals = [0] * 640
            for i in range(200,400) :
                y_vals[i] = abs(np.nanmedian(num[:,i].nonzero())-240)
            dist = abs(y_vals - 240) # distance of dot from center y_axis only
	        #save the dists of all..... stuff
        camera.close()
    return y_vals
'''
isCalibrated = False

#CalcDistCalibration
with picamera.PiCamera() as camera:
    with picamera.array.PiRGBArray(camera) as stream:
        x = input("system ready")
        camera.capture(stream, format='bgr')
        image = stream.array
        num = (image[...,...,1] > 200)
        y_vals = [0] * 640
        for i in range(640) :
            y_vals[i] = abs(np.median(num[:,i].nonzero())-240)
        dist = abs(y_vals - 240) # distance of dot from center y_axis only
        pixelDist = [0] * 640

        for i in range(640) :
            if DistConsts[i] != 0 :
                pixelDist[i] = y_vals[i]*DistConsts[i].Slope + DistConsts[i].Intercept
            y_vals[i] = abs(np.median(num[:,i].nonzero())-240)        

        
	    # work out distance using D = h/tan(theta)

	    #theta =0.0011450*dist + 0.0154
	    #tan_theta = math.tan(theta)

		#if tan_theta > 0: # bit of error checking
		#obj_dist =  int(5.33 / tan_theta)

	    #print "\033[12;0H" + "the dot is " + str(obj_dist) + "cm  away"s
'''