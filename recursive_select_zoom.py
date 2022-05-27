# select26.py
"""	recursive draw.  Take everything else out"""

import sys

sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/myProjects/myModules')
sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/my-python-project')

from PIL import Image
import PIL
# import matplotlib.pyplot as plt
from math import log10
from colorsys import hsv_to_rgb
# import matplotlib.pyplot as plt

from window_object1 import WindowObject
from button3 import *
# from zoom_draw3 import MyImage
from graphics import *
from mygraphics import *
from ruler0 import Ruler
from helpers import *
# from histogram22 import HueGraph

# stem = '/Users/jillwellman_sept09_2012/Desktop/Python/my-python-project/draw_zoom_may5/'

import inspect
myself = lambda: inspect.stack()[1][3]

X,Y = Ruler.X,Ruler.Y
# zX,zY = Ruler.zX,Ruler.zY
maxIt = Ruler.maxIt  # may need to change with multiple zooms


class State(Ruler):
	gzbox = -2,-1.5,1,1.5
	gscreen = 0,Y,X,0
	
	def __init__(self,parent,dp) -> None:
		self.dp = dp
		self.parent = parent
		
	def select(self):
		"""select box region with cursor  Confirm with ==> button
		window in parent class"""
		bx = Circle(Point(0,0),1).draw(self.parent.wo.win)  #dummy for undraw
		bx_drawn = False   	  				 # only dummy drawn
		while True:
			if bx_drawn: self.parent.bt.activate()
			c = self.parent.wo.win.getMouse()
			if self.parent.bt.clicked(c) and bx_drawn: break
			if c.x > X - Ruler.xside2: continue  # don't allow extension over right side
			self.cx,self.cy,self.wd = c.x,c.y,Ruler.xside2
			self.parent.xsel = self.xsel = box_from_center(self.cx,self.cy,self.wd)
			bx.undraw()
			bx = rec_draw(self.xsel,self.parent.wo.win)
			bx_drawn = True
		self.parent.bt.deactivate()

	def draw_image(self,trxz,dp):
		self.depth = dp
		sp = 2

		self.image = PIL.Image.new('RGB', (X,Y), color = (255,255,255))
		self.image.pixels = self.image.load() 

		mn = MandelbrotCode()

		for x in range(0,X,sp):
			for y in range(0,Y,sp):
				hue,r,g,b = mn.mandelbrot(*trxz.world(x,y),maxIt)
				self.image.pixels[x,y] = r,g,b

class StatePath(Ruler):

	def __init__(self,label) -> None:
		self.wo = WindowObject(label)

	def zoom_loop(self):
		dp = 0

		st = State(self,dp)  # creates State object with parent ip which holds the Transform
		self.zsel = State.gzbox  # whole z window
		st.xsel = State.gscreen # whole x window
		self.zsel_transform(st,dp)

		st.draw_image(self.trxz,dp)
		st.image.save('imfile.png')
		in_window(X/2,Y/2,'imfile.png',self.wo.win)

		self.bt = Button(self.wo.win,Point(X - 50,Y - 30),60,30,'==>')
		self.bt.draw()

		dp = 1
		while True:  # loop over post-initial states
			self.bt.deactivate()

			st = State(self,dp)  # parent = self
			st.select()  # selects xsel which goes to zsel
			self.zsel_transform(st,dp)
			
			st.draw_image(self.trxz,dp)
			st.image.save('imfile.png')
			in_window(X/2,Y/2,'imfile.png',self.wo.win)
			dp += 1
	
			self.bt.draw()

	def zsel_transform(self,st,dp):
		"""freeze
		comes from two states bounding transition"""
		self.trxz = Transform(X,Y,*self.zsel)

		xsel = st.xsel  # created in state.select
		zxa,zya,zxb,zyb = self.trxz.world(xsel[0],xsel[1]) + self.trxz.world(xsel[2],xsel[3])
		dw = (zxb-zxa)
		self.zsel  = min(zxa,zxb),min(zya,zyb),max(zxa,zxb),max(zya,zyb)
		
		# use for upcoming draw image
		self.trxz = Transform(X,Y,*self.zsel)

	def init_button(self,win):
		self.bt = Button(win, Point( 460, 480), 70,30,'==>')
		self.bt.label.setSize(24)
		self.bt.draw()
		self.bt.activate()

class MandelbrotCode:

	def __init__(self):
		pass

	def mandelbrot(self,x,y,maxIt):
		c = complex(x,y)
		z = complex(0,0)
		for i in range(maxIt):
			if abs(z) > 2: break
			# zn+1 = zn2 + c. 
			z = z * z + c
		hue = (2*i/maxIt)
		r,g,b = hsv_to_rgb(hue,1,1)
		r,g,b = int(255*r),int(255*g),int(255*b)
		# hue and saturation (inverse) hilight for escape time
		return hue,r,g,b



if __name__ == "__main__":
	path_loc_file = 'data/0523' + '/path_locations' + '.txt'
	sp = StatePath('X')
	sp.zoom_loop()

