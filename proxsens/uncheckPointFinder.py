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
	while q:
		point=q.pop([0])
		if point is status.uncheck:
			flag=True
			break
		q=q+getNeighbours(point,graph)

	if flag:
		path=pathfinder(start,point)
		return (path,point)
	else:
		return False



def getNeighbours(point,graph):

	rightP=tuple(map(op.add, point,(1,0)))
	frontP=tuple(map(op.add, point,(0,1)))
	leftP=tuple(map(op.add, point,(-1,0)))
	backP=tuple(map(op.add, point,(0,-1)))

	templist=[rightP,frontP,leftP,backP]

	markblockpoint(templist)
	anslist=[]

	for temp in templist:
		if temp not in blockpoints and temp not in checkedpoints:
			anslist.append(temp)
			parentlist.append(temp,point)


	return anslist
	
	

def isuncheckPoint(point,graph):
	if graph[point[0]][point[1]] is status.uncheck:
		return True
	else:
		return False


def markblockpoint(pointlist,graph):
	for point in pointlist:
		if graph[point[0]][point[1]] is status.block:
			blocklist.append(point)
			checkedpoints.append(point)
		else:
			checkedpoints.append(point)

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

	param=uncheckFinder(start,grid)
	endpoint=param[1]

	print(str(endpoint))


main()