import xml.etree.ElementTree as ET
import csv

def getCase_id(tree):
    ref = tree.findall('HDR/ref')
    case_ref = ''
    case_num = ''
    case_year = ''
    case_id = ''

    #UKHL number is not found
    if len(ref) == 0:
        case_id = 'N/A'
        return case_id

    for el in ref:
        case_ref = el.text
    length = len(case_ref)

    #get UKHL case number
    if case_ref[length-2] == ' ':
        case_num = '0' + case_ref[length-1]
    else: 
        case_num = case_ref[length-2:length]
        
    #get the last two digits of year by iterating through year block 
    # e.g. [2002]
    case_year = case_ref[(case_ref.index(']')-2):case_ref.index(']')]

    case_id = case_year + '.' + case_num

    return case_id

def getSent_id(sent_element):
    return sent_element.attrib.get('sid')
    
def getPara_id(para_element):
    return para_element.attrib.get('no')

def getJudgelist(root, judgeList):
    for el in root.iter('lordname'):
        text = el.text
        if '\n' in text:
            text = text.replace('\n', ' ')
        judgeList.append(text)

def completecsv():
    corpusList = ["2001Apr04eastbrn-1.ling.xml", "2001Dec13aib-1.ling.xml", "2001Dec13smith-1.ling.xml", "2001Feb08kuwait-1.ling.xml",
    "2001Feb08presto-1.ling.xml", "2001Jan18intern-1.ling.xml", "2001Jan31card-1.ling.xml", "2001Jul05m-1.ling.xml", "2001Jul12mcgra-1.ling.xml",
    "2001Jul12news-1.ling.xml", "2001Jul25dan-1.ling.xml", "2001Jun28norris-1.ling.xml", "2001Mar08mehann-1.ling.xml", "2001Mar22hallam-1.ling.xml",
    "2001May23daly-1.ling.xml", "2001May23liver-1.ling.xml", "2001Nov01moham-1.ling.xml", "2001Oct11uratem-1.ling.xml", "2001Oct25dela-1.ling.xml",
    "2002Apr18gersn-1.ling.xml", "2002Apr25cave-1.ling.xml", "2002Jul04graham-1.ling.xml", "2002Jul25robert-1.ling.xml", "2002Jul25sten-1.ling.xml",
    "2002Jun20pope-1.ling.xml", "2002Jun20wngton-1.ling.xml", "2002Jun27ash-1.ling.xml", "2002May16morgan-1.ling.xml", "2002May23burket-1.ling.xml",
    "2002Nov14byrne-1.ling.xml", "2002Nov25lich-1.ling.xml", "2002Oct31regina-1.ling.xml", "2003Apr03green-1.ling.xml", "2003Apr10bellin-1.ling.xml",
    "2003Apr10sage-1.ling.xml", "2003Feb20glaz-1.ling.xml", "2003Feb27diets-1.ling.xml", "2003Feb27inrep-1.ling.xml", "2003Jan30kanar-1.ling.xml",
    "2003Jan30regina-1.ling.xml", "2003Jul31moyna-1.ling.xml", "2003Jul31mulkrn-1.ling.xml", "2003Jun12kuwa-1.ling.xml", "2003Jun12lyon-1.ling.xml",
    "2003Mar20sepet-1.ling.xml", "2003Mar20sivak-1.ling.xml", "2003May22john-1.ling.xml"]

    #Prototype
    #Will be iterating through corpusList in later stage
    tree =  ET.parse('./uob_fp/' + corpusList[0])
    root = tree.getroot()
    hdr = tree.findall('HDR/')
    body = tree.findall('BODY/')

    #first_case = True
    new_case = True
    case_id = getCase_id(tree)
    sentence_id = '0'
    par_dp = False
    para_id = '0'
    
    judgeList = []
    judgeCount = 0
    judge = ''
    getJudgelist(root, judgeList)

    for lords in body:
        if lords.tag == 'LORD':
            judge = judgeList[judgeCount]
        for paragraphs in lords:
            if getPara_id(paragraphs) == None and par_dp == False:
                para_id = para_id + '.5'
                par_dp = True
            elif getPara_id(paragraphs) == None and par_dp == True: 
                pass
            else: 
                para_id = getPara_id(paragraphs)
                par_dp = False

            if paragraphs.tag == 'quoteblock':
                #print('start of quoteblock')
                for subpar in paragraphs:
                    for sentences in subpar:
                        #print(sentences.tag, sentences.attrib)
                        sentence_id = getSent_id(sentences)
                        print(case_id, sentence_id, para_id, judge, 'text-for-later')
                #print('end of quoteblock')

            for sentences in paragraphs:
                if new_case == True:
                    print(case_id, '0', '0', 'none')
                    new_case = False
                if sentences.attrib.get('sid') != None:
                    sentence_id = getSent_id
                    print(case_id, getSent_id(sentences), para_id, judge, 'text-for-later')
        judgeCount += 1

completecsv()

    # pass new case and all the columns, if FIRST case then write, otherwise append
    # with open('./uob_fp/test_completecsv.csv', 'w', newline='') as new_file:
    #     fieldnames = ['case_id', 'sentence_id', 'para_id', 'judge', 'text', 'role', 'align', 'agree', 'outcome']

    #     csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames)

    #     csv_writer.writeheader()
    #     csv_writer.writerow({'case_id' : 2.23, 'sentence_id' : 1, 'para_id' : 0, 'judge' : 'none', 
    #                         'text' : '[2002] UKHL 23', 'role' : '<new-case>', 'align' : 'none', 
    #                         'agree' : 'slynn+steyn', 'outcome' : 'allow'})
