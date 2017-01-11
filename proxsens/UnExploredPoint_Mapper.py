import proxsens as p
import operator as op
from robotModels import status
import math


def unexploredpoint(position,graph):

	direction=p.cosmos[p.dir].value
	front_distance=p.getLaserDist()
	point=position
	if front_distance<30:
		point=temp =tuple(map(op.add,position,direction))
		graph[point[0]][point[1]]=status.block
	else:
		for x in range(math.floor(front_distance/15)):
			point=tuple(map(op.add,point,direction))
			graph[point[0]][point[1]]=status.clear