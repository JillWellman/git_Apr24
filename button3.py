# button.py
#    A simple Button widget.
import sys
sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/myProjects/myModules')

from graphics import *
from mygraphics import *

import inspect
myself = lambda: inspect.stack()[1][3]

class Button:

	"""A button is a labeled rectangle in a window.
	It is activated or deactivated with the activate()
	and deactivate() methods. The clicked(p) method
	returns true if the button is active and p is inside it."""

	def __init__(self, enclosing_win, center, width, height, label):
		""" Creates a rectangular button, eg:
		qb = Button(myWin, Point(30,25), 20, 10, 'Quit') """ 

		self.enclosing_win = enclosing_win
		w,h = width/2.0, height/2.0
		x,y = center.x,center.y
		self.xmax, self.xmin = x+w, x-w
		self.ymax, self.ymin = y+h, y-h
		p1 = Point(self.xmin, self.ymin)
		p2 = Point(self.xmax, self.ymax)
		self.rect = Rectangle(p1,p2)
		self.rect.setFill('lightgray')
		self.label = Text(center, label)
		self.label.setSize(24)
		# self.deactivate()

	def draw(self):
		self.undraw()
		try: self.rect.draw(self.enclosing_win)
		except:
			GraphicsError
		try: self.label.draw(self.enclosing_win)
		except:
			GraphicsError

	def undraw(self):
		self.rect.undraw()
		self.label.undraw()

	def clicked(self, p):
		""" RETURNS true if button active and p is inside"""
		return self.active and \
			   self.xmin <= p.getX() <= self.xmax and \
			   self.ymin <= p.getY() <= self.ymax

	def flash(self):
		""" deactivate/pause/activate"""
		self.deactivate()
		self.activate()

	def getLabel(self):
		"""RETURNS the label string of this button."""
		return self.label.getText()

	def activate(self):
		"""Sets this button to 'active'."""
		self.label.setFill('black')
		self.rect.setWidth(2)
		self.active = 1

	def deactivate(self):
		"""Sets this button to 'inactive'."""
		self.label.setFill('darkgrey')
		self.rect.setWidth(1)
		self.active = 0

	def hide(self):
		"""Sets  button to 'inactive' and undraws it"""
		self.undraw()
		self.deactivate()

	def wait(self):
		bt = self
		"""pauses action until button click"""
		while True:
			clk = self.enclosing_win.getMouse()
			if bt.clicked(clk): break

	

if __name__=='__main__':
	X,Y = 500,500
	enclosing_win = GraphWin('button test',X,Y)
	bt = Button(enclosing_win, Point( (X-50),(Y-30)), 60, 25,'==>')
	bt.draw()
	bt.label.setSize(24)
	bt.activate()
	bt.wait()
	print('done')
