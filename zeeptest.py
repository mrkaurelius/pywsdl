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

def GetSubCategoriesIterate(): #!!! mainCatId icin parametre ayarla  # BUNU BIRDE TEST ET
	# 1003221 Fitness & Kondisyon ana kategori 
	client = categoryDriver()
	mainCatId = 1003221 #fitness
	full_result = client.service.GetSubCategories(auth,mainCatId)
	full_result_ordered = zeep.helpers.serialize_object(full_result, target_cls= collections.OrderedDict)
	print(">>> result: ", full_result['result']['status'])
	print(full_result)
	#subCatOrderedDict = full_result_ordered['category'][0]['subCategoryList'] #buradan istersem ust kategoriyide itere edebilirim 
	mylists = full_result_ordered['category']
	for mainListElement in mylists:				#BIRDEN FAZLA KATEGORİ GELIRSE ONLARI ISLEMEK ICIN, 	
		mainID = mainListElement['id']			#BUNLARI BU SEKILDE KULLANMAK ETKILI OLMAZ 
		mainName = mainListElement['name']
		subCategory = mainListElement['subCategoryList']['subCategory']
		for subCategoryDict in subCategory:
			for k,v in subCategoryDict.items():
				print(k,v)		#BUNUN FAYDALRI VAR AMA HER IMPLEMENTASYONDA GEREKLI OLACAK MI ?
				pass
		pass

	"""	
	for DictElement in subCatOrderedDict['subCategory']:
		print(type(DictElement))
		print(str(DictElement['id']) ," -> ", str(DictElement['name']))
	pass
	"""

def GetParentCategoryIterate():
	client = categoryDriver()
	subCategoryID = 1003234
	full_result = client.service.GetParentCategory(auth,subCategoryID)
	full_result_ordered = zeep.helpers.serialize_object(full_result, target_cls= collections.OrderedDict)
	print(">>> result: ", full_result['result']['status'])
	print((full_result)) #zeep object 
	mydic = full_result_ordered['category']['parentCategory'] # zeep den ordereddict e cevirmesen bile bir sekilde calısıyor 
	print(str(mydic['id'] ) ," -> ", str(mydic['name']))

def GetCategoryAttributesIdIterate():#!!!SIKINTI LXML'i recursive sekilde itere etmenin yolunu ara 
	#rawelementleri buluyour ITEREETMIYOR
	client = categoryDriver()
	mainCatId = 1003221
	full_result = client.service.GetCategoryAttributesId(auth,mainCatId)
	full_result_ordered = zeep.helpers.serialize_object(full_result, target_cls= collections.OrderedDict)
	print(">>> result: ", full_result['result']['status'])
	#print(full_result)
	#BURADAKI SKINITI GELEN CEVABIN birden fazla olması subcatlistin sizeında for ile birseyler yapılabilir
	categoryProductAttributeList = full_result_ordered['categoryProductAttributeList']['categoryProductAttribute']
	#print(type(rawElement)) # deque e ulastık ama lxml.etree objesi 
	# liste olan categoryProductAttribute
	for listElement in categoryProductAttributeList:
		#print(listElement)	
		for dequeElement in listElement['_raw_elements']:
			root = dequeElement.getroottree() #lxml i tuttuk bunu python data type nasıl kolay bit sekilde geciririz
			print(etree.tostring(root,pretty_print=True).decode("utf-8"))
			pass
		pass


	#https://stackoverflow.com/questions/7684333/converting-xml-to-dictionary-using-elementtree BURADA BIR ORNEK VAR
	#zeep rawelementin valid oldugunu anlamıyormu yoksa ben mi beceremiyorum
	#!!! lxml.etree zeep donusumu yapmam lazım yada direkt lsml python native baska bir sekilde donusturecegim (recursive tree iterate)
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

def GetCategoryAttributesIterate(): # !!!SIKINTI LXML'i recursive sekilde itere etmenin yolunu ara
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

def getGetCities():
	client = cityDriver()
	full_result = client.service.GetCities()
	full_result_ordered = zeep.helpers.serialize_object(full_result, target_cls= collections.OrderedDict)
	print(">>> result: ", full_result['result']['status'])
	#print(full_result)
	cityList = full_result_ordered['cities']['city']
	#print(type(cityList))
	for listElement in cityList:
		#print(listElement) -> ordereddict 
		print(str(listElement['cityCode']) ," -> ", str(listElement['cityId']) ," -> ", str(listElement['cityName']) ) 
		pass
	pass

def getGetCity():
	cityPlate = 29
	client = cityDriver()
	full_result = client.service.GetCity(cityPlate)
	full_result_ordered = zeep.helpers.serialize_object(full_result, target_cls= collections.OrderedDict)
	print(">>> result: ", full_result['result']['status'])
	print(full_result)
	cityAttr = full_result_ordered['city']
	for k, v in cityAttr.items(): #bu standarta mı donsem
		print(k ,v)
		pass
	pass

def getGetDistrict(): #!!!SIKINTI LXML #!!!gerekesız yere 6 array donuyor buyuk ihtimal n11 hatası  #alt ilçeleri listeleme
	#root = dequeElement.getroottree() #lxml i tuttuk bunu python data type nasıl kolay bit sekilde geciririz
	#print(etree.tostring(root,pretty_print=True).decode("utf-8"))
	cityPlate = 29
	client = cityDriver()
	full_result = client.service.GetDistrict(cityPlate)
	full_result_ordered = zeep.helpers.serialize_object(full_result, target_cls= collections.OrderedDict)
	print(">>> result: ", full_result['result']['status'])
	print(full_result) #!!! ilçe bilgileri raw element geldi 
	districstList = full_result['districts']['district'] #!!! full_result_ordered KULLANILMADI
	for listElement in districstList:
		dequeElement =  listElement['_raw_elements']
		for x in dequeElement:
			root = x.getroottree()
			print(etree.tostring(root,pretty_print=True).decode("utf-8")) #!!! SOAP DECODING ?
		pass

def getGetNeighborhoods(): #!!!SIKINTI LXML
	# 22339 gümüşhane merkez
	districtId = 22339 
	client = cityDriver()
	full_result = client.service.GetNeighborhoods(districtId)
	full_result_ordered = zeep.helpers.serialize_object(full_result, target_cls= collections.OrderedDict)
	print(">>> result: ", full_result['result']['status'])
	neighborhoodsList = full_result_ordered['neighborhoods']['neighborhood']
	for listElement in neighborhoodsList:
		rawElement = listElement['_raw_elements']
		for dequeElement in rawElement:
			root = dequeElement.getroottree() #lxml i tuttuk bunu python data type nasıl kolay bit sekilde geciririz
			print(etree.tostring(root,pretty_print=True).decode("utf-8"))
			pass
		#print(type(rawElement))
		pass
	print(full_result)
	pass

def categoryDriver():	
	settings = Settings(strict=False, xml_huge_tree=True)
	wsdl = 'https://api.n11.com/ws/CategoryService.wsdl' 
	history = HistoryPlugin()
	client = zeep.Client(wsdl=wsdl,plugins=[history],settings = settings)
	return client
	pass

def cityDriver():
	settings = Settings(strict=False, xml_huge_tree=True)
	wsdl = 'https://api.n11.com/ws/CityService.wsdl' 
	history = HistoryPlugin()
	client = zeep.Client(wsdl=wsdl,plugins=[history],settings = settings)
	return client
	pass	

def productDriver():
	settings = Settings(strict=False, xml_huge_tree=True)
	wsdl = 'https://api.n11.com/ws/ProductService.wsdl'
	history = HistoryPlugin()
	client = zeep.Client(wsdl=wsdl,plugins=[history],settings = settings)
	return client
	pass

def getGetProductList():
	pagingData = {'currentPage' : 0 , 'pageSize' : 100}
	client = productDriver()
	full_result = client.service.GetProductList(auth,pagingData)
	full_result_ordered = zeep.helpers.serialize_object(full_result, target_cls= collections.OrderedDict)
	print(">>> result: ", full_result['result']['status'])
	print(full_result)

###!!! EXCEPTİONLARI OGREN VE NETWORK EXEPCTİONLARINI AYALA
###!!! NESNESLER BU YONTEMLE ERISMENIN ZARARLARI NE OLABLIR
###!!! RAW ELEMENTSI ZEEP ILE HALLEDEBİLİR MIYIM 

#Ürün Listeleme (GetProductList) detaylı urun bilgilerini alabilmek icin bunu calıstır

authfileName = "auth";
lines = [line.rstrip('\n') for line in open(authfileName)] # file objesi ???
appKey = lines[0]
appSecret = lines[1]
auth = { 'appKey' : appKey , 'appSecret' : appSecret}
pagingData = {'currentPage' : 0 , 'pageSize' : 100}
 


#Parametre ayarla 
#categoryDriver() #!!! DETAYLI TESTLERINI YAP simdilik hata yok BOSUNA CAGIRMA PERFOMANSA ETKISI VAR
#cityDriver()
#GetTopLevelCatIterate() #GetTopLevelCategories
#GetSubCategoriesIterate() 
#GetParentCategoryIterate() 
#GetCategoryAttributesIdIterate() #!!!SIKINTI LXML # BURADA KALDIM
#GetCategoryAttributeValueIterate()
#GetCategoryAttributesIterate() #!!!SIKINTI LXML
#getGetCities()
#getGetCity()
#getGetDistrict()
#getGetNeighborhoods() #BUNLARI CACHE ALMANIN FAYDASI OLUR 
getGetProductList()

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