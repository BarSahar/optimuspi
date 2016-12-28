import proxsens as sens
import operator as op



cposition=(0,0)
home=(0,0)
first =True


def outline():
	while True:
		if (home==cposition) and (~first):
			return True
		first=False


		if sens.getLaserDist()>67 and sens.getProxDist()>60: #door or slit
			if doorcheck():
				sens.turnright()
				sens.moveForward()
				updateCposition()
		elif sens.getProxDist()>33 and sens.getProxDist()<37:  #wall too far on the right
				sens.turnright()
				sens.moveForward()
				updateCposition()
				sens.turnleft()
		elif sens.getProxDist()<13.5: # wall too close on the right
				sens.turnleft()
				sens.moveForward()
				updateCposition()
				sens.turnright()
		else:                         # wall on the right is OK
			if sens.getLaserDist()>33:
				sens.moveForward()
				updateCposition()
			else:
				sens.turnleft()



	
	
def updateCposition():
	cposition=tuple(map(op.add, cposition,sens.cosmos[sens.dir]))

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


def main():
	outline()


