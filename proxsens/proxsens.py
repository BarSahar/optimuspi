import RPi.GPIO as GPIO
import time
import datetime
import threading 
from threading import Thread
GPIO.setwarnings(False)

con=threading.Condition()



cosmos=(1,2,-1,-2) #1=y,2=x
dir=0

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
def addleft(channel):
	global counterleft,con
	counterleft+=1
	print "left counter "+ str(counterleft)
	if counterleft>=counterleft_limit:
		GPIO.setmode(GPIO.BCM)
		GPIO.output(26,False)
		GPIO.output(27,False)
		con.acquire()
		print "notify left "+str(counterleft)
		con.notify()
		con.release()
		GPIO.remove_event_detect(channel)
def turnright():
	global counterleft
	global counterright
	global con
	global counterright_limit
	global counterleft_limit
	global dir
	globalinit();

	counterright_limit=58
	counterleft_limit=58

	GPIO.setmode(GPIO.BCM)
	A1 = 26
	A2 = 27
	B1 = 24
	B2 = 25
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
	 if counterleft>=counterleft_limit and counterright>=counterright_limit:
	  break
	con.release()
	dir=(dir+1)%4

	    
def turnleft():
	global counterleft
	global counterright
	global con
	global counterright_limit
	global counterleft_limit
	global dir
	globalinit()
	counterright_limit=56
	counterleft_limit=56
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
		print "Sleep"
		con.wait()
		print "counters in turn: left "+str(counterleft)+" right"+str(counterright)
		if counterleft>=counterleft_limit  and counterright>=counterright_limit:
			break
	counterleft=0
	counterright=0
	con.release()
	dir=(dir-1)%4
def addright(channel):
	global counterright,con
	counterright+=1
	print "right counter: "+str(counterright)
	if counterright>=counterright_limit:
		GPIO.setmode(GPIO.BCM)
		GPIO.output(24,False)
		GPIO.output(25,False)
		con.acquire()
		con.notify()
		print "notify right"+str(counterright)
		con.release()
		GPIO.remove_event_detect(channel)

def moveForward():
	global counterleft
	global counterright
	global con
	global counterright_limit
	global counterleft_limit
	globalinit()
	counterright_limit=110
	counterleft_limit=110
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
	GPIO.output(A1, False)
	GPIO.output(A2, True)
	GPIO.output(B1, False)
	GPIO.output(B2, True)
	con.acquire()
	while True:
	 con.wait()
	 print "wait left "+str(counterleft)+" right: "+str(counterright)
	 if counterleft>=counterleft_limit and counterright>=counterright_limit:
	  break
	con.release()
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
	for x in range(0,4):
		time.sleep(1)
		turnleft()
		



def main():
	#turnsens()
	#turnleft()
	#turn360()
	moveForward()
	#print "end forward"
	#time.sleep(3)
	#print "after sleep"
	#turnleft()
	#stop()
	while True:
	 pass



main()	