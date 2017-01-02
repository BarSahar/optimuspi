from enum import Enum 

class DistConst:
    'Constants to compute distance per pixel'
    Slope=0
    Intercept=0

    def __init__(self, slope,intercept):
        self.Slope = slope
        self.Intercept = intercept
    def __str__(self):
        return "Slope is: " + str(self.Slope) + ". Intercept is: " + str(self.Intercept)

class direction(Enum):
	north=(0,1)
	east=(1,0)
	south=(0,-1)
	west=(-1,0)

class status(Enum):
	block=0
	clear=1
	uncheck=-1
