# select26.py
"""	26a starting view_images and other ui features
	26 recursive zoom works.  Saving saving copy saving on git.
		will start integrating build from location.
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
from tracemalloc import start

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

	def draw_image(self,trxz):
		print('   ',myself(),dp,end=' ')
		
		if State.LIST: self.hueLst = []
		sp = 2

		self.image = PIL.Image.new('RGB', (X,Y), color = (255,255,255))
		self.image.pixels = self.image.load() 

		start_time = time.time()

		mn = MandelbrotCode()
		for x in range(0,X,sp):
			for y in range(0,Y,sp):
				hue,r,g,b = mn.mandelbrot(*trxz.world(x,y),maxIt)
				if 1 - hue < 0.01:  # magenta red
					self.image.pixels[x,y] = Ruler.interior
				else:
					self.image.pixels[x,y] = r,g,b

				if State.LIST: self.hueLst.append(hue)

		elapsed_time = time.time() - start_time
		print('elapsed time',elapsed_time)
		print('self.zsel',self.zsel)

	def location_data(self,dp):  # compute and write
		zxa,zya,zxb,zyb = self.zsel
		dw = zxb-zxa
		cx,cy = (zxa + zxb)/2 , (zya + zyb)/2 
		self.loc_data = str(dp) + ': ' + str(cx) + ',' + str(cy) + ',' + str(dw) 
	
		with open(self.location_data_file ,"a") as f:
			print(self.location_data_file)
			f.write('\n' + self.loc_data)

	def zsel_transform(self,dp):
		print('    ',myself(),end=' ')
		"""comes from two states bounding transition
		attached to preceding/original state"""
		# if not hasattr(self,'zsel'):
		# 	self.zsel = Ruler.gzbox
		self.trxz = Transform(X,Y,*self.zsel)

		xsel = self.xsel  
		zxa,zya,zxb,zyb = self.trxz.world(xsel[0],xsel[1]) + self.trxz.world(xsel[2],xsel[3])
		
		

		zxa,zya,zxb,zyb = self.zsel  = min(zxa,zxb),min(zya,zyb),max(zxa,zxb),max(zya,zyb)
		cx,cy = (zxa+zxb)/2,(zya+zyb)/2
		dw = (zxb-zxa)
		print('cx,cy,dw',cx,cy,dw)
		# use for upcoming draw image
		self.trxz = Transform(X,Y,*self.zsel)
		self.trzz = Transform(3,3,*self.zsel)
	
	def create_image_from_location(self,cx,cy,dw,dp):
		zsel = box_from_center(cx,cy,dw/2)
		trxz = Transform(X,Y,*zsel)
		self.draw_image(trxz)

		self.store_huefile(dp)
		self.store_image(dp)

		in_window(X/2,Y/2,self.ifile,self.parent.wo.win)

	def draw_graph(self,dp,hueLst):
		hg = HueGraph(dp,hueLst)
		self.graph_image = hg.create_frequency_graph()
	
	# -----------------------
	def store_location_string(self):   # in data file for whole state path
		with open(sp.location_data_file, 'a') as f:  
			f.write(self.cx,self.cy.self.dw)

	def store_huefile(self,dp):
		# during view activity, don't store location string  on top of source file
		self.hueFile = 'data/0525/huefile' + str(dp) + '.txt'
		with open(self.hueFile, 'w') as f:	
			f.write(str(self.hueLst))

	def store_show_image(self,dp):
		self.ifile = self.parent.directory + '/ifile' + str(dp) + '.png'
		print('state ifile',self.ifile)
		self.image.save(self.ifile)
		in_window(X/2,Y/2,self.ifile,self.parent.wo.win)

	def store_graph(self):
		self.graph_image_filename = 'data/graph_image_fileB' + str(dp) + '.png'
		self.graph_image.save(self.graph_image_filename)

class StatePath(Ruler):
	GRAPH = False  # Flag for doing graphs  
	LIST = True  # flag for writing hueLst


	def __init__(self,label,directory,start_dp) -> None:
		self.label = label
		self.wo = WindowObject(label)  # graphic opened
		self.start_dp = start_dp
		self.directory = directory
		self.location_data_file = directory + 'loc_data.txt'


	def erase_file_contents(self,file_name):
		with open(file_name,"w") as f:
			f.write('')
	
	def zoom_loop(self,start_dp):
		dp = start_dp
	
		st = State(self,dp)  # creates State object with parent ip which holds the Transform
		# st.erase_file_contents(st.location_data_file)
		st.zsel = st.gzbox
		st.trxz = Transform(X,Y,*st.zsel)

		print('st.zsel',st.zsel)
		st.draw_image(st.trxz)
		st.store_show_image(dp)
		st.store_huefile(dp)
		print('st.zsel',st.zsel)

		if StatePath.GRAPH: self.graph_state(st,dp)

		self.bt = Button(self.wo.win,Point(X - 50,Y - 30),60,30,'==>')
		self.bt.draw()
		self.bt.wait()

		dp = 1
		while True:  # loop over post-initial states
			self.bt.deactivate()
			st = State(self,dp)   # new state im

			print('**',st.zsel)

			st.zsel_transform(dp)
			st.trxz = Transform(X,Y,*st.zsel)

			st.draw_image(st.trxz)
			st.store_show_image(dp)
			st.store_huefile(dp)
			print('**',st.zsel)

			# st.location_data(dp)
	
			if StatePath.GRAPH: self.graph_state(st,dp)
			
			self.bt.draw()
			dp += 1

# transforms
	

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

	def	new_path_from(self,cx,cy,dw):
		with open(sp.location_data_file, 'r') as f:  
			data = f.read()


	def view_path(self,start_dp):
		directory = 'data/0525'
		self = StatePath('X',directory)
		
		dp = start_dp
		self.wo.bt = Button(self.wo.win, Point( (X-50),(Y-30)), 60, 25,'==>')

		while True:
			file = self.directory + '/ifile' + str(dp) + '.png'
			print(file)
			try:
				PIL.Image.open(file)
			except:
				FileNotFoundError
				return

			in_window(X/2,Y/2,file,self.wo.win)

			dp += 1
			self.wo.bt.draw()
			self.wo.bt.wait()


	
	def	states_from_location(self):
		
		with open(sp.location_data_file, 'r') as f:  
			data = f.read()

		data = data.split('\n')
		data = data[1:-1]
		self.init_button(self.wo.win)
		for item in data:
			item = item.split(',')
			dp,cx,cy,dw = item
			dp,cx,cy,dw = int(dp),float(cx),float(cy),float(dw)
			st = State(sp,dp)
			print('State',dp,end=' ')
			st.create_image_from_location(dp,cx,cy,dw)
			st.store_huefile(dp)
			st.store_image(dp)

			self.bt.draw()
			self.bt.wait()
			self.bt.deactivate()

	def graph_state(self,st,dp):
		hg = HueGraph(1,dp)
		st.graph_image = hg.color_frequency_graph()
		st.graph_image_filename = 'data/0523_' + str(dp) + '.png'
		st.graph_image.save(st.graph_image_filename)

		# wd_graph = st.graph_image.width
		# wd_win = self.wo.win.width
		in_window(2.25*X,Y/2,st.graph_image_filename,self.wo.win)


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

	
class Task():
	def __init__(self,name,graph,dp) -> None:
		self.name = name
		self.graph = False
		self.dp = dp
		self.taskLst = [
			'create new states'
			'view states'
			're_create in large size'
		]

if __name__ == "__main__":
	tsk = Task('view states',False,5)
	tsk = Task('create states',False,0)


	if tsk.name=='view states':
		sp = StatePath('X','data/0525')
		sp.view_path(tsk.dp)
		sp.wo.win.getMouse()


	elif tsk.name=='create states':	
		dp = tsk.dp	
		sp = StatePath('X','data/0526',dp)
		file_name = 'data/0526/loc_data.txt' 
		sp.erase_file_contents('data/0526/loc_data.txt' )
		sp.zoom_loop(dp)

	

	elif tsk.name=='create state from location':
		dp = 3
		sp = StatePath('X','data/0525')
		st = State(sp,dp)
		cx,cy,dw =  0.15041053520754566,-0.5857989914681447,0.0241929638534831
		dp = 3
		st.create_image_from_location(cx,cy,dw,dp)
		sp.wo.win.getMouse()
