# id numbers repr

class Data():
	def __init__(self,id,number):
		self.id = id
		self.number = number

	def __repr__(self):
		return str(self.id) + ' ' + str(self.number) 

for i in range(3):
	id = i + 4
	dt = Data(id,600)
	print(dt)

