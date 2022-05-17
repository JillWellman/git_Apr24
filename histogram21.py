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

	def __init__(self,dp,hueLst) -> None:
		self.dp = dp
		self.hueLst = hueLst
		
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

	def check_counts(self,dp):
		print(sci_not(500*500), '500 squared')
		print('hueLst length',sci_not(len(self.hueLst)))
		print('10 exp5, top of graph, 10**5',sci_not(10**5))

	def key_numbers(self):
		print('\nn_colors/width',len(self.hueDic))
		print('max value / height', sci_not(max( list( self.hueDic.values() ))))


	def color_frequency_graph(self,dp,hueLst):
		self.hueLst = hueLst
		self.dp = dp
		
		self.hueDic = count_frequency(self.hueLst)
		self.ncolors = len(self.hueDic)
		print('ncolors',self.ncolors)
		# print(self.hueDic,len(self.hueDic))
		# self.key_numbers()

		self.graph = sorted( list( self.hueDic.items())  )

		self.data_bars()
		self.description()
		self.axes()
		return self.im

	def data_bars(self):
		self.x_offset,self.y_offset = 35,15
		self.extension = 300
		y_unit = Y/6
		x_unit = 500
		
		
		self.im = PIL.Image.new("RGB", (self.extension+int(3.5*X)+self.x_offset,Y), (255, 255, 255))
		draw = PIL.ImageDraw.Draw(self.im)

		i = 0
		# plotting values
		for (k,v) in self.graph:
			count = y_unit*(log10(v))  # y coord
			hue = k						# bar color
			x = i						# x coord (2 pix/hue)
			x = self.x_offset + x

			r,g,b = colorsys.hsv_to_rgb(hue,1,1)
			r,g,b = int(255*r),int(255*g),int(255*b)
			draw.line((x,Y-count)+(x,Y),fill=(r,g,b),width=1)
			i += 1


		lastbar = [x, log10(self.graph[-1][1])]
		print('lastbar',lastbar)
		xya = x,Y*y_unit
		xyb = x,Y-lastbar[1]*y_unit
		draw.line(xya + xyb, width=2,fill='magenta')
	

	def axes(self):
		image_width = self.im.width

		draw2 = PIL.ImageDraw.Draw(self.im)
		font = ImageFont.load_default().font
		font = ImageFont.truetype("Verdana.ttf",24)
		



		y = log10(X*Y) # total pixels
		draw2.line((self.x_offset,Y - y*Y/6) + (image_width,Y - y*Y/6),fill= 'magenta',width=2)  # one bar = total pixels
		line_label = str(round( y,2) )
		draw2.text((self.x_offset,Y - y*Y/6), line_label,fill = 'blue')

		draw2.line((self.x_offset,0)+(self.x_offset,Y),fill='black')  # mark zero point
		# y axis labels
		for i in range(7):
			draw2.text((self.x_offset-10, Y-i*Y/6), str(i),fill='black')

	def description(self):
		draw = PIL.ImageDraw.Draw(self.im)
		font = ImageFont.load_default().font
		font = ImageFont.truetype("Verdana.ttf",24)

		n_hues = sci_not( len(self.hueDic) )
		max_hue_count = max(list(self.hueDic.values())) 
		log_max_count = round(log10(max_hue_count),2)
		max_hue_count = sci_not(max_hue_count)


		draw.text((100,0),"State " + str(self.dp) + "   Number of Hues " + str(n_hues) \
			+ "  Max hue count " + str(max_hue_count) + '    (' + str(log_max_count)+')' \
			,(0,0,0),font=font)

		y = log10(X*Y)
		line_label = str(round(y ,2) )
		draw.text((self.x_offset,Y - y*Y/6), line_label,fill = 'magenta')


		
if __name__ == "__main__":	

	def hueLst_to_display(dp):
		# img = PIL.Image.open('data/graph_image_fileB'+str(dp) + '.png')
		# img.show()
		hue_text_file = 'data/text_fileB'+str(dp) + ".txt"
		with open(hue_text_file,"r") as f:
			hueStr = f.read()
		lst = string_to_list(hueStr)
		hueLst = [float(l) for l in lst]
		hg = HueGraph(dp,hueLst)
		hg.color_frequency_graph(dp,hueLst)
		hg.im.show()


	for dp in range(9,10):
		hueLst_to_display(dp)



	exit()
	
