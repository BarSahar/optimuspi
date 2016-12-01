import RPi.GPIO as GPIO
import time

def getDist():
    #{
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
    return distance;
    #}

def moveForward():
    #{
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
    return;
    #}

def stop():
    #{
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
    return;
    #}

#if getDist()<20:
#    print "HERE WE GO!!!!!!"
#    moveForward()
#    while (getDist() <20):
#        print "STILL ROLLING!"
#    stop()
#    print "tired"
#stop()
#print "lost it"##

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(21,GPIO.IN)
    while True:
        print GPIO.input(21)

    print "end"

