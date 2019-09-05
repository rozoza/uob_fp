import xml.etree.ElementTree as ET
# tree =  ET.parse('./uob_fp/2001Apr04eastbrn-1.ling.xml')
tree =  ET.parse('./uob_fp/2002May23burket-1.ling.xml')

root = tree.getroot()
#print(root)

lord = tree.findall('BODY/LORD/')
paragraph = tree.findall('BODY/LORD/P/')
sentence = tree.findall('BODY/LORD/P/SENT/')
committee = tree.findall('HDR/committee/')

# for el in root.iter('lordname'):
#     text = el.text
#     if '\n' in text:
#         text = text.replace('\n', ' ')
#     print(text)

for el in paragraph:
        if el.tag == 'W':
                print(el.tag, el.attrib)

# for el in sentence:
#     if el.tag == 'TIMEX':
#         print('HELLOS')
#         # for el2 in el:
#         #     print(el2.tag, el2.attrib)

# for s in sentence:
#     # sentence_attributes = s.attrib
#     # align_value = s.attrib.get('ALIGN')
#     # print(sentence_attributes)
#     #print(align_value)
#     print(s.tag, s.attrib)

# for p in paragraph:
#     print(p.tag, p.attrib)