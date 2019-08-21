import xml.etree.ElementTree as ET
tree =  ET.parse('./uob_fp/2001Apr04eastbrn-1.ling.xml')

root = tree.getroot()
#print(root)

lord = tree.findall('BODY/LORD')
paragraph = tree.findall('BODY/LORD/P')
sentence = tree.findall('BODY/LORD/P/SENT')

for s in sentence:
    # sentence_attributes = s.attrib
    # align_value = s.attrib.get('ALIGN')
    # print(sentence_attributes)
    #print(align_value)
    print(s.tag, s.attrib)

# for p in paragraph:
#     print(p.tag, p.attrib)