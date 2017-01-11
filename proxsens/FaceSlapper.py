import proxsens as p
from robotModels import direction


def facesalpper(start,end):

	point_direction=(0,0)
	current_direction=p.cosmos[p.dir]
	
	if end[0]>start[0]:
		point_direction=direction.east
	elif end[0]<start[0]:
		point_direction=direction.west
	elif end[1]>start[1]:
		point_direction=direction.north
	elif end[1]<start[1]:
		point_direction=direction.south

	if point_direction!=(0,0):
		point_direction_index=p.cosmos.index(ndir)
		delta=sindex-sdir
		if delta==0:
			pass
		elif fabs(delta)==2:
			p.turnleft()
			p.time.sleep(1)
			p.turnleft()
		elif fabs(delta)==3:
			if helper>0:
				p.turnleft()
			else:
				p.turnright()
		elif delta>0:
			p.turnright()
		else:
			p.turnleft()