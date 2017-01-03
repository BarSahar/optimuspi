import proxsens as sens
import operator as op
import numpy as np
from robotModels import status

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
			break
		first=False
		x =input('befor')

		frontdis=sens.getLaserDist()
		sidedis=sens.getProxDist()

		print ("Front: "+str(frontdis))
		print ("Side: "+str(sidedis))
		print("current pos: "+str(cposition))
		x =input('after')


		if frontdis>65 and sidedis>60: #door or slit
			if doorcheck():
				sens.turnright()
				sens.moveForward()
				updateCposition()
				
		elif sidedis>30 and sidedis<45:  #wall too far on the right
				print("wall too far on the right")
				sens.turnright()
				sens.moveForward()
				updateCposition()
				sens.turnleft()
		elif sidedis<13.5: # wall too close on the right
				print("wall too close on the right")
				sens.turnleft()
				sens.moveForward()
				updateCposition()
				sens.turnright()
		else:                         # wall on the right is OK
			if frontdis>30:
				print("wall on the right is OK")
				sens.moveForward()
				updateCposition()
				markrightpoint()
			else:
				print("wall on the right is not OK")
				sens.turnleft()
				sens.moveForward()
				updateCposition()



	xoffset=0
	yoffset=0
	
	offsetHome

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


	if  minx<0 or miny<0:
		for node in outlinenodes:
			node[0]=node[0]+xoffset
			node[1]=node[1]+yoffset
		offsetHome=tuple(map(op.add,home,(xoffset,yoffset)))
	
	grid=[]

	for x in range(xsize):
		grid.append([])
		for y in range(ysize):
			grid[x].append(status.uncheck)

	for node in outlinenodes:
		grid[outlinenodes[0]][outlinenodes[1]]=outlinenodes[2]
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
def markrightpoint():  
	rpoint=tuple(map(op.add, cposition,sens.giverightdir()))
	outlinenodes.append((rpoint[0],rpoint[1],status.block))
	updateParam(rpoint)
		
	
def updateCposition():
	global cposition
	print("current pos: "+str(cposition)+"+"+str(sens.cosmos[sens.dir].value))
	cposition=tuple(map(op.add, cposition,sens.cosmos[sens.dir].value))
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
			updateCposition()
			if ifathome():
				return False
		else:
			markrightpoint()
			return False

	sens.turnleft()
	sens.turnleft()
	for x in range(4):
		sens.moveForward()
	sens.turnright()	
	sens.turnright()
	return True

