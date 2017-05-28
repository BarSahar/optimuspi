import outliner as ot
import unexploredPointFinder as finder
import UnExploredPoint_Mapper as mapit
import proxsens as sens
import numpy as np
import FaceSlapper as slap
from robotModels import status
import time

grid = []


def mapStart(xsize, ysize, steps):
    global grid, home
    grid = []
    home = (1, 1)

    # making the temp grid
    for x in range(xsize):
        grid.append([])
        for y in range(ysize):
            grid[x].append(status.clear)
    for x in range(xsize):
        grid[x][0] = status.block
        grid[x][ysize - 1] = status.block
    for y in range(ysize):
        grid[0][y] = status.block
        grid[xsize - 1][y] = status.block
    for x in range(int(xsize / 2), xsize - 1):
        for y in range(1, ysize - 1):
            grid[x][y] = status.unexplored

    sens.cposition = home
    sens.showoff(grid)

    for step in range(steps):
        print(34 * "-")
        print("step {}/{} \n".format(step + 1, steps))
        path, endPoint = finder.uncheckFinder(sens.cposition, grid)
        if path == (-1, -1):
            print("didn't find unexplored points")
            break
        else:
            while path:
                nextpoint = path.pop()
                slap.facesalpper(sens.cposition, nextpoint)
                sens.moveForward()
                time.sleep(1)
            slap.facesalpper(sens.cposition, endPoint)
            mapit.unexploredpoint(sens.cposition, grid)
        sens.showoff(grid)
        print('\n\n\n')

    goToPoint(home)


def goToPoint(target):
    if len(grid) == 0:
        return
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
