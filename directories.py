# directories.py

import os
import pathlib

print( pathlib.Path.cwd )
print( pathlib.Path )


dira = './data/archive'
print(dira)

def print_files(dir_name):
	print()
	for x in os.listdir(dir_name):
		print(x)

dira = './data/archive'
fileLst = [file for file in os.listdir(dira)]
print(fileLst)

print_files(dira)
print( 'file0.png' in fileLst)


exit()