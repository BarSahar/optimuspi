import time
import picamera
import picamera.array
import cv2
import numpy as np
import math
from scipy import stats
import RPi.GPIO as GPIO
from proxsens import move30cm 
GPIO.setwarnings(False)

#global variables
DistConstArr = np.zeros(640)
distH = 5
initialD = 285
isCalibrated = False
#Calibration Constants 

#DistConsts = np.loadtxt()

#Calibration
def getLaserDistArr():
    with picamera.PiCamera() as camera:
        with picamera.array.PiRGBArray(camera) as stream:
            camera.capture(stream, format='bgr')
            image = stream.array
            num = (image[...,...,1] > 200)
            y_vals = [np.nan]*640
            for i in range(200,400) :
                x = num[:,i].nonzero()
                if len(x) != 0 :
                    y_vals[i] = abs(np.median(x)-240)
                    print(str(i))
	        #save the dists of all..... stuff
        camera.close()
    return y_vals

def cali():
    GPIO.setmode(GPIO.BCM)
    R1 = 18 # RELAY PIN	
    GPIO.setup(R1,GPIO.OUT)
    pixelDist = []
    theta = [initialD]*10 #instantaniates as D in cm, later converted to theta
    for x in range(10):
            GPIO.output(R1, True) # laser on
            pixelDist.append(getLaserDistArr())
            theta[x] = math.atan(distH/(theta[x]-30*x))
            GPIO.output(R1, False) #laser off
            print ("ended loop" + str(x))
            #move30cm()
            time.sleep(2)
    
    np_pixelDist = np.asarray(pixelDist)
    for i in range(200,400) :
        x = np_pixelDist[:,i]
        mask = ~np.isnane(x)
        slope, intercept = stats.linregress(x[mask],theta[mask])
        DistConstArr[i] = DistConst(slope,intercept)
    np.savetxt('consts.txt', DistConstArr)
    isCalibrated=True
##clac here

cali()


'''

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