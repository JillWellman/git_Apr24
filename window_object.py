
if __name__=='__main__':
	import sys
	sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/my-python-project/myImports')
	sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/myProjects/myModules')

from graphics import *
from mygraphics import *
from helpers import *
from ruler0 import Ruler

X,Y = Ruler.X,Ruler.Y

class WindowObject(Ruler):
	label_list = []

	def __init__(self,label,X,Y):
		self.label = label
		WindowObject.label_list.append(self.label)
		self.implement()

	def implement(self):
		self.name = 'win' + self.label
		self.win = GraphWin(self.name,X,Y)  # win attrute is GraphWin
		self.dtpl = (X,Y)
		if self.label=='X':
			self.ctpl = Ruler.gscreen
			self.win.setCoords(*self.ctpl)
		elif self.label=='C':
			self.lctpl = (X,Y,  X + 80, 60)			 # middle panel
			window_location(self.win,*self.lctpl)  
			self.ctpl = Ruler.gscreen
			self.win.setCoords(*self.ctpl)
		elif self.label=='Z':
			self.lctpl = (X,Y,  X + 160, 60)
			window_location(self.win,*self.lctpl)  # right panel
			self.ctpl = Ruler.gzbox
			self.win.setCoords(*self.ctpl)
		else:
			print('no such window as',label)
			exit()
		self.mark_min_window_corner() 

	def mark_min_window_corner(self):
		xa,ya,xb,yb = self.ctpl
		minx,miny = min_corner(self.ctpl)
		side = abs(xb - xa)
		Circle(Point(minx,miny),side/20).draw(self.win).setFill('black')


if __name__=='__main__':
	pass