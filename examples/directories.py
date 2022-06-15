# directories.py

import os
import pathlib

def print_files(dir_name):
	print()
	for x in os.listdir(dir_name):
		if x.startswith('image_file'):
			print(x)

def file_list(dir_name):
	fLst = []
	for f in os.listdir(dir_name):
		if f.startswith('image_file'):
			fLst.append(f)
	print(fLst)
	

mydir = './'
print('mydir',mydir)
print(  os.listdir(mydir)  )
print()
wo_file = mydir + 'window_object1.py'
from window_object1 import *
print( wo_file )


exit()
print( pathlib.Path.cwd )
print( pathlib.Path )


# dira = './data/archive'
# print(dira)




# print(fileLst)

# print_files(dira)
# print( 'file0.png' in fileLst)


exit()