import RPi.GPIO as GPIO
import time
import datetime
import threading
from threading import Thread
from robotModels import direction, distanceerror, status
import picamera
import picamera.array
import operator as op
import numpy as np
import compass
import compTest
from math import tan

# mypwm=GPIO.PWN(17,10)
# mypwn.start(50)


# region Globals
GPIO.setwarnings(False)
con = threading.Condition()
stoper = ""
# myCompass = compass.compass(declination=(4, 35))
myCompass = compTest.LSM9DS0()
HeadingAngle = -1

cposition = (0, 0)
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN)
GPIO.setup(20, GPIO.IN)
A1 = 26
A2 = 27
B1 = 24
B2 = 25
GPIO.setup(A1, GPIO.OUT)
GPIO.setup(A2, GPIO.OUT)
GPIO.setup(B1, GPIO.OUT)
GPIO.setup(B2, GPIO.OUT)

counterleft = 0
counterright = 0
counterleft_limit = 0
counterright_limit = 0
TRIG_pin = 23
ECHO_pin = 22

cosmos = (direction.north, direction.east, direction.south, direction.west)
dir = 1


# endregion

def updateCposition():
    global cposition
    #	print("current pos: "+str(cposition)+"+"+str(sens.cosmos[sens.dir].value))
    cposition = tuple(map(op.add, cposition, cosmos[dir].value))


def addleft(channel):
    global counterleft, con
    counterleft += 1
    # print("left: " + str(counterleft))
    # print(str(getCompRead()))
    if counterleft >= counterleft_limit:
        # GPIO.setmode(GPIO.BCM)
        GPIO.output(26, False)
        GPIO.output(27, False)
        con.acquire()
        # print ("left finito")
        # print (datetime.datetime.now()-stoper)
        con.notify()
        con.release()
        # GPIO.remove_event_detect(channel)


def addright(channel):
    global counterright, con
    counterright += 1
    # print ("right: " + str(counterright))
    # if counterright>=counterright_limit or (abs(thisAng-HeadingAngle)>4 and HeadingAngle!=-1):
    if counterright >= counterright_limit:
        # GPIO.setmode(GPIO.BCM)
        GPIO.output(24, False)
        GPIO.output(25, False)
        con.acquire()
        con.notify()
        # print ("right finito")
        # print (datetime.datetime.now()-stoper)
        con.release()
        # GPIO.remove_event_detect(channel)


GPIO.add_event_detect(21, GPIO.RISING, callback=addright)
GPIO.add_event_detect(20, GPIO.RISING, callback=addleft)


def giverightdir():
    right = ((dir + 1) % 4)
    return cosmos[right].value


def givebackdir():
    right = ((dir + 2) % 4)
    return cosmos[right].value


def getProxDist():
    # GPIO.setmode(GPIO.BCM)
    TRIG = 23
    ECHO = 22
    GPIO.setup(TRIG_pin, GPIO.OUT)
    GPIO.setup(ECHO_pin, GPIO.IN)
    GPIO.output(TRIG_pin, False)

    distance1 = measureProx()
    distance2 = measureProx()
    distance3 = measureProx()
    return (distance1 + distance2 + distance3) / 3


def measureProx():
    # GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG_pin, GPIO.OUT)
    GPIO.setup(ECHO_pin, GPIO.IN)
    GPIO.output(TRIG_pin, False)

    GPIO.output(TRIG_pin, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_pin, False)
    while GPIO.input(ECHO_pin) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO_pin) == 1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return distance


def stop():
    GPIO.output(A1, True)
    GPIO.output(A2, True)
    GPIO.output(B1, True)
    GPIO.output(B2, True)
    return


def showoff(graph):
    line = ""
    for x in range(len(graph)):
        for y in range(len(graph[0])):
            if graph[x][y] == status.clear:
                line = line + ". "
            elif graph[x][y] == status.block:
                line = line + "x "
            else:
                line = line + "* "
        print(line)
        line = ""

def showSavedGrap():
    grid = np.load('Grid.npy')
    showoff(grid)

def putWall():
    grid = np.load('Grid.npy')
    for y in range(0,7):
        grid[y][6]=status.block

    showoff(grid)

    np.save('Grid', grid)


def fill(graph):
    for x in range(2, 9):
        for y in range(2, 13):
            graph[x][y] = status.clear
    graph[5][5] = status.unexplored
    np.save('Home2.npy', graph)


def globalinit():
    global counterleft
    global counterright
    global counterright_limit
    global counterleft_limit
    counterleft = 0
    counterright = 0
    counterleft_limit = 0
    counterright_limit = 0


def turnright(x=77):
    # global counterright_limit
    # global counterleft_limit
    global dir
    # originalAngle = getCompRead()
    # globalinit()
    # counterright_limit = 50
    # counterleft_limit = 50
    # goright()
    # time.sleep(0.5)
    # fixAngle((originalAngle + 90) % 360)  # fine tuning
    dir = (dir + 1) % 4
    moveTicksL(x, "R")


# ONLY USE AFTER SETTING COUNTER LIMITS!!!
def goright():
    global counterleft
    global counterright
    global con
    GPIO.output(A1, False)
    GPIO.output(A2, True)
    GPIO.output(B1, True)
    GPIO.output(B2, False)
    con.acquire()
    while True:
        con.wait()
        if counterleft >= counterleft_limit and counterright >= counterright_limit:
            break
    con.release()


def turnleft(x=83):
    # global counterright_limit
    # global counterleft_limit
    global dir
    # originalAngle = getCompRead()
    # globalinit()
    # counterright_limit = 50
    # counterleft_limit = 50
    # goleft()
    # time.sleep(0.5)
    # fixAngle(((originalAngle - 90 + 360) % 360))  # fine tuning
    dir = (dir - 1) % 4

    moveTicksL(x, "L")





# ONLY USE AFTER SETTING COUNTER LIMITS!!!
def goleft():
    global counterleft
    global counterright
    global con
    GPIO.output(A1, True)
    GPIO.output(A2, False)
    GPIO.output(B1, False)
    GPIO.output(B2, True)
    con.acquire()
    while True:
        con.wait()
        if counterleft >= counterleft_limit and counterright >= counterright_limit:
            break
    con.release()


def moveForwardMicro():
    global counterleft
    global counterright
    global con
    global counterright_limit
    global counterleft_limit
    global stoper
    global HeadingAngle
    globalinit()
    counterright_limit = 50
    counterleft_limit = 45
    HeadingAngle = getCompRead()
    # print("HeadingAngle: " + str(HeadingAngle))
    GPIO.output(A1, False)
    GPIO.output(A2, True)
    GPIO.output(B1, False)
    GPIO.output(B2, True)
    con.acquire()
    while True:
        con.wait()
        if counterleft >= counterleft_limit and counterright >= counterright_limit:
            break
    con.release()
    time.sleep(0.1)
    fixAngle(HeadingAngle)
    HeadingAngle = -1


def moveForward():
    moveForwardMicro() #physically move forward
    updateCposition() #update current position


def fixAngle(destAngle): #function to fix position according to destAngle
    # going left is negative angle
    # variables
    global counterleft
    global counterright
    global counterleft_limit
    global counterright_limit

    # save previous counter state
    old_counterleft = counterleft
    old_counterright = counterright
    old_counterleft_limit = counterleft_limit
    old_counterright_limit = counterright_limit

    # reset counters
    currAngle = getCompRead()
    # print("currAngle: " + str(currAngle))
    # print("Delta: " + str(abs(currAngle - destAngle)))
    #    print("fixAngle::")
    #    print("destAngle: "+ str(destAngle))
    #    print("currAngle: " +str(currAngle))
    while abs(currAngle - destAngle) > 1:
        counterleft = 0
        counterright = 0
        counterleft_limit = 1
        counterright_limit = 1
        #        print("current: "+str(currAngle) + ". heading to: " + str(destAngle))
        if (currAngle - destAngle > 0 and currAngle - destAngle < 90) or currAngle - destAngle < -90:
            goleft()
        else:
            goright()
        time.sleep(0.1)
        currAngle = getCompRead()

    # restore previous counter state
    counterleft = old_counterleft
    counterright = old_counterright
    counterleft_limit = old_counterleft_limit
    counterright_limit = old_counterright_limit
    # print("angle after fix: " + str(getCompRead()))


def turnsens(): #function for testing hardware - not relevant
    # GPIO.add_event_detect(21,GPIO.RISING,callback=addright)
    # GPIO.add_event_detect(20,GPIO.RISING,callback=addleft)
    globalinit()
    global counterright_limit
    global counterleft_limit
    counterleft_limit = 1000
    counterright_limit = 1000


# gets safe reading from compass
def getCompRead():
    while True:
        try:
            one = myCompass.heading()
            time.sleep(0.01)
            two = myCompass.heading()
            time.sleep(0.01)
            three = myCompass.heading()

            return (one + two + three) / 3
        except IOError as e:
            pass


LaserSlope = 0.002043
LaserInters = -0.00257


def getPicture():
    with picamera.PiCamera() as camera:
        with picamera.array.PiRGBArray(camera) as stream:
            camera.resolution = (640, 480)
            time.sleep(0.5)
            camera.capture(stream, format='rgb')  # take a photo
            image = stream.array
        camera.close()
    return image


def getLaserDist(): #function to get distance from laser.
    i = 0
    dist1 = laserDistHelper() #inner function to get raw distance from laser.
    if dist1 < 200:
        return dist1 - 4 #compensate for side sensor which is 4 cm farther away
    else:
        dist2 = laserDistHelper()
        dist3 = laserDistHelper()
        res = min(dist1, dist2, dist3) #if dist is more than 2m, takes minimum of 3 readings
        while res == 999 and i < 5:
            i = i + 1
            res = laserDistHelper()
            if res < 999:
                break
    if res == 999:
        return 50
    else:
        return res - 4 #compensate for side sensor which is 4 cm farther away


def laserDistHelper():
    # GPIO.setmode(GPIO.BCM)
    R1 = 18  # RELAY PIN
    GPIO.setup(R1, GPIO.OUT)
    GPIO.output(R1, True)  # laser on
    image = getPicture()
    GPIO.output(R1, False)  # laser off
    num = (image[..., ..., 1] > 254) # only pixels that are bright green
    xy_val = num.nonzero()
    if len(xy_val[0]) == 0:
        #   print("Error detecting dot")
        return 999
    # filter all indeces below horizon - reflections on the floor
    noiseFilterx1 = (xy_val[1][...] > 250)
    noiseFilterx2 = (xy_val[1][...] < 350)
    # filter all indeces left and right father than 50 pixels from center - reflections from walls and shiny surfaces
    noiseFiltery1 = (xy_val[0][...] < 270)
    noiseFiltery2 = (xy_val[0][...] > 50)
    finalFilter = np.logical_and(np.logical_and(noiseFilterx1, noiseFilterx2),
                                 np.logical_and(noiseFiltery1, noiseFiltery2))
    y_val = np.median(xy_val[0][finalFilter]) #in case multiple pixels (big dot), median gets the middle of it
    dist = abs(y_val - 240)
    # print ("pixel dist is" + str(dist))
    theta = LaserSlope * dist + LaserInters
    try:
        tan_theta = tan(theta)
        obj_dist = int(5.0 / tan_theta)
        return obj_dist
    except:
        return 999

#def moveBunch(): #function for testing hardware - not relevant
#    tick = 0
#    for x in range(20):
#        moveForwardMicro()
#        print("step: " + str(tick) + " out of 20")
#        tick = tick + 1
#        time.sleep(0.5)
#        print(34 * "-")
#        x=input()


def moveTicksL(num, dir):
    for x in range(num):
        counterleft = 0
        counterright = 0
        counterleft_limit = 1
        counterright_limit = 1
        if dir == "R":
            goright()
        else:
            goleft()
        time.sleep(0.1)


#def newplan(): #function for testing hardware - not relevant
#    for x in range(4):
#        for x in range(5):
#            moveForwardMicro()
#            time.sleep(1)
#        turnleft()
