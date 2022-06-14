# mandelbrot_code.py

"""mandelbrot eqn implementation plus various coloring algorithms"""


import sys

sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/myProjects/myModules')
sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/my-python-project')

from PIL import Image
import numpy as np
from PIL import Image as im
import PIL
import itertools
import time
from math import log10
from colorsys import hsv_to_rgb
# import matplotlib.pyplot as plt
import numpy as np

from window_object1 import WindowObject
from button3 import *
# from zoom_draw3 import MyImage
from graphics import *
from mygraphics import *
from ruler0 import Ruler
from helpers import *


import inspect
myself = lambda: inspect.stack()[1][3]

X,Y = Ruler.X,Ruler.Y
maxIt = Ruler.maxIt  # may need to change with multiple zooms

class MandelbrotCode:
	
	def __init__(self,location,dp):
		self.location = location
		self.dp = dp
		self.trxz = self.trxz_return()

	def trxz_return(self):
		zsel = box_from_center(*self.location)
		return Transform(X,Y,*zsel)
		
	def mandelbrot(self,x,y,maxIt):
		c = complex(x,y)
		z = complex(0,0)
		for i in itertools.count(0):
			if i==maxIt: break
			if abs(z) > 2: break
			z = z * z + c
			hue = (i/maxIt)
			clr = colorsys.hsv_to_rgb(hue,1,1)
			r,g,b = [int(255*j) for j in clr]
		return hue

	def mandelbrot_image(self,dp):
		print(myself())
		self.image = PIL.Image.new('RGB', (X,Y), color = (255,255,255))
		self.image.pixels = self.image.load() 
		sp = 1
		self.hueLst = []
		for x in itertools.count(0,sp):
			if x==X:break
			for y in itertools.count(0,sp):
				if y==Y: break
				hue= self.mandelbrot(*self.trxz.world(x,y),maxIt)
				self.hueLst.append(hue)
				r,g,b = self.hue_to_rgb(hue)
				self.image.pixels[x,y] = r,g,b

		self.write_data_files(dp)
		return self.trxz

	def write_data_files(self,dp):
		print('max hueLst',max(self.hueLst))
		# self.image.show()

		# 800 (=maxIt hues/image??)
		self.hfile = Ruler.datadir2+'hfile' + str(dp) + '.txt'
		with open(self.hfile, "w") as f:
			f.write(str(self.hueLst))
		self.ifile = Ruler.datadir2+'ifile' + str(dp) + '.png'
		self.image.save(self.ifile)

				

	def hue_to_rgb(self,hue):
		r,g,b = colorsys.hsv_to_rgb(hue,1,1)
		r,g,b = int(255*r),int(255*g),int(255*b)
		# r,g,b = [int(255*i) for i in clr]
		return r,g,b


	def hueLst_to_image(self):
		print(myself())
		print(np.shape(self.hueLst))
		self.hueLst = np.reshape(self.hueLst,(X,Y))
		print(np.shape(self.hueLst))
		data = Image.fromarray(self.hueLst)
		# data.save('ifile.png')
		data.show()
		# data.save('ifile.png')
		# img = PIL.Image.open('ifile.png')
		# img.show()

	def mandelbrot(self,x,y,maxIt):
		c = complex(x,y)
		z = complex(0,0)
		for i in itertools.count(0):
			if i==maxIt: break
			if abs(z) > 2: break
			z = z * z + c
		return (i/maxIt)   # hue


	def mandelbrot_image_minimal(self,dp):
		print(myself(),'start')
		start = time.time()
		self.hueLst = []

		sp = 2
		self.image = PIL.Image.new('RGB', (X,Y), color = (255,255,255))
		self.image.pixels = self.image.load() 
		for x in itertools.count(0,sp):
			if x==X:break
			for y in itertools.count(0,sp):
				if y==Y: break
				hue = self.mandelbrot(*self.trxz.world(x,y),maxIt)
				self.hueLst.append(hue)

		# 800 (=maxIt hues/image??)
		self.hfile = Ruler.datadir2+'hfile' + str(dp) + '.txt'
		with open(self.hfile, "w") as f:
			f.write(str(self.hueLst))

		print('done',start - time.time())

	def image_from_hfilex(self,dp):
		'''NumPy uses the asarray() class to convert PIL images into NumPy arrays. The np.array function also produce the same result. The type function displays the class of an image.
		The process can be reversed using the Image.fromarray() f'''

		# print(self.hueLst[1000:1500])
		print(len(self.hueLst))
		array = np.reshape(self.hueLst,(450,450))
		# array = Image.fromarray(array)
		# array.show()

	

	
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
	location = -0.75,0,0.6
	location = - 0.5,0,3
	dp = 0
	mn = MandelbrotCode(location,dp)
	mn.mandelbrot_image(dp)
	# mn.hueLst_to_image()    np conversion needs a repeated pattern
	# mn.image_from_hfile(dp)
	