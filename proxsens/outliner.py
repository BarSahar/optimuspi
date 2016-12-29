import proxsens as sens
import operator as op


cposition=(0,0)
home=(0,0)
first =True


def outline():
	global first

	while True:
		if (home==cposition) and not first:
			return True
		first=False

		frontdis=sens.getLaserDist()
		sidedis=sens.getProxDist()
		print ("Fromt: "+str(frontdis))
		print ("Side: "+str(sidedis))
		print("current pos: "+str(cposition))

		if frontdis>65 and sidedis>60: #door or slit
			if doorcheck():
				sens.turnright()
				sens.moveForward()
				updateCposition()
		elif sidedis>30 and sidedis<45:  #wall too far on the right
				sens.turnright()
				sens.moveForward()
				updateCposition()
				sens.turnleft()
		elif sidedis<13.5: # wall too close on the right
				sens.turnleft()
				sens.moveForward()
				updateCposition()
				sens.turnright()
		else:                         # wall on the right is OK
			if frontdis>30:
				sens.moveForward()
				updateCposition()
			else:
				sens.turnleft()



	
	
def updateCposition():
	global cposition
	cposition=tuple(map(op.add, cposition,sens.cosmos[sens.dir].value))

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
			return False

	sens.turnleft()
	sens.turnleft()
	for x in range(4):
		sens.moveForward()
	sens.turnright()	
	sens.turnright()
	return True

 


#def main():
#	outline()


