import zeep
import sys
import collections
import json
import pickle
from lxml import etree
from zeep import Client , Settings, helpers
from zeep.plugins import HistoryPlugin

sys.stdout = open("buildsout.xml","w")
	# fonksyon mantıgını anlamak lazım wsdl nesnesine nasıl bir erişim oluyor
	# **kwargs ve mapping detayı var onları simdılık atlayacağım ve çağrıları burdan yapmaya calısacağım
def GetTopLevelCatIterate(): 

	client = categoryDriver()
	full_result = client.service.GetTopLevelCategories(auth)
	full_result_ordered = zeep.helpers.serialize_object(result_topCategories, target_cls= collections.OrderedDict)
	print(">>> result: ", result_topCategories['result']['status'])
	orderedCats = full_result_ordered['categoryList']
	bareCatList = orderedCats['category']
	for listElement in bareCatList:
		print(str(listElement['id']) ," -> ", str(listElement['name'])) # evet metodun ıskeleti ortaya cıktı

def GetSubCategoriesIterate(): #!!! mainCatId icin parametre ayarla  # IC ICE FOR DA PRINT VAR TEST ET
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

def GetParentCategoryIterate():
	client = categoryDriver()
	subCategoryID = 1003234
	full_result = client.service.GetParentCategory(auth,subCategoryID)
	full_result_ordered = zeep.helpers.serialize_object(full_result, target_cls= collections.OrderedDict)
	print(">>> result: ", full_result['result']['status'])
	print((full_result)) #zeep object 
	mydic = full_result_ordered['category']['parentCategory'] # zeep den ordereddict e cevirmesen bile bir sekilde calısıyor 
	print(str(mydic['id'] ) ," -> ", str(mydic['name']))

def GetCategoryAttributesIdIterate():# TEK DEQUE ELEMENTI GELIYOR ILERIDE SIKINTI OLABILIR
	client = categoryDriver()
	mainCatId = 1003221
	full_result = client.service.GetCategoryAttributesId(auth,mainCatId)
	full_result_ordered = zeep.helpers.serialize_object(full_result, target_cls= collections.OrderedDict)
	print(">>> result: ", full_result['result']['status'])
	print(full_result)
	categoryProductAttributeList = full_result_ordered['categoryProductAttributeList']['categoryProductAttribute']
	for listElement in categoryProductAttributeList:
		for dequeElement in listElement['_raw_elements']:
			root = dequeElement.getroottree() #lxml i tuttuk bunu python data type nasıl kolay bit sekilde geciririz
			print(etree.tostring(root,pretty_print=True).decode("utf-8"))

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

def GetCategoryAttributesIterate(): # !!!BU TARZDA VALID VE TEKRARSIZ SONUC URETTI BURADAKI SONUCLARI INCELE VE KOLAYLASTIR, PAGINGI HATALI YAPIYORUM
	client = categoryDriver()
	mainCatId = 1003221
	pagingData = {'currentPage' : 0 , 'pageSize' : 126}
	full_result = client.service.GetCategoryAttributes(auth,mainCatId,pagingData)
	full_result_ordered = zeep.helpers.serialize_object(full_result, target_cls= collections.OrderedDict)
	#print(">>> result: ", full_result['result']['status'])
	#print(full_result)
	rawElement = full_result_ordered['category']['_raw_elements']
	for dequeElement in rawElement:
		#print(type(dequeElement))
		root = dequeElement.getroottree() 
		#print(etree.tostring(dequeElement,pretty_print=True).decode("utf-8"))
		break
	print(etree.tostring(root,pretty_print=True).decode("utf-8")) #ROOT SCOPTA KAYBOLMADI
			

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

def getGetDistrict(): # DISTRCITLER ARRAY SEKLINDE GELIYOR ILERIDE PROBLEM OLABILIR
	cityPlate = 29
	client = cityDriver()
	full_result = client.service.GetDistrict(cityPlate)
	full_result_ordered = zeep.helpers.serialize_object(full_result, target_cls= collections.OrderedDict)
	#print(">>> result: ", full_result['result']['status'])
	#print(full_result) 
	districstList = full_result['districts']['district'] #!!! full_result_ordered KULLANILMADI
	for listElement in districstList:
		dequeElement =  listElement['_raw_elements']
		for x in dequeElement:
			root = x.getroottree()
			#print(etree.tostring(root,pretty_print=True).decode("utf-8")) #!!! SOAP DECODING ?
	print(etree.tostring(root,pretty_print=True).decode("utf-8")) #!!! SOAP DECODING ?

def getGetNeighborhoods(): 
	# 22339 gümüşhane merkez
	districtId = 22339 
	client = cityDriver()
	full_result = client.service.GetNeighborhoods(districtId)
	full_result_ordered = zeep.helpers.serialize_object(full_result, target_cls= collections.OrderedDict)
	#print(">>> result: ", full_result['result']['status'])
	neighborhoodsList = full_result_ordered['neighborhoods']['neighborhood']
	for listElement in neighborhoodsList:
		rawElement = listElement['_raw_elements']
		for dequeElement in rawElement:
			root = dequeElement.getroottree() #lxml i tuttuk bunu python data type nasıl kolay bit sekilde geciririz
	print(etree.tostring(root,pretty_print=True).decode("utf-8"))

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

def getGetProductList(): #YENİ LXML COZUMU CALISIYOR
	pagingData = {'currentPage' : 2 , 'pageSize' : 3}
	client = productDriver()
	full_result = client.service.GetProductList(auth,pagingData)
	full_result_ordered = zeep.helpers.serialize_object(full_result, target_cls= collections.OrderedDict)
	productList = full_result_ordered['products']['product']
	for productElement in productList:
		rawElements = productElement['_raw_elements']
		myDeque = rawElements
		root = myDeque.pop().getroottree()
		print(etree.tostring(root,pretty_print=True).decode("utf-8"))

def getGetProductByProductId(): 
	productID = 301302394
	productSellerCode = '6C0129607L'
	client = productDriver()
	full_result = client.service.GetProductByProductId(auth,productID)
	full_result_ordered = zeep.helpers.serialize_object(full_result, target_cls= collections.OrderedDict)
	#print(full_result)
	myDeque =  full_result_ordered['product']['_raw_elements']
	root = myDeque.pop().getroottree()
	print(etree.tostring(root,pretty_print=True).decode("utf-8"))

def getGetProductBySellerCode():
	productSellerCode = '6C0129607L'
	client = productDriver()
	full_result = client.service.GetProductBySellerCode(auth,productSellerCode)
	full_result_ordered = zeep.helpers.serialize_object(full_result, target_cls= collections.OrderedDict)
	#print(full_result)
	myDeque = full_result_ordered['product']['_raw_elements']
	root = myDeque.pop().getroottree()
	print(etree.tostring(root,pretty_print=True).decode("utf-8"))

def getSaveProduct(): #KAYITLI URUN GOSTERIYORSA GUNCELLENIR YOKSA EKLENIR (UPSERT) #BU BIRAZ RISKLI ONCE ARAMAYI DENE
	client = productDriver()
	"""
	However instead of creating an object from a type defined in the XSD you can also pass in a dictionary.
	Zeep will automatically convert this dict to the required object (and nested child objects) during the call.
	client = Client('http://my-enterprise-endpoint.com')
	client.service.submit_order(user_id=1, order={
    'number': '1234',
    'price': 99,
	}) gibi aslında bunu basından beri yapıyordum bkz pagingdata
	"""

	#SaveProduct(auth: ns0:Authentication, product: ns0:ProductRequest) -> result: ns0:ResultInfo, product: ns0:ProductBasic
	productSellerCode = 'DENEMEU1296'
	productItem = dict()
	productItem.append(prod)

	#full_result = client.service.SaveProduct(auth,product)



def getSearchProducts():
	client = productDriver()
	pagingData = {'currentPage' : 0 , 'pageSize' : 1} #PAGING DATA BILDIGIMIZDEN FARKLI OLABILIR 
	#client = productDriver()
	#SIRANIN ONEMLI OLMADIGI SENERYU DENE
	productSearch = {
		'name' : 'Polo Hava Filtre Kutusu' ,
		'approvalStatus' : 1,
	}
	saleDate = {
		'startDate' : '26/11/2018' ,'endDate' : '01/01/2050'
	}
	productSearch['saleDate'] = saleDate #CALISIYAH
	print(productSearch)
	full_result = client.service.SearchProducts(auth,pagingData,productSearch);
	print(full_result)
	#SearchProducts(auth: ns0:Authentication, pagingData: ns0:RequestPagingData, productSearch: ns0:ProductSearch)
	# -> result: ns0:ResultInfo, products: ns0:ProductBasicList, pagingData: ns0:PagingData



###!!! ORNEK URUN XML'I OLUSTUR 
###!!! APININ SAGLADIGI URUN ARAMA SISTEMI KARMASIGA BENZIYOR
###!!! getGetProductByProductId()e göre lxml root bulmayı ayarla
###!!! PAGING'I HATALI YAPIYORUM CURRENT PAGE I BIR SEKILDE ARTTIRIP METHODU YENIDEN CALISTIR, YADA ZEEPI ARASTIR BASKA YOLU VARMI
		#>BAZI PAGINGLERI CACHE YAPARIM BAZILARINI ISE DRIVER ILE KULLANIRIM
###!!! LXML OBJELERINI NATIVE PYTHON A CEVIRMEYI BUL (XML'I JULLANMAK DAHA KOLAY OLACAK GIBI)
###!!! WSDLLERE GORE DOSYALARI AYIR (BELKI)

"""
###TODO 
	>EXCEPTİONLARI OGREN VE NETWORK EXEPCTİONLARINI AYALA
	>BASIT BIR DEMO SITESI HAZIRLA
	>XML GORUNTULEME SOUTU BIRBIRINDEN AYIR, BELKIDE BUNUN ICIN BIR FONKSYON YAZ
		> XMLI VE IO'YU EKRANA BASTIRAN FONKSYON BELKI
"""

authfileName = "auth";
lines = [line.rstrip('\n') for line in open(authfileName)] # file objesi ???
appKey = lines[0]
appSecret = lines[1]
auth = { 'appKey' : appKey , 'appSecret' : appSecret}

#categoryDriver() 
#cityDriver()
#GetTopLevelCatIterate() #GetTopLevelCategories
#GetSubCategoriesIterate() 
#GetParentCategoryIterate() 
#GetCategoryAttributesIdIterate() # TEK DEQUE ELEMENTI GELIYOR ILERIDE SIKINTI OLABILIR
#GetCategoryAttributeValueIterate()
#GetCategoryAttributesIterate() #!!!SIKINTI LXML
#getGetCities()
#getGetCity()
#getGetDistrict()
#getGetNeighborhoods() 
#getGetProductList() #YENİ LXML COZUMU CALISIYOR
#getGetProductByProductId() #YENİ LXML COZUMU CALISIYOR #GELEN KOMPLEKS CEVAPLARI BOYLE OKU 
#getGetProductBySellerCode()
#getSaveProduct()
getSearchProducts()

#print(history.last_sent)
#print(history.last_received)