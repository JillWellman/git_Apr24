# test write a and w



def write_location():
	data_string = [ str('3,4,5'),'8,9,10','slow cat']
	
	f = open("file.txt","w")
	f.write('quick fox')
	f.close()
		
	for s in data_string:
		with open('file.txt', 'a') as f:
			f.write('\n'+s)

write_location()


# output
"""
quick fox
3,4,5
8,9,10
slow cat

"""

