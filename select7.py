# select7.py
"""	select7 zooming isn't quite accurate
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
maxIt = 1000   # may need to change with multiple zooms

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

	def	ztransform(self):
		xsel = self.xsel
		self.zsel = self.trxz.world(xsel[0],xsel[1]) + self.trxz.world(xsel[2],xsel[3])
		self.parent.trxz = Transform(X,Y,*self.zsel)

	def darkgray_circles(self):
		xdr = Select.xside2/20 
		zdr = self.trxz.xscale*2*xdr  # xdr * zxscale
		xsel,zsel = self.xsel,self.zsel
		Circle(Point(zsel[0],zsel[1]),zdr).draw(self.parent.woZ.win).setFill('darkgray')
		Circle(Point(xsel[0],xsel[1]),xdr).draw(self.parent.woX.win).setFill('darkgray')

	

class SelectSeries(Ruler):

	def __init__(self) -> None:
		self.woZ = WindowObject('Z',X,Y)
		self.woX = WindowObject('X',X,Y)
		self.woC = WindowObject('C',X,Y)
		self.zsel= Ruler.gzbox

	def zoom_loop(self):
		dp = 0
		while True:
			s = Select(self,dp)
			s.select()
			self.xsel = s.xsel
			s.parent.get_zsel()
			self.print_stats(dp)
			self.bt.wait()

			dp += 1
			self.draw_image(dp,self.trxz)
			self.save_show_window(dp,'X')
			if dp >=1: self.save_show_window(dp,'C')
			rec_draw(s.xsel,self.woC.win)

			self.bt.draw()
			self.bt.wait()



	def get_zsel(self):
		print(myself())
		# grid((-3,-3,3,3),self.parent.woZ.win,1)
		if not hasattr(self,'zsel'):
			self.zsel = Ruler.gzbox
		self.trxz = Transform(X,Y,*self.zsel)

		xsel = self.xsel
		zsel = self.zsel = self.trxz.world(xsel[0],xsel[1]) + self.trxz.world(xsel[2],xsel[3])
		rec_draw(self.zsel,self.woZ.win)

		self.trxz = Transform(X,Y,*self.zsel)

	def draw_image(self,dp,trxz):
		"""draws part of image mapped by trxz from zsel onto gscreen"""
		print(myself(),dp,'trxz',trxz)
		self.depth = dp
		sp = 1

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
		pass

	def save_show_window(self,dp,win):
		print(myself(),win)
		self.file_name = Select.file_stub+str(dp) + '.png'
		if not hasattr(self,'image'): print('no image')
		else:
			self.image.save(self.file_name)
			if win=='X':
				in_window(X/2,Y/2,self.file_name,self.woX.win)
			elif win=='Z':
				in_window(-0.5,0,self.file_name,self.woZ.win)

			elif win=='C':
				self.file_name = Select.file_stub+str(dp-1) + '.png'
				in_window(X/2,Y/2,self.file_name,self.woC.win)

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
		self.xsel = Select.gscreen
		self.zsel = Select.gzbox
		rec_draw(self.xsel,self.woX.win).setWidth(10)
		rec_draw(self.zsel,self.woZ.win).setWidth(10)

		self.trxz = Transform(X,Y,*Ruler.gzbox)  # used for draw selection
		self.print_stats(0)

		self.draw_image(0,self.trxz)

	def select_seriesx(self,dp):
		# might use dp to start at arbitrary depth
		self.dp = dp
		self.init_windows(dp)
		self.init_button(self.woX.win)
		
		while True:
			print(3*' = = =')
			s = Select(self,dp)   # s is state, self is parent/select_series
			s.select()  # select region by center
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
		dp = 0
		ss = SelectSeries()
		ss.init_windows(dp)
		ss.init_button(ss.woX)
		ss.zoom_loop()
		
	zoom_sequence()

