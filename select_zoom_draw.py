# select_zoom_draw
"""	recursive draw.  Take everything else out"""

from multiprocessing.dummy import DummyProcess
import sys

sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/myProjects/myModules')
sys.path.append (r'/Users/jillwellman_sept09_2012/Desktop/Python/my-python-project')

from PIL import Image
import PIL
# import matplotlib.pyplot as plt
from math import log10
from colorsys import hsv_to_rgb
# import matplotlib.pyplot as plt

from window_object1 import WindowObject
from button3 import *
from mandelbrot_code import MandelbrotCode
from graphics import *
from mygraphics import *
from ruler0 import Ruler
from helpers import *
from graph0a import HueGraph

# from histogram22 import HueGraph

# stem = '/Users/jillwellman_sept09_2012/Desktop/Python/my-python-project/draw_zoom_may5/'

import inspect
myself = lambda: inspect.stack()[1][3]

X,Y = Ruler.X,Ruler.Y
maxIt = Ruler.maxIt  

def mandelbrot(x,y,maxIt):
	c = complex(x,y)
	z = complex(0,0)
	for i in range(maxIt):
		if abs(z) > 2: break
		# zn+1 = zn2 + c. 
		z = z * z + c
		hue = (i/maxIt)
		clr = colorsys.hsv_to_rgb(hue,1,1)
		r,g,b = [int(255*i) for i in clr]
	return hue,r,g,b



class State(Ruler):
	LIST = True  # flag to record hues
	gzbox = -2,-1.5,1,1.5
	gscreen = 0,Y,X,0
	
	
	def __init__(self,parent,dp) -> None:
		self.dp = dp
		self.parent = parent
		self.hfile = Ruler.datadir + 'hfile'+ str(dp) + '.txt'
		self.ifile = Ruler.datadir + 'ifile'+ str(dp) + '.png'
		self.gfile = Ruler.datadir + 'gfile' + str(dp) + '.png'
		self.lfile = Ruler.datadir + 'lfile.txt'
	
	def select(self):
		"""select box region with cursor  Confirm with ==> button
		window in parent class"""
		bx = Circle(Point(0,0),1).draw(self.parent.wo.win)  #dummy for undraw
		bx_drawn = False   	  				 # only dummy drawn
		while True:
			if bx_drawn: self.parent.bt.activate()
			c = self.parent.wo.win.getMouse()
			if self.parent.bt.clicked(c) and bx_drawn: break
			if c.x > X - Ruler.xside2: continue  # don't allow extension over right side
			self.cx,self.cy,self.wd = c.x,c.y,Ruler.xside2
			self.parent.xsel = self.xsel = box_from_center(self.cx,self.cy,self.wd)
			bx.undraw()
			bx = rec_draw(self.xsel,self.parent.wo.win)
			bx_drawn = True
		self.parent.bt.deactivate()

	def make_image(self,trxz,dp):
		self.draw_image(trxz,dp)
		self.image.save(self.ifile)

		in_window(X/2,Y/2,self.ifile,self.parent.wo.win)


	def draw_image(self,trxz,dp):
		print(myself(),end= ' ')
		self.hueLst = []
		sp = 2

		self.image = PIL.Image.new('RGB', (X,Y), color = (255,255,255))
		self.image.pixels = self.image.load() 

		# mn = MandelbrotCode()
		start_time = time.time()

		for x in range(0,X,sp):
			# if x%100==0: print('.',end='')
			for y in range(0,Y,sp):
				hue,r,g,b = mandelbrot(*trxz.world(x,y),Ruler.maxIt)
				self.image.pixels[x,y] = r,g,b
				self.hueLst.append(hue)

		with open(self.hfile, "w") as f:
			f.write(str(self.hueLst))
		
		print(dp,'time',time.time() - start_time)

	
	def request_graph(self,dp):
		print(myself())
		gr = HueGraph('G',dp)
		gfile = gr.create_graph(dp)
		# print(gr_im)
		# gfile = Ruler.datadir + 'gfile' + str(dp) + '.png'
		# gr_im.save(gfile)
		in_window(2.35*X,Y/2,gfile,self.parent.wo.win)

class StatePath(Ruler):

	def __init__(self,label) -> None:
		self.wo = WindowObject(label)
		self.dir = dir
		self.start_dp = start_dp

	def zoom_loop(self):
		dp = 0
		
		st = State(self,dp) 
		st.xsel,self.zsel  = State.gscreen, State.gzbox # whole x & z windows 
		self.loc = - 0.75, 0, 3

		# self.zsel_transform(st,dp)
		
		trxz = Transform(X,Y,*self.zsel)   # transform from state0 to current state zbox
		# st.make_image(trxz,dp)
		in_window(X/2,Y/2,st.ifile,self.wo.win)



		# write location		
		with open(st.lfile, "w") as f:
			f.write(str(self.loc) + str(st.xsel) + '\n')

		self.bt = Button(self.wo.win,Point(X - 50,Y - 30),60,30,'==>')
		self.bt.draw()
		# self.bt.wait()
		dp = 1

		while True:  # loop over post-initial states
			self.bt.deactivate()

			# select region from existing state displayed
			st = State(self,dp)  # parent = self
			st.select()  # selects xsel which goes to zsel
			# loc, current trxz0 (with new_zsel), new trxz
			self.zsel_transform(st,dp)
			# ============ loc,xsel defined =======
			with open(st.lfile, "a") as f:
				f.write(str(self.loc + st.xsel) + '\n')
			# new state begins
			st.make_image(self.trxz,dp)
			# st.request_graph(dp)
			dp += 1
			

			
			# print(dp)
			
			self.bt.draw()

	def get_location_from_zsel(self,dp):
		zxa,zya,zxb,zyb = self.zsel
		dw = zxb-zxa
		cx,cy = (zxa+zxb)/2,(zya+zyb)/2
		self.loc = cx,cy,dw

	def get_location_stored(self,dp):
		with open(self.self, "r") as f:
			lstr = f.read()
		print(lstr)
		return

		lstr = lstr[1:-2]  # remove parens and extr \n
		lst = lstr.split(',')
		lst =  [float(l) for l in lst]
		print(lst)
		return lst

	def zsel_transform(self,st,dp):
		# calculates loc, new_zsel, and trxz (with new_zsel)
		"""freeze
		comes from two states bounding transition"""
		self.trxz0 = Transform(X,Y,*self.zsel)  # old zsel

		xsel = st.xsel  # created in state.select
		zxa,zya,zxb,zyb = self.trxz0.world(xsel[0],xsel[1]) + self.trxz0.world(xsel[2],xsel[3])
		dw = (zxb-zxa)
		cx,cy = (zxa+zxb)/2,(zya+zyb)/2,
		self.loc = cx,cy,dw   # loc for next state

		# new zsel
		self.zsel  = min(zxa,zxb),min(zya,zyb),max(zxa,zxb),max(zya,zyb)
		# use for upcoming draw image
		self.trxz = Transform(X,Y,*self.zsel)

	def init_button(self,win):
		self.bt = Button(win, Point( 460, 480), 70,30,'==>')
		self.bt.label.setSize(24)
		self.bt.draw()
		self.bt.activate()



if __name__ == "__main__":
	start_dp = 0
	pth = StatePath('G')
	pth.zoom_loop()

