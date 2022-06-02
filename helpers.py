import sys
sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/my-python-project/myImports')
sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/myProjects/myModules')

import PIL
import PIL.Image

from graphics import *
from mygraphics import *
import colorsys
from ruler0 import Ruler

maxIt = Ruler.maxIt




def inside(clk,box):
	cx,cy = clk
	xa,ya,xb,yb = box
	return xa < cx < xb and ya < cy < yb




def string_to_list(str):
	str = str[1:-1]
	lst = str.split(', ')
	return(lst)
	# hueLst = list(map(lambda l: float(l),lst))

	print('list',lst)

def count_frequency(my_list):
	   count = {}
	   for i in my_list:
		   count[i] = count.get(i, 0) + 1
	   return count

def sci_not(num):
	return f"{num:,}"

def rec_draw(abox,win) :
    xa,ya,xb,yb =  abox
    return Rectangle(Point(xa,ya),Point(xb,yb)).draw(win)


def grid(crnLst,win,u):
	xa,ya,xb,yb = crnLst
	xa,xb = int(xa),int(xb)
	for i in range(xa,xb+1,u):
		for j in range(ya,yb+1,u):
			Rectangle(Point(i,j),Point(i+u,j+u)).draw(win)
			# Text(Point(i-0.03*u,j-0.07*u),str(i)+', '+str(j)).draw(win).setSize(18)
			Text(Point(i+0.15,j-0.07*u),str(i)+', '+str(j)).draw(win).setSize(18)



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

def window_location(win,w,h,x,y):
    win.master.geometry( '%dx%d+%d+%d' % (w, h, x, y) )



def rect_from_center(cx,cy,w):
	xa,ya,xb,yb = cx-w,cy-w,cx+w,cy+w
	return Rectangle(Point(xa,ya),Point(xb,yb))
	


def rec_draw(abox,win) :
    xa,ya,xb,yb =  abox
    return Rectangle(Point(xa,ya),Point(xb,yb)).draw(win)

def round_all(lst,n):
	return list(map(lambda l : round(l,n) , lst))

def min_corner(box):
	xa,ya,xb,yb = box
	return min(xa,xb),min(ya,yb)

def in_window(cx,cy,file,wind):
    imW = gImage(Point(cx,cy),file)
    imW.draw(wind)





