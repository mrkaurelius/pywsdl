from lxml import etree
import collections
import sys
#sys.stdout = open("buildsout.xml","w")

#basit ulke taslagı hazırla sonra edinilen bilgilerle xml türet
#python literaller ilginc onlara bir bak
#n11 soap cevaplarını kayıt edip onları etree ile okuyup oynanabilecek hale getir

"""
root = etree.Element("root")
root.append(etree.Element("child1"))
child2 = etree.SubElement(root,"child2")
child3 = etree.SubElement(root,"child3")
subchild1 = etree.SubElement(child2,"subchild1")
subsubchild = etree.SubElement(subchild1,"asdfafd")
print(etree.tostring(root,pretty_print=True).decode("utf-8"))
"""

#avrupa birliği ulkereli baskentleri birde subelement icin birsey uydur 
root = etree.Element("eucountry")

country = etree.SubElement(root,"fullname")
capital = etree.SubElement(root,"capital")
regions = etree.SubElement(root,"regions")
region1 = "Branderburg"
region2 = "Saxony"
region1a = etree.SubElement(regions,"region")
region2a = etree.SubElement(regions,"region")

fn = "The Federal Republic of Germany"
cap = "Berlin"
#childa deger girmeyi nasıl yapacagız iste boyle
#degisken isimleri daha guzel olabilir
country.text = fn
capital.text = cap
region1a.text = region1
region2a.text = region2
print(etree.tostring(root,pretty_print=True).decode("utf-8"))

#as oredered list 

orderedEu = collections.OrderedDict()
orderedRegion = collections.OrderedDict()

orderedRegion['regions'] = region2
orderedRegion['regions'] = region1 # orederdic degilde orderdicteki listeye ekleme yapmaya calıs
orderedRegion.append(region2)
orderedEu['capital'] = cap
orderedEu['fullname'] = fn

print(orderedEu)
print(orderedRegion)
#xmlin sonuna tail ekleyebiliyoruz neden boyle birsey lazm bilmiyorum

# TREE ITERATION
