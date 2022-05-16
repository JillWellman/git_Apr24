# histograms17.py switching from graphics to PIL

from math import log10

import numpy as np
import colorsys  
from PIL import ImageDraw,ImageFont
import PIL.Image,PIL.ImageDraw
from helpers import *
from graphics import *
from colorsys import rgb_to_hsv, hsv_to_rgb
from ruler0 import Ruler
from helpers import *

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

	def string_to_list_float(self,str,n):
		str = str[1:-1]   #remove outer brackets
		lst = str.split(', ')
		# round to 10 bins in 0-1 region
		lst = [round(float(l),n) for l in lst]
		return(lst)



	def create_histogramZelle(self,dp):  # simple top level
		print('direct count hueLst',sci_not(len(self.hueLst)))
		self.dict = count_frequency(self.hueLst)
		print('len(self.dict), # color bins',len(self.dict))

		# create window
		self.winG = GraphWin('log10(Count Pixels)',2*X,Y)
		
		self.winG.setBackground('lightgray')
		# write depth number
		Text(Point(0.1,5.8),'Graph '+ str(dp)).draw(self.winG).setSize(18)
		self.axes()
		self.color_bars()
		self.winG.getMouse()

	def check_counts(self,dp):
		print(sci_not(500*500), '500 squared')
		print('hueLst length',sci_not(len(self.hueLst)))
		print('10 exp5, top of graph, 10**5',sci_not(10**5))


	def create_frequency_graph(self):
		self.count_pixels()
		graph_image = self.draw_graph()
		return graph_image
		

	def count_pixels(self):
		self.hueLst = [ round(hue,4) for hue in self.hueLst ]
		self.dict = count_frequency(self.hueLst)
		tplLst1 = [(k, v) for k, v in self.dict.items()]
		self.tplLst= sorted(tplLst1)  # tplLst sorted
		print('number of colors ',len(self.tplLst))
		print('---- maxHue,count(maxHue),log(count)',end=' ')
		print(self.tplLst)
		# print(self.tplLst[-1][0],sci_not(self.tplLst[-1][1]),round(log10(self.tplLst[-1][1]),2),'----') 
		
	def draw_graph(self):
		"""graph hue, count of pixels"""
		self.pixel_total = X*Y
		self.bin_count= 0  # total number of values in each bin

		im = PIL.Image.new("RGB", (X,Y), (255, 255, 255))
		draw = PIL.ImageDraw.Draw(im)
		self.pixel_count = 0
		self.color_count = 0
		for (k,v) in self.tplLst:
			self.pixel_count += v   # check sum of pixels
			self.color_count += 1
			hue =float(k) #+ 0.05  # hue at value for center of bar
			r,g,b = colorsys.hsv_to_rgb(hue,1,1)
			r,g,b = int(255*r),int(255*g),int(255*b)
			
			# pixel count for hue
			hue = int(500*k)  # hue in pixel plot units
			# count = 500 log(count)= 6
			zero_pt = 0
			draw.line((hue+zero_pt,Y)+(hue+zero_pt,Y-500/6*log10(v)),fill=(r,g,b),width=2)
	
			# y axis labels
			I1 = ImageDraw.Draw(im)
			for i in range(7):
				I1.text((X/100, Y-i*Y/6), str(i), fill=("black"),fontsize = 1)
		print('pixel count',sci_not(self.pixel_count))
		print('color count',self.color_count)
		print('pixel total',Ruler.X*Ruler.Y)

		y = log10(self.pixel_total)
		draw.line((0,Y - y*Y/6) + (X,Y - y*Y/6),fill= 'magenta')
		draw.line((0,0)+(0,Y),fill='black')  # mark zero point
			# check sum of pixels = pixel_total

		return im

	def axes(self):
		self.winG.setCoords(-0.03,-1.3,1.02, 6)
		# y_ticks  on top of left data bar
		for i in range(1,6):
			# Line(Point(0,i),Point(0.025,i)).draw(self.winG).setWidth(2)
			Text(Point(-0.01,i),str(i)).draw(self.winG).setSize(16)

		Text(Point(0.5,-1.0),'Hue/Wavelength').draw(self.winG).setSize(18)

		nbins = 10
		for i in range(nbins+1):
			Text(Point((i/nbins), -0.2),str(i/nbins)).draw(self.winG).setSize(16)
			wavelength = 700 - int(i*3*nbins)
			Text(Point((i/nbins), -0.6),str(wavelength)).draw(self.winG).setSize(16)

		



if __name__ == "__main__":	
	pass

	dp = 0
	hueLst = []
	hg = HueGraph(dp,hueLst)
	hg.color_bars()

	
	exit()
	
	dp = 0
	for dp in range(10):
		print(dp)
		print(hueLst[300:500])
		# text_file  = 'data/text_fileB'  + str(dp) + '.txt'
		graph_file = 'data/graph_fileB' + str(dp) + '.png'
		hg.color_bars()
		hg.check_counts(dp)



