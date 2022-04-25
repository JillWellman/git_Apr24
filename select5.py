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
zX,zY = Ruler.zX,Ruler.zY

class Select(Ruler):
	file_stub = 'images/hsb'
	
	def __init__(self,parent,dp) -> None:
		self.dp = dp
		self.parent = parent

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

	def save_show(self,dp):
		self.file_name = Select.file_stub+str(dp) + '.png'
		if not hasattr(self,'image'): print('no image')
		else:
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
		# self.parent.bt.draw()
		# self.parent.bt.activate()
		bx = Circle(Point(0,0),1).draw(self.parent.woX.win)  #dummy for undraw
		bx_drawn = False   	  				 # dummy drawn
		while True:
			c = self.parent.woX.win.getMouse()
			if self.parent.bt.clicked(c) and bx_drawn: break
			self.cx,self.cy,self.wd = c.x,c.y,Ruler.xside2
			self.xsel = box_from_center(self.cx,self.cy,self.wd)
			bx.undraw()
			bx = rec_draw(self.xsel,self.parent.woX.win)
			bx_drawn = True
		xdr = Select.xside2/20  # xside/10 = diameter
		Circle(Point(self.xsel[0],self.xsel[1]),5).draw(self.parent.woX.win).setFill('darkgray')
		self.parent.bt.undraw
		self.parent.bt.deactivate

	def draw_selection(self,trxz):
		"""draw selected region using transform and iteration"""
		print(myself(),'trxz',trxz)
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
				#  for debugging
				#  Point(*self.trxz.world(x,y)).draw(self.parent.woZ.win).setOutline(color_rgb(r,g,b))
				#  Point(x,y).draw(self.parent.woX.win) 
		# self.image.show()
		print('')

	def get_zsel(self,dp):
		xsel = self.xsel
		xdr = Select.xside2/20 
		if dp==0: 
			self.trxz = Transform(X,Y,*Ruler.gzbox)
			zsel = self.zsel = self.trxz.world(xsel[0],xsel[1]) + self.trxz.world(xsel[2],xsel[3])
			rec_draw(self.zsel,self.parent.woZ.win)
		else:
			self.trxz = Transform(X,Y,*self.zsel)
			zsel = self.zsel = self.trxz.world(xsel[0],xsel[1]) + self.trxz.world(xsel[2],xsel[3])
			rec_draw(self.zsel,self.parent.woZ.win)
		zdr = self.trxz.xscale*2*xdr  # xdr * zxscale
		Circle(Point(zsel[0],zsel[1]),zdr).draw(self.parent.woZ.win).setFill('darkgray')

		# use in draw_selection
		self.trxz = Transform(X,Y,*self.zsel)

	def get_xz_Transformx(self):
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

	def __init__(self) -> None:
		self.woZ = WindowObject('Z',X,Y)
		self.woX = WindowObject('X',X,Y)
		self.zsel= Ruler.gzbox

	def init_windows(self):
		"""shows initial state in both windows"""
		self.file_name = Select.file_stub + '0.png'
		in_window(-0.5,0,self.file_name,self.woZ.win)
		in_window(X/2,Y/2,self.file_name,self.woX.win)
		Circle(Point(0,0),3*X/50).draw(self.woX.win).setFill('darkgray')
		Circle(Point(-2,-1.5),3*zX/50).draw(self.woZ.win).setFill('darkgray')


	def init_button(self,win):
		win = self.woX.win
		self.bt = Button(win, Point( 460, 480), 70,30,'==>')
		self.bt.label.setSize(24)
		# self.bt.draw()
		# self.bt.activate()

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

	def select_series(self,dp):
		s = Select(self,dp)   # self is selseries id
		s.file_name = Select.file_stub+str(dp)+'.png'
		print('select series',s.file_name)
		s.save_show(dp) 
		Circle(Point(0,0),3*X/50).draw(self.woX.win).setFill('blue')
		s.parent.bt.draw()
		s.parent.bt.activate()
		while True:
			s.select()
			grid((-3,-3,3,3),s.parent.woZ.win,1)
			s.get_zsel(dp)
			rec_draw(s.zsel,s.parent.woZ.win) 
			s.print_stats()
			s.draw_selection(s.trxz)

			dp += 1			 
			s.file_name = Select.file_stub+str(dp)+'.png'
			s.save_show(dp) 
			Circle(Point(0,0),3*X/50).draw(self.woX.win).setFill('blue')
			s.parent.bt.draw()
			s.parent.bt.activate()

if __name__ == "__main__":
	def draw_state0():
		ss = SelectSeries()
		ss.draw_whole()
	# draw_state0()

	def driver2():
		ss = SelectSeries()
		ss.init_windows()
		ss.sequence_click_select()

		s.wo.win.getMouse
	# driver2()

	def zoom_sequence():
		ss = SelectSeries()
		ss.init_windows()
		ss.init_button(ss.woX)
		ss.select_series(0)

	zoom_sequence()

