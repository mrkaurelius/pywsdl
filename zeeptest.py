import zeep
import sys
import collections
import json
from lxml import etree
from zeep import Client , Settings, helpers
from zeep.plugins import HistoryPlugin
sys.stdout = open("buildsout","w")

def GetTopLevelCatIterate(): 
	# fonksyon mantıgını anlamak lazım wsdl nesnesine nasıl bir erişim oluyor
	# **kwargs ve mapping detayı var onları simdılık atlayacağım ve çağrıları burdan yapmaya calısacağım
	client = categoryDriver()
	result_topCategories = client.service.GetTopLevelCategories(auth)
	myResultOrderedDict = zeep.helpers.serialize_object(result_topCategories, target_cls= collections.OrderedDict)
	print(">>> result: ", result_topCategories['result']['status'])
	#!!! bunu GetSubCategoriesIterate gore duzenle
	orderedCats = myResultOrderedDict['categoryList']
	bareCatList = orderedCats['category']
	for listElement in bareCatList:
		print(str(listElement['id']) ," -> ", str(listElement['name'])) # evet metodun ıskeleti ortaya cıktı
		pass
	#returne gerek varmı gerekli iterasyonu burda yaparız gibi
	pass

def GetSubCategoriesIterate(): #!!!SIKINTI #!!! mainCatId icin parametre ayarla PARAMETRELERİ OGREN 
	# 1003221 Fitness & Kondisyon ana kategori 
	client = categoryDriver()
	mainCatId = 1003221
	full_result = client.service.GetSubCategories(auth,mainCatId)
	full_result_ordered = zeep.helpers.serialize_object(full_result, target_cls= collections.OrderedDict)
	print(">>> result: ", full_result['result']['status'])
	#BURADAKI SKINITI GELEN CEVABIN birden fazla olması subcatlistin sizeında for ile birseyler yapılabilir
	subCatOrderedDict = full_result_ordered['category'][0]['subCategoryList'] #buradan istersem ust kategoriyide itere edebilirim 
	#print(subCatOrderedDict) #!!! üst kategoriler birden falza olabirmi ?? 
	for DictElement in subCatOrderedDict['subCategory']:
		print(type(DictElement))
		print(str(DictElement['id']) ," -> ", str(DictElement['name']))
	pass

def GetParentCategoryIterate():
	client = categoryDriver()
	subCategoryID = 1003234
	full_result = client.service.GetParentCategory(auth,subCategoryID)
	full_result_ordered = zeep.helpers.serialize_object(full_result, target_cls= collections.OrderedDict)
	print(">>> result: ", full_result['result']['status'])
	print((full_result)) #zeep object 
	mydic = full_result_ordered['category']['parentCategory'] # zeep den ordereddict e cevirmesen bile bir sekilde calısıyor 
	print(str(mydic['id'] ) ," -> ", str(mydic['name']))

def GetCategoryAttributesIdIterate():#!!!SIKINTI !!!SIKINTI LXML
	client = categoryDriver()
	mainCatId = 1003221
	full_result = client.service.GetCategoryAttributesId(auth,mainCatId)
	full_result_ordered = zeep.helpers.serialize_object(full_result, target_cls= collections.OrderedDict)
	print(">>> result: ", full_result['result']['status'])
	#BURADAKI SKINITI GELEN CEVABIN birden fazla olması subcatlistin sizeında for ile birseyler yapılabilir
	rawElement = full_result_ordered['categoryProductAttributeList']['categoryProductAttribute'][0]['_raw_elements']
	print(type(rawElement)) # deque e ulastık ama lxml.etree objesi 
	for dequeElement in rawElement:
		print(type(dequeElement))
		root = dequeElement.getroottree() #lxml i tuttuk bunu python data type nasıl kolay bit sekilde geciririz
		print(etree.tostring(root,pretty_print=True).decode("utf-8"))
		pass
	#lxml ogrenip kendim birseyler yapsam daha kolay olur gibi
	#!!!LXML DE BIRAKTIM
	#https://stackoverflow.com/questions/7684333/converting-xml-to-dictionary-using-elementtree BURADA BIR ORNEK VAR
	print(rawElement)
	pass

def GetCategoryAttributeValueIterate():
	client = categoryDriver()
	myID = 354080385
	ApıRefID = 354080997 # hoparlor galiba
	pagingData = {'currentPage' : 0 , 'pageSize' : 100}
	full_result = client.service.GetCategoryAttributeValue(auth,myID,pagingData)
	full_result_ordered = zeep.helpers.serialize_object(full_result, target_cls= collections.OrderedDict)
	print(">>> result: ", full_result['result']['status'])
	atrrList = full_result_ordered['categoryProductAttributeValueList']['categoryProductAttributeValue']
	for listElement in atrrList:
		print(str(listElement['id']) ," -> ", str(listElement['name']) , "dependedName" ,str(listElement['dependedName']) )
		pass

#bu son olsun bu son
def GetCategoryAttributesIterate(): # !!!SIKINTI LXML
	client = categoryDriver()
	mainCatId = 1003221
	pagingData = {'currentPage' : 0 , 'pageSize' : 100}
	full_result = client.service.GetCategoryAttributes(auth,mainCatId,pagingData)
	full_result_ordered = zeep.helpers.serialize_object(full_result, target_cls= collections.OrderedDict)
	print(">>> result: ", full_result['result']['status'])
	print(full_result)
	#BU OZELLİKLERİ TUTMAK GEREKIRMI full_result_ordered['category']
	rawElement = full_result_ordered['category']['_raw_elements']
	print(type(rawElement))
	for dequeElement in rawElement:
		print(type(dequeElement))
		root = dequeElement.getroottree() #lxml i tuttuk bunu python data type nasıl kolay bit sekilde geciririz
		print(etree.tostring(root,pretty_print=True).decode("utf-8"))
		pass		
	#lxml ogrenip kendim birseyler yapsam daha kolay olur gibi
	#!!!LXML DE BIRAKTIM
	print(rawElement)
	pass

def categoryDriver():	
	settings = Settings(strict=False, xml_huge_tree=True)
	wsdl = 'https://api.n11.com/ws/CategoryService.wsdl' 
	history = HistoryPlugin()
	client = zeep.Client(wsdl=wsdl,plugins=[history],settings = settings)
	return client
	pass

###!!! NESNESLER BU YONTEMLE ERISMENIN ZARARLARI NE OLABLIR
###!!! SIKINTILI OLANLAR ANA KATEGORİLER DISINDA PATLIYOR
###!!! NEYI NEYLE ATLATICAGIMIZI IYICE KAVRA

authfileName = "auth";
lines = [line.rstrip('\n') for line in open(authfileName)] # file objesi ???
appKey = lines[0]
appSecret = lines[1]
auth = { 'appKey' : appKey , 'appSecret' : appSecret}

"""
settings = Settings(strict=False, xml_huge_tree=True)
wsdl = 'https://api.n11.com/ws/CategoryService.wsdl' 
history = HistoryPlugin()
client = zeep.Client(wsdl=wsdl,plugins=[history],settings = settings)
"""
pagingData = {'currentPage' : 0 , 'pageSize' : 100}

#categoryDriver() #!!! DETAYLI TESTLERINI YAP simdilik hata yok
#GetTopLevelCatIterate() #GetTopLevelCategories
#GetSubCategoriesIterate() #Parametre ayarla #!!!SIKINTI 
#GetParentCategoryIterate() 
#GetCategoryAttributesIdIterate() #!!!SIKINTI !!!SIKINTI LXML
#GetCategoryAttributeValueIterate()
#GetCategoryAttributesIterate() #!!!SIKINTI LXML

# 10.12.18 07:37 BURADA KALDIM KATEGORILER NEREDEYSE BITTI

""" 
requesti lxml formatına cevirme
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

#print(history.last_sent)
#print(history.last_received)