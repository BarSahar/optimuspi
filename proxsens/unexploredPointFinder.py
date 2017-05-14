import operator as op
from robotModels import mark, status
from enum import Enum

checkedpoints = []
parentlist = []


def uncheckFinder(start, graph):
    global checkedpoints, parentlist
    matrixinit(len(graph), len(graph[0]))
    checkedpoints[start[0]][start[1]] = mark.checked
    q = []
    q = getNeighbours(start, graph)
    flag = False
    point = (-2, -2)
    while q:
        point = q.pop(0)
        if graph[point[0]][point[1]] == status.unexplored:
            flag = True
            break
        q = q + getNeighbours(point, graph)
    if flag:
        print("start: "+str(start))
        print("point: "+str(point))
        path = pathfinder(start, point)
        checkedpoints = []
        parentlist = []
        return (path, point)
    else:
        checkedpoints = []
        parentlist = []
        return ((-1, -1), (-1, -1))


def matrixinit(xsize, ysize):
    global parentlist
    global checkedpoints
    for x in range(xsize):
        checkedpoints.append([])
        parentlist.append([])
        for y in range(ysize):
            checkedpoints[x].append(mark.uncheck)
            parentlist[x].append([])


def getNeighbours(point, graph):
    rightP = tuple(map(op.add, point, (1, 0)))
    frontP = tuple(map(op.add, point, (0, 1)))
    leftP = tuple(map(op.add, point, (-1, 0)))
    backP = tuple(map(op.add, point, (0, -1)))
    templist = [rightP, frontP, leftP, backP]
    clearNeighbours = GiveClearPoints(templist, graph)
    parentUpdate(clearNeighbours, point)
    return clearNeighbours


def parentUpdate(pointlist, parent):
    for point in pointlist:
        parentlist[point[0]][point[1]] = parent
        checkedpoints[point[0]][point[1]] = mark.checked


def GiveClearPoints(pointlist, graph):
    clearList = []
    for point in pointlist:
        if graph[point[0]][point[1]] != status.block and checkedpoints[point[0]][point[1]] == mark.uncheck:
            clearList.append(point)
    return clearList


def pathfinder(start, end):
    path = []
    temp = end
    while True:
        if temp == start:
            break
        parentOfTemp = parentlist[temp[0]][temp[1]]
        path.append(parentOfTemp)
        temp = parentOfTemp
    path.pop()
    return path
