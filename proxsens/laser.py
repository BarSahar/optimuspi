import time
import picamera
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

def getPicture():
   with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.capture('foo.jpg')
        camera.close()

def storePic():
    GPIO.setmode(GPIO.BCM)
    R1 = 18 # RELAY PIN	
    GPIO.setup(R1,GPIO.OUT)
    GPIO.output(R1, True) # laser on
    image = getPicture()
    GPIO.output(R1, False) # laser off