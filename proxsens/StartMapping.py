import outliner as ot
import unexploredPointFinder as finder
import UnExploredPoint_Mapper as mapit
import proxsens as sens
import numpy as np
import FaceSlapper as slap
from robotModels import status
import time

try:
    grid = np.load('Grid.npy')
    home = np.load('Home.npy')
    home=tuple(home)
    sens.cposition = home
except:
    grid = []
    home = (-1, -1)

def mapStart():
    global grid
    grid = []
    home = (-1, -1)
    try:
        grid = np.load('Grid.npy')
        home = np.load('Home.npy')
        home=tuple(home)
    except:
        grid, home = ot.outline()
        np.save('Grid', grid)
        np.save('Home', home)

    finally:
        sens.showoff(grid)
        sens.cposition = home  # TODO delete this
        grid[5][5] = status.unexplored
        while True:
            path, endPoint = finder.uncheckFinder(sens.cposition, grid)
            print(str(path))
            print(str(endPoint))
            if path == (-1, -1):
                print("didnt find any path")
                break
            else:
                while path:
                    nextpoint = path.pop()
                    slap.facesalpper(sens.cposition, nextpoint)
                    sens.moveForward()
                    time.sleep(1)
                slap.facesalpper(sens.cposition, endPoint)
                mapit.unexploredpoint(sens.cposition, grid)

        np.save('Grid', grid)
        np.save('Home', home)
        goToPoint(home)


def goToPoint(target):
    if len(grid) == 0:
        print("Error: no map saved")
        return
    print("goToPoint: "+str(target))
    prevStat = grid[target[0]][target[1]]
    grid[target[0]][target[1]] = status.unexplored
    path, endPoint = finder.uncheckFinder(sens.cposition, grid)
    grid[target[0]][target[1]] = prevStat
    print(str(path))
    print(str(endPoint))
    if path == (-1, -1):
        print("didnt find any path")
        return
    else:
        while path:
            nextpoint = path.pop()
            slap.facesalpper(sens.cposition, nextpoint)
            sens.moveForward()
            time.sleep(1)
        slap.facesalpper(sens.cposition, endPoint)
        sens.moveForward()



#DEBUGGING FUNCTIONS
def debug_makegrid(xsize,ysize):
	grid=[]
	for x in range(xsize):
		grid.append([])
		for y in range(ysize):
			grid[x].append(status.clear)
	for x in range(xsize):
		grid[x][0]=status.block
		grid[x][ysize-1]=status.block
	for y in range(ysize):
		grid[0][y]=status.block
		grid[xsize-1][y]=status.block
	return grid
def debug_main():
    grid=debug_makegrid(10,15)
    start=(1,1)
    np.save('Grid', grid)
    np.save('Home', start)
	#grid[3][1]=status.unexplored
	#grid[3][3]=status.unexplored
	#path,endpoint=uncheckFinder(start,grid)
	#print("start: "+str(start))
	#print("path: "+str(path))
	#print("end point:"+str(endpoint))