import proxsens as sens
import operator as op
import numpy as np
from robotModels import status
import time

cposition=(0,0)
home=(0,0)

maxx=0
minx=0
maxy=0
miny=0

outlinenodes=[]
outlinenodes.append((cposition[0],cposition[1],status.clear))



def outline():
    first =True

    while True:
        if (home==cposition) and not first:
            markrightpoint(0)
            break
        first=False
        frontdis=sens.getLaserDist()
        sidedis=sens.getProxDist()

        print ("Front: "+str(frontdis))
        print ("Side: "+str(sidedis))
        print ("current pos: "+str(cposition))

        #input()
        time.sleep(2)

        if frontdis>60 and sidedis>60: #door or slit
            if doorcheck():
                sens.turnright()
                time.sleep(0.5)
                sens.moveForward()
                updateCposition()
        elif sidedis>30 and sidedis<45:  #wall too far on the right
                print("wall too far on the right")
                sens.turnright()
                time.sleep(0.5)
                sens.moveForward()
                #updateCposition()
                time.sleep(0.5)
                sens.turnleft()
        elif sidedis<13.5: # wall too close on the right
                print("wall too close on the right")
                sens.turnleft()
                time.sleep(0.5)
                sens.moveForward()
                #updateCposition()
                time.sleep(0.5)
                sens.turnright()
                #markrightpoint(0)
        else:                         # wall on the right is OK
            if frontdis>30:
                print("wall on the right is OK")
                markrightpoint(0)
                sens.moveForward()
                updateCposition()
            else:
                print("corner")
                markrightpoint(0)
                sens.turnleft()
                markrightpoint(0)
                sens.moveForward()
                updateCposition()
#        printlist()


    xoffset=0
    yoffset=0

    offsetHome=(0,0)

    xsize=0
    ysize=0


    if minx<0:
        xoffset=-minx
        xsize=(maxx-minx)+1
    else:
        xsize=maxx


    if miny<0:
        yoffset=-miny
        ysize=(maxy-miny)+1
    else:
        ysize=maxy




    offsetHome=tuple(map(op.add,home,(xoffset,yoffset)))

    grid=[]

    print ('xoff: '+str(xoffset)+' yoff: '+str(yoffset))
    print ('xsize'+str(xsize)+' ysize: '+str(ysize))



    for x in range(xsize):
        grid.append([])
        for y in range(ysize):
            grid[x].append(status.unexplored)
	#remember to check duplicate nodes and take the bloked

    for node in outlinenodes:
        grid[node[0]+xoffset][node[1]+yoffset]=node[2]
    print('done')
    return (grid,offsetHome)


def updateParam(point):
	global maxx
	global minx
	global maxy
	global miny

	x=point[0]
	y=point[1]

	if x>maxx:
		maxx=x
	elif x<minx:
		minx=x

	if y>maxy:
		maxy=y
	elif y<miny:
		miny=y
				 
# mark right point as block
def markrightpoint(num):  
	bpoint = cposition	
	for x in range (num+1):
		temp = tuple(map(op.add, bpoint,sens.giverightdir()))
		updateParam(temp)
		outlinenodes.append((temp[0],temp[1],status.block))
		bpoint=tuple(map(op.add, bpoint,sens.givebackdir()))

			
	
def updateCposition():
	global cposition
#	print("current pos: "+str(cposition)+"+"+str(sens.cosmos[sens.dir].value))
	cposition=tuple(map(op.add, cposition,sens.cosmos[sens.dir].value))
    cposition = tuple(map(op.add, cposition, cosmos[dir].value))
	outlinenodes.append((cposition[0],cposition[1],status.clear))
	updateParam(cposition)

def ifathome():
	if (home==cposition):
		return True
	else:
		return False

def doorcheck():
	for x in range(4):
		if sens.getProxDist()>60 and sens.getLaserDist()>17:
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
		print( str(node))