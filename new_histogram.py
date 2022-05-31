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

class HueGraph(WindowObject):
	label = 'G'
	width = int(3.5*X)
	win = GraphWin('G',width,Y)

	def __init__(self,label):
		self.label = label

	def show_image(self,ifile):
		try: 
			in_window(X/2,Y/2,ifile,self.win)
		except:
			FileNotFoundError

	def show_graphs(self):
		dp = 0
		while True:
			hfile = 'data/jhw0527/hues' + str(dp) + '.txt'
			ifile = 'data/jhw0527/image' + str(dp) + '.png'
			gfile = 'data/jhw0527/gfile' + str(dp) + '.png'

			self.show_image(ifile)

			self.read_hueLst(dp)
			self.graph_numbers(dp)
			self.draw_graph_image(dp)
			self.show_graph(gfile)

			clk = self.win.getMouse()
			x,y = clk.x,clk.y
			if x < X: dp -= 1
			else: dp += 1

	def show_graph(self,gfile):
		try: 
			in_window(2.85*X,Y/2,gfile,self.win)
		except:
			FileNotFoundError
			print('file not found error')
			time.sleep(2)
			exit()
		

	def read_hueLst(self,dp):
		file_name = 'data/jhw0527/hues' 	+ str(dp) + '.txt'
		try:
			with open(file_name,"r") as f:
				hueStr = f.read()
		except:
			FileNotFoundError
			return
		hueStr = hueStr[1:-1]  # remove parens
		lst = hueStr.split(', ')
		self.hueLst =  [float(l) for l in lst]

	def graph_numbers(self,dp):
		self.hueDic = count_frequency(self.hueLst)
		# print(self.hueDic)
		self.n_hues = len(self.hueDic)
		self.all_pixels = X*Y
		self.graph_array = sorted( list( self.hueDic.items())  )


		print('\n',dp,self.n_hues,self.graph_array[0:8])
		
	def draw_graph_image(self,dp):
		y_unit = 0.95*Y/6
		x_offset = 35  # for writing y units
		
		self.image = PIL.Image.new('RGB', (int(3.5*X),Y), color = (255,255,255))
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
		vmax = 0
		for (k,v) in self.graph_array:
			y_draw = y_unit*(log10(v))  # y coord
			hue = k						# bar color
			x = i						# x coord  does not equal hue, but count(hue)
			x = x_offset + 5 + x
				
			r,g,b = colorsys.hsv_to_rgb(hue,1,1)
			r,g,b = int(255*r),int(255*g),int(255*b)

			draw.line((x,Y-y_draw)+(x,Y),fill=(r,g,b),width=1)
			i += 1

		# self.image.show()
		gfile = 'data/jhw0527/gfile' + str(dp) + '.png'
		self.image.save(gfile)
		# in_window(2.8*X,Y/2,gfile,self.win)
		# self.win.getMouse()

	
			
		# end of bars for interior pixels  last bar in graph_image

		self.interior_pixels = v
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

		width = int( 2.5*Ruler.X )
		self.im = PIL.Image.new("RGB", (width,Y), (255, 255, 255))

	

class Viewer(WindowObject):

	def __init__(self, label):
		super().__init__(label)

	

	def show_image_file(self,imfile):
		# print(myself())
		# print(imfile)
		try:
			im = PIL.Image.open(imfile)
		except:
			FileNotFoundError

		in_window(X/2,Y/2,imfile,self.super.wo.win)

	def show_graph_file(self,dp):
		file = 'data/movie_sequence/graph_image_fileB' + str(dp) + '.png'
		print(file,end=' ')
		try: 
			PIL.Image.open(file)
			in_window(2.25*X,Y/2,file,vw.win)
	
		except:
			FileNotFoundError
			print('not found',end='')
		print()
		
	def thumbnails(self):
		dp = 0
		while True:
			self.make_thumbnail(dp)
			# vw.win.getMouse()
			dp += 1

	def view0530(self):
		print(myself())
		directory = 'data/jhw0530'
		print(os.listdir(directory))
		file_list1(directory)
		# end_string = '.png'
		# fLst = file_list(directory,end_string)
		# f1Lst = []

		# sort images
		for n in range(len(fLst)):
			f = 'data/jhw0527/image' + str(n) + '.png'
			# show images
			im = PIL.Image.open(f)
			in_window(X/2,Y/2,f,self.win)
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
		print(name)
		self.name = name
		hg = HueGraph('G')
		if name=='viewjhw0530':
			vw = Viewer('X')
			vw.view0530()
		elif name=='create_graphs':
			hg = HueGraph('G')
			hg.create_graphs()
			dp = 0
			hg.read_hueLst(dp)
			hg.graph_numbers()
			hg.draw_image()

			# hfile = 'data/jhw0527/hfile' + str(dp) + '.txt'

			# gfile = 'data/jhw0527/gfile' + str(dp) + '.png'
			# hg.image.save(gfile)
		elif name=='show_graphx':
			dp = 5
			gfile = 'data/jhw0527/gfile5.png'
			PIL.Image.open(gfile)
			hg.show_graph(dp)

		elif name=='show_graphx':
			hg = HueGraph('G')
			dp = 5
			hg.read_hueLst(dp)
			hg.graph_numbers(dp)
			hg.draw_image(gfile)

		
		
		elif name=='show_images':
			hg = HueGraph('G')
			hg.show_graphs()

		elif name=='show_image':
			dp = 5
			ifile = 'data/jhw0527/ifile5.png'
			hg = HueGraph('G')
			hg.show_image(dp)

		elif name=='show_graphs':
			hg = HueGraph('G')
			hg.show_graphs()

		elif name=='test_pil_drawing':
			# GraphAnnotations()
			hg = HueGraph('')
			hg.draw_image(5)
			hg.show_graph(5)
			hg.win.getMouse()

	



if __name__ == "__main__":
	


	# tsk = Task('test_pil_drawing')

	tsk = Task('view0530')

	# tsk = Task('show_graphs') 

	# tsk = Task('show_graph')

	# tsk = Task('show_images')

	# tsk = Task('show_all')


	

	
		


			

	