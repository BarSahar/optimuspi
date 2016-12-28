import RPi.GPIO as GPIO
import time
import datetime
import threading 
from threading import Thread
from robotModels import direction 
import picamera
import picamera.array
import numpy as np
import compass
from math import tan

GPIO.setwarnings(False)
con=threading.Condition()
stoper=0
myCompass = compass.compass()
HeadingAngle=0
cosmos=(direction.north,direction.west,direction.south,direction.east) 
dir=0
GPIO.setmode(GPIO.BCM)
GPIO.setup(21,GPIO.IN)
GPIO.setup(20,GPIO.IN)
counterleft=0
counterright=0
counterleft_limit=0
counterright_limit=0
TRIG_pin = 23
ECHO_pin = 22

def getProxDist():
    GPIO.setmode(GPIO.BCM)
    TRIG = 23
    ECHO = 22
    GPIO.setup(TRIG_pin,GPIO.OUT)
    GPIO.setup(ECHO_pin,GPIO.IN)
    GPIO.output(TRIG_pin, False)

    distance1=measureProx()
    #time.sleep(0.1)
    distance2=measureProx()
    #time.sleep(0.1)
    distance3=measureProx()
    return (distance1 + distance2 + distance3)/3
     

def measureProx():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG_pin,GPIO.OUT)
    GPIO.setup(ECHO_pin,GPIO.IN)
    GPIO.output(TRIG_pin, False)

    GPIO.output(TRIG_pin, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_pin, False)
    while GPIO.input(ECHO_pin)==0:
        pulse_start = time.time()
    while GPIO.input(ECHO_pin)==1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return distance

def stop():
    GPIO.setmode(GPIO.BCM)
    A1 = 26
    A2 = 27
    B1 = 24
    B2 = 25
    GPIO.setup(A1,GPIO.OUT)
    GPIO.setup(A2,GPIO.OUT)
    GPIO.setup(B1,GPIO.OUT)
    GPIO.setup(B2,GPIO.OUT)
    GPIO.output(A1, 0)
    GPIO.output(A2, 0)
    GPIO.output(B1, 0)
    GPIO.output(B2, 0)
    return
def addleft(channel):
	global counterleft,con
	counterleft+=1
#    print("left: " + str(counterleft))
	if counterleft>=counterleft_limit:
		GPIO.setmode(GPIO.BCM)
		GPIO.output(26,False)
		GPIO.output(27,False)
		con.acquire()
		#print ("left finito")
		#print (datetime.datetime.now()-stoper)
		con.notify()
		con.release()
		GPIO.remove_event_detect(channel)

def addright(channel):
    global counterright,con
    counterright+=1
    thisAng = myCompass.heading()
    #print ("right: " + str(counterright))
    if (counterright>=counterright_limit) or abs(thisAng-HeadingAngle)>1:
        GPIO.setmode(GPIO.BCM)
        GPIO.output(24,False)
        GPIO.output(25,False)
        con.acquire()
        con.notify()
        #print ("right finito")
        #print (datetime.datetime.now()-stoper)
        con.release()
        GPIO.remove_event_detect(channel)

def loopgetDist():
	while True:
		print (getDist())
		 
def turnright():
	global counterright_limit
	global counterleft_limit
	global dir
	globalinit();
	counterright_limit=80
	counterleft_limit=80
	goright()
	dir=(dir+1)%4

def goright():
	global counterleft
	global counterright
	global con
	GPIO.setmode(GPIO.BCM)
	A1=26
	A2=27
	B1=24
	B2=25
	GPIO.setup(A1,GPIO.OUT)
	GPIO.setup(A2,GPIO.OUT)
	GPIO.setup(B1,GPIO.OUT)
	GPIO.setup(B2,GPIO.OUT)
	GPIO.output(A1, False)
	GPIO.output(A2, True)
	GPIO.output(B1, True)
	GPIO.output(B2, False)
	GPIO.add_event_detect(21,GPIO.RISING,callback=addright)
	GPIO.add_event_detect(20,GPIO.RISING,callback=addleft)
	con.acquire()
	while True:
		con.wait()
#		print "counters in turn: left "+str(counterleft)+" right"+str(counterright)
		if counterleft>=counterleft_limit  and counterright>=counterright_limit:
			break
	con.release()


def turnleft():
	global counterright_limit
	global counterleft_limit
	global dir
	globalinit()
	counterright_limit=80
	counterleft_limit=80
	dir=(dir-1)%4

#ONLY USE AFTER SETTING COUNTER LIMITS!!!
def goleft():
	global counterleft
	global counterright
	global con
	GPIO.setmode(GPIO.BCM)
	A1=26
	A2=27
	B1=24
	B2=25
	GPIO.setup(A1,GPIO.OUT)
	GPIO.setup(A2,GPIO.OUT)
	GPIO.setup(B1,GPIO.OUT)
	GPIO.setup(B2,GPIO.OUT)
	GPIO.output(A1, True)
	GPIO.output(A2, False)
	GPIO.output(B1, False)
	GPIO.output(B2, True)
	GPIO.add_event_detect(21,GPIO.RISING,callback=addright)
	GPIO.add_event_detect(20,GPIO.RISING,callback=addleft)
	con.acquire()
	while True:
		con.wait()
#		print "counters in turn: left "+str(counterleft)+" right"+str(counterright)
		if counterleft>=counterleft_limit  and counterright>=counterright_limit:
			break
	con.release()


def moveForward():
    global counterleft
    global counterright
    global con
    global counterright_limit
    global counterleft_limit
    global stoper
    global HeadingAngle
    globalinit()
    counterright_limit=100
    counterleft_limit=100
    GPIO.setmode(GPIO.BCM)
    GPIO.add_event_detect(21,GPIO.RISING,callback=addright)
    GPIO.add_event_detect(20,GPIO.RISING,callback=addleft)
    A1 = 26
    A2 = 27
    B1 = 24
    B2 = 25
    GPIO.setup(A1,GPIO.OUT)
    GPIO.setup(A2,GPIO.OUT)
    GPIO.setup(B1,GPIO.OUT)
    GPIO.setup(B2,GPIO.OUT)
    stoper=datetime.datetime.now()
    HeadingAngle = myCompass.heading()
    GPIO.output(A1, False)
    GPIO.output(A2, True)
    GPIO.output(B1, False)
    GPIO.output(B2, True)
    con.acquire()
    while True:
        con.wait()
        #if abs(myCompass.heading()-HeadingAngle)>1:
        #    stop()            
        #    fixAngle(HeadingAngle)
        if counterleft>=counterleft_limit and counterright>=counterright_limit:
            break
        con.release()

def fixAngle(destAngle):
    #going left is negative angle    
    #variables
    global counterleft
    global counterright
    global counterleft_limit
    global counterright_limit
    GPIO.setmode(GPIO.BCM)
    A1=26
    A2=27
    B1=24
    B2=25
    GPIO.setup(A1,GPIO.OUT)
    GPIO.setup(A2,GPIO.OUT)
    GPIO.setup(B1,GPIO.OUT)
    GPIO.setup(B2,GPIO.OUT)

    #save previous counter state
    old_counterleft=counterleft
    old_counterright=counterright
    old_counterleft_limit=counterleft_limit
    old_counterright_limit=counterright_limit

    #reset counters
    counterleft =0
    counterright =0
    currAngle = myCompass.heading()
    #TODO FIX AREA AROUND 0
    while abs(currAngle-destAngle)>1:
        counterleft_limit = 1
        counterright_limit = 1
        if currAngle-destAngle>0 :
            goright()
        else :
            goleft()
        currAngle = myCompass.heading()

    #restore previous counter state
    counterleft = old_counterleft
    counterright = old_counterright
    counterleft_limit = old_counterleft_limit
    counterright_limit = old_counterright_limit

def turnsens():
	GPIO.add_event_detect(21,GPIO.RISING,callback=addright)
	GPIO.add_event_detect(20,GPIO.RISING,callback=addleft)
	globalinit()
	global counterright_limit
	global counterleft_limit
	counterleft_limit=1000
	counterright_limit=1000
def globalinit():
	global counterleft
	global counterright
	global counterright_limit
	global counterleft_limit
	counterleft=0
	counterright=0
	counterleft_limit=0
	counterright_limit=0
def turn360():
	for x in range(4):
		turnleft()
		time.sleep(1)


def move30cm():    
	global counterleft
	global counterright
	global con
	global counterright_limit
	global counterleft_limit
	global stoper
	globalinit()
	counterright_limit=200
	counterleft_limit=200
	GPIO.setmode(GPIO.BCM)
	GPIO.add_event_detect(21,GPIO.RISING,callback=addright)
	GPIO.add_event_detect(20,GPIO.RISING,callback=addleft)
	A1 = 26
	A2 = 27
	B1 = 24
	B2 = 25
	GPIO.setup(A1,GPIO.OUT)
	GPIO.setup(A2,GPIO.OUT)
	GPIO.setup(B1,GPIO.OUT)
	GPIO.setup(B2,GPIO.OUT)
	stoper=datetime.datetime.now()
	GPIO.output(A1, False)
	GPIO.output(A2, True)
	GPIO.output(B1, False)
	GPIO.output(B2, True)
	con.acquire()
	while True:
	 con.wait()
	 if counterleft>=counterleft_limit and counterright>=counterright_limit:
	  break
	con.release()


LaserSlope=0.001852056
LaserInters=-0.018442568


def getPicture():
	with picamera.PiCamera() as camera:
		with picamera.array.PiRGBArray(camera) as stream:
			camera.resolution=(640,480)
			time.sleep(0.5)
			camera.capture(stream, format='rgb') #take a photo
			image = stream.array
		camera.close()
	return image

def getLaserDist():
    GPIO.setmode(GPIO.BCM)
    R1 = 18 # RELAY PIN	
    GPIO.setup(R1,GPIO.OUT)
    GPIO.output(R1, True) # laser on
    image = getPicture()
    GPIO.output(R1, False) #laser off
    num = (image[...,...,1] > 254)
    xy_val = num.nonzero()
    y_val = np.median(xy_val[0])
    dist = abs(y_val - 240)
    print (str(dist))
    theta = LaserSlope*dist+LaserInters
    tan_theta = tan(theta)
    obj_dist =  int(5.0 / tan_theta)
    return obj_dist


def main():
	#turnsens()
	#turnleft()
	#turn360()
	#moveForward()
	#movenone()
	#print "end forward"
	#time.sleep(3)
	#print "after sleep"
	#turnleft()
	#stop()
	#cali()
	print (str(getProxDist()))
	#move30cm()
	#loopgetDist()
	while True:
	 pass

#main()