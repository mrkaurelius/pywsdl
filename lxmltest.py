from lxml import etree
import sys
sys.stdout = open("buildsout.xml","w")
#python literaller ilginc onlara bir bak
"""
input =	'''
	<root> burdaki formattan oturu tostring patlamıs olabilir
		<child1>deneme1</child1>
	</root>

'''
"""

root = etree.Element("root")
#print("rootrag -> " + root.tag)

root.append(etree.Element("child1"))
child2 = etree.SubElement(root,"child2")
child3 = etree.SubElement(root,"child3")
subchild1 = etree.SubElement(child2,"subchild1")
subsubchild = etree.SubElement(subchild1,"asdfafd")
print(etree.tostring(root,pretty_print=True).decode("utf-8"))

#elements are lists 

for child in root:
	#child.Element(child,interesting = "asdf") yemedi 
	#child.Element(root,"deneme1") -> bunu nasıl itere edecegiz
	#print(child.tag)

	pass

#elements carry attributes as dict 
