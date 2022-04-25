# select3.py
"""	select5 clean up and commit to git
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

from window_object import WindowObject
from button3 import *
# from zoom_draw3 import MyImage
from helpers import *
from draw3 import Draw

import inspect
myself = lambda: inspect.stack()[1][3]

from ruler0 import Ruler

X,Y = Ruler.X,Ruler.Y

class Select(Ruler):
	file_stub = 'git_Apr24/images/hsb'
	
	def __init__(self,parent,dp) -> None:
		self.dp = dp
		self.parent = parent
		self.pt_win = self.parent.woZ.win

	def change_coords(self):
		"""illustrates effect of setCoords on box drawings"""
		print(myself(),end=' ')
		print(round_all(self.zsel,3))
		pt_win = self.parent.woZ
		pt_win.ctpl = Ruler.gzbox
		pt_win.win.setCoords(*pt_win.ctpl)  # initial coords
		rec_draw(self.zsel,pt_win.win).setOutline('magenta')

		print('CLICK')
		pt_win.win.getMouse()

		pt_win.win.setCoords(*self.zsel)   # coords of zsel
		pt_win.win.getMouse()

	def draw_selection(self,dp,trxz):
		"""draws part of image mapped by trxz from zsel onto gscreen"""
		print(myself(),'trxz',trxz)
		self.depth = dp
		sp = 1
		maxIt = 100   # may need to change with multiple zooms

		self.image = PIL.Image.new('RGB', (X,Y), color = (255,255,255))
		self.image.pixels = self.image.load() 

		for x in range(0,X,sp):
		 	for y in range(0,Y,sp):
				 hue = mandelbrot(*trxz.world(x,Y-y),maxIt)
				 r,g,b = colorsys.hsv_to_rgb(hue,0.5,1)
				 r,g,b = int(255*r),int(255*g),int(255*b)
				 self.image.pixels[x,y] =  r,g,b
				#  use for debugging coord systems
				#  Point(*self.trxz.world(x,y)).draw(self.parent.woZ.win).setOutline(color_rgb(r,g,b))
				#  Point(x,y).draw(self.parent.woX.win) 
		self.save_show()

	def save_show(self):
		self.file_name = Select.file_stub+str(self.dp) + '.png'
		self.image.save(self.file_name)
		in_window(X/2,Y/2,self.file_name,self.parent.woX.win)
		
	def show_image_file(self,dp,label):  # from label symbol
		self.file_name = Select.file_stub+str(dp) + '.png'
		if label=='X':
			in_window(X/2,Y/2,self.file_name,self.parent.woX.win)
		elif label=='Z':
			in_window(-0.5,0,self.file_name,self.parent.woZ.win)

	def select(self):
		"""select box region with cursor  Confirm with ==> button"""
		print(myself())
		win = self.parent.woX.win
		self.parent.bt.activate()
		bx = Circle(Point(0,0),1).draw(win)  #dummy for undraw
		bx_drawn = False   	  				 # just dummy drawn
		while True:
			c = win.getMouse()
			if self.parent.bt.clicked(c) and bx_drawn: break
			self.cx,self.cy,self.wd = c.x,c.y,Ruler.xside2
			self.xsel = box_from_center(self.cx,self.cy,self.wd)
			bx.undraw()
			bx = rec_draw(self.xsel,self.parent.woX.win)
			bx_drawn = True		
		# self.bt.flash()
		# self.bt.wait()

	def draw_selection(self,trxz):
		"""draw selected region using transform and iteration"""
		print(myself(),'trxz',trxz)
		# self.depth = dp
		sp = 1
		maxIt = 100

		self.image = PIL.Image.new('RGB', (X,Y), color = (255,255,255))
		self.image.pixels = self.image.load() 

		for x in range(0,X,sp):
		 	for y in range(0,Y,sp):
				#  zx,zy = self.trxz.world(x,y)
				 hue = mandelbrot(*trxz.world(x,Y-y),maxIt)
				 r,g,b = colorsys.hsv_to_rgb(hue,0.5,1)
				 r,g,b = int(255*r),int(255*g),int(255*b)
				 self.image.pixels[x,y] =  r,g,b
				#  Point(*self.trxz.world(x,y)).draw(self.parent.woZ.win).setOutline(color_rgb(r,g,b))
				#  Point(x,y).draw(self.parent.woX.win)  
		self.dp = 0
		self.save_show()

	def get_zsel(self,dp):
		xsel = self.xsel
		if dp==0: 
			self.trxz = Transform(X,Y,*Ruler.gzbox)
			zsel = self.zsel = self.trxz.world(xsel[0],xsel[1]) + self.trxz.world(xsel[2],xsel[3])
			rec_draw(self.zsel,self.parent.woZ.win)
			Circle(Point(xsel[0],xsel[1]),5).draw(self.parent.woX.win)
			self.trxz = Transform(X,Y,*self.zsel)   # same as zsel0
		else:
			self.trxz = Transform(X,Y,*self.zsel)
			zsel = self.zsel = self.trxz.world(xsel[0],xsel[1]) + self.trxz.world(xsel[2],xsel[3])
			rec_draw(self.zsel,self.parent.woZ.win)
			Circle(Point(xsel[0],xsel[1]),5).draw(self.parent.woX.win)
			self.trxz = Transform(X,Y,*self.zsel)   # same as zsel0

		# new zsel
		# zsel = self.zsel = self.trxz.world(xsel[0],xsel[1]) + self.trxz.world(xsel[2],xsel[3])
		# print('zsel',round_all(self.zsel,3))
		# self.parent.zsel = self.zsel
			Circle(Point(zsel[0],zsel[1]),0.05).draw(self.parent.woZ.win)

	def get_xz_Transform(self):
		xsel = self.xsel
		zsel = self.zsel = Select.gzbox
		self.trxz = Transform(X,Y,*self.zsel)
		# self.zsel = self.trxz.world(xsel[0],xsel[1]) + self.trxz.world(xsel[2],xsel[3])
		print('trxz',self.trxz)

	def transform_illustrationx(self):
		print(myself())
		self.trzz = Transform(3,3,*self.zsel)

		self.dp += 1
		self.wd = 2/10**self.dp
		print('zx,zy,wd,dp',self.zx,self.zy,self.wd,self.dp)

		rec_draw( self.zsel, self.woZ.win ).setWidth(3)
		rec_draw( self.zsel, self.woZ.win ).setOutline('orange')
		rec_draw(Ruler.gzbox, self.woZ.win).setWidth(8)
		# self.print_stats()
		self.bt.wait() 

	def print_stats(self):
		print('\n',myself(),'---- depth',self.dp)
		print('xsel',round_all(self.xsel,0))
		print('zsel',round_all(self.zsel,4))
		if hasattr(self,'trxz'):
			print('trxz',self.trxz)

	def selection_sequence(self,dp,cx,cy):
		xside2 = Select.xside2
		ss = self.parent
		if dp==0:
			self.xsel = xsel = box_from_center(cx,cy,xside2)
			self.zsel = Select.gzbox
			ss.trxz = Transform(X,Y,*self.zsel)
			self.zsel = ss.trxz.world(xsel[0],xsel[1]) + ss.trxz.world(xsel[2],xsel[3]) 
		elif dp==1:
			self.xsel = xsel = box_from_center(cx,cy,xside2)
			self.zsel = ss.trxz.world(xsel[0],xsel[1]) + ss.trxz.world(xsel[2],xsel[3])
			
class SelectSeries(Ruler):
	file_stub = 'git_Apr24/images/hsb'

	
	def __init__(self) -> None:
		self.woZ = WindowObject('Z',X,Y)
		self.woX = WindowObject('X',X,Y)
		self.zsel= Ruler.gzbox

	def init_windows(self):
		"""shows initial state in both windows"""
		self.file_name = SelectSeries.file_stub + '0.png'
		print(self.file_name)
		in_window(-0.5,0,self.file_name,self.woZ.win)
		in_window(X/2,Y/2,self.file_name,self.woX.win)

	def init_button(self,win):
		win = self.woX.win
		self.bt = Button(win, Point( 460, 480), 70,30,'==>')
		self.bt.label.setSize(24)
		self.bt.draw()
		self.bt.activate()

	def draw_whole(self):
		sl = Select(self,0)
		sl.xsel = Select.gscreen
		sl.zsel = Select.gzbox
		rec_draw(sl.xsel,sl.parent.woX.win).setWidth(10)
		rec_draw(sl.zsel,sl.parent.woZ.win).setWidth(10)

		self.trxz = Transform(X,Y,*Ruler.gzbox)  # used for draw selection
		sl.print_stats()

		sl.parent.woX.win.getMouse()
		sl.draw_selection(self.trxz)

		sl.parent.woX.win.getMouse()

	def sequence_click_select(self):
		"""implement states 0 and 1"""
		for dp in range(2):
			s = Select(self,dp)
			clk = s.parent.woX.win.getMouse()
			cx,cy = clk.x,clk.y
			self.selection_sequence(dp,cx,cy)

			rec_draw(s.xsel,self.parent.woX.win)
			rec_draw(s.zsel,s.parent.woZ.win).setOutline('blue')

			self.print_stats()
			self.trxz = Transform(X,Y,*self.zsel)  # used for draw selection

			s.parent.woX.win.getMouse()
			s.draw_selection(dp,self.trxz)

	def implement_series(self):
		dp = 0
		while True:
			s = Select(self,dp)   # self is selseries parent ss
			s.select()

			grid((-3,-3,3,3),s.parent.woZ.win,1)
			s.get_zsel(dp)
			rec_draw(s.zsel,s.parent.woZ.win) 
			s.print_stats()
			self.bt.wait()

			s.draw_selection(s.trxz)
			s.save_show() 
			dp += 1			 

if __name__ == "__main__":
	def driver1():
		ss = SelectSeries()
		ss.draw_whole()
	driver1()

	def driver2():
		ss = SelectSeries()
		ss.init_windows()
		ss.sequence_click_select()

		s.wo.win.getMouse
	# driver2()

	def driver3():
		ss = SelectSeries()
		ss.init_windows()
		ss.init_button(ss.woX)
		ss.implement_series()

	# driver3()

