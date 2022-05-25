# histogram19.py works with select19.
# histogram20.py new graph type so each color has its own bar

from math import log10
from modulefinder import LOAD_CONST
from re import T
from unittest.mock import PropertyMock

import numpy as np
import colorsys  
from PIL import ImageDraw,ImageFont
import PIL.Image,PIL.ImageDraw
from helpers import *
from graphics import *
from colorsys import rgb_to_hsv, hsv_to_rgb
from ruler0 import Ruler
from helpers import *
from window_object1 import WindowObject

# graph_image_fileB1.png

import inspect

myself = lambda: inspect.stack()[1][3]       

X,Y = Ruler.X,Ruler.Y


class HueGraph:

	def __init__(self,dp) -> None:
		self.dp = dp
		self.process_raw_file()

	def get_hues_from_image(self,dp):
		hueLst = []
		imagefile = 'data/image_fileB' + str(dp) + '.png'
		img = PIL.Image.open(imagefile)
		px = img.load()
		for x in range(X):
			for y in range(Y):
				r,g,b = px[x,y]
				hue,sat,val = rgb_to_hsv(r,g,b)
				hueLst.append(hue)
		return hueLst

	@staticmethod
	def string_to_list_float(str,n):
		str = str[1:-1]   #remove outer brackets
		lst = str.split(', ')
		# round to n bins in 0-1 region
		lst = [round(float(l),n) for l in lst]
		return(lst)

	def process_raw_file(self):
		self.text_file = 'data/text_fileB'+str(self.dp) + ".txt"
		with open(self.text_file,"r") as f:
			hueStr = f.read()
		lst = string_to_list(hueStr)
		self.hueLst =  [float(l) for l in lst]

	def color_frequency_graph(self):
		self.process_raw_file()

		self.calc_graph_numbers()

		# draw graph
		self.data_bars()
		self.description()
		self.y_scale_labels()

		return self.im

	def calc_graph_numbers(self):
		self.hueDic = count_frequency(self.hueLst)
		self.n_hues = len(self.hueDic)
		self.all_pixels = X*Y
		self.graph = sorted( list( self.hueDic.items())  )

		width = int( Ruler.winX -Ruler.X )
		self.im = PIL.Image.new("RGB", (width,Y), (255, 255, 255))

	def data_bars(self):
		draw = PIL.ImageDraw.Draw(self.im)
		self.y_unit = Y/6
		self.x_offset = 35

		i = 0
		vmax = 0
		for (k,v) in self.graph:
			draw_pnt = self.y_unit*(log10(v))  # y coord
			hue = k						# bar color
			x = i						# x coord  does not equal hue, but count(hue)
			x = self.x_offset + x
				
			r,g,b = colorsys.hsv_to_rgb(hue,1,1)
			r,g,b = int(255*r),int(255*g),int(255*b)

			draw.line((x,Y-draw_pnt)+(x,Y),fill=(r,g,b),width=1)
			i += 1
			
	
			
		# end of bars for interior pixels  last bar in graph

		self.interior_pixels = v
		draw.line((x,Y-draw_pnt)+(x,Y),fill=(r,g,b),width=3)
	
		self.exterior_pixels = self.all_pixels - self.interior_pixels

		self.draw_all_pixels_line()

	def draw_all_pixels_line(self):
		draw = PIL.ImageDraw.Draw(self.im)
		# line for all_pixels level in graph
		wd = self.im.width
		y = Y-self.y_unit*(log10(X*Y))
		draw.line((self.x_offset,y)+(wd,y),fill=Ruler.interior, width=4)

	def y_scale_labels(self):
		image_width = self.im.width

		draw1 = PIL.ImageDraw.Draw(self.im)
		font = ImageFont.load_default().font
		font = ImageFont.truetype("Verdana.ttf",18)

		# y_axis line
		draw1.line((self.x_offset,0)+(self.x_offset,Y),fill='black')  # mark zero point
		# y axis labels
		for i in range(7):
			draw1.text((self.x_offset-15, Y-i*Y/6),str(i),(0,0,0),font=font)

	def description(self):
		draw = PIL.ImageDraw.Draw(self.im)
		font = ImageFont.load_default().font
		font = ImageFont.truetype("Verdana.ttf",18)

		self.exterior_pixels = self.all_pixels - self.interior_pixels
		self.calc_log_pixels()
	

		draw.text((50,10),"State " + str(self.dp) + "   # Hues " + str(self.n_hues) \
			+ "  # Pixels:  Total " + sci_not(self.all_pixels) + ' (5.4)  Exterior ' \
				   + str(sci_not(self.exterior_pixels)) + ' (' + self.logexterior\
			+ ")  Interior " + str(sci_not(self.interior_pixels)) + ' (' + self.loginterior +')'  \
			,(0,0,0),font=font)

	def calc_log_pixels(self):
		if self.interior_pixels > 1:
			self.loginterior = str(round( log10(self.interior_pixels), 1) )
		else: 
			self.loginterior = 'undefined'
		if self.exterior_pixels > 1:
			self.logexterior = str( round( log10(self.exterior_pixels), 1) )
		else: 
			self.logexterior = 'undefined'


class Viewer(WindowObject):
	def __init__(self, label):
		super().__init__(label)

	def show_image_file(self,imfile):
		print(myself())
		print(imfile)
		try:
			im = PIL.Image.open(imfile)
		except:
			FileNotFoundError

		in_window(X/2,Y/2,imfile,m.vw.win)

	def show_graph_file(self,dp):
		file = 'data/movie_sequence/graph_image_fileB' + str(dp) + '.png'
		print(file,end=' ')
		try: 
			PIL.Image.open(file)
			in_window(2.25*X,Y/2,file,vw.win)
	
		except:
			FileNotFoundError
			print('not found',end='')
		print()
		
	def thumbnails(self):
		dp = 0
		while True:
			self.make_thumbnail(dp)
			# vw.win.getMouse()
			dp += 1

class Menu(WindowObject):
	def __init__(self, label,seq):
		self.label = label
		self.seq = seq
		super().__init__(label)

	# @property
	def image_file(self,seq,typ):
		if seq==0:
			dir = 'data/sequence_baby_mand'
		elif seq==1:
			dir = 'data/movie_sequence' 
		elif seq==2:
			dir = 'data/varied_path'
		if typ=='image':
			ext = '/image_fileB'
		elif typ=='tnail':
			ext = '/thumb'
		else:
			ext = '/thumb'
		stem = dir + ext
		return stem, dir


	def place_tnails(self):
		self.win.setCoords(-0.5,-0.5,3.5,4.5)
		stem,dir = self.image_file(1,'thumb')
		for p in range(len(self.fLst)):
			thfile = stem + str(p+2) + '.png'
			print(thfile)
			try: 
				img = PIL.Image.open(thfile)
			except:
				FileNotFoundError
				return
			# tnail coords and dp
			j,i = 4 - p//4, p%4
			in_window(i ,j,thfile,m.win)
			Text(Point(i,j),str(p+2)).draw(m.win).setFill('white')

	def select_tnail(self):
		while True:
			clk = m.win.getMouse()
			cx,cy = clk.x,clk.y
			ci = Circle(Point(cx,cy),0.04).draw(m.win)

			n = len(self.fLst)
			for p in range(n-2):
				j,i = 4 - p//4, p%4
				if abs(cx-i) < 0.3 and abs(cy-j) < 0.3:
					ci.setFill('cyan')
					imfile = image_file(self.seq,'tnail')
					print(p+2,imfile)
					return imfile

	def file_list(self,dir_name='data/movie_sequence'):
		self.fLst = []
		for f in os.listdir(dir_name):
			if f.startswith('image_file'):
				self.fLst.append(f)
		print(self.fLst)

	def make_thumbnail(self,dp):
		# self.dir = self.dir1
		self.imfile = self.image_file(1,'tnail')
		if hasattr(self,'thfile'):
			return
		
		try: 
			img = PIL.Image.open(self.imfile)
		except:
			FileNotFoundError
			return
		
		self.thfile = self.dir + self.thext + str(dp) + '.png'
		img.thumbnail((100,100))
		img.save(self.thfile)

	def interact(self):
		# self.dir =self.dir1
		while True:
			imfile = m.select_tnail()
			m.vw.show_image_file(imfile)

if __name__ == "__main__":
	m = Menu('M',1)
	m.vw = Viewer('X')
	# m.sequence_files()
	m.file_list('data/movie_sequence')  
	for dp in range(len(m.fLst)):
		m.make_thumbnail(dp)
	m.place_tnails()
	m.interact()  # select then show



	exit()
	
