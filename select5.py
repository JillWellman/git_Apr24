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

def show_image_file(dp,label,win):  # from label symbol
	file_name = Select.file_stub+str(dp) + '.png'
	if label=='X':
		in_window(X/2,Y/2,file_name,win)
	elif label=='Z':
		in_window(-0.5,0,file_name,win)


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

	def draw_image(self,dp,trxz):
		"""draws part of image mapped by trxz from zsel onto gscreen"""
		print(myself(),'trxz',trxz)
		self.depth = dp
		sp = 1
		maxIt = 100   # may need to change with multiple zooms

		self.image = PIL.Image.new('RGB', (X,Y), color = (255,255,255))
		self.image.pixels = self.image.load() 

		for x in range(0,X,sp):
		 	for y in range(0,Y,sp):
				 hue = mandelbrot(*trxz.world(x,y),maxIt)
				 r,g,b = colorsys.hsv_to_rgb(hue,0.5,1)
				 r,g,b = int(255*r),int(255*g),int(255*b)
				 self.image.pixels[x,y] =  r,g,b
				#  use for debugging coord systems
				#  Point(*self.trxz.world(x,y)).draw(self.parent.woZ.win).setOutline(color_rgb(r,g,b))
				#  Point(x,y).draw(self.parent.woX.win) 
		self.save_show_window(dp,self.parent.woX.win)

	def save_show_window(self,dp,win):
		self.file_name = Select.file_stub+str(dp) + '.png'
		if not hasattr(self,'image'): print('no image')
		else:
			self.image.save(self.file_name)
			if win==self.parent.woX.win:
				in_window(X/2,Y/2,self.file_name,self.parent.woX.win)
			elif win==self.parent.woZ.win:
				in_window(-0.5,0,self.file_name,self.parent.woZ.win)
		
	def select(self):
		"""select box region with cursor  Confirm with ==> button"""
		print(myself())
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
		# minimum coord corner of xsel
		xdr = Select.xside2/20  # xside/10 = diameter
		Circle(Point(self.xsel[0],self.xsel[1]),5).draw(self.parent.woX.win).setFill('darkgray')
	
	def draw_image(self,trxz):
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

	def get_zsel(self):
		if not hasattr(self,'zsel'):
			self.zsel = Ruler.gzbox
		self.trxz = Transform(X,Y,*self.zsel)

		xsel = self.xsel
		zsel = self.zsel = self.trxz.world(xsel[0],xsel[1]) + self.trxz.world(xsel[2],xsel[3])
		rec_draw(self.zsel,self.parent.woZ.win)
		self.darkgray_circles()

		zsel = self.zsel = self.trxz.world(xsel[0],xsel[1]) + self.trxz.world(xsel[2],xsel[3])
		self.trxz = Transform(X,Y,*self.zsel)
	def xtransform_on_zsel(self):
		print(myself())
		zsel = self.zsel 
		self.trxx = Transform(X,Y,*self.xsel)
		self.zsel = self.trxx.world(zsel[0],zsel[1]) + self.trxx.world(zsel[2],zsel[3])
		self.print_stats()
		rec_draw(self.zsel,self.parent.woZ.win).setOutline('magenta')


	def darkgray_circles(self):
		xdr = Select.xside2/20 
		zdr = self.trxz.xscale*2*xdr  # xdr * zxscale
		xsel,zsel = self.xsel,self.zsel
		Circle(Point(zsel[0],zsel[1]),zdr).draw(self.parent.woZ.win).setFill('darkgray')
		Circle(Point(xsel[0],xsel[1]),xdr).draw(self.parent.woX.win).setFill('darkgray')

	def print_stats(self):
		print('\n',myself(),'---- depth',self.dp)
		print('xsel',round_all(self.xsel,0))
		print('zsel',round_all(self.zsel,4))
		print('zside',round((self.zsel[1] - self.zsel[0]),4) )
		if hasattr(self,'trxz'):
			print('trxz',self.trxz)
		if hasattr(self,'trxx'):
			print('trxx',self.trxx)

class SelectSeries(Ruler):

	def __init__(self) -> None:
		self.woZ = WindowObject('Z',X,Y)
		self.woX = WindowObject('X',X,Y)
		self.zsel= Ruler.gzbox

	def init_windows(self,dp):
		"""shows initial state in both windows"""
		self.file_name = Select.file_stub + str(dp) + '.png'
		in_window(-0.5,0,self.file_name,self.woZ.win)
		in_window(X/2,Y/2,self.file_name,self.woX.win)
		Circle(Point(0,0),3*X/50).draw(self.woX.win).setFill('darkgray')
		Circle(Point(-2,-1.5),3*zX/50).draw(self.woZ.win).setFill('darkgray')

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

		# sl.parent.woX.win.getMouse()
		sl.draw_selection(self.trxz)


	def select_series(self,dp):
		# might use dp to start at arbitrary depth
		self.dp = dp
		self.init_windows(dp)
		self.init_button(self.woX.win)
		
		while True:
			print(3*' = = =')
			s = Select(self,dp)   # s is state, self is parent/select_series
			s.select()  # select region by center
			# confirm and exit on bt clicked

			# zsel calc/draw
			# grid((-3,-3,3,3),s.parent.woZ.win,1)
			s.get_zsel()
			dp += 1		
			s.depth = dp 
			s.file_name = Select.file_stub+str(dp)+'.png'

			s.draw_image(s.trxz)
			s.save_show_window(dp,s.parent.woX.win) 
			Circle(Point(0,0),3*X/50).draw(self.woX.win).setFill('darkgray')
			self.bt.draw()

			s.print_stats()   #Transform will be different

			self.bt.wait()
			in_window(-0.5,0,s.file_name,self.woZ.win)

			


if __name__ == "__main__":
	def draw_state0():
		ss = SelectSeries()
		ss.draw_whole()
		show_image_file(0,'X',ss.woX.win)
		show_image_file(0,'Z',ss.woZ.win)
		ss.woX.win.getMouse()

	# draw_state0()


	def zoom_sequence():
		ss = SelectSeries()
		ss.init_windows(1)
		ss.init_button(ss.woX)
		ss.select_series(1)

	zoom_sequence()

