from enum import Enum  
import collections
import operator as op
from robotModels import status

def bfs(graph, start, end):
    # maintain a queue of paths
    queue = collections.deque()
    # push the first path into the queue
    queue.append([start])
    while len(queue)>0:
        # get the first path from the queue
        path = queue.popleft()
        # get the last node from the path
        node = path[-1]
        # path found
        if node == end:
            return path
        # enumerate all adjacent nodes, construct a new path and push it into the queue
        rightP=(node[0]+1,node[1])
        frontP=(node[0],node[1]+1)
        leftP=(node[0]-1,node[1])
        backP=(node[0],node[1]-1)
        for node in [rightP,frontP,leftP,backP]:
            print("graph in node"+str(node) +"::"+ graph[node[0]][node[1]])
            if graph[node[0]][node[1]]!=status.block:
                new_path = list(path)
                new_path.append(node)
                queue.append(new_path)

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
    grid=makegrid(10,10)
    start=(1,1)
    end=(3,1)
    path,endpoint=bfs(grid,start,grid)
    print("start: "+str(start))
    print("path: "+str(path))
    print("end point:"+str(endpoint))

main()