"""	draw2 copy of zoom_draw3.  replacing class methods with instance methods."""
"""(rp  
depth = 0  initial state:
	max_iterations=20, escape_radius=1000)  	width = 3  (orig 3.5)
depth = 3, show spiral
	max_iterations=512, escape_radius=1000)
	viewport = Viewport(image, center=-0.7435 + 0.1314j, width=0.002)"""
#spiral -0.7435, 0.1314,0.002)

import sys

from matplotlib.pyplot import box
from numpy import recarray
sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/my-python-project/myImports')
sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/myProjects/myModules')
from graphics import *
from mygraphics import *

from PIL import Image
from PIL.ImageColor import getrgb
import PIL
import button3
from window_object import WindowObject
from helpers import *

# from git_Apr24.mandelbrot_03 import MandelbrotSet
# from viewport import Viewport

def hsb(hue_degrees: int, saturation: float, brightness: float):
	return getrgb(
		f"hsv({hue_degrees % 360},"
		f"{saturation * 100}%,"
		f"{brightness * 100}%)"
	)


import inspect
myself = lambda: inspect.stack()[1][3]

from ruler0 import Ruler

X,Y = Ruler.X,Ruler.Y

class Draw(Ruler):
	"""totally in z space"""
	file_stub = 'select_draw_zoom/images/hsb'
	depth = 0

	def __init__(self,zx,zy,wd,wo,dp) -> None:
		self.zx,self.zy = zx,zy
		self.wd = wd
		self.wo = wo
		self.depth = dp
		self.X,self.Y = Ruler.X,Ruler.Y

	def implement_hsb(self):
		escape_radius, maximum_iterations = self.mandelbrot_parameters()
		mandelbrot_set = MandelbrotSet(maximum_iterations, escape_radius)
		print(self.depth,'zx,zy,wd,  dp',self.zx,self.zy,self.wd)
		self.image = Image.new(mode="RGB", size=(X, Y))
		for pixel in Viewport(self.image, self.zx + self.zy*1j, self.wd):
			stability = mandelbrot_set.stability(complex(pixel), smooth=True)
			pixel.color = (0, 0, 0) if stability == 1 else hsb(
				hue_degrees=int(stability * 360),
				saturation=stability,
				brightness=1,
				)
		return self.image 

	def draw_zsel(self,zx,zy,wd):
		# self.depth += 1
		# print(self.depth)
		# wd = 2/10**self.depth
		zsel = box_from_center(self.zx,self.zy,self.wd/2)
		rec_draw(zsel,self.wo.win).setOutline('lightblue')
		
	def save_show(self):
		self.image.save(self.file_name)
		in_window(-0.5,0,self.file_name,self.wo.win)
		
	def mandelbrot_parameters(self):
		escape_radius = 1000
		if self.depth==0: maximum_iterations = 20       # initial
		elif self.depth==1: maximum_iterations = 100    # neck
		else:  maximum_iterations = 200   # lace and spiral
		
		return escape_radius, maximum_iterations

	def draw_click_pointsx(self):
		for dp in range(5):
			
			if dp==0: 
				zx,zy = -0.7435,0.1314
				wd = 3.5
			else: wd = 3/(5*dp)

			dr = Draw(zx,zy,wd,wo,dp)
			dr.depth = dp
			dr.image = dr.implement_hsb()
			dr.file_name = Draw.file_stub + str(dr.depth) + '.png'
			dr.save_show()
			Circle(Point(zx,zy),0.05).draw(wo.win).setFill('red')
			zsel = box_from_center(zx,zy,wd/2)
			rec_draw(zsel,dr.wo.win)
			clk = dr.wo.win.getMouse()
			zx,zy = clk.x,clk.y

	def draw_pre_set_points(self):
		for dp in range(5):
			wd = 2/(10**dp)
			zx,zy = -0.7435,0.1314
			dr = Draw(zx,zy,wd,wo,dp)
			dr.depth = dp
			dr.image = dr.implement_hsb()
			dr.file_name = Draw.file_stub + str(dr.depth) + '.png'
			dr.save_show()
			Circle(Point(dr.zx,dr.zy),0.05).draw(wo.win).setFill('red')

			clk = dr.wo.win.getMouse()

	def	draw_six(self,w_obj):
		self.images = []
		for i in range(5):	
			dr = Draw(self.zx,self.zy,self.wd,self.wo)	
			self.six_pack.append(dr)	
			dr.file_name = Draw.file_stub + str(dr.depth) + '.png'
			
			try:
				in_window(-0.5,0,im.file_name,self.woZ.win)				
			except:
				FileNotFoundError
				dr.image = dr.implement_hsb()
				dr.save_show(dr.wo.win)
				in_window(X/2,Y/2,dr.file_name,self.wo.win)

			# dr.set_hsb_zoom_region()
			dr.wd = 2/10**i
			zsel = box_from_center(dr.zx,dr.zy,dr.wd/5)
			rec_draw(zsel,self.wo.win).setOutline('red')
			Circle(Point(dr.zx,dr.zy),dr.wd/50).draw(self.wo.win).setFill('red')

			wo.win.getMouse()
	
if __name__ == "__main__":
	zx,zy,wd =  -0.7435, 0.1314,2
	wo = WindowObject('Z',X,Y)
	dr = Draw(zx,zy,wd,wo,0)
	# dr.draw_click_points()
	

	exit()

	

