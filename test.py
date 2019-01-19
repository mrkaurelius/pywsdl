import pickle 
import zeep
from lxml import etree

mydump = pickle.load(open("save.p","rb"))
print(mydump)