import RPi.GPIO as GPIO
import time
import datetime
import threading 
from threading import Thread
from robotModels import direction,distanceerror,status
import picamera
import picamera.array
import operator as op
import numpy as np
import compass
from math import tan

GPIO.setwarnings(False)
con=threading.Condition()
stoper=0
myCompass = compass.compass()
HeadingAngle=0

cposition=(0,0)
def updateCposition():
	global cposition
#	print("current pos: "+str(cposition)+"+"+str(sens.cosmos[sens.dir].value))
	cposition=tuple(map(op.add, cposition,cosmos[dir].value))
	outlinenodes.append((cposition[0],cposition[1],status.clear))
	updateParam(cposition)


cosmos=(direction.north,direction.east,direction.south,direction.west) 
dir=1

def addleft(channel):
    global counterleft,con
    counterleft+=1
    #print("left: " + str(counterleft))
    if counterleft>=counterleft_limit:
        #GPIO.setmode(GPIO.BCM)
        GPIO.output(26,False)
        GPIO.output(27,False)
        con.acquire()
        #print ("left finito")
        #print (datetime.datetime.now()-stoper)
        con.notify()
        con.release()
        #GPIO.remove_event_detect(channel)

def addright(channel):
	global counterright,con
	counterright+=1
	thisAng = getCompRead()
	#print ("right: " + str(counterright))
	#or abs(thisAng-HeadingAngle)>1:
	if counterright>=counterright_limit or abs(thisAng-HeadingAngle)>4:
		#GPIO.setmode(GPIO.BCM)
		GPIO.output(24,False)
		GPIO.output(25,False)
		con.acquire()
		con.notify()
		#print ("right finito")
		#print (datetime.datetime.now()-stoper)
		con.release()
		#GPIO.remove_event_detect(channel)

GPIO.setmode(GPIO.BCM)
GPIO.setup(21,GPIO.IN)
GPIO.setup(20,GPIO.IN)
A1 = 26
A2 = 27
B1 = 24
B2 = 25
GPIO.setup(A1,GPIO.OUT)
GPIO.setup(A2,GPIO.OUT)
GPIO.setup(B1,GPIO.OUT)
GPIO.setup(B2,GPIO.OUT)
GPIO.add_event_detect(21,GPIO.RISING,callback=addright)
GPIO.add_event_detect(20,GPIO.RISING,callback=addleft)
counterleft=0
counterright=0
counterleft_limit=0
counterright_limit=0
TRIG_pin = 23
ECHO_pin = 22

def giverightdir():
	right=((dir+1)%4)
	return cosmos[right].value

def givebackdir():
	right=((dir+2)%4)
	return cosmos[right].value


def getProxDist():
    #GPIO.setmode(GPIO.BCM)
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
    #GPIO.setmode(GPIO.BCM)
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
    #GPIO.setmode(GPIO.BCM)
    #A1 = 26
    #A2 = 27
    #B1 = 24
    #B2 = 25
    #GPIO.setup(A1,GPIO.OUT)
    #GPIO.setup(A2,GPIO.OUT)
    #GPIO.setup(B1,GPIO.OUT)
    #GPIO.setup(B2,GPIO.OUT)
    GPIO.output(A1, False)
    GPIO.output(A2, False)
    GPIO.output(B1, False)
    GPIO.output(B2, False)
    #GPIO.remove_event_detect(21)
    #GPIO.remove_event_detect(20)
    return

def showoff(graph):
  line=""
  for x in range(len(graph)):
    for y in range(len(graph[0])):
      if graph[x][y]==status.clear:
        line=line+". "
      elif graph[x][y]==status.block:
          line=line+"x "
      else:
        line=line+"*"
    print(line)
    line=""


		 
def turnright():
    global counterright_limit
    global counterleft_limit
    global dir
    originalAngle = getCompRead()
    globalinit()
    counterright_limit=80
    counterleft_limit=80
    goright()
    print("finished. now fine tuning")
    #fixAngle((originalAngle+90)%360) #fine tuning
    dir=(dir+1)%4

#ONLY USE AFTER SETTING COUNTER LIMITS!!!
def goright():
    global counterleft
    global counterright
    global con
    #GPIO.setmode(GPIO.BCM)
    #A1=26
    #A2=27
    #B1=24
    #B2=25
    #GPIO.setup(A1,GPIO.OUT)
    #GPIO.setup(A2,GPIO.OUT)
    #GPIO.setup(B1,GPIO.OUT)
    #GPIO.setup(B2,GPIO.OUT)
    GPIO.output(A1, False)
    GPIO.output(A2, True)
    GPIO.output(B1, True)
    GPIO.output(B2, False)
    #GPIO.remove_event_detect(21)
    #GPIO.remove_event_detect(20)
    #GPIO.add_event_detect(21,GPIO.RISING,callback=addright)
    #GPIO.add_event_detect(20,GPIO.RISING,callback=addleft)
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
    originalAngle = getCompRead()
    globalinit()
    counterright_limit=80
    counterleft_limit=80
    goleft()
    fixAngle((originalAngle-90+360)%360) #fine tuning
    dir=(dir-1)%4

#ONLY USE AFTER SETTING COUNTER LIMITS!!!
def goleft():
    global counterleft
    global counterright
    global con
    #GPIO.setmode(GPIO.BCM)
    #A1=26
    #A2=27
    #B1=24
    #B2=25
    #GPIO.setup(A1,GPIO.OUT)
    #GPIO.setup(A2,GPIO.OUT)
    #GPIO.setup(B1,GPIO.OUT)
    #GPIO.setup(B2,GPIO.OUT)
    GPIO.output(A1, True)
    GPIO.output(A2, False)
    GPIO.output(B1, False)
    GPIO.output(B2, True)
    #GPIO.remove_event_detect(21)
    #GPIO.remove_event_detect(20)
    #GPIO.add_event_detect(21,GPIO.RISING,callback=addright)
    #GPIO.add_event_detect(20,GPIO.RISING,callback=addleft)
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
    #GPIO.setmode(GPIO.BCM)
    #GPIO.remove_event_detect(21)
    #GPIO.remove_event_detect(20)
    #GPIO.add_event_detect(21,GPIO.RISING,callback=addright)
    #GPIO.add_event_detect(20,GPIO.RISING,callback=addleft)
    #A1 = 26
    #A2 = 27
    #B1 = 24
    #B2 = 25
    #GPIO.setup(A1,GPIO.OUT)
    #GPIO.setup(A2,GPIO.OUT)
    #GPIO.setup(B1,GPIO.OUT)
    #GPIO.setup(B2,GPIO.OUT)
	#stoper=datetime.datetime.now()
    HeadingAngle = getCompRead()
    GPIO.output(A1, False)
    GPIO.output(A2, True)
    GPIO.output(B1, False)
    GPIO.output(B2, True)
    con.acquire()
    while True:
        con.wait()

        if abs(getCompRead()-HeadingAngle)>4:
            stop()
            print("stop and start fixAngle("+str(HeadingAngle) +")")
			#time.sleep(1)
			#print("now")
            fixAngle(HeadingAngle)
            print("finished turning")
            print("continue on")
            time.sleep(1)
            GPIO.output(A1, False)
            GPIO.output(A2, True)
            GPIO.output(B1, False)
            GPIO.output(B2, True)
        elif counterleft>=counterleft_limit and counterright>=counterright_limit:
            break
    con.release()
    updateCposition()

def fixAngle(destAngle):
    #going left is negative angle    
    #variables
    global counterleft
    global counterright
    global counterleft_limit
    global counterright_limit
    #GPIO.setmode(GPIO.BCM)
    #A1=26
    #A2=27
    #B1=24
    #B2=25
    #GPIO.setup(A1,GPIO.OUT)
    #GPIO.setup(A2,GPIO.OUT)
    #GPIO.setup(B1,GPIO.OUT)
    #GPIO.setup(B2,GPIO.OUT)

    #save previous counter state
    old_counterleft=counterleft
    old_counterright=counterright
    old_counterleft_limit=counterleft_limit
    old_counterright_limit=counterright_limit
    print("counter left : "+str(counterleft))
    print("counter right : "+str(counterright))
    print("counter left limit : "+str(counterleft_limit))
    print("counter right limit : "+str(counterright_limit))

    #reset counters
    counterleft =0
    counterright =0
    currAngle = getCompRead()
    
    while abs(currAngle-destAngle)>2:
        counterleft_limit = 1
        counterright_limit = 1
        #print("current: "+str(currAngle) + ". heading to: " + str(destAngle))
        if (currAngle-destAngle>0 and currAngle-destAngle<45)  or currAngle-destAngle<-45:
            #print("need to go left")
            goleft()
        else :
            #print("need to go right")
            goright()
        currAngle = getCompRead()
        time.sleep(0.1)
	#restore previous counter state
    counterleft = old_counterleft
    counterright = old_counterright
    counterleft_limit = old_counterleft_limit
    counterright_limit = old_counterright_limit
    print("finished turning")
    print("counter left : "+str(counterleft))
    print("counter right : "+str(counterright))
    print("counter left limit : "+str(counterleft_limit))
    print("counter right limit : "+str(counterright_limit))
    time.sleep(5)


def turnsens():
	#GPIO.add_event_detect(21,GPIO.RISING,callback=addright)
	#GPIO.add_event_detect(20,GPIO.RISING,callback=addleft)
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

#gets safe reading from compass
def getCompRead():
    while True:
        try:
            return myCompass.heading()
        except IOError as e:
            pass

LaserSlope=0.002043
LaserInters=-0.00257

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
	i=0
	dist1 = laserDistHelper()
	if dist1<200:
		return dist1
	else:
		dist2 = laserDistHelper()
		dist3 = laserDistHelper()
		res = min(dist1,dist2,dist3)
		while res==999 and i < 5:
			i=i+1
			res = laserDistHelper()
			if res <999:
				break
	if res==999:
		raise distanceerror()
	else:
		return res


def laserDistHelper():
	#GPIO.setmode(GPIO.BCM)
	R1 = 18 # RELAY PIN	
	GPIO.setup(R1,GPIO.OUT)
	GPIO.output(R1, True) # laser on
	image = getPicture()
	GPIO.output(R1, False) #laser off
	num = (image[...,...,1] > 254)
	xy_val = num.nonzero()
	if len(xy_val[0])==0:
		#   print("Error detecting dot")
		return 999
	#filter all indeces below horizon = reflections on the floor
	noiseFilterx1 = (xy_val[1][...]>250)
	noiseFilterx2 = (xy_val[1][...]<350)
	noiseFiltery1 = (xy_val[0][...]<270)
	noiseFiltery2 = (xy_val[0][...]>50)
	finalFilter = np.logical_and(np.logical_and(noiseFilterx1,noiseFilterx2),np.logical_and(noiseFiltery1,noiseFiltery2))
	y_val = np.median(xy_val[0][finalFilter])
	dist = abs(y_val - 240)
	#print ("pixel dist is" + str(dist))
	theta = LaserSlope*dist+LaserInters
	try:
		tan_theta = tan(theta)
		obj_dist =  int(5.0 / tan_theta)
		return obj_dist
	except:
		return 999

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