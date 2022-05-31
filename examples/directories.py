# directories.py
import PIL
from PIL import Image


import os
import pathlib



def print_files(dir_name):
	print()
	for x in os.listdir(dir_name):
		if x.startswith('image_file'):
			print(x)



def file_list1(dir_name,end_string):
	fLst = []

	for f in os.listdir(dir_name):
		if f.endswith(end_string):
			print(f)
			im = PIL.Image.open(dir_name +'/' + f)
			im.show()
			fLst.append(f)
	print(fLst)



dir_name = 'data/jhw0527'
file_list1(dir_name,'png')


	






exit()

print( pathlib.Path.cwd )
print( pathlib.Path )


# dira = './data/archive'
# print(dira)




# print(fileLst)

# print_files(dira)
# print( 'file0.png' in fileLst)


exit()