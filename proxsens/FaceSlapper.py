import proxsens as p
from robotModels import direction


def facesalpper(start,end):
	ndir=(0,0)
	sdir=p.cosmos[p.dir]
	
	if end[0]>start[0]:
		ndir=direction.east
	elif end[0]<start[0]:
		ndir=direction.west
	elif end[1]>start[1]:
		ndir=direction.north
	elif end[1]<start[1]:
		ndir=direction.south

	if ndir!=(0,0):
		sindex=p.cosmos.index(ndir)
		helper=sindex-sdir
		if helper==0:
			p.moveForward
		elif fabs(helper)==2:
			p.turnleft()
			p.time.sleep(1)
			p.turnleft()
		elif fabs(helper)==3:
			if helper>0:
				p.turnleft()
			else:
				p.turnright()
		elif helper>0:
			p.turnright()
		else:
			p.turnleft()