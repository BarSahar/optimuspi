﻿import RPi.GPIO as GPIO
import time
import datetime
import threading 
from threading import Thread
GPIO.setwarnings(False)

con=threading.Condition()



GPIO.setmode(GPIO.BCM)
GPIO.setup(21,GPIO.IN)
GPIO.setup(20,GPIO.IN)
GPIO.setup(19,GPIO.IN)

counterleft=0
counterright=0
counterleft_limit=0
counterright_limit=0

def getDist():
    GPIO.setmode(GPIO.BCM)
    TRIG = 23
    ECHO = 22
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    GPIO.output(TRIG, False)
    time.sleep(1)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    while GPIO.input(ECHO)==0:
        pulse_start = time.time()
    while GPIO.input(ECHO)==1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return distance
def moveForward():
    #{
    global counterright_limit
    global counterleft_limit
    counterright_limit=100
    counterleft_limit=100
    GPIO.setmode(GPIO.BCM)
    A1 = 26
    A2 = 27
    B1 = 24
    B2 = 25
    GPIO.setup(A1,GPIO.OUT)
    GPIO.setup(A2,GPIO.OUT)
    GPIO.setup(B1,GPIO.OUT)
    GPIO.setup(B2,GPIO.OUT)
    GPIO.output(A1, False)
    GPIO.output(A2, True)
    GPIO.output(B1, False)
    GPIO.output(B2, True)
    #time.sleep(3)
    return
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
    GPIO.cleanup()
    return
def prtinter(channel):
    print "Right"+str(counterright)
    print "Left"+str(counterleft)
def addleft(channel):
	global counterleft,con
	counterleft+=1
	print str(counterleft)
	if counterleft==counterleft_limit:
		GPIO.setmode(GPIO.BCM)
		GPIO.output(26,False)
		GPIO.output(27,False)
		con.acquire()
		print "notify left"+str(counterleft)
		con.notify()
		con.release()
def turnright():
        GPIO.setmode(GPIO.BCM)
        A1 = 26
        A2 = 27
        B1 = 24
        B2 = 25
        GPIO.setup(A1,GPIO.OUT)
        GPIO.setup(A2,GPIO.OUT)
        GPIO.setup(B1,GPIO.OUT)
        GPIO.setup(B2,GPIO.OUT)
        print "Startng to turn"
        GPIO.output(A1, True)
        GPIO.output(A2, False)
        GPIO.output(B1, False)
        GPIO.output(B2, True)
        return    
def turnleft():
	global counterleft
	global counterright
	global con
	global counterright_limit
	global counterleft_limit
	counterright_limit=24
	counterleft_limit=24
	
	con.acquire()
	GPIO.setmode(GPIO.BCM)
	A1=26
	A2=27
	B1=24
	B2=25
	GPIO.setup(A1,GPIO.OUT)
	GPIO.setup(A2,GPIO.OUT)
	GPIO.setup(B1,GPIO.OUT)
	GPIO.setup(B2,GPIO.OUT)
	while True:
		print "Sleep"
		con.wait()
		print "counters in turn: left "+str(counterleft)+" right"+str(counterright)
		if counterleft>=counterright_limit and counterright>=counterleft_limit:
			print "pe"
			break
	
	counterleft=0
	counterright=0
	con.release()
def addright(channel):
	global counterright,con
	counterright+=1
	print str(counterright)
	if counterright==counterright_limit:
		GPIO.setmode(GPIO.BCM)
		GPIO.output(24,False)
		GPIO.output(25,False)
		con.acquire()
		con.notify()
		print "notify right"+str(counterright)
		con.release()

GPIO.add_event_detect(20,GPIO.RISING,callback=addleft)
GPIO.add_event_detect(21,GPIO.RISING,callback=addright)
GPIO.add_event_detect(19,GPIO.RISING,callback=prtinter)



#turnleft()
moveForward()
#stop()
print "Hello"
while True:
    pass
