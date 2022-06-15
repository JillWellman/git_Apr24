# graph1.py
"""pairing with click_draw streamlined select_zoom_draw"""

from math import log10
import numpy as np
import colorsys  
from PIL import ImageDraw,ImageFont
import PIL.Image,PIL.ImageDraw
from collections import Counter 
import itertools
from helpers import *
from graphics import *
from colorsys import rgb_to_hsv, hsv_to_rgb
from ruler0 import Ruler
from helpers import *
from window_object1 import WindowObject

import inspect

myself = lambda: inspect.stack()[1][3]       

X,Y = Ruler.X,Ruler.Y
# datadir2 = Ruler.datadir2

def Sort_Tuples(tup):
 
    reverse = None    #(Sorts in Ascending order)
    # key is set to sort using second element of
    # sublist lambda has been used
    tup.sort(key = lambda x: x[0])
    return tup
 
 
# printing the sorted list of tuples
# print(Sort_Tuple(tup))


class HueGraph:
	"""Converts pixel hues to graph bars showing #pixels with that hue
	reports # different hues produced, finds number of pixels in figure interior
	draws graph and reports info"""

	def __init__(self,dp) -> None:
		self.dp = dp
		self.gfile = 'data/june14/gfile' + str(dp) + '.png'

		gr = 200
		self.img = PIL.Image.new("RGB", (int(3*X),Y), (gr,gr,gr))
		self.img.save(self.gfile)
		
	def frequency_core(self,dp):
		print(myself(),dp)

		# draw y_scale and set spacing parameters
		self.xy_axes()
		# self.dictionary(dp)
		# self.data_bars(dp)

		
		# create bar graph object
		# self.time_list()

		# self.location_list()
		# cx,cy,dw = self.locLst[dp+1]
		# print(cx,cy)
		# Circle(Point(cx,cy),10).draw(self.parent.wo.win)

		# self.hue_list(dp)
		# if self.hue_list==[]: return
		if False:
			self.dictionary(dp)
			self.data_bars(dp)

			# pixel counts
			self.fifty_line()
			self.percent_interior()
			self.caption(dp)

			self.gfile = 'data/june14/gfile' + str(dp) + '.png'
			self.img.save(self.gfile)
			self.img.show()
			# in_window(X + 3*X/2,Y/2,self.gfile,self.parent.wo.win)
		
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

	def hue_list(self,dp):
		self.hfile = Ruler.datadir1+'/hfile' + str(dp) + '.txt'
		try:
			with open(self.hfile, "r+") as f:
				hStr = f.read()
			hLst = hStr.split(', ')
			hLst = hLst[2:-2]  # strip off parens
			hLst = [float(s) for s in hLst]
			self.hueLst =  [float(l) for l in hLst]
		except:
			FileNotFoundError
			self.hueLst = []

	def dictionary(self,dp):
		self.hue_dic = count_frequency(self.hueLst)
		self.n_hues = len(self.hue_dic)
		self.all_pixels = X*Y
		self.gr_list = sorted( list( self.hue_dic.items())  )
		# last values of hue,count in graph dictionary
		print(self.gr_list)
		self.x_max = self.gr_list[-1][0]
		self.count_interior = self.gr_list[-1][1]

	def data_bars(self,dp):
		print(myself())

		draw = PIL.ImageDraw.Draw(self.img)
		font = ImageFont.load_default().font
		font = ImageFont.truetype("Verdana.ttf",14)
		
		i = 0
		for (k,v) in self.gr_list:
			y= self.y_unit*(log10(v)) + self.y_offset  # y coord
			hue = k						# bar color
			x = i						# x coord  does not equal hue, but count(hue)
			x = x + 5+ self.x_offset  # 5 x from y axis
				
			r,g,b = colorsys.hsv_to_rgb(hue,1,1)
			r,g,b = int(255*r),int(255*g),int(255*b)

			draw.line((x,Y-y-self.y_offset)+(x,Y-self.y_offset),fill=(r,g,b),width=1)  # 10 px space beside axis
			i += 1
		
		print('\ninterior data -- final data bar')
		self.x_max = x
		self.count_interior = v

		self.img.show()

		print('x_max',self.x_max)
		print('count_interior=v',v)

	def xy_axes(self):
		
		print(myself())
		"""defines image and graph scale parameters and draws y axis"""
	
		self.y_unit = 0.85*Y/6
		self.x_offset = 90  # left of y axis
		self.y_offset = 20 # lower margin


		draw = PIL.ImageDraw.Draw(self.img)
		font = ImageFont.load_default().font
		font = ImageFont.truetype("Verdana.ttf",14)

		draw.line((0,0) + (X,Y),fill = 'magenta')
		
		# y_axis line
		draw.line((self.x_offset,0)+(self.x_offset,Y),fill='black')  # mark zero point
		# y axis labels
		for i in range(7):
			draw.text((self.x_offset-75, Y-i*self.y_unit-self.y_offset),str(comma_not(10**i)),(0,0,0),font=font,align='right')
		# x axis labels
		for i in range(4):
			draw.text((self.x_offset+ i*2.5*X/3, Y-self.y_offset),str(round(i/3,2)),(0,0,0),font=font)

		self.img.show()
		self.img.save('data/june14/gfile' + str(dp) + '.png')

	def save_show(self,dp):
		# self.img.show()
		print(myself())
		self.gfile = Ruler.datadir2 + 'gfile' + str(dp) + '.png'
		# print(self.gfile)
		self.img.save(self.gfile)
		
	def fifty_line(self):	
		print(myself())
		fifty = Y - self.y_unit*log10(X*Y/2) - self.y_offset   # height of 50% line

		# print('fifty series',log10(100000),log10(X*Y/2),fifty,log10(X*Y),log10(1000000))
		# print('fifty plot', self.y_unit*log10(X*Y/2) + self.y_offset)
		fifty = round( Y - ( self.y_unit*log10(X*Y/2) + self.y_offset ), 0 )

		draw = PIL.ImageDraw.Draw(self.img)
		font = ImageFont.load_default().font
		font = ImageFont.truetype("Verdana.ttf",18)

		pos0 = self.x_offset,fifty
		pos1 = self.x_max,fifty
		draw.line(pos0 + pos1,fill='lightgray',width=1)

	def percent_interior(self):
		# print(myself())

		# print('---')
		count_interior = self.gr_list[-1][1]  # v in last value of (k,v)
		# print('fifty',X*Y/2,'\t\t',log10(X*Y/2))
		print('count_interior',comma_not(self.count_interior), '\t',log10(self.count_interior))

		self.percent_interior = 100 * self.count_interior/(X*Y)
		# print(self.count_interior,self.percent_interior*X*Y/100)
		# print('percent_interior',self.percent_interior )


	def location_list(self):
		
		tfile = 'data/June08Movie/# times.txt'  # time and location

		self.locLst = []
		try:
			with open(tfile, "r+") as f:
				tStr = f.read()
			tStr = tStr.replace("location","")
			tStr = tStr.replace(")",'')
			tStr = tStr.replace("(",'')

			tLst = tStr.split('\n')
			tLst = tLst[1:-1]
			# print('tLst',tLst)
		
			for elt in tLst: 
				eLst = elt.split(', ')
				locElt= eLst[1:]

				for e in locElt:
					e = float(e)
				# print(locElt)
				self.locLst.append(locElt);

			# for elt in self.locLst:
				# print('*',locElt)
				

		except:
			FileNotFoundError
			return

	def time_list(self):
		tfile = 'data/June08Movie/# times.txt'
		try:
			with open(tfile, "r+") as f:
				tStr = f.read()
			tLst = tStr.split('\n')
			tLst = tLst[1:-1]
			self.alltime =[]
			for elt in tLst: 
				eLst = elt.split(', ')
				eStr0 = eLst[0]
				eLst0 = eStr0.split(' ')
				self.alltime.append(float(eLst0[2]))
			# print(self.alltime)
	

		except:
			FileNotFoundError
			return


	def caption(self,dp):
		draw = PIL.ImageDraw.Draw(self.img)
		font = ImageFont.load_default().font
		font = ImageFont.truetype("Verdana.ttf",18)

		# time = round( self.alltime[dp], 1)

		txt_str = f"State {self.dp}  Number of Hues: {self.n_hues}.    Interior Pixels: {round(self.percent_interior,1)}%."  # Processing time =  {time} sec. "
		draw.text((110,30),txt_str ,(0,0,0),font=font)


		print(dp)
		print(self.locLst)  # is empty
		# displayLst = [ float(e) for e in self.locLst[dp] ]
		# # print('dp,locLst',displayLst)


		# txt_str2 = f"Location [center(x,y), region-width]: = {displayLst} "
		# draw.text((110,60),txt_str2 ,(0,0,0),font=font)
		
class Viewer(WindowObject):
	
	def __init__(self, label):
		self.label = label
		self.wo = WindowObject(label)

	def clk_ordered(self,dp):
		clk = self.wo.win.getMouse()
		cx,cy = clk.x,clk.y
		Circle(Point(cx,cy),10).draw(self.wo.win)
		if cx > X: dp += 1
		elif cx < X and dp > 0: dp -= 1
		return dp
	
		
	def show_image(self,dp):
		try:
			file = 'data/June14/ifile' + str(dp) + '.png'
			in_window(X/2,Y/2,file,self.wo.win)
		except:
			FileNotFoundError
	
	def show_graph(self,dp):
		try:
			file = 'data/June14/gfile' + str(dp) + '.png'
			in_window(X + 3*X/2,Y/2,file,self.wo.win)
		except:
			FileNotFoundError

	
		


# =================== Tasks ======================
if __name__ == "__main__":
	task = "click_show_all"
	task = "click_create_graphs"
	task = "show a graph"
	
	if task=='show a graph':
		vw = Viewer('G')
		
		dp = 0
		hg = HueGraph(dp)
		hg.frequency_core(dp)
		
		hg.gfile = 'data/june14/gfile' + str(dp) + '.png'
		hg.img.save(hg.gfile)
		hg.img.show()
		in_window(X + 3*X/2 + 10,Y/2,hg.gfile,vw.wo.win)
		vw.wo.win.getMouse()

	elif task=="click_create_graphs":
		vw = Viewer('G')
		dp = 0
		while True:
			vw.show_image(dp)
			vw.show_graph(dp)

			vw.hg = HueGraph(dp)  #vw = parent
			vw.hg.create_graph(dp)

			dp = vw.clk_ordered(dp)

	elif task=="click_show_all":
		vw = Viewer('G')
		dp = 0
		while True:
			vw.show_image(dp)
			vw.show_graph(dp)
			dp = vw.clk_ordered(dp)

			
			