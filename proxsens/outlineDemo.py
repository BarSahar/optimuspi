import proxsens as sens
import operator as op
import numpy as np
from robotModels import status
import time

cposition = (0, 0)
home = (0, 0)

maxx = 0
minx = 0
maxy = 0
miny = 0

outlinenodes = []
outlinenodes.append((cposition[0], cposition[1], status.clear))


def outline(steps):

    for step in range(steps):
        print(34*"-")
        print("step {}/{} \n".format(step+1,steps))
        frontdis = sens.getLaserDist()
        sidedis = sens.getProxDist()

        print("Front Distance: " + str(frontdis))
        print("Side Distance: " + str(sidedis))
        print("Current Position: ({},{})\n".format(cposition[0],cposition[1]))

        # input()
        time.sleep(2)

        if frontdis > 60 and sidedis > 45:  # door or slit
            if doorcheck() is True:
                sens.turnright()
                time.sleep(0.5)
                sens.moveForward()
                updateCposition()
        elif sidedis > 30 and sidedis < 45:  # wall too far on the right
            print("output: wall too far on the right")
            sens.turnright()
            time.sleep(0.5)
            sens.moveForward()
            updateCposition()
            time.sleep(0.5)
            sens.turnleft()
        elif sidedis < 13.5 :  # wall too close on the right
            print("output: wall too close on the right")
            sens.turnleft()
            time.sleep(0.5)
            sens.moveForward()
            updateCposition()
            time.sleep(0.5)
            sens.turnright()
            markrightpoint(0)
        else:  # wall on the right is OK
            if frontdis > 30:
                print("output: wall on the right is OK")
                markrightpoint(0)
                sens.moveForward()
                updateCposition()
            else:
                print("output: corner")
                markrightpoint(0)
                sens.turnleft()
                markrightpoint(0)
                sens.moveForward()
                updateCposition()
    printlist()



# mark right point as block
def markrightpoint(num):
    global outlinenodes
    bpoint = cposition
    for x in range(num + 1):
        temp = tuple(map(op.add, bpoint, sens.giverightdir()))
        outlinenodes.append((temp[0], temp[1], status.block))
        bpoint = tuple(map(op.add, bpoint, sens.givebackdir()))


def updateCposition():
    global cposition,outlinenodes
    cposition = tuple(map(op.add, cposition, sens.cosmos[sens.dir].value))
    outlinenodes.append((cposition[0], cposition[1], status.clear))


def ifathome():
    if (home == cposition):
        return True
    else:
        return False


def doorcheck():
    for x in range(4):
        if sens.getProxDist() > 60 and sens.getLaserDist() > 17:
            sens.moveForward()
            time.sleep(0.5)
            updateCposition()
            if ifathome():
                return False
        else:
            markrightpoint(x)
            return False

    sens.turnleft()
    time.sleep(0.5)
    sens.turnleft()
    for x in range(4):
        sens.moveForward()
        updateCposition()
        time.sleep(0.5)

    sens.turnleft()
    time.sleep(0.5)
    sens.turnleft()
    time.sleep(0.5)
    return True


def printlist():
    for node in outlinenodes:
        print("({},{}) Status: {}".format(node[0],node[1],node[2].name))
