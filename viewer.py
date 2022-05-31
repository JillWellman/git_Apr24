# viewer.py
"""	recursive draw.  Take everything else out"""

import sys

sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/myProjects/myModules')
sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/my-python-project')

from PIL import Image
import PIL
# import matplotlib.pyplot as plt
# from math import log10
from colorsys import hsv_to_rgb
# import matplotlib.pyplot as plt

from window_object1 import WindowObject
from mandelbrot0 import MandelbrotCode
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
maxIt = Ruler.maxIt  


class State(Ruler):
	gzbox = -2,-1.5,1,1.5
	gscreen = 0,Y,X,0
	
	def __init__(self,parent,dp) -> None:
		self.dp = dp
		self.parent = parent
		
	def create_image_from_location(self,cx,cy,dw,dp):

		zsel = box_from_center(cx,cy,dw/2)
		trxz = Transform(X,Y,*zsel)
		self.make_image(trxz,dp)

	def make_image(self,trxz,dp):
		print(myself())
		print(hues0.txt in 'data/jhw0527/')
			# if im.startswith('image'):
			# 	print(im)
		# self.draw_image(trxz,dp)
		# self.image.save('imfile.png')
		# in_window(X/2,Y/2,'imfile.png',self.parent.wo.win)

	def draw_image(self,trxz,dp):
		print(dp)
		hueLst=[]
		self.depth = dp
		sp = 1
		print('viewer ',dp,end=' ')

	
		self.image = PIL.Image.new('RGB', (X,Y), color = (255,255,255))
		self.image.pixels = self.image.load() 

		self.create_image(trxz,dp)

	def create_image(self,trxz,dp):
		sp = 1
		hueLst = []
		mn = MandelbrotCode(dp)
		start_time = time.time()
		# compute mandelbrot pixls
		for x in range(0,X,sp):
			for y in range(0,Y,sp):
				hue,r,g,b = mn.mandelbrot(*trxz.world(x,y),maxIt)
				hueLst.append(hue)
				self.image.pixels[x,y] = r,g,b
		

		print('time',time.time()-start_time)

		self.ifile = 'image' + str(dp) + '.png'
		self.image.save(self.ifile)
		in_window(X/2,Y/2,self.ifile,self.parent.wo.win)
		hfile = 'hues' + str(dp) + '.txt'
		with open(hfile, "w") as f:
			f.write(str(hueLst))

class StatePath(Ruler):

	def __init__(self,label) -> None:
		self.wo = WindowObject(label)
		self.locLst = []
		self.directory = 'data/0527/'

	def read_csv(self,directory,file_name):
		"""read a file holding rows of csv 
		return a matrix of the same shape with the same numbers"""
		file_name = 'data/jhw0527/'+ 'locations.txt'
		with open(file_name, "r") as f:
			data = f.read()
		processed = []
		records = data.split('\n')
		for r in records:
			r = r[1:-1]  # strip parens
			nums = r.split(',')
			try: 
				dp,cx,cy,dw = nums
			except:
				ValueError
				continue
			dp,cx,cy,dw = int(dp),float(cx),float(cy),float(dw)
			processed.append((cx,cy,dw) )
		return processed

	def draw_states_from_location(self,file_name):
		self.init_button(self.wo.win)
		data = self.read_csv('data/jhw0527' ,'locations.txt')
		dp = 0
		for rec in data:
			cx,cy,dw = rec
			st = State(pth,dp)
			self.bt.deactivate()
			st.create_image_from_location(cx,cy,dw,dp)
			self.bt.activate()
			self.bt.draw()
			self.bt.wait()
			dp += 1

	def init_button(self,win):
		self.bt = Button(win, Point( 460, 480), 70,30,'==>')
		self.bt.label.setSize(24)
		self.bt.draw()
		self.bt.activate()




if __name__ == "__main__":
	pth = StatePath('X')
	pth.draw_states_from_location('locations.txt')
	st = State(pth,dp=3)
	# st.create_image_from_location('locations.txt')
	

