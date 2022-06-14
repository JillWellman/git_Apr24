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

# from histogram22 import HueGraph

# stem = '/Users/jillwellman_sept09_2012/Desktop/Python/my-python-project/draw_zoom_may5/'

import inspect
myself = lambda: inspect.stack()[1][3]

X,Y = Ruler.X,Ruler.Y
maxIt = Ruler.maxIt  



class State():

	def __init__(self,parent,loc,dp) -> None:
		self.dp = dp
		self.loc = loc
		self.parent = parent
		self.hfile = Ruler.datadir2 + 'hfile'+ str(dp) + '.txt'
		self.ifile = Ruler.datadir2 + 'ifile'+ str(dp) + '.png'
		self.gfile = Ruler.datadir2 + 'gfile' + str(dp) + '.png'
		self.slt_file = Ruler.datadir2 + 'slt_file.txt'
	
	
	def make_imagex(self,trxz,dp):
		start = time.time()
		self.mandelbrot_core(trxz)
		self.time = time.time() - start

		print(dp,'time',self.time,end=' ')
		print('location',self.loc)
		with open(self.lfile, "a") as f:
			f.write(str(self.loc))
		ifile = Ruler.datadir + 'ifile' + str(dp) + '.png'
		self.image.save(ifile)
		in_window(X/2,Y/2,ifile,self.parent.wo.win)

class StatePath():

	def __init__(self):
		self.wo = WindowObject('G')

	def click_loop(self):
		"""path space holds window and accepts clicks"""
		loc = -0.5,0,3  # inital state
		dp = 0
		st = State(self,loc,dp)
		with open(st.slt_file, "w") as f:
			f.write(str(st.loc))

		mn = MandelbrotCode(loc,dp)
		# mn.mandelbrot_image(dp)  # optional
		in_window(X/2,Y/2,Ruler.datadir2 + 'ifile0.png',self.wo.win)
		st.trxz = mn.trxz

		# select
		self.wo.graphic = Circle(Point(0,0),2).draw(self.wo.win)
		while True:
			# ========= select ============
			clk = self.wo.win.getMouse()
			cx,cy=clk.x,clk.y
			print(cx,cy)
			if cx >= X-10: continue  # ignores click outside of image
			self.wo.graphic.undraw()
			self.wo.graphic = Circle(Point(cx,cy),10).draw(self.wo.win)

			# ===== location next image =====
			dw = st.loc[2]/5
			zx,zy = st.trxz.world(cx,cy)
			loc = zx,zy,dw
			
			# write selection /time /location next image


			dp += 1
			st = State(self,loc,dp)
			mn = MandelbrotCode(loc,dp)
			mn.mandelbrot_image(dp)
			# ifile = Ruler.datadir2 + 'ifile' + str(dp) + '.png'
			in_window(X/2,Y/2,st.ifile,self.wo.win)
			st.trxz = mn.trxz

			# hg = HueGraph(dp)   # dp, uncle
			# hg.create_graph(dp)
			# gfile = Ruler.datadir + 'gfile' + str(dp) + '.png'
			# in_window(2.6*X,Y/2,gfile,self.wo.win)


	def init_button(self,win):
		self.bt = Button(win, Point( 460, 480), 70,30,'==>')
		self.bt.label.setSize(24)
		self.bt.draw()
		self.bt.activate()

if __name__ == "__main__":
	pth = StatePath()
	pth.click_loop()

