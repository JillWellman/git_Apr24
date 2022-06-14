# ruler0
import colorsys

class Ruler():
	X,Y = 500,500
	zX,zY = 3,3
	gscreen = 0,Y,X,0
	gzbox = -2,-1.5,1,1.5
	xside2 = X/10
	maxIt = 800

	datadir1 = 'data/june08_movie/'
	datadir2 = 'data/june09/'

	# interior color
	r,g,b = colorsys.hsv_to_rgb(0.99,0.5,0.5)
	interior = int(r*255),int(g*255),int(b*255)

	
	


	# winX,winY = (3.5*X,2*Y)  # fills width of laptop