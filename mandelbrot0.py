# my_mandelbrot0

import sys
from xml.dom.pulldom import parseString

sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/myProjects/myModules')
sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/my-python-project')

from PIL import Image
import PIL
# import matplotlib.pyplot as plt
import numpy as np
import time
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
from histogram22 import HueGraph

# stem = '/Users/jillwellman_sept09_2012/Desktop/Python/my-python-project/draw_zoom_may5/'

import inspect
myself = lambda: inspect.stack()[1][3]

X,Y = Ruler.X,Ruler.Y
# zX,zY = Ruler.zX,Ruler.zY
maxIt = Ruler.maxIt  # may need to change with multiple zooms

def location_to_trxz(cx,cy,dw):
	# cx,cy,dw = -0.66,0,3  # -0.66,0,3
	zsel = box_from_center(cx,cy,dw/2)
	trxz = Transform(X,Y,*zsel)
	return trxz

class MandelbrotCode:
	hueLst = []
	image = PIL.Image.new('RGB', (X,Y), color = (255,255,255))

	def __init__(self,dp):
		def __init__(self,dp):
			self.dp = dp

	def read_image(self,trxz,dp):

		start_time = time.time()
		self.image.pixels = self.image.load() 
		self.create_pixels()
		# print('time',time.time()-start_time)

	def read_hist(self):
		file = 'hues' + str(dp) + '.txt'
		with open(file, "w") as f:
			f.write(str(self.hueLst))
		
	def create_pixels(self):
		MandelbrotCode.hueLst
		sp = 1
		# compute mandelbrot pixels
		for x in range(0,X,sp):
			for y in range(0,Y,sp):
				hue,r,g,b = self.mandelbrot(*trxz.world(x,y),maxIt)
				self.image.pixels[x,y] = r,g,b
				self.hueLst.append(hue)
				
		
		ifile = 'istem' + str(dp) +'.png'
		self.image.save(ifile)
		in_window(X/2,Y/2,ifile,self.wo.win)
		
	def mandelbrot(self,x,y,maxIt):
		c = complex(x,y)
		z = complex(0,0)
		for i in range(maxIt):
			if abs(z) > 2: break
			# zn+1 = zn2 + c. 
			z = z * z + c
		hue = (2*i/maxIt)  # double spectrum codes escape speed
		r,g,b = hsv_to_rgb(hue,1,1)
		r,g,b = int(255*r),int(255*g),int(255*b)
		# hue and saturation (inverse) hilight for escape time
		return hue,r,g,b

	def highlight_escape_time(self,hue):
		n_low,n_high=0,0
		if hue < 0.005:
			r,g,b = 0,0,0
		elif hue > 0.95:
			r,g,b = 0.4,0.4,0.4
		else:
			r,g,b = colorsys.hsv_to_rgb(hue,1,1)
		r,g,b = int(255*r),int(255*g),int(255*b)
		return hue, r,g,b

	def spectral(self):
		hue = mandelbrot(*trxz.world(x,y),maxIt)
		r,g,b = hsv_to_rgb((hue,1,1))
		r,g,b = int(255*r),int(255*g),int(255*b)
		self.image.pixels[x,y] = r,g,b
	
	def stationary(self):
		if abs(hue - 1) < 0.01: 
			self.image.pixels[x,y] = (70,70,70)
		else:
			self.image.pixels[x,y] = self.pixel_color(hue,x,y)

	def pixels_plots(self):
		#  use for debugging coord systems
		 Point(*self.trxz.world(x,y)).draw(self.parent.woZ.win).setOutline(color_rgb(r,g,b))
		 Point(x,y).draw(self.parent.woX.win) 

	def binary(self,x,y,maxIt):
		c = complex(x,y)
		z = complex(0,0)
		for i in range(maxIt):
			if abs(z) > 2: break
			z = z * z + c
		return (i % 4 * 64, i % 8 * 32, i % 16 * 16)

	def mandelbrot_edges(self,x,y,maxIt):
		c = complex(x,y)
		z = complex(0,0)
		for i in range(maxIt):
			if abs(z) > 2: break
			z = z * z + c
		hue = i/maxIt
		if hue > 0.98:
			gr = 255
		else:
			gr = int( 255*( 1 - hue ) )
			# r,g,b = int(gr),int(gr),int(gr)
		return gr, gr, gr

	


if __name__ == "__main__":
	from viewer import State
	dp = 5
	mn = MandelbrotCode(dp)
	cx,cy,dw = -0.75,0.14 ,0.35  #test values  good starter
	trxz = location_to_trxz(cx,cy,dw)
	State.draw_image(trxz,dp)
	

