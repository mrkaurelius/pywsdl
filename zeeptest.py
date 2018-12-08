import zeep
import sys
import collections
import json
from lxml import etree
from zeep import Client , Settings, helpers
from zeep.plugins import HistoryPlugin
#sys.stdout = open("buildsout","w")

#kompleks tiplere cevap alabildim serizlize etmem gerekiyor
#deque yada ordered list sekinde serialize edebilirim ordered list i becerebildim 
#kompleks cevabı orderedlist'e cevirebildim ama ordered listini cindede unserialised bolum var
#result = client.service.GetTopLevelCategories(auth)
#result = client.service.GetCategoryAttributeValue(auth,categoryId,pagingData) -> neye yaradagını anlayamadım geri dondugu liste boş
#result = client.service.GetParentCategory(auth,SubCategoryId)

authfileName = "auth";
lines = [line.rstrip('\n') for line in open(authfileName)] # file objesi ???
appKey = lines[0]
appSecret = lines[1]

auth = { 'appKey' : appKey , 'appSecret' : appSecret}
settings = Settings(strict=False, xml_huge_tree=True)
wsdl = 'https://api.n11.com/ws/CategoryService.wsdl' #typo was here
history = HistoryPlugin()
client = zeep.Client(wsdl=wsdl,plugins=[history],settings = settings)

SubCategoryId = 1002958
categoryId = 1003221
pagingData = {'currentPage' : 0 , 'pageSize' : 100}

#zeep objesini ordereddict e donusturup ilk olarak recursive olmadan sonra recursive bir bicimde kendim olusturabilirim
result_topCategories = client.service.GetTopLevelCategories(auth)
print(type(result_topCategories))
print(result_topCategories)

myOrederedDict = zeep.helpers.serialize_object(result_topCategories, target_cls= collections.OrderedDict)
#print(zeep.helpers.guess_xsd_type(myOrederedDict)) xsd:string
#ordereddict'pickle ile ayırmaya calıs ordan lxmltest.py ye geç (ordered pick zor olacak gibi)
#ordered listten sonra buyuk ihtimal deque de lazım olacak
print("myOrederedDict -> ")
print(myOrederedDict['categoryList'])

orderedCats = myOrederedDict['categoryList']

""" requesti lxml formatına cevirme
client1 = Client('https://api.n11.com/ws/CategoryService.wsdl')
node = client1.create_message(client1.service,'GetTopLevelCategories',auth = auth)
print(type(node))
#requesti alabildik peki cevabı alabilecek miyiz
#create_mesage lxml objesi mi donduruyor EVET 
print(etree.tostring(node,pretty_print=True).decode("utf-8"))
"""

#result = client.service.GetCategoryAttributesId(auth,SubCategoryId)
#raw elements i foreach ile itere edebilir miyim
#print(result.categoryProductAttributeList.categoryProductAttribute[0])

"""	 bu sekildede yapmaya calıs
Mydeque = result.categoryProductAttributeList.categoryProductAttribute[0]
serializedDeque = zeep.helpers.serialize_object(Mydeque, target_cls= collections.deque)
print("deque unserialised \n" + Mydeque + "serialized deque \n"  + serializedDeque)
"""


#bu deque objesini nasıl işlerim  kuyruk çalşıyor gibi 03.11.18 BURADA KALDIM 	 

"""
for listelement in serializedRawElements:
	print("liste elementlerin tipleri -> ")
	print(type(listelement))
	print(etree.tostring(listelement,pretty_print = True))
	pass
	#neden basic tipleri itere edemedi ama tıpı ogrendik <class 'lxml.etree._Element'>
"""
#print(">>>" + topCategories.result['status'])

#print(history.last_sent)
#print(history.last_received)

"""
for categoryItem in result.categoryList.category:
	print("kategori numarası -> "+str(categoryItem['id']) +" "+ categoryItem['name'])
	i = i + 1
	pass
"""