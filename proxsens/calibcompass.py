import compTest

import time
import math
import csv

if __name__ == "__main__":

    myCompass = compTest.LSM9DS0()

    minx = 0
    maxx = 0
    miny = 0
    maxy = 0

    for i in range(0,500):
        axes = myCompass.readMag()
        x_out = read_word_2c(0)
        y_out = read_word_2c(1)
        
        if x_out < minx:
            minx=x_out
        
        if y_out < miny:
            miny=y_out
        
        if x_out > maxx:
            maxx=x_out
        
        if y_out > maxy:
            maxy=y_out

        time.sleep(0.1)

    print ("minx: " + str(minx))
    print ("miny: " + str(miny))
    print ("maxx: " + str(maxx))
    print ("maxy: " + str(maxy))
    print ("x offset: " + str((maxx + minx) / 2))
    print ("y offset: " + str((maxy + miny) / 2))