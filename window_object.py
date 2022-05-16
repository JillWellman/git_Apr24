
if __name__=='__main__':
	import sys
	sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/my-python-project/myImports')
	sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/myProjects/myModules')
	sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/my-python-project/draw_zoom_may5')

from graphics import *
from mygraphics import *
from ruler0 import Ruler
stem = '/Users/jillwellman_sept09_2012/Desktop/Python/my-python-project/draw_zoom_may5/'

from helpers import *

X,Y = Ruler.X,Ruler.Y

class WindowObject(Ruler):
	label_list = []

	def __init__(self,label,w,h):
		self.label = label
		self.w,self.h = w,h
		self.label_list.append(self.label)
		self.implement()

	def draw(self):
		self.win = GraphWin(self.name,self.w,self.h)

	def implement(self):
		self.name = 'win' + self.label
		#need to make graphics win to hold some attributes of windowObject
		if self.label=='G':
			self.w = 3.5*X
			self.win = GraphWin(self.name,self.w,self.h)  # win attrute is GraphWin
		else:
			self.win = GraphWin(self.name,self.w,self.h)  # win attrute is GraphWin
			self.dtpl = (self.w,self.h)

		if self.label=='G':
			self.dtpl = (self.w,self.h)
		elif self.label=='X':
			self.ctpl = Ruler.gscreen
			self.win.setCoords(*self.ctpl)
		elif self.label=='C':
			self.dtpl = (self.w,self.h)
			self.lctpl = (self.w,self.h,  self.w + 80, 60)			 # middle panel
			window_location(self.win,*self.lctpl)  
			self.ctpl = Ruler.gscreen
			self.win.setCoords(*self.ctpl)
		elif self.label=='Z':
			self.lctpl = (self.w,self.h,  2*self.w + 130, 60)
			window_location(self.win,*self.lctpl)  # right panel
			self.ctpl = Ruler.gzbox
			self.win.setCoords(*self.ctpl)
		else:
			print('no such window as',self.label)

		print(self.label)



if __name__=='__main__':
	"""demo grid for gzbox and gscreen"""

	labels = ['G','X','C','Z']
	for label in labels:
		wo = WindowObject(label,X,Y)
		# if self.label=='G':
		# 	wo = WindowObject(label,2*X+20,Y)
		# else:
		# 	wo = WindowObject(label,X,Y)
		# wo.name = 'win' + str(label)

		# if label=='C': grid((0,0,X,Y),wo.win,100)
		# elif label=='Z': grid((-3,-3,3,3),wo.win,1)


	wo.win.getMouse()