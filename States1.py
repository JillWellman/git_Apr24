# click_draw.py
"""	quick draw from click on location.  """

import sys

from mandelbrot_code import MandelbrotCode
sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/myProjects/myModules')
sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/my-python-project')

import itertools
from PIL import Image, ImageFont, ImageDraw
import PIL
# import matplotlib.pyplot as plt
from math import log10
from colorsys import hsv_to_rgb
from pathlib import Path
# import matplotlib.pyplot as plt
# import os
from window_object1 import WindowObject
from button3 import *
# from mandelbrot_code import MandelbrotCode
from graphics import *
from mygraphics import *
from ruler0 import Ruler
from helpers import *
from graph1 import HueGraph

import inspect
myself = lambda: inspect.stack()[1][3]

X,Y = Ruler.X,Ruler.Y
maxIt = Ruler.maxIt  

class State():

	def __init__(self,path,location,dp) -> None:
		self.path =path
		self.dp = dp
		self.location = location
		self.ifile = 'data/june14/ifile' + str(dp) + '.png'
		self.gfile = 'data/june14/gfile' + str(dp) + '.png'

	def make_drawing(self,dp):
		print(myself())
		if dp <=1: sp = 2
		else: sp = 1
		zsel = box_from_center(*self.location)
		self.trxz = Transform(X,Y,*zsel)

		start = time.time()
		mn = MandelbrotCode()
		mn.mandelbrot_core(self.trxz,sp)
		self.time = round( (time.time() - start),2 )
		
		self.hueLst = mn.hueLst
		self.image = mn.img
		self.image.save(self.ifile)	
		
	def data_bars(self,dp):
		"""encapsulated module for getting data bars out of hue list"""
		print('\n',myself())
		if dp <=1: sp = 2
		else: sp = 1
		y_unit = 0.85*Y/6
		x_offset = 90  # left of y axis
		y_offset = 20 # lower margin

		draw1 = PIL.ImageDraw.Draw(self.img)
		
		hdic = count_frequency(self.hueLst)
		hLst = [ (k,v) for k,v in hdic.items() ]
		hLst.sort()
		self.nhues = len(hLst)
		# print(hLst)

		# i = 0
		for (k,v) in hLst:
			y= self.y_unit*(log10(v)) + self.y_offset  # y coord
			hue = float(k)						# bar color
			x = int(maxIt*hue)					# x coord  does not equal hue, but count(hue)
			x = x + 5+ self.x_offset  # 5 x from y axis
				
			clr = colorsys.hsv_to_rgb(hue,1,1)
			r,g,b = [int(255*c) for c in clr]

			draw1.line((x,Y-y-self.y_offset)+(x,Y-self.y_offset),fill=(r,g,b),width=1)  # 10 px space beside axis

		self.min_hue = hLst[0][0]
		int_pixels = hLst[-1][1]
		self.pc_int_pix = int( 100*int_pixels/(X*Y*sp*sp) )

	def description(self,dp):
		print(myself())
		# show elapsed time.  move all lines to left 

		draw = PIL.ImageDraw.Draw(self.img)
		font = ImageFont.load_default().font
		font = ImageFont.truetype("Verdana.ttf",18)

		# y_axis line
		txt_str0 = f"State {dp}, elapsed time {self.time}, % internal pixels {self.pc_int_pix}"
		txt_str1 = f"location {self.location}"
		txt_str2 = f"# hues {self.nhues}, minimum hue {self.min_hue}, maxIt {maxIt}"
		draw.text((125,10),txt_str0,font=font,fill='blue')
		draw.text((125,30),txt_str1,font=font,fill='blue')
		draw.text((125,50),txt_str2 ,font=font,fill='blue')

	def make_graph(self,dp):
		print(myself())
		# create image
		gr = 200
		self.img = PIL.Image.new("RGB", (int(2*X),Y), (gr,gr,gr))
		self.img.save(self.gfile)

		self.xy_axes()
		self.data_bars(dp)
		self.img.save(self.gfile)
		self.description(dp)
		self.img.save(self.gfile)

	def clk_show_image(self,dp):
		self.ifile.show

	def clk_ordered(self,dp):
		clk = self.wo.win.getMouse()
		cx,cy = clk.x,clk.y
		Circle(Point(cx,cy),10).draw(self.wo.win)
		if cx > X: dp += 1
		elif cx < X and dp > 0: dp -= 1
		return dp

	def xy_axes(self):
		print(myself())
		"""defines image and graph scale parameters and draws y axis"""
		gr = 200


		self.y_unit = 0.85*Y/6
		self.x_offset = 90  # left of y axis
		self.y_offset = 20 # lower margin
		xaxlen = 800

		y_unit = 0.85*Y/6
		x_offset = 90  # left of y axis
		y_offset = 20 # lower margin



		draw = PIL.ImageDraw.Draw(self.img)
		font = ImageFont.load_default().font
		font = ImageFont.truetype("Verdana.ttf",14)

		# y_axis line
		draw.line((self.x_offset,0)+(self.x_offset,Y),fill='black')  # mark zero point
		# y axis labels
		for i in range(7):
			draw.text((self.x_offset-75, Y-i*self.y_unit-self.y_offset),str(comma_not(10**i)),(0,0,0),font=font,align='right')
		xg = X + 10 + 4*X
		for i in range(1,7):
			draw.text((xaxlen+100, Y-i*self.y_unit-self.y_offset),str(comma_not(10**i)),(0,0,0),font=font,align='right')# x axis labels
		for i in range(4):
			draw.text((self.x_offset+ i*xaxlen/3, Y-self.y_offset),str(round(i/3,2)),(0,0,0),font=font)
		
class StatePath():

	def __init__(self):
		self.wo = WindowObject('G')

	def click_loop(self):
		r = 10
		"""path space holds window, displays states, and accepts clicks"""
		location = -0.5,0,3  # inital state
		dp = 0

		st = State(self,location,dp)

		st.make_drawing(dp)
		st.make_graph(dp)
		self.image_placement(st)
		
		self.wo.win.getMouse()

		# select
		self.wo.graphic = Circle(Point(0,0),2).draw(self.wo.win)
		
		while True:
			# ========= select ============
			clk = self.wo.win.getMouse()
			cx,cy=clk.x,clk.y
			if cx >= X-10: continue  # ignores click outside of image
			self.wo.graphic.undraw()
			self.wo.graphic = Circle(Point(cx,cy),r).draw(self.wo.win)
			st.image.save(st.ifile)

			# permanent click mark on state images
			draw = PIL.ImageDraw.Draw(st.image)
			draw.ellipse((cx-r, cy-r, cx+r, cy+r), outline=(0,0,0),width=1)
			st.image.save(st.ifile)

			# ===== location next state =====
			dw = st.location[2]/5
			zx,zy = st.trxz.world(cx,cy)
			location = zx,zy,dw
			dp += 1
			st = State(pth,location,dp)
			st.make_drawing(dp)
			st.make_graph(dp)
			self.image_placement(st)

	def clk_show(self):
		dp = 0
		while True:
			ifile = 'data/june14/ifile' + str(dp) + '.png'
			in_window(X/2,Y/2,ifile,self.wo.win)
			try:
				im = PIL.Image.open(ifile)
			except:
				FileNotFoundError
				return

			gfile = 'data/june14/gfile' + str(dp) + '.png'
			in_window(X+10 + 2*X/2,Y/2,gfile,self.wo.win)
			self.wo.win.getMouse()
			
			dp += 1

	def image_placement(self,st):
		in_window(X/2,Y/2,st.ifile,self.wo.win)
		in_window(X+10 +  (2*X)/2, Y/2,st.gfile,self.wo.win)

	def init_button(self,win):
		self.bt = Button(win, Point( 460, 480), 70,30,'==>')
		self.bt.label.setSize(24)
		self.bt.draw()
		self.bt.activate()

if __name__ == "__main__":
	task = 'show'
	pth = StatePath()
	if task=='make':
		pth.click_loop()
	elif task=='show':
		pth.clk_show()

