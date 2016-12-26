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

		if sens.getDist>33:  #wall too far on the right
			if sens.getLaserDist>45: #enough room to enter "door size"
				sens.turnright()
				sens.moveForward()
				updateCposition()
			elif sens.getLaserDist<13.5: # wall infront
				sens.turnleft()
				sens.moveForward()
				updateCposition()
			else:
				sens.moveForward() #skiping slit
				updateCposition()
		elif sens.getDist<13.5:
			sens.turnleft()
			if sens.getLaserDist>33:
				sens.moveForward() 
				updateCposition() 
				sens.turnright()
				#ignoring getLaserDist <13.5 for now


	
	
def updateCposition():
	cposition=tuple(map(op.add, cposition,sens.cosmos[sens.dir]))
	