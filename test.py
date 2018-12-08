import collections

d = collections.OrderedDict()

x = 0
for x in range(1,10):
	d[str(x)] = ["thisis " + str(x * 10)]
	pass


for k,v in d.items():
	print (k, v)
	print(type(v)) #v nin tipi list 
#print(d['1'])
#print(d)