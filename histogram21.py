# histogram19.py works with select19.
# histogram20.py new graph type so each color has its own bar

from math import log10
from modulefinder import LOAD_CONST
from re import T

import numpy as np
import colorsys  
from PIL import ImageDraw,ImageFont
import PIL.Image,PIL.ImageDraw
from helpers import *
from graphics import *
from colorsys import rgb_to_hsv, hsv_to_rgb
from ruler0 import Ruler
from helpers import *

# graph_image_fileB1.png

import inspect

myself = lambda: inspect.stack()[1][3]       

X,Y = Ruler.X,Ruler.Y
stem = '/Users/jillwellman_sept09_2012/Desktop/Python/my-python-project/draw_zoom_may5/'


class HueGraph:

	def __init__(self,dp) -> None:
		self.dp = dp

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
		# calc graph points
		self.hueDic = count_frequency(self.hueLst)
		self.n_hues = len(self.hueDic)
		self.all_pixels = X*Y

		self.graph = sorted( list( self.hueDic.items())  )

		self.im = PIL.Image.new("RGB", (2*X,Y), (255, 255, 255))

		self.data_bars()
		self.description()

		self.y_scale_labels()

		# if __name__=='main': self.im.show()
		
		return self.im

	
		

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

			if i<10:
				if v > vmax:
					vmax = v
				
			r,g,b = colorsys.hsv_to_rgb(hue,1,1)
			r,g,b = int(255*r),int(255*g),int(255*b)

			draw.line((x,Y-draw_pnt)+(x,Y),fill=(r,g,b),width=1)
			i += 1
		print(self.dp,'vmax1',vmax, round( log10(vmax),2) )

		# end of bars for interior pixels  last bar in graph

		self.interior_pixels = v	
		self.exterior_pixels = self.all_pixels - self.interior_pixels



		# print(self.all_pixels,self.interior_pixels,self.exterior_pixels)
		draw.line((x,Y) + (x,Y-draw_pnt), width=3,fill=Ruler.interior)  #interior bar in graph

		# line for all_pixels ht in graph
		wd = self.im.width
		y = Y-self.y_unit*(log10(X*Y))
		draw.line((0,y)+(wd,y),fill=Ruler.interior, width=2)

		draw.line((self.x_offset-5,0)+(self.x_offset-5,Y),fill='black')  # mark zero point

	def y_scale_labels(self):
		image_width = self.im.width

		draw = PIL.ImageDraw.Draw(self.im)
		font = ImageFont.load_default().font
		font = ImageFont.truetype("Verdana.ttf",14)

		draw.line((self.x_offset,0)+(self.x_offset,Y),fill='black')  # mark zero point
		# y axis labels
		for i in range(7):
			draw.text((self.x_offset-10, Y-i*Y/6), str(i),fill='black')


	def description(self):
		draw = PIL.ImageDraw.Draw(self.im)
		font = ImageFont.load_default().font
		font = ImageFont.truetype("Verdana.ttf",18)

		self.exterior_pixels = self.all_pixels - self.interior_pixels
		
		loginterior = round( log10(self.interior_pixels), 1)
		logexterior = round( log10(self.exterior_pixels), 1)

		draw.text((50,10),"State " + str(self.dp) + "   # Hues " + str(self.n_hues) \
			+ "  # Pixels:  Total " + sci_not(self.all_pixels) + ' (5.4)  Exterior ' \
			       + str(sci_not(self.exterior_pixels)) + '   (' + str(logexterior)\
			+ ")  Interior " + str(sci_not(self.interior_pixels)) + '   (' + str(loginterior) +')'  \
			,(0,0,0),font=font)

		

		# if __name__=="name": 
		# 	self.im.show()
		# 	exit()

		
if __name__ == "__main__":	

	def hueLst_to_display(dp):
		hg = HueGraph(dp)
		hg.process_raw_file()
		hg.color_frequency_graph()
		hg.im.show()

	for dp in range(2,10):
		hueLst_to_display(dp)




	exit()
	
