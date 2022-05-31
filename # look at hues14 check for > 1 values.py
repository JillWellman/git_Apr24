# look at hues14  check for > 1 values
# import 'hues14_copy.txt'



with open('hues14_copy.txt',"r") as f:
	hueStr = f.read()

hueStr = hueStr[1:-2]  # remove parens and extr CR at end
lst = hueStr.split(', ')
hueLst =  [float(l) for l in lst]
print(hueLst[0:8])
print(max(hueLst))


