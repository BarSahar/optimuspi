import outliner as ot
import unexploredPointFinder as finder
import UnExploredPoint_Mapper as mapit
import proxsens as sens
import numpy as np
import FaceSlapper as slap
import time

def mapStart():
	try:
		grid=np.load('Grid')
		home=np.load('Home')
	except:
		home=np.load('Home')
		grid,home=ot.outline()
		np.save('Grid',grid)
		np.save('Home',home)
	finally:
		sens.showoff(grid)
		sens.cposition=home

		while True:
			path,endPoint=finder.uncheckFinder(sens.cposition,grid)
			if path==(-1,-1):
				print("didnt find any path")
				break
			else:
				while path:
					nextpoint=path.pop()
					slap.facesalpper(sens.cposition,nextpoint)
					sens.moveForward()
					time.sleep(1)
				slap.facesalpper(sens.cposition,endPoint)
				mapit.unexploredpoint(sens.cposition,endPoint)

		np.save('Grid',grid)
		np.save('Home',home)