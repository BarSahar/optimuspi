#from enum import Enum 

class DistConst:
    'Constants to compute distance per pixel'
    Slope=0
    Intercept=0

    def __init__(self, slope,intercept):
        self.Slope = slope
        self.Intercept = intercept
    def __str__(self):
        return "Slope is: " + str(self.Slope) + ". Intercept is: " + str(self.Intercept)

'''class direction(Enum):
	north=1
	east=2
	south=3
	west=4
'''