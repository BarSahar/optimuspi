import time
import picamera
import picamera.array
import cv2
import numpy as np
import math
from scipy import stats
import RPi.GPIO as GPIO
from proxsens import move30cm 
from robotModels import DistConst
GPIO.setwarnings(False)

slope=0.000923485


inters=-0.074563241



def dotlaster():
	with picamera.PiCamera() as camera:
		with picamera.array.PiRGBArray(camera) as stream:
			camera.resolution=(640,280)
			camera.capture(stream, format='rgb') #take a photo
			image = stream.array
			num = (image[...,...,1] > 255)
			xy_val =  num.nonzero()
			y_val = np.median(xy_val[0])
			dist = abs(y_val - 240)
			
			print (str(dist))
			'''
			theta=slope*dist+inters
			tan_theta = math.tan(theta)
			obj_dist =  int(5.0 / tan_theta)
			print ("the dot is " + str(obj_dist) + "cm  away")

			camera.close()'''



def main():
	GPIO.setmode(GPIO.BCM)
	R1 = 18 # RELAY PIN	
	GPIO.setup(R1,GPIO.OUT)
	GPIO.output(R1, True) # laser on

	dotlaster()
	GPIO.output(R1, False) #laser off


main()

while True:
	pass