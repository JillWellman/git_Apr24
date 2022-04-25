import sys
sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/my-python-project/myImports')
sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/myProjects/myModules')

from graphics import *
from mygraphics import *
import colorsys


def cont(win, point = (35,15),lable = 'CONTINUE'):	
	px,py = point
	xa,ya,xb,yb = X-2,Y-2, X-2*px,Y-2*py
	r = Rectangle(Point(xa,ya),Point(xb,yb)).draw(win)
	r.setFill('white')
	r.setWidth(2)
	t = Text(Point(X-px,Y-py),lable).draw(win)
	while True:
		clk = win.getMouse()
		cx,cy = clk.x,clk.y
		if X - cx <= 70 and Y - cy <= 30:
			t.undraw()
			r.undraw()
			break
	return 

def rec_draw(abox,win) :
    xa,ya,xb,yb =  abox
    return Rectangle(Point(xa,ya),Point(xb,yb)).draw(win)

def grid(crnLst,win,u):
	xa,ya,xb,yb = crnLst
	for i in range(xa,xb):
		for j in range(ya,yb):
			Rectangle(Point(i*u,j*u),Point((i+1)*u,(j+1)*u)).draw(win)
			Text(Point(i-0.08,j+0.07),str(i)+','+str(j)).draw(win).setSize(18)

def grid_labels(box,win):
	u = 1/2
	xa,ya,xb,yb = box
	for i in range(-5,5):
		for j in range(-5,5):
			re=Rectangle(Point(cx+i*u,cy+j*u),Point(cx+(i+1)*u,cy+(j+1)*u)).draw(win)
			re.setOutline('lightgray')

		dx = xb-xa 
		Text( Point(-0.44,(ya+yb)/2), str(round(xa,2))).draw(win).setSize(18)
		Text( Point(xb-dx/5,(ya+yb)/2), str(round(xb,2))).draw(win).setSize(18)

		Text( Point((xa+xb)/2,ya), str(round(ya,2))).draw(win).setSize(18)
		Text( Point((xa+xb)/2,yb), str(round(yb,2))).draw(win).setSize(18)


def box_from_center(cx,cy,w):
	xa,ya,xb,yb = cx-w,cy-w,cx+w,cy+w
	Rectangle(Point(xa,ya),Point(xb,yb))
	return xa,ya,xb,yb 


def rec_draw(abox,win) :
    xa,ya,xb,yb =  abox
    return Rectangle(Point(xa,ya),Point(xb,yb)).draw(win)

def round_all(lst,n):
	return list(map(lambda l : round(l,n) , lst))

def min_corner(box):
	xa,ya,xb,yb = box
	return min(xa,xb),min(ya,yb)

def mandelbrot(x,y,maxIt):
	c = complex(x,y)
	z = complex(0,0)
	for i in range(maxIt):
		if abs(z) > 2: break
		z = z * z + c
	hue = (i/maxIt)
	return hue
	
	r,g,b = colorsys.hsv_to_rgb(hue,1,1)
	return  int(255*r),int(255*g),int(255*b)

def mandelbrot_edges(x,y,maxIt):
	c = complex(x,y)
	z = complex(0,0)
	for i in range(maxIt):
		if abs(z) > 2: break
		z = z * z + c
	hue = i/maxIt
	# grayscale through colorsys is more gradieated
	# direct i to hue is pretty stark black and white
	# r,g,b = colorsys.hsv_to_rgb(hue,1,1)
	
	if hue > 0.98:
		gr = 255
	else:
		gr = int( 255*( 1 - hue ) )
		# r,g,b = int(gr),int(gr),int(gr)
	return gr, gr, gr

