import operator as op
from robotModels import status

checkedpoints=[]
parentlist=[]
blockpoints=[]

#(point,parent)

def uncheckFinder(start,graph):

	# q=all Neighbours that are not block or checked
	q=getNeighbours(start,graph)

	flag=False
	point

	while q:
		point=q.pop(0)
		if graph[point[0]][point[1]] == status.uncheck:
			flag=True
			break
		q=q+getNeighbours(point,graph)

	if flag:
		path=pathfinder(start,point)
		return (path,point)
	else:
		return ((-1,-1),(-1,-1)) 


def markblockpoint(pointlist,graph):
	for point in pointlist:
		if graph[point[0]][point[1]] == status.block:
			blockpoints.append(point)

def getNeighbours(point,graph):

	checkedpoints.append(point)
	rightP=tuple(map(op.add, point,(1,0)))
	frontP=tuple(map(op.add, point,(0,1)))
	leftP=tuple(map(op.add, point,(-1,0)))
	backP=tuple(map(op.add, point,(0,-1)))

	templist=[rightP,frontP,leftP,backP]

	markblockpoint(templist,graph)
	anslist=[]
	for temp in templist:
		if temp not in blockpoints and temp not in checkedpoints:
			anslist.append(temp)
			parentlist.append((temp,point))
	return anslis


#	unmark=GiveUncheckPoints(templist)
#	unblock=GiveUnblockPoints(unmark,graph)
#	markPoints(unblock)
#	return unblock
	
def markPoints(points):
	for point in points:
		checkedpoints.append(point)


def GiveUncheckPoints(pointlist):
	list=[]
	for point in pointlist:
			if point not in checkedpoints:
				list.append(point)
	return list

def isuncheckPoint(point,graph):
	if graph[point[0]][point[1]] == status.uncheck:
		return True
	else:
		return False


def GiveUnblockPoints(pointlist,graph):
	lst=[]
	for point in pointlist:
		if graph[point[0]][point[1]] == status.block:
			blockpoints.append(point)
		else:
			lst.append(point)
	return lst
		



#(child,parent)
def pathfinder(start,end):

	path=[]
	temp=end

	while True:
		if temp==start:
			break
		for x in parentlist:
			if x[0]==temp:
				path.insert(0,x[1])
				temp=x[1]
				break

	path.pop(0)
	return path


# blocking x=0,x=xsize-1 and y=0,y=ysize-1
def makegrid(xsize,ysize):
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
		
	

def main():

	grid=makegrid(20,20)
	start=(1,1)
	p1=(17,1)
	p2=(17,17)
	grid[17][1]=status.uncheck
	grid[17][17]=status.uncheck

	

	path,endpoint=uncheckFinder(start,grid)
	
	print("start: "+str(start))
	print("path: "+str(path))
	print("end point:"+str(endpoint))


main()