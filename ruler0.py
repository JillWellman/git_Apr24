# ruler0

class Ruler():
	X,Y = 500,500
	zX,zY = 3,3
	gscreen = 0,Y,X,0
	gzbox = -2,-1.5,1,1.5
	xside2 = X/10

	interior = (255,0,50)
	maxIt = 1000

	winX,winY = (3.5*X,2*Y)  # fills width of laptop