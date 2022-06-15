thumbnail_menu.py

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