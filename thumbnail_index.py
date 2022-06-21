# archive.py
""" task: draw from location.  nice interface  click on thumbnail to see full-size

		Lots around net for cool displays
		could also do a grid
	save: key: thumbnail, value: location  let's me get back to all those cool drawings
file with images and locations as long term storage
- image / thumbnail
- location
- mand eqn
- coloring 
- uuid
archive module with dict database"""



from email.utils import decode_params
import sys
from venv import create
sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/myProjects/myModules')
sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/my-python-project')

from PIL import Image
import PIL
import numpy as np
import time
from math import log10
from colorsys import hsv_to_rgb

from window_object1 import WindowObject
from button3 import *
from select23 import MandelbrotCode
# from zoom_draw3 import MyImage
from graphics import *
from mygraphics import *
from ruler0 import Ruler
from helpers import *
from histogram22 import HueGraph
import inspect
myself = lambda: inspect.stack()[1][3]


X,Y = Ruler.X,Ruler.Y



class DataFile():

	def __init__(self,file_name,id,center,width):	
		self.file_name = file_name
		self.id = id
		self.center = center
		self.width = width

	def write_to_file(id,self,center,width):
		with open(file_name + '.txt', "a") as f:
			record = str(id) + ',' + str(center) + ',' + str(width)
			f.write(record)



class Archive():
	
	def __init__(self) -> None:
		self.itemLst = []

	@property
	def dataLst(self):
		return [
((-0.59990625, -0.4290703125),3/1024),
((0.34649107183915934, -0.37546362183256504 ),0.02419296385348313),
((-0.1010963684562, 0.9562865108914),0.025 ),  # dw is guess
((0.4244,0.200759),0.00479616),
# ((-1.747370489, 0.004733564), 1/4.42685e+06)  ultra-deep

]
		
	def items_create(self):
		# def __init__(self,center,width,parent,dp) -> None:
	
		self.winI = GraphWin('Images',X,Y)
		dp = 0
		for d in self.dataLst:
			center,width = d
			parent = self
			it = Item(center,width,parent,dp)
			self.itemLst.append(it)
			dp += 1
		
	def items_implement(self):
		for it in self.itemLst:
			it.show_image()

	def	menu_create(self):
		self.winM = GraphWin('Menu',X,2*Y)
		
		for it in self.itemLst:
			tnail = 'data/archive/tnail' + str(it.dp) + '.png'
			im = PIL.Image.open(tnail)
			bt_center = (X/4,(0.5+it.dp)*(Y/4 + 20))
			in_window(*bt_center,tnail,ar.winM)
			it.create_button(bt_center)

	def menu_respond(self):
		# print(myself())
		while True:
			clk = ar.winM.getMouse()
			cx,cy = clk.x,clk.y
			# Circle(Point(cx,cy),5).draw(ar.winM)
			for it in ar.itemLst:
				if inside((cx,cy),it.bbox):
					re = rec_draw(it.bbox,ar.winM)
					re.setOutline('cyan')
					re.setWidth(5)
					break
			it.show_image()
			time.sleep(1)
			re.setOutline('darkgray')
		
class Item():
	twd = 128

	def __init__(self,center,width,parent,dp) -> None:
		self.center = center
		self.width = width
		self.parent = parent
		self.dp = dp

	def __repr__(self):
		return str(self.dp) + ' ' + str(self.center) + ' ' + str(self.width)
	
	def show_image(self):
		# print(myself(),self.dp)
		file = 'data/archive/file' + str(self.dp) + '.png'
		try:	
			self.image = PIL.Image.open(file)
		except:
			FileNotFoundError
			self.image_from_location()

		self.image.save(file)
		in_window(X/2,Y/2,file,ar.winI)

	def create_button(self,center):
		cx,cy = center
		self.bbox = cx-Item.twd/2,cy-Item.twd/2,cx+Item.twd/2,cy+Item.twd/2
		re = Rectangle(Point(cx-Item.twd/2,cy-Item.twd/2),Point(cx+Item.twd/2,cy+Item.twd/2)).draw(ar.winM)
		re.setOutline('darkgray')
		re.setWidth(3)

	def image_from_location(self):
		zsel = box_from_center(*self.center,self.width/2)
		trxz = Transform(X,Y,*zsel)
		self.image = draw_image(trxz)

	def thumbnail(self,num):
		# print(myself(),num)
		outfile = 'data/archive/tnail' + str(num) + '.png'
		try: 
			tnail = PIL.Image.open(outfile)
		except:
			FileNotFoundError
			infile = 'data/archive/file' + str(num) + '.png'
			# make this file into thumbnail
		
			tnail = PIL.Image.open(infile)
			tnail.thumbnail((Item.twd,Item.twd))
			tnail.save(outfile)

	
if __name__ == "__main__":
	ar = Archive()
	ar.items_create()
	# ar.items_implement()


	ar.menu_create()
	it = ar.menu_respond()

	

	

