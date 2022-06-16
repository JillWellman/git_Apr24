# ruler0
import colorsys

class Ruler():
	X = Y = 500
	zX,zY = 3,3
	gscreen = 0,Y,X,0
	gzbox = -2,-1.5,1,1.5
	xside2 = X/10
	maxIt = 800

	dta = 'data/june14/'

	# interior color
	h_int_color = 0.99
	clr = colorsys.hsv_to_rgb(0.99,0.5,1)
	rgb_int_color = [int(c*255) for c in clr]
	# int(r*255),int(g*255),int(b*255)

	
	


	# winX,winY = (3.5*X,2*Y)  # fills width of laptop