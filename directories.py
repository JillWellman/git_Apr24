# directories.py

import os
import pathlib

print( pathlib.Path.cwd )
print( pathlib.Path )


dir_sdz = '../'



def print_files(dir_name):
	print()
	for x in os.listdir(dir_name):
		print(x)

print_files(dir_sdz)
# print_files('my-python-project')


exit()