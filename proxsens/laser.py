

import RPi.GPIO as GPIO
GPIO.setwarnings(False)

LaserSlope=0.002126104
LaserInters=0.009691016

def getPicture():
    with picamera.PiCamera() as camera:
        with picamera.array.PiRGBArray(camera) as stream:
            camera.resolution=(640,480)
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

getLaserDist()