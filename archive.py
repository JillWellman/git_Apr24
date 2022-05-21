# archive.py
""" file with images and locations as long term storage
- image / thumbnail
- location
- mand eqn
- coloring 
- uuid
archive module with dict database"""


import sys
sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/myProjects/myModules')
sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/my-python-project')

from PIL import Image
import PIL
import numpy as np
import time
from math import log10
from colorsys import hsv_to_rgb
# import matplotlib.pyplot as plt

from window_object1 import WindowObject
from button3 import *
from select22 import State
# from zoom_draw3 import MyImage
from graphics import *
from mygraphics import *
from ruler0 import Ruler
from helpers import *
from histogram22 import HueGraph
import inspect
myself = lambda: inspect.stack()[1][3]

X,Y = Ruler.X,Ruler.Y

class Archive():
	def __init__(self) -> None:
		self.win = GraphWin('',X,Y)
		self.dict = {

		}
		# image 
		# thumbnail
		# location
		# mand eqn
		# coloring 
		# uuid

	def add_image_dict(self,image,location):
		pass

	def create_image_from_location(self):
		dp = 3 
		# cx,cy,dw = 0.34649107183915934, -0.37546362183256504, 0.02419296385348313
		

		dw = 3/1024 # base dimension over magnification
		cx,cy,dw = -0.59990625, -0.4290703125, dw
		
		zsel = box_from_center(cx,cy,dw/2)
		trxz = Transform(X,Y,*zsel)
		State.self.draw_image(dp)
		self.store_image_and_text(dp)
		in_window(X/2,Y/2,self.image_filename,self.parent.wo.win)




	def thumbnail(self):
		size = 128, 128

		for dp in range(23):
			infile = 'data/image_fileB' + str(dp) + '.png'
			image = PIL.Image.open(infile)
			image.thumbnail((128,128))
			outfile = 'data/image_fileB_thumb' + str(dp) + '.png'
			image.save(outfile)


			# outfile = os.path.splitext(infile)[0] + ".thumbnail"
			# if infile != outfile:
			# 	try:
			# 		im = Image.open(infile)
			# 		im.thumbnail(size)
			# 		im.save(outfile, "JPEG")
			# 	except IOError:
			# 		print("cannot create thumbnail for", infile)



if __name__ == "__main__":
	ar = Archive()
	ar.create_image_from_location()


	

