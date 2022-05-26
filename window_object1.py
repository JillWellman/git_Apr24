
if __name__=='__main__':
	import sys
	sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/my-python-project/myImports')
	sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/myProjects/myModules')
	sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/my-python-project/draw_zoom_may5')

from cProfile import label
from graphics import *
from mygraphics import *
from ruler0 import Ruler
import inspect
myself = lambda: inspect.stack()[1][3]

from helpers import *

X,Y = Ruler.X,Ruler.Y

class WindowObject(Ruler):

	def __init__(self,label):
		self.label = label
		self.name = 'win' + self.label

		self.dimensions()
		self.graphic()
		self.coords()
		self.location()

	def dimensions(self):
		if self.label=='G':
			self.dtpl = (3.5*X,Y)
		elif self.label=='M':
			self.dtpl = (X,1.5*Y)
		else:
			self.dtpl = X,Y
	
	def coords(self):
		# self.ctpl = (0,0,X,Y)
		if self.label=='C':
			self.ctpl = Ruler.gscreen
		elif self.label=='Z':
			self.ctpl = (-2,-1.5,1,1.5)
			self.win.setCoords(-3,-3,3,3)
		elif self.label=='M':
			self.ctpl = (-0.5,-0.5,3.5,4.5)
		elif self.label=='X':
			self.ctpl = (0,0,X,Y)
		
	def location(self):
		self.lctpl = (80,60)
		if self.label in ['C','M']:
			self.lctpl = (X+ 100, 60)			 # middle panel
		elif self.label=='Z':
			self.lctpl = (2*X + 130, 60)
		w,h,x,y = *self.dtpl,*self.lctpl
		window_location(self.win,w,h,x,y)

	def graphic(self):
		self.win = GraphWin(self.name,*self.dtpl)

	def draw_grid(self,n): 
		self.win.setCoords(-2,-1.5,1,1.5)

		for i in range(-n+1,n,1):
		    tx=Text(Point(i,-1.4),str(i)).draw(self.win)
		    tx.setSize(18)
		for j in range(-n+1,n,1):
		    tx=Text(Point(-1.9,j-0.07),str(j)).draw(self.win)
		    tx.setSize(18)

		for i in range(-n+1,n,1):
			for j in range(-n+1,n,1):
				rect_from_center(i+0.5,j+0.5,0.5).draw(self.win)

	def grid(self):
		if self.label=='C': grid((0,0,X,Y),self.win,100)
		if self.label=='Z': 
			self.draw_grid(3)




if __name__=='__main__':
	"""demo grid for gzbox and gscreen"""


	labels = ['G','M','X','C','Z']
	for label in labels:
		wo = WindowObject(label)
		wo.graphic()
		wo.coords()
		wo.location()
		wo.grid()
		
	wo.win.getMouse()