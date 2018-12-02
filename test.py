import zeep
import xml 
from zeep import Client , Settings
from zeep.plugins import HistoryPlugin

#!!!Complex tipli cevapları alamıyorum dokumantasyonda var 
#n11 referansındakilerin cogu calısmıyor
#CALISANLAR wsdl de tanımlı olanlar calısıyor
#result = client.service.GetTopLevelCategories(auth)
#result = client.service.GetCategoryAttributeValue(auth,categoryId,pagingData) -> neye yaradagını anlayamadım geri dondugu liste boş
#result = client.service.GetParentCategory(auth,SubCategoryId)

#result = client.service.GetCategoryAttributes(auth,categoryId,pagingData) -> parse ederken hata veriyor buyuk ihtimal zeep ile alakalı
#result = client.service.GetCategoryAttributesId(auth,categoryId) -> aynı hata 

authfileName = "auth";
lines = [line.rstrip('\n') for line in open(authfileName)] # file objesi ???
appKey = lines[0]
appSecret = lines[1]

auth = { 'appKey' : appKey , 'appSecret' : appSecret}
settings = Settings(strict=False, xml_huge_tree=True)
wsdl = 'https://api.n11.com/ws/CategoryService.wsdl'
history = HistoryPlugin()
client = zeep.Client(wsdl=wsdl,plugins=[history],settings = settings)



SubCategoryId = 1002958
categoryId = 1003221
pagingData = {'currentPage' : 0 , 'pageSize' : 100}

result = client.service.GetCategoryAttributesId(auth,SubCategoryId)

# raw elements i foreach ile itere edebilir miyim
print(result.categoryProductAttributeList)

print(result)
print(">>>" + result.result['status'])

print(history.last_sent)
print(history.last_received)

"""
for categoryItem in result.categoryList.category:
	print("kategori numarası -> "+str(categoryItem['id']) +" "+ categoryItem['name'])
	i = i + 1
	pass
"""