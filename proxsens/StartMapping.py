import outliner as ot
import unexploredPointFinder as finder
import UnExploredPoint_Mapper as mapit
import proxsens as sens
import numpy as np
import FaceSlapper as slap
from robotModels import status
import time

grid = []

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
        sens.cposition = home
        while True:
            path, endPoint = finder.uncheckFinder(sens.cposition, grid)
            print(str(path))
            print(str(endPoint))
            xx=input()
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
        return

    grid[target[0]][target[1]] = status.unexplored
    path, endPoint = finder.uncheckFinder(sens.cposition, grid)
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
