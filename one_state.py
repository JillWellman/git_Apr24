# one_state.py


def discussion_example():
	cx = -0.59990625
	cy = -0.4290703125
	mag = 1024
	return (cx,cy),mag






from os import stat
import sys

sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/myProjects/myModules')
sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/my-python-project')

from PIL import Image
import PIL
# import matplotlib.pyplot as plt
import numpy as np
import time
from math import log10
from colorsys import hsv_to_rgb
from select22 import MandelbrotCode
# import matplotlib.pyplot as plt

from window_object1 import WindowObject
from button3 import *
from graphics import *
from mygraphics import *
from ruler0 import Ruler
from helpers import *
from histogram22 import HueGraph
from select22 import State, StatePath
import inspect
myself = lambda: inspect.stack()[1][3]

X,Y = Ruler.X,Ruler.Y
zX,zY = Ruler.zX,Ruler.zY
maxIt = Ruler.maxIt  # may need to change with multiple zooms

class WindowParent():
	def __init__(self) -> None:
		self.wo = WindowObject('X')

class OneState():
	def __init__(self,window_parent,center,width,magnification) -> None:
		self.window_parent = window_parent
		self.center = center
		self.width = width
		self.magnification = magnification
		
	def select_xsel(self):
		# center/width of selected region.  Maps to center of window
		self.xsel = box_from_center(*self.center,self.width/2)
		rec_draw(self.xsel,self.window_parent.wo.win)

	def z_transform(self):
		xa,ya,xb,yb = self.xsel
		self.trxz0 = Transform(X,Y,*Ruler.gzbox)
		zsel = self.trxz0.world(xa,ya) + self.trxz0.world(xb,yb)
		self.trxz = Transform(X,Y,*zsel)
		print(self.trxz)
	
	def draw_image(self,trxz):
		print('   ',myself(),end='  -- ')
		# if self.parent.LIST: self.hueLst = []
		"""draws part of image mapped by trxz from zsel onto gscreen"""
		sp = 1

		self.image = PIL.Image.new('RGB', (X,Y), color = (255,255,255))
		self.image.pixels = self.image.load() 

		start_time = time.time()

		trxz = self.trxz
		mn = MandelbrotCode()

		for x in range(0,X,sp):
			if x==0:print('.',end='')
			for y in range(0,Y,sp):
				hue,r,g,b = mn.mandelbrot(*trxz.world(x,y),maxIt)
				if abs(hue - 1) < 0.01: 
					self.image.pixels[x,y] = Ruler.interior
				else:
					self.image.pixels[x,y] = r,g,b
				# if self.parent.LIST: 
					# self.hueLst.append(hue)

		elapsed_time = time.time() - start_time
		print('elapsed time',round(elapsed_time,3))
			
	def store_image_and_text(self,dp):
		# store_text (filename,write,hueLst)
		# self.text_filename = 'data/text_fileB' + str(dp) + '.txt'
		# with open(self.text_filename, 'w') as f:
		# 	f.write(str(self.hueLst))

		self.image_filename = 'data/image_fileB' + str(dp) + '.png'
		print(self.image_filename)
		self.image.save(self.image_filename)

if __name__ == "__main__":
	wp = WindowParent()

	center= (X/2,Y/2)
	width = X
	magnification = 1
	dp = 0

	st = OneState(wp,center,width,magnification) 
	st.select_xsel()
	st.z_transform()

	# show initial state
	st.draw_image(st.trxz0)
	st.store_image_and_text(dp)
	in_window(X/2,Y/2,st.image_filename,st.window_parent.wo.win)

	st.window_parent.wo.win.getMouse()

# 	===================== state 1 ========
	# dp = 1
	# center= ((0.40)*500,255)
	# width = X/8
	# magnification = 8

	# =================== state 2 =======
	cx,cy = center = (-0.59990625, -0.4290703125) 
	width = 0.48828125 
	magnification = 1024
	dp = 2

	# center,magnification = discussion_example()
	# width = X/magnification
	# print(width)
	# print(center,width,magnification)


	st = OneState(wp,center,width,magnification) 
	st.select_xsel()
	st.window_parent.wo.win.getMouse()

	st.z_transform()
	st.draw_image(st.trxz)
	st.store_image_and_text(dp)
	in_window(X/2,Y/2,st.image_filename,st.window_parent.wo.win)
	
	st.window_parent.wo.win.getMouse()




	
		