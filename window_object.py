
if __name__=='__main__':
	import sys
	sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/my-python-project/myImports')
	sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/myProjects/myModules')

from graphics import *
from mygraphics import *
from helpers import *
from ruler0 import Ruler
from helpers import *

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
			self.lctpl = (X,Y,  2*X + 160, 60)
			window_location(self.win,*self.lctpl)  # right panel
			self.ctpl = Ruler.gzbox
			self.win.setCoords(*self.ctpl)
		else:
			print('no such window as',label)
			exit()



if __name__=='__main__':
	"""demo grid for gzbox and gscreen"""

	labels = ['X','C','Z']
	n = 0
	for label in labels:
		wo = WindowObject(label,X,Y)
		wo.name = 'win' + str(label)

		if n==1: grid((0,0,X,Y),wo.win,100)
		elif n==2: grid((-3,-3,3,3),wo.win,1)

		n += 1

	wo.win.getMouse()