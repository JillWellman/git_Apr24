# select26.py
"""	24 and 26 recursive zoom works.  Saving saving copy saving on git.
		in 26 will start integrating build from location.
		all the fussy directory stuff.
	25 broke and wasn't well backed up

	24 backed out to last night's 23.  renamed as 24
	23 move draw_object and related into helper (maybe mandelbrot)
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
	LIST = True
	
	def __init__(self,parent,dp) -> None:
		self.dp = dp
		self.parent = parent
		self.write_directory = self.parent.write_directory
		self.read_directory = self.parent.read_directory
		
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

	def zsel_transform(self,dp):
		"""comes from two states bounding transition"""

		if not hasattr(self,'zsel'):
			st.zsel = Ruler.gzbox
		self.trxz = Transform(X,Y,*st.zsel)
		if not hasattr(self,'xsel'):
			st.xsel = Ruler.gscreen
		xsel = self.xsel  # created in state.select
		zxa,zya,zxb,zyb = self.trxz.world(xsel[0],xsel[1]) + self.trxz.world(xsel[2],xsel[3])
		self.zsel  = min(zxa,zxb),min(zya,zyb),max(zxa,zxb),max(zya,zyb)
		
		# use for upcoming draw image
		self.trxz = Transform(X,Y,*self.zsel)
		self.trzz = Transform(3,3,*self.zsel)
		# coords

	def draw_image(self,trxz,dp):
		# print('   ',myself(),dp)
		if State.LIST: self.hueLst = []
		self.depth = dp
		sp = 2

		self.image = PIL.Image.new('RGB', (X,Y), color = (255,255,255))
		self.image.pixels = self.image.load() 

		# start_time = time.time()

		mn = MandelbrotCode()

		for x in range(0,X,sp):
			for y in range(0,Y,sp):
				hue,r,g,b = mn.mandelbrot(*trxz.world(x,y),maxIt)
				# if 1 - hue < 0.01:  # magenta red
				# 	self.image.pixels[x,y] = Ruler.interior
				# else:
				self.image.pixels[x,y] = r,g,b
				# if State.LIST: self.hueLst.append(hue)

		# elapsed_time = time.time() - start_time

	def create_image_from_location(self):
		dp = 3 
		# cx,cy,dw = 0.34649107183915934, -0.37546362183256504, 0.02419296385348313
		dw = 3/1024 # base dimension over magnification
		cx,cy,dw = -0.59990625, -0.4290703125, dw
		
		zsel = box_from_center(cx,cy,dw/2)
		trxz = Transform(X,Y,*zsel)
		self.draw_image(trxz,dp)
		self.store_image_and_text(dp)
		in_window(X/2,Y/2,self.image_filename,self.parent.wo.win)
		
	def write_location_string(self):   # in data file for whole state path
		with open(self.loc_file, 'a') as f:  
			f.write(self.loc_data+ '\n')

	def store_image_and_text(self,dp):
		self.txfile = self.parent.write_directory + '/txfile_' + str(dp) + '.txt'
		if dp==0:
			with open(self.txfile, 'w') as f:
				f.write(str(self.hueLst))
		else:
			with open(self.txfile, 'a') as f:	
				f.write(str(self.hueLst))

		# store_image(filename,save,image_name)
		self.ifile = self.parent.write_directory + '/ifile_' + str(dp) + '.png'
		self.image.save(self.ifile)

	# -----------------------
	def draw_graph(self,dp,hueLst):
		hg = HueGraph(dp,hueLst)
		self.graph_image = hg.create_frequency_graph()

	def storegraph(self):
		self.graph_image_filename = 'data/graph_image_fileB' + str(dp) + '.png'
		self.graph_image.save(self.graph_image_filename)

	

class StatePath(Ruler):
	GRAPH = False  # Flag for doing graphs  
	LIST = True  # flag for writing hueLst
	# x_offset,y_offset = 100,20


	def __init__(self,label,read_directory,write_directory,loc_data) -> None:
		self.wo = WindowObject(label)
		self.read_directory = read_directory
		self.write_directory = write_directory
		self.write_directory
		self.ldata_file = self.write_directory+'/loc_data.txt'


		

	def zoom_loop(self):
		dp = 0

		st = State(self,dp)  # creates State object with parent ip which holds the Transform
		self.zsel_transform(st,dp)
		self.draw_store(st,dp)

		if StatePath.GRAPH: self.graph_state(st,dp)

		self.bt = Button(self.wo.win,Point(X - 50,Y - 30),60,30,'==>')
		self.bt.draw()

		dp = 1
		while True:  # loop over post-initial states
			self.bt.deactivate()
			st = State(self,dp)   # new state im

			st.select()
			self.zsel_transform(st,dp)
			self.draw_store(st,dp)
	
			if StatePath.GRAPH: self.graph_state(st,dp)
			
			self.bt.draw()
			dp += 1

	def graph_state(self,st,dp):
		hg = HueGraph(1,dp)
		st.graph_image = hg.color_frequency_graph()
		st.graph_image_filename = 'data/0523_' + str(dp) + '.png'
		st.graph_image.save(st.graph_image_filename)

		# wd_graph = st.graph_image.width
		# wd_win = self.wo.win.width
		in_window(2.25*X,Y/2,st.graph_image_filename,self.wo.win)


	def zsel_transform(self,st,dp):
		"""comes from two states bounding transition"""
		if not hasattr(self,'zsel'):
			self.zsel = Ruler.gzbox
		self.trxz = Transform(X,Y,*self.zsel)

		if not hasattr(st,'xsel'):
			st.xsel = Ruler.gscreen
		xsel = st.xsel  # created in state.select
		zxa,zya,zxb,zyb = self.trxz.world(xsel[0],xsel[1]) + self.trxz.world(xsel[2],xsel[3])
		dw = (zxb-zxa)
		print('zsel_transform: dw',dw)
		self.zsel  = min(zxa,zxb),min(zya,zyb),max(zxa,zxb),max(zya,zyb)
		
		# use for upcoming draw image
		self.trxz = Transform(X,Y,*self.zsel)
		self.trzz = Transform(3,3,*self.zsel)
		# coords


	def draw_store(self,st,dp):
		# self.zsel_transform(st,dp)
		st.draw_image(self.trxz,dp)
		st.store_image_and_text(dp)
		in_window(X/2,Y/2,st.ifile,self.wo.win)

	
		


		zxa,zya,zxb,zyb = self.zsel
		dw = zxb-zxa
		cx,cy = (zxa + zxb)/2 , (zya + zyb)/2 
		st.loc_data = str(dp) + ','+ str(cx) + ',' + str(cy) + ',' + str(dw)
		print('dw',dw)
		

		with open(self.ldata_file,"a") as f:
			print(st.loc_data)
			f.write('\n'+st.loc_data)
			# f.write('\n'+s)

	
	def print_stats(self,dp):
		print('\n',myself(),'---- depth',dp)
		print('xsel',round_all(self.xsel,0))
	
		print()
		print('zsel',round_all(self.zsel,4))
		if hasattr(self,'trxz'):
			print('trxz',self.trxz)
		if hasattr(self,'trxx'):
			print('trxx',self.trxx)

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
		if hue > 0.98:
			gr = 255
		else:
			gr = int( 255*( 1 - hue ) )
			# r,g,b = int(gr),int(gr),int(gr)
		return gr, gr, gr

	


if __name__ == "__main__":
	if False:
		sp = StatePath('X')
		st = State(sp,3)
		st.create_image_from_location()

		sp.wo.win.getMouse()
	else:
		path_loc_file = 'data/0523' + '/path_locations' + '.txt'
		sp = StatePath('X','data/0523','data/0525',path_loc_file)
		sp.zoom_loop()

