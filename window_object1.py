
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

	def __init__(self,label):
		self.label = label
		self.name = 'win' + self.label
		self.label_list.append(self.label)
		if self.label=='G':
			self.dtpl = (3.5*X,Y)
		else:
			self.dtpl = (X,Y)
		# when you make a wo, the window is drawn
		self.win = GraphWin(self.name,*self.dtpl)

	def implement(self):
		if self.label=='G':
			self.dtpl = (3*X,Y)
		elif self.label=='X':
			self.dtpl = X,Y
			self.ctpl = Ruler.gscreen
			self.win.setCoords(*self.ctpl)
		elif self.label=='C':
			self.lctpl = (*self.dtpl,  X+ 80, 60)			 # middle panel
			window_location(self.win,*self.lctpl)  
			self.ctpl = Ruler.gscreen
			self.win.setCoords(*self.ctpl)
		elif self.label=='Z':
			w,h = self.dtpl
			self.lctpl = (w,h,  2*w + 130, 60)
			window_location(self.win,*self.lctpl)  # right panel
			self.ctpl = Ruler.gzbox
			self.win.setCoords(*self.ctpl)
		else:
			print('no such window as',self.label)




if __name__=='__main__':
	"""demo grid for gzbox and gscreen"""


	labels = ['G','X','C','Z']
	for label in labels:
		if label=='G':
			wo = WindowObject(label) # window width on laptop
			wo.w,wo.h = 3*Ruler.X,Ruler.Y
			# wo.win = GraphWin('',wo.w,wo.h)
		else:
			wo = WindowObject(label)
			wo.w,wo.h = Ruler.X,Ruler.Y
		wo.name = 'win' + str(label)



		wo.win = GraphWin(wo.name,Ruler.winX,Ruler.Y)

		# if label=='C': grid((0,0,X,Y),wo.win,100)
		# elif label=='Z': grid((-3,-3,3,3),wo.win,1)


	wo.win.getMouse()