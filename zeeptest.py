import zeep
import sys
import collections
import json
from lxml import etree
from zeep import Client , Settings, helpers
from zeep.plugins import HistoryPlugin
sys.stdout = open("buildsout","w")

def GetTopLevelCatIterate(): #GetTopLevelCategories
	# fonksyon mantıgını anlamak lazım wsdl nesnesine nasıl bir erişim oluyor
	# **kwargs ve mapping detayı var onları simdılık atlayacağım ve çağrıları burdan yapmaya calısacağım
	result_topCategories = client.service.GetTopLevelCategories(auth)
	myResultOrderedDict = zeep.helpers.serialize_object(result_topCategories, target_cls= collections.OrderedDict)
	orderedCats = myResultOrderedDict['categoryList']
	bareCatList = orderedCats['category']
	for listElement in bareCatList:
		print(str(listElement['id']) , str(listElement['name'])) # evet metodun ıskeleti ortaya cıktı
		pass
	#returne gerek varmı gerekli iterasyonu burda yaparız gibi

def GetSubCategoriesIterate():
	# 1003221 Fitness & Kondisyon ana kategori 
	fcat = 1003221
	result_subCategories = client.service.GetSubCategories(auth,fcat)
	myResultOrderedDict = zeep.helpers.serialize_object(result_subCategories, target_cls= collections.OrderedDict)
	parentCat = myResultOrderedDict['category'] #buradan istersem ust kategoriyide itere edebilirim 
	print(parentCat) #!!! üst kategoriler birden falza olabirmi ?? 
	#BURADA KALDIM 

###!!! NESNESLER BU YONTEMLE ERISMENIN ZARARLARI NE OLABLIR
authfileName = "auth";
lines = [line.rstrip('\n') for line in open(authfileName)] # file objesi ???
appKey = lines[0]
appSecret = lines[1]
auth = { 'appKey' : appKey , 'appSecret' : appSecret}
settings = Settings(strict=False, xml_huge_tree=True)
wsdl = 'https://api.n11.com/ws/CategoryService.wsdl' 
history = HistoryPlugin()
client = zeep.Client(wsdl=wsdl,plugins=[history],settings = settings)

pagingData = {'currentPage' : 0 , 'pageSize' : 100}

#GetTopLevelCatIterate() #GetTopLevelCategories
GetSubCategoriesIterate()


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