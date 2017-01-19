import proxsens as p
from robotModels import direction


def facesalpper(start,end):

	pointToFace=(-1,-1)
		
	if end[0]>start[0]:
		pointToFace=direction.east
	elif end[0]<start[0]:
		pointToFace=direction.west
	elif end[1]>start[1]:
		pointToFace=direction.north
	elif end[1]<start[1]:
		pointToFace=direction.south

	if pointToFace!=(-1,-1):

		pointToFace_index=p.cosmos.index(pointToFace)

		delta=pointToFace_index-p.dir

		if delta==0:
			return
		elif fabs(delta)==2:
			p.turnleft()
			p.time.sleep(1)
			p.turnleft()
		elif fabs(delta)==3:
			if delta>0:
				p.turnleft()
			else:
				p.turnright()
		elif delta>0:
			p.turnright()
		else:
			p.turnleft()