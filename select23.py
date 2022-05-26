# select23.py
"""	23 move draw_object and related into helper (maybe mandelbrot)
		so that others can use it -- all it needs is location
	select 22 shows image and graph. Returns center and magnification
	select22 works with histogram22.  used for movie
	select21 copied from working 19  numerical summaries for histograms
	select19 froze 18, now cleaning and checking and enjoying
	select 18  select zoom works.  Adding graphs
		works in single window, combined file/classes
	select17  seems perfect with select zoom -- moving to add graph
	select16 with my_hueLst4
	select15  combine draw image and view histogram
		principled highlighting of spectral/escape speed regions
	select14  13 broke while working on hist/ recovered and saved  now stay in my_hueLst
	select13 rationalize new functions  graphs(Zelle versions)  progress towards more git
	select 12 try more nuanced color
	select 11 combining image draws and grapsh to show in combined display
	select10 in frequency_graphs  working towards tight algorithm/image/colorgraph connection
	select9  add hueLst sort --> dict make scatterplot
	select8 zooming seems great.  hueLst can collect hues
	select7 zooming seems accurate / upside down bug cured
	select6 builds on skeleton select wherre I demo how to recursively select regions
	select5 clean up and commit to git
	SelectSeries draw_whole draws initial state.  reorganize to Select
	select 4c sequential process for xsel and zsel through zooms
	select4b going back to pixel coord z-coord Transforms too confusing
	select.2 switching from class to instance methods"""

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



class State(Ruler):
	gzbox = -2,-1.5,1,1.5
	gscreen = 0,Y,X,0
	
	def __init__(self,parent,dp) -> None:
		self.dp = dp
		self.parent = parent
		
	def select(self):
		"""select box region with cursor  Confirm with ==> button
		window in parent class"""
		# print('   ',myself())
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
		# print('   ',myself(),dp)
		self.hueLst = []
		"""draws part of image mapped by trxz from zsel onto gscreen"""
		self.depth = dp
		if trxz==None:
			trxz = self.parent.trxz
		sp = 1

		self.image = PIL.Image.new('RGB', (X,Y), color = (255,255,255))
		self.image.pixels = self.image.load() 

		start_time = time.time()

		mn = MandelbrotCode()

		for x in range(0,X,sp):
			if x==0:print('.',end='')
			for y in range(0,Y,sp):
				hue,r,g,b = mn.mandelbrot(*trxz.world(x,y),maxIt)
				if abs(hue - 1) < 0.01: 
					self.image.pixels[x,y] = Ruler.interior
				else:
					self.image.pixels[x,y] = r,g,b
				self.hueLst.append(hue)

		elapsed_time = time.time() - start_time
		# print('elapsed time',round(elapsed_time,3))

	def create_image_from_location(self,cx,cy,dw):
		# cx,cy,dw = -0.59990625, -0.4290703125, 3/1024
		self.draw_image(self.trxz)
		self.store_image_and_text(self.dp)
		in_window(X/2,Y/2,self.image_filename,self.parent.wo.win)

		
	def store_image_and_text(self,dp):
		# store_text (filename,write,hueLst)
		self.text_filename = 'data/text_fileB' + str(dp) + '.txt'
		with open(self.text_filename, 'w') as f:
			f.write(str(self.hueLst))

		# store_image(filename,save,image_name)
		self.image_filename = 'data/image_fileB' + str(dp) + '.png'
		self.image.save(self.image_filename)

	# -----------------------
	def draw_graph(self,dp,hueLst):
		hg = HueGraph(dp,hueLst)
		self.graph_image = hg.create_frequency_graph()

	def storegraph(self):
		self.graph_image_filename = 'data/graph_image_fileB' + str(dp) + '.png'
		self.graph_image.save(self.graph_image_filename)

class StatePath(Ruler):
	GRAPH = True  # Flag for doing graphs  
	LIST = False  # flag for writing hueLst

	def __init__(self,label) -> None:
		self.wo = WindowObject(label)

	def zoom_loop(self):
		GRAPH = True
		# self.wo.draw()
		# create state_path
		dp = 0
		self.x_offset,self.y_offset = 100,20
		ip = StatePath('G')   #string of states in the run

		# create initial state
		im = State(ip,dp)  # creates State object with parent ip which holds the Transform
		ip.zoom_draw_display(im,dp)
		self.print_coords(dp)


		if StatePath.GRAPH:
			# create draw display graph
			hg = HueGraph(dp)
			im.graph_image = hg.color_frequency_graph()

			im.graph_image_filename = 'data/graph_image_fileA' + str(dp) + '.png'
			im.graph_image.save(im.graph_image_filename)

			wd = self.wo.win.width 
			in_window(2.25*X,Y/2,im.graph_image_filename,ip.wo.win)

		ip.bt = Button(ip.wo.win,Point(X - 50,Y - 30),60,30,'==>')
		ip.bt.draw()

		dp = 1
		while True:  # loop over post-initial states
			ip.bt.deactivate()
			im = State(ip,dp)   # new state im

			im.select()
			ip.zoom_draw_display(im,dp)
			
			# self.print_coords()
	
			if GRAPH==True:
				# create,store, display graph
				hg = HueGraph(dp)
				im.graph_image = hg.color_frequency_graph()
				im.graph_image_filename = 'data/graph_image_fileB' + str(dp) + '.png'
				im.graph_image.save(im.graph_image_filename)

				wd_graph = im.graph_image.width
				wd_win = ip.wo.win.width
				wd_win/2
				# wd = self.wo.win.width 
				in_window(2.25*X,Y/2,im.graph_image_filename,ip.wo.win)
			
			ip.bt.draw()
			dp += 1

	def zoom_draw_display(self,im,dp):
		self.zsel_transform(dp)
		self.transforms()
		cx,cy,dw = self.location_triad()
		im.create_image_from_location(cx,cy,dw)
		in_window(X/2,Y/2,im.image_filename,self.wo.win)

	def zsel_transform(self,dp):
		"""comes from two states bounding transition"""

		if not hasattr(self,'zsel'):
			self.zsel = Ruler.gzbox
		self.trxz = Transform(X,Y,*self.zsel)
		if not hasattr(self,'xsel'):
			self.xsel = Ruler.gscreen
		xsel = self.xsel  # created in state.select
		zxa,zya,zxb,zyb = self.trxz.world(xsel[0],xsel[1]) + self.trxz.world(xsel[2],xsel[3])
		self.zsel  = min(zxa,zxb),min(zya,zyb),max(zxa,zxb),max(zya,zyb)

		self.location_triad()
		self.transforms()

	def location_triad(self):
		if not hasattr(self,'zsel'): return
		zxa,zya,zxb,zyb = self.zsel
		zxc,zyc = (zxa + zxb)/2,(zya + zyb)/2
		dw = abs(zxb-zxa)
		return zxc,zyc,dw	

	


	def transforms(self):
		# use for upcoming draw image
		self.trxz = Transform(X,Y,*self.zsel)
		self.trzz = Transform(3,3,*self.zsel)
		self.print_coords(dp)

	def print_stats(self,dp):
		print('\n',myself(),'---- depth',dp)
		print('xsel',round_all(self.xsel,0))
	
		print()
		print('zsel',round_all(self.zsel,4))
		if hasattr(self,'trxz'):
			print('trxz',self.trxz)
		if hasattr(self,'trxx'):
			print('trxx',self.trxx)

	

	def init_windows(self,dp):
		"""shows initial state in both windows"""
		self.trxz = Transform(X,Y,*SelectSeries.gzbox)
		self.draw_image(dp,self.trxz)
		self.image_filename = 'image'+str(dp) + '.png'
		self.image.save(self.image_filename)
		in_window(X/2,Y/2,self.image_filename,self.woX.win)


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
		# grayscale through colorsys is more gradieated
		# direct i to hue is pretty stark black and white
		# r,g,b = colorsys.hsv_to_rgb(hue,1,1)
		
		if hue > 0.98:
			gr = 255
		else:
			gr = int( 255*( 1 - hue ) )
			# r,g,b = int(gr),int(gr),int(gr)
		return gr, gr, gr

	


if __name__ == "__main__":
	sp = StatePath('X')
	st = State(sp,3)

	sp.wo.win.getMouse()

	exit()
	sp = StatePath('X')
	sp.zoom_loop()

