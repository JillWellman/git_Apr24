import PIL.Image
import numpy as np
import colorsys
import os
import sys
sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/myProjects/myModules')
from graphics import *
from mygraphics import *
X,Y = 500,500

def file_list(dir,start,end):
	fLst = []
	for f in os.listdir(dir_name):
		if f.startswith(start)  and f.endswith(end):
			fLst.append(f)
	return fLst


def show_images():
	win = GraphWin('',2.5*X,Y)
	dir = 'data/0530'
	fLst = file_list(dir,'image','.png')
	N = len(fLst)

	for dp in range(N):
		# fl = dir + '/' + f
		fl = dir + '/' + 'image' + str(dp) + '.png'
		# im = PIL.Image.open(fl)
		# im.show()
		in_window(X/2,Y/2,fl,win)
		win.getMouse()


def show_graph_images():
	win = GraphWin('',2.5*X,Y)
	dir = 'data/0530'
	gLst = file_list(dir,'gfile','.png')

	for gf in gLst:
		gfl = dir + '/' + gf
		in_window(1750/2,500/2,gfl,win)
		win.getMouse()


class ImageToArray():

	def __init__(self,dp):
		self.dp = dp


	def im_file_driver(self,dp):
		self.image_to_nparray(dp)
		self.hueLst_from_image_array()
		self.write_hfile(dp)

	def image_to_nparray(self,dp):
		dir = 'data/0530'
		iLst = file_list(dir,'image','.png')
		N = len(iLst)

		for dp in range(dp,dp+1):
			ifile = dir + '/' + 'image' + str(dp) + '.png'
			im = PIL.Image.open(ifile)
			self.numpydata = np.asarray(im)
			X,Y,n = self.numpydata.shape

	def hueLst_from_image_array(self):
		X,Y = 500,500
		self.hueLst = []
		for i in range(X):
			for j in range(Y):
				r,g,b = self.numpydata[i][j]
				(hue,sat,val) = colorsys.rgb_to_hsv(r,g,b)
				self.hueLst.append(hue)


	def write_hfile(self,dp):
		hfile = 'data/0530/hues' + str(dp) + '.txt'
		with open(hfile,"w") as f:
			f.write(str(self.hueLst))
		print(self.hueLst[0:8])

