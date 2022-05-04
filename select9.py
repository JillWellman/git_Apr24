# select9.py
"""	select9  add hueLst sort --> dict make scatterplot
	select8 zooming seems great.  hueLst can collect hues
	select7 zooming seems accurate / upside down bug cured
	select6 builds on skeleton select wherre I demo how to recursively select regions
	select5 clean up and commit to git
	SelectSeries draw_whole draws initial state.  reorganize to Select
	select 4c sequential process for xsel and zsel through zooms
	select4b going back to pixel coord z-coord Transforms too confusing
	select.2 switching from class to instance methods"""

import sys
sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/my-python-project/myImports')
sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/myProjects/myModules')
from PIL import Image
import PIL
from graphics import *
from mygraphics import *
import time

from window_object import WindowObject
from button3 import *
# from zoom_draw3 import MyImage
from helpers import *
# from draw3 import Draw

import inspect
myself = lambda: inspect.stack()[1][3]

from ruler0 import Ruler

X,Y = Ruler.X,Ruler.Y
zX,zY = Ruler.zX,Ruler.zY
maxIt0 = 100  # may need to change with multiple zooms

# def show_image_filex(dp,label,win):  # from label symbol
# 	file_name = SelectSeries.file_stub+str(dp) + '.png'
# 	self.image.save(file_name)
# 	if label=='X':
# 		in_window(X/2,Y/2,file_name,win)
# 	elif label=='Z':
# 		in_window(-0.5,0,file_name,win)


class Select(Ruler):
	
	def __init__(self,parent,dp) -> None:
		self.dp = dp
		self.parent = parent

	def select(self):
		"""select box region with cursor  Confirm with ==> button"""
		# print(myself())
		bx = Circle(Point(0,0),1).draw(self.parent.woX.win)  #dummy for undraw
		bx_drawn = False   	  				 # only dummy drawn
		while True:
			if bx_drawn: self.parent.bt.activate()
			c = self.parent.woX.win.getMouse()
			if self.parent.bt.clicked(c) and bx_drawn: break
			self.cx,self.cy,self.wd = c.x,c.y,Ruler.xside2
			self.xsel = box_from_center(self.cx,self.cy,self.wd)
			bx.undraw()
			bx = rec_draw(self.xsel,self.parent.woX.win)
			bx_drawn = True

	def darkgray_circles(self):
		xdr = Select.xside2/20 
		zdr = self.trxz.xscale*2*xdr  # xdr * zxscale
		xsel,zsel = self.xsel,self.zsel
		Circle(Point(zsel[0],zsel[1]),zdr).draw(self.parent.woZ.win).setFill('darkgray')
		Circle(Point(xsel[0],xsel[1]),xdr).draw(self.parent.woX.win).setFill('darkgray')

class SelectSeries(Ruler):
	file_stub = 'images/hsb'
	LIST = False
	hueLst = []

	def __init__(self) -> None:
		self.woX = WindowObject('X',X,Y)
		self.woZ = WindowObject('Z',X,Y)
		self.woC = WindowObject('C',X,Y)
		self.zsel= Ruler.gzbox

		self.implement()

	def implement(self):
		dp = 0
		self.init_windows(dp)
		self.init_button(self.woX)
		if SelectSeries.LIST: hueLst = []
		self.zoom_loop()

	def zoom_loop(self):
		dp = 0
		self.bt.deactivate()
		while True:
			s = Select(self,dp)
			s.select()
			self.bt.deactivate()
			self.xsel = s.xsel
			self.get_zsel()
			maxIt = int(maxIt0*(1 + (dp/4)**2))  # worked into 20's

			dp += 1
			self.print_stats(dp)
			print('maxIt',maxIt)
			self.draw_image(dp,self.trxz)
			if dp >=1: self.save_show_window(dp,'C')
			rec_draw(s.xsel,self.woC.win).setOutline('blue')
			self.save_show_window(dp,'X')
			
			self.bt.draw()
			
	def get_zsel(self):
		# print(myself())
		if not hasattr(self,'zsel'):
			self.zsel = Ruler.gzbox
		self.trxz = Transform(X,Y,*self.zsel)
		

		xsel = self.xsel
		xa,ya,xb,yb = self.trxz.world(xsel[0],xsel[1]) + self.trxz.world(xsel[2],xsel[3])
		self.zsel  = min(xa,xb),min(ya,yb),max(xa,xb),max(ya,yb)
		
		rec_draw(self.zsel,self.woZ.win)

		self.trxz = Transform(X,Y,*self.zsel)

	def draw_image(self,dp,trxz):
		"""draws part of image mapped by trxz from zsel onto gscreen"""
		print(myself(),'trxz',trxz)
		if SelectSeries.LIST: self.hueLst = []

		sp = 1

		start_time = time.time()

		self.image = PIL.Image.new('RGB', (X,Y), color = (255,255,255))
		self.image.pixels = self.image.load() 

		for x in range(0,X,sp):
			for y in range(0,Y,sp):
				# self.image.pixels[x,y] = mandelbrot_edges(*trxz.world(x,y),maxIt)
				hue = mandelbrot(*trxz.world(x,y),maxIt0)
				if SelectSeries.LIST: 
					SelectSeries.hueLst.append(hue)
				r,g,b = colorsys.hsv_to_rgb(hue,1,1)
				r,g,b = int(255*r),int(255*g),int(255*b)
				self.image.pixels[x,y] =  r,g,b
				#  use for debugging coord systems
				#  Point(*self.trxz.world(x,y)).draw(self.parent.woZ.win).setOutline(color_rgb(r,g,b))
				#  Point(x,y).draw(self.parent.woX.win) 
			pass
		
		if SelectSeries.LIST: 
			with open (text_filename, 'w') as f:
				f.write(str(SelectSeries.hueLst))
		elapsed_time = time.time() - start_time
		print('elapsed_time',round(elapsed_time,2))
		
	def save_show_window(self,dp,win):
		# print(myself(),win)
		self.file_name = SelectSeries.file_stub+str(dp) + '.png'
		if not hasattr(self,'image'): print('no image')
		else:
			self.image.save(self.file_name)
			if win=='X':
				in_window(X/2,Y/2,self.file_name,self.woX.win)
			elif win=='Z':
				in_window(-0.5,0,self.file_name,self.woZ.win)
			elif win=='C':
				self.file_name = SelectSeries.file_stub+str(dp-1) + '.png'
				in_window(X/2,Y/2,self.file_name,self.woC.win)

		if win in ['X','C']:
			self.origin_marker(win)

	def print_stats(self,dp):
		print('\n',myself(),'---- depth',dp)
		print('xsel',round_all(self.xsel,0))
		print('zsel',round_all(self.zsel,4))
		print('zside',round((self.zsel[1] - self.zsel[0]),4) )
		if hasattr(self,'trxz'):
			print('trxz',self.trxz)
		if hasattr(self,'trxx'):
			print('trxx',self.trxx)

	def init_windows(self,dp):
		"""shows initial state in both windows"""
		dp = 0
		trxz = Transform(X,Y,*Ruler.gzbox)
		self.draw_image(dp,trxz)
		self.file_name = SelectSeries.file_stub + str(dp) + '.png'
		in_window(-0.5,0,self.file_name,self.woZ.win)
		in_window(X/2,Y/2,self.file_name,self.woX.win)
		self.origin_marker('X')
		self.origin_marker('Z')

	def origin_marker(self,win_label):
		if win_label in ['X','C']:
			Circle(Point(0,0),3*X/50).draw(self.woX.win).setFill('darkgray')
		elif win_label=='Z':
			Circle(Point(-2,-1.5),3*zX/50).draw(self.woZ.win).setFill('darkgray')

	def init_button(self,win):
		win = self.woX.win
		self.bt = Button(win, Point( 460, 480), 70,30,'==>')
		# self.bt.label.setSize(24)
		self.bt.draw()
		self.bt.activate()

			

if __name__ == "__main__":
	def draw_state0():
		ss = SelectSeries()
		ss.draw_whole()
		# show_image_file(0,'X',ss.woX.win)
		# show_image_file(0,'Z',ss.woZ.win)
		ss.image.save(SelectSeries.file_stub + '0.png')
		ss.woX.win.getMouse()

	# draw_state0()

	


	def zoom_sequence():
		dp = 0
		ss = SelectSeries()
		ss.init_windows(dp)
		ss.init_button(ss.woX)
		ss.zoom_loop()
		
	zoom_sequence()

