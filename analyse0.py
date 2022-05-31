# new_histogram

"""input hues output images, graphs
	also use with select_zoom_draw for exploration"""
from math import log10
import numpy as np
import colorsys  
from PIL import ImageDraw,ImageFont
import PIL.Image,PIL.ImageDraw
from helpers import *
from graphics import *
from colorsys import rgb_to_hsv, hsv_to_rgb
from button3 import Button
from ruler0 import Ruler
from window_object1 import WindowObject


import inspect
myself = lambda: inspect.stack()[1][3]       

X,Y = Ruler.X,Ruler.Y


class GraphAnnotations():
	def __init__(self) -> None:
		X = Y = 500

		self.image = PIL.Image.new('RGB', (X,Y), color = (255,255,255))
		draw = PIL.ImageDraw.Draw(self.image)
		draw.line((0,0) + (500,500), fill = 'magenta',width = 3 )

		self.y_scale_labels(self.image)		
		self.image.show()
	
	def draw_all_pixels_line(self):

		draw = PIL.ImageDraw.Draw(self.im)
		# line for all_pixels level in graph_display
		wd = X
		y = Y-self.y_unit*(log10(X*Y))
		draw.line((self.x_offset,y)+(wd,y),fill=Ruler.interior, width=4)

	def y_scale_labels(self,image):
		# image_width = self.im.width
		self.x_offset = 35
		self.y_unit = Y/6

		draw = PIL.ImageDraw.Draw(image)
		font = ImageFont.load_default().font
		font = ImageFont.truetype("Verdana.ttf",18)

		# y_axis line
		draw.line((self.x_offset,0)+(self.x_offset,Y),fill='black')  # mark zero point
		draw.line((0,0) + (X,Y), fill = 'magenta',width = 3 )
		
		# y axis labels
		for i in range(7):
			draw.text((self.x_offset-15, Y-i*Y/6),str(i),(0,0,0),font=font)

	def description(self):
		draw = PIL.ImageDraw.Draw(self.im)
		font = ImageFont.load_default().font
		font = ImageFont.truetype("Verdana.ttf",18)

		self.exterior_pixels = self.all_pixels - self.interior_pixels
		self.calc_log_pixels()


		

	

		draw.text((50,10),"State " + str(self.dp) + "   # Hues " + str(self.n_hues) \
			+ "  # Pixels:  Total " + sci_not(self.all_pixels) + ' (5.4)  Exterior ' \
				   + str(sci_not(self.exterior_pixels)) + ' (' + self.logexterior\
			+ ")  Interior " + str(sci_not(self.interior_pixels)) + ' (' + self.loginterior +')'  \
			,(0,0,0),font=font)


	def draw_all_pixels_line(self):
		draw = PIL.ImageDraw.Draw(self.im)
		# line for all_pixels level in graph_image
		wd = self.im.width
		y = Y-self.y_unit*(log10(X*Y))
		draw.line((self.x_offset,y)+(wd,y),fill=Ruler.interior, width=4)

	def y_scale_labels(self):
		image_width = self.im.width

		draw1 = PIL.ImageDraw.Draw(self.im)
		font = ImageFont.load_default().font
		font = ImageFont.truetype("Verdana.ttf",18)

		# y_axis line
		draw1.line((self.x_offset,0)+(self.x_offset,Y),fill='black')  # mark zero point
		# y axis labels
		for i in range(7):
			draw1.text((self.x_offset-15, Y-i*Y/6),str(i),(0,0,0),font=font)

	def description(self,dp):
		draw = PIL.ImageDraw.Draw(self.im)
		font = ImageFont.load_default().font
		font = ImageFont.truetype("Verdana.ttf",18)

		self.exterior_pixels = self.all_pixels - self.interior_pixels
		self.calc_log_pixels()
	

		draw.text((50,10),"State " + str(self.dp) + "   # Hues " + str(self.n_hues) \
			+ "  # Pixels:  Total " + sci_not(self.all_pixels) + ' (5.4)  Exterior ' \
				   + str(sci_not(self.exterior_pixels)) + ' (' + self.logexterior\
			+ ")  Interior " + str(sci_not(self.interior_pixels)) + ' (' + self.loginterior +')'  \
			,(0,0,0),font=font)

	def log_pixel_groups(self):
		if self.interior_pixels > 1:
			self.loginterior = str(round( log10(self.interior_pixels), 1) )
		else: 
			self.loginterior = 'undefined'
		if self.exterior_pixels > 1:
			self.logexterior = str( round( log10(self.exterior_pixels), 1) )
		else: 
			self.logexterior = 'undefined'	

class Graph(WindowObject):
	label = 'G'
	width = int(3.5*X)
	# win = GraphWin('G',width,Y)

	def __init__(self,label):
		self.label = label

	def create_graphs(self):
		for dp in range(33):
			self.create_graph(dp)
	
	def create_graph(self,dp):
		# print(myself())
		self.hues_file(dp)
		self.hue_Lst(dp)
		self.hue_dictionary(dp)
		self.graph_image(dp)
		# self.analyse_pixels(dp)
		self.save_graph_file(dp)
		# self.show_graph(dp)

	def hues_file(self,dp):
		# print(myself())
		hfile = 'data/0530/hues' + str(dp) + '.txt'
		try:
			with open(hfile,"r") as f:
				self.hueStr = f.read()
		except:
			FileNotFoundError
			print(str(hfile),'not found')

	def show_graph(self,dp):
		# print(myself(),end=' ')
		try: 
			gfile = 'data/0530/gfile' + str(dp) + '.png'
			in_window(2.85*X,Y/2,gfile,self.win)
		except:
			FileNotFoundError
			print(gfile,'file not found')
		
	def hue_Lst(self,dp):
		# print(myself())
		self.hueStr = self.hueStr[1:-2]  # remove parens and extr CR at end
		lst = self.hueStr.split(', ')
		self.hueLst =  [float(l) for l in lst]
			
	def hue_dictionary(self,dp):
		# print(myself())
		self.hueDic = count_frequency(self.hueLst)
		# print(self.hueDic)
		self.n_hues = len(self.hueDic)
		self.all_pixels = X*Y
		self.graph_array = sorted( list( self.hueDic.items())  )

		# print('\n',dp,self.n_hues,self.graph_array[0:8])
		
	def graph_image(self,dp):
		# print(myself())
		y_unit = 0.95*Y/6
		x_offset = 35  # for writing y units
		
		self.image = PIL.Image.new('RGB', (int(2*X),Y), color = (255,255,255))
		self.image.pixels = self.image.load() 

		draw = PIL.ImageDraw.Draw(self.image)
		font = ImageFont.load_default().font
		font = ImageFont.truetype("Verdana.ttf",18)

		# y_axis line
		draw.line((x_offset,0) + (x_offset,Y), fill = 'black',width = 1 )
		
		# y axis labels
		for i in range(7):
			draw.text((x_offset-20, Y-i*y_unit),str(i),(0,0,0),font=font)

		# State number and number of hues
		draw.text((50,5),"State " + str(dp) +    ' #Hues: ' + str(self.n_hues),(0,0,0),font=font)

		

		i = 0
		for (k,v) in self.graph_array:
			y_draw = y_unit*(log10(v))  # y coord
			hue = k						# bar color
			x = i					# x coord  does not equal hue, but count(hue)
			x = x_offset + 25 + x	# space to y axis & extra offset of graph lines
				
			r,g,b = colorsys.hsv_to_rgb(hue,1,1)
			r,g,b = int(255*r),int(255*g),int(255*b)

			draw.line((x,Y-y_draw)+(x,Y),fill=(r,g,b),width=2)
			i += 2

	def save_graph_file(self,dp):
		gfile = 'data/0530/gfile' + str(dp) + '.png'
		self.image.save(gfile)

	def analyse_pixels(self,dp):
			
		# end of bars for interior pixels  last bar in graph_image

		self.interior_pixels = v   # at last graph bar plotted
		print('% interior pixels ',round( self.interior_pixels/(X*Y)  *100 ,0))
		draw.line((x,Y-y_draw)+(x,Y),fill=(r,g,b),width=3)
	
		self.exterior_pixels = self.all_pixels - self.interior_pixels

		# self.draw_all_pixels_line()

	
		if self.interior_pixels > 1:
			self.loginterior = str(round( log10(self.interior_pixels), 1) )
		else: 
			self.loginterior = 'undefined'
		if self.exterior_pixels > 1:
			self.logexterior = str( round( log10(self.exterior_pixels), 1) )
		else: 
			self.logexterior = 'undefined'

		# width = int( 2.5*Ruler.X )
		# self.im = PIL.Image.new("RGB", (width,Y), (255, 255, 255))

class ShowPair():
	def __init__(self) -> None:
		self.win = GraphWin('',3*X,Y)
		
		
	def show_image(self,ifile):
		ifile = 'data/0530/image' + str(dp) + '.txt'
		try: 
			in_window(X/2,Y/2,ifile,self.win)
		except:
			FileNotFoundError

	def create_graph(self,dp):
		pass
	
	def show_graph(self,dp):
		gfile = 'data/0530/gfile' + str(dp) + '.png'

		try: 
			in_window(X/2,Y/2,ifile,self.win)
		except:
			FileNotFoundError

	def show_collection(self):
		dp = 0
		while True:
			gfile = 'data/0530/gfile' + str(dp) + '.png'
			in_window(3*X,Y/2,gfile,self.win)
			ifile = 'data/0530/image' + str(dp) + '.png'
			in_window(X/2,Y/2,ifile,self.win)

			dp = self.click_transfer(dp)

	def	click_transfer(self,dp):
			clk = self.win.getMouse()
			cx,cy = clk.x,clk.y
			if cx < X: dp -= 1
			else: dp += 1
			return dp

class Viewer():

	def __init__(self, label):
		self.label = label
		self.wo = WindowObject('G')
		self.wo.graphic()
		

	

	def show_images(self,dir):
		print(myself())
		print(dir)
		fLst = os.listdir(dir)
		dp = 0
		while True:
			ifile = dir + '/image' + str(dp) + '.png'
			try:
				im = PIL.Image.open(ifile)
				in_window(X/2,Y/2,ifile,self.wo.win)
				self.wo.win.getMouse()
			except:
				FileNotFoundError
				print('not found')


			dp += 1
		for f in fLst:
			if not f=='locations.txt':
				file = dir + '/' + f
				try:
					# im = PIL.Image.open(file)
					in_window(X/2,Y/2,file,self.wo.win)
					self.wo.win.getMouse()
				except:
					FileNotFoundError
					print('not found')

		exit()

		in_window(X/2,Y/2,imfile,self.super.wo.win)

		
	def thumbnails(self):
		dp = 0
		while True:
			self.make_thumbnail(dp)
			# vw.win.getMouse()
			dp += 1

	def view0527(self,directory):
		print(myself())
		# directory = 'data/jhw0527'
		directory = 'data/0530'
		fLst = file_list(directory)
		print( os.listdir(directory) )

		# sort images
		for n in range(len(fLst)):
			f = 'data/05230/image' + str(n) + '.png'
			print(f)
			# im = PIL.Image.open(f)
			
			# in_window(X/2,Y/2,f,self.win)
			self.win.getMouse()


class Menu(WindowObject):
	def __init__(self, label,directory):
		self.label = label
		self.directory = directory
		super().__init__(label)

	@property
	def data_file_directoryx(self,seq):
		if seq==0:
			directory = 'data/sequence_baby_mand'
		elif seq==1:
			directory = 'data/movie_sequence' 
		elif seq==2:
			directory = 'data/varied_path'
		elif seq==3:
			directory = '0525'
		return directory
	
	@property
	def image_file_name_stemx(typ):
		if typ=='image':
			stem = '/ifile_'
		elif typ=='tnail':
			stem = '/tfile_'
		return stem

	def place_tnails(self):
		self.win.setCoords(-0.5,-0.5,3.5,4.5)
		directory= self.data_file_directory(3)
		for p in range(len(self.fLst)):
			thfile = stem + str(p+2) + '.png'
			print(thfile)
			try: 
				img = PIL.Image.open(thfile)
			except:
				FileNotFoundError
				return
			# tnail coords and dp
			j,i = 4 - p//4, p%4
			in_window(i ,j,thfile,m.win)
			Text(Point(i,j),str(p+2)).draw(m.win).setFill('white')

	def select_tnail(self):
		while True:
			clk = m.win.getMouse()
			cx,cy = clk.x,clk.y
			ci = Circle(Point(cx,cy),0.04).draw(m.win)

			n = len(self.fLst)
			for p in range(n-2):
				j,i = 4 - p//4, p%4
				if abs(cx-i) < 0.3 and abs(cy-j) < 0.3:
					ci.setFill('cyan')
					imfile = self.image_file(1,'tnail')
					print(p+2,imfile)
					return imfile

	def file_list(self,dir_name='data/movie_sequence'):
		self.fLst = []
		for f in os.listdir(dir_name):
			if f.startswith('image_file'):
				self.fLst.append(f)

	def make_thumbnail(self,dp):
		if hasattr(self,'tnail'):
			return
		try: 
			img = PIL.Image.open(self.tnail)
		except:
			FileNotFoundError
			return
		
		self.tnail = self.directory + '/tfile' + str(dp) + '.png'
		img.thumbnail((100,100))
		img.save(self.tnail)

	def interact(self):
		# self.dir =self.dir1
		while True:
			imfile = m.select_tnail()
			m.vw.show_image_file(imfile)

class Task():
	def __init__(self,name) -> None:
		self.name = name
		# gr = Graph('G')

		if name=='create_graphs':
			for dp in range(1,15):
				gr = Graph('G')
				gr.create_graph(dp)

		elif name=='create_graph':
			gr = Graph('G')
			dp = 0
			gr.create_graph(dp)

		elif name=='show_image_create_graph':
			win = GraphWin('',3*X,Y)
			for dp in range(30):
				gr = Graph('G')

				ifile = 'data/0530/image' + str(dp) + '.png'
				in_window(X/2,Y/2,ifile,win)
				gr.create_graph(dp)

				gfile = 'data/0530/gfile' + str(dp) + '.png'
				in_window(3.9*X/2,Y/2,gfile,win)
				win.getMouse()

		elif name=='show_image_create_one_graph':
			gr = Graph('G')
			
			ifile = 'data/0530/image' + str(dp) + '.png'
			in_window(X/2,Y/2,ifile,win)
			gr.create_graph(dp)

			gfile = 'data/0530/gfile' + str(dp) + '.png'
			in_window(3.9*X/2,Y/2,gfile,win)
			win.getMouse()



		
		elif name=='show_images':
			vw = Viewer('G')
			vw.show_images('data/0530')

		elif name=='show_collection':
			pr = ShowPair()
			pr.show_collection()





if __name__ == "__main__":
	


	Task('show_image_create_graph')   # 14
	# Task('show_collection')



	


	
		


			

	