# click_draw.py
"""	quick draw from click on location.  """

import sys

from mandelbrot_code import MandelbrotCode
sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/myProjects/myModules')
sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/my-python-project')

import itertools
from PIL import Image
import PIL
# import matplotlib.pyplot as plt
from math import log10
from colorsys import hsv_to_rgb
from pathlib import Path
# import matplotlib.pyplot as plt
# import os
from window_object1 import WindowObject
from button3 import *
# from mandelbrot_code import MandelbrotCode
from graphics import *
from mygraphics import *
from ruler0 import Ruler
from helpers import *
from graph1 import HueGraph

import inspect
myself = lambda: inspect.stack()[1][3]

X,Y = Ruler.X,Ruler.Y
maxIt = Ruler.maxIt  

class State():

	def __init__(self,path,location,dp) -> None:
		self.path =path
		self.dp = dp
		self.location = location
		self.ifile = 'data/june14/ifile' + str(dp) + '.png'
		self.gfile = 'data/june14/gfile' + str(dp) + '.png'
	
	def make_drawing(self,dp):
		zsel = box_from_center(*self.location)
		self.trxz = Transform(X,Y,*zsel)

		start = time.time()
		mn = MandelbrotCode()
		if dp>1:
			mn.mandelbrot_core(self.trxz)
			self.time = time.time() - start
			self.image = mn.image
			self.image.save(self.ifile)

		

	def make_graph(self,dp):
		hg = HueGraph(dp)
		hg.xy_axes(dp)
		hg.dictionary(dp)
		hg.image.show()
		# hg.dictionary(dp)   # works off hueLst local to State
		# hg.data_bars(dp)
		self.image = hg.image
		self.image.save(self.gfile)

		

class StatePath():

	def __init__(self):
		self.wo = WindowObject('G')

	def click_loop(self):
		r = 10
		"""path space holds window and accepts clicks"""
		location = -0.5,0,3  # inital state
		dp = 0
		st = State(self,location,dp)
		st.make_drawing(dp)
		# st.make_graph(dp)

		in_window(X/2,Y/2,st.ifile,self.wo.win)
		in_window(X + 3*X/2 + 10,Y/2,st.gfile,self.wo.win)
		self.wo.win.getMouse()

		# select
		self.wo.graphic = Circle(Point(0,0),2).draw(self.wo.win)
		while True:
			# ========= select ============
			clk = self.wo.win.getMouse()
			cx,cy=clk.x,clk.y
			if cx >= X-10: continue  # ignores click outside of image
			self.wo.graphic.undraw()
			self.wo.graphic = Circle(Point(cx,cy),10).draw(self.wo.win)

			# permanent click mark on state images
			draw = PIL.ImageDraw.Draw(st.image)
			draw.ellipse((cx-r, cy-r, cx+r, cy+r), outline=(0,0,0),width=1)
			st.image.save(st.ifile)

			# ===== location next state =====
			dw = st.location[2]/5
			zx,zy = st.trxz.world(cx,cy)
			location = zx,zy,dw
			dp += 1
			st = State(pth,location,dp)
			st.make_drawing(dp)



	def init_button(self,win):
		self.bt = Button(win, Point( 460, 480), 70,30,'==>')
		self.bt.label.setSize(24)
		self.bt.draw()
		self.bt.activate()

if __name__ == "__main__":
	pth = StatePath()
	pth.click_loop()

