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
from analyse0 import *
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
maxIt = Ruler.maxIt  

def rect_from_box(box):
	xa,ya,xb,yb = box
	return Rectangle(Point(xa,ya),Point(xb,yb))

class State(Ruler):
	LIST = True  # flag to record hues
	gzbox = -2,-1.5,1,1.5
	gscreen = 0,Y,X,0
	
	
	def __init__(self,parent,dp) -> None:
		self.dp = dp
		self.parent = parent
		locdir = self.parent.dir
		self.hfile = locdir+ 'hues' + str(dp) + '.txt'
		self.ifile = locdir + 'image' + str(dp) + '.png'
		self.gfile = locdir+ 'gfile' + str(dp) + '.png'
		self.locfile = locdir + 'locations.txt'
		
	
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

	def make_image(self,trxz,dp):
		self.draw_image(trxz,dp)
		self.image.save(self.ifile)
		in_window(X/2,Y/2,self.ifile,self.parent.wo.win)

	def draw_image(self,trxz,dp):
		if State.LIST: 
			print('j')
			self.hueLst = []
			self.hfile = 'data/0530/hues' + str(dp) + '.txt'
		print(str(dp),end= ' ')
		self.depth = dp
		sp = 1

		self.image = PIL.Image.new('RGB', (X,Y), color = (255,255,255))
		self.image.pixels = self.image.load() 

		mn = MandelbrotCode()
		start_time = time.time()

		for x in range(0,X,sp):
			for y in range(0,Y,sp):
				hue,r,g,b = mn.mandelbrot(*trxz.world(x,y),maxIt)
				self.image.pixels[x,y] = r,g,b
				self.hueLst.append(hue)
		
		print('time',time.time() - start_time,end=' ')

		with open(self.hfile, "w") as f:
			f.write(str(self.hueLst) + '\n')

		self.get_related_graph(dp)
	
	
	def get_related_graph(self,dp):
		gr = Graph('G')
		gr.create_graph(dp)
		gfile = 'data/0530/gfile' + str(dp) + '.png'
		in_window(2*X,Y/2,gfile,self.parent.wo.win)
		

class StatePath(Ruler):

	def __init__(self,label,dir,start_dp) -> None:
		self.wo = WindowObject(label)
		self.locLst = []
		self.dir = dir
		self.start_dp = start_dp

	def zoom_loop(self):
		dp = self.start_dp
		st = State(self,dp)  # State object with parent ip holding the Transform and window
		in_window(X/2,Y/2,st.ifile,self.wo.win)

		if dp==0:
			st.xsel,self.zsel  = State.gscreen, State.gzbox # whole x & z windows 
			self.trxz = Transform(X,Y,*self.zsel)   # transform from state0 to current state zbox
		else:
		
			# pre-0 transform
			dp,cx,cy,dw = self.get_location_stored(dp)   # for existing state
			self.zsel = box_from_center(cx,cy,dw)
			self.trxz0 = Transform(X,Y,*self.zsel)   # transform from state0 to current state zbox
			print(self.trxz0)
			self.loc = (cx,cy,dw)
			with open(self.dir + 'locations.txt', "w") as f:
				f.write(str(self.loc) + '\n')

		self.bt = Button(self.wo.win,Point(X - 50,Y - 30),60,30,'==>')
		self.bt.draw()
		dp = 1

		while True:  # loop over post-initial states
			self.bt.deactivate()



			# select region from existing state displayed
			st = State(self,dp)  # parent = self
			st.select()  # selects xsel which goes to zsel

			# find transform from xsel
			self.zsel_transform(st,dp)
			# st.rect_from_box(st.xsel).draw(self.wo.win).setOutline('red')

			with open('locations.txt', "a") as f:
				f.write(str(self.loc) + '\n')
		

			# make next image from transform
			st.make_image(self.trxz,dp)
			print(self.get_location_from_zsel(dp))

			dp += 1
	
			self.bt.draw()

	def get_location_from_zsel(self,dp):
		zxa,zya,zxb,zyb = self.zsel
		dw = zxb-zxa
		cx,cy = (zxa+zxb)/2,(zya+zyb)/2
		return dp,cx,cy,dw

	def get_location_stored(self,dp):
		with open(self.dir + 'locations.txt', "r") as f:
			lstr = f.read()
		# print(lstr)

		lstr = lstr[1:-2]  # remove parens and extr \n
		lst = lstr.split(',')
		lst =  [float(l) for l in lst]
		print(lst)
		return lst

	def zsel_transform(self,st,dp):
		"""freeze
		comes from two states bounding transition"""
		# self.trxz = Transform(X,Y,*self.zsel)
		# print(self.trxz)

		xsel = st.xsel  # created in state.select
		zxa,zya,zxb,zyb = self.trxz.world(xsel[0],xsel[1]) + self.trxz.world(xsel[2],xsel[3])
		dw = (zxb-zxa)
		cx,cy = (zxa+zxb)/2,(zya+zyb)/2,
		self.loc = cx,cy,dw
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
			# if abs(i - maxIt) < 1.5:
			# 	r,g,b = Ruler.interior_color
			# else:
			hue = (2*i/maxIt)
			r,g,b = hsv_to_rgb(hue,1,1)
			r,g,b = int(255*r),int(255*g),int(255*b)
				# hue and saturation (inverse) hilight for escape time
		return hue,r,g,b



if __name__ == "__main__":
	start_dp = 0
	directory = 'data/0531/'
	pth = StatePath('G',directory,start_dp)
	pth.zoom_loop()

