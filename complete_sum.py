import xml.etree.ElementTree as ET
import csv
import string
import difflib

def getRef(tree):
    ref = tree.findall('HDR/ref')
    #UKHL number is not found
    if len(ref) == 0:
        return 'N/A'

    for el in ref:
        case_ref = el.text
    return case_ref

def getCase_id(tree):
    case_ref = ''
    case_num = ''
    case_year = ''
    case_id = ''

    case_ref = getRef(tree)
    #UKHL number is not found
    if case_ref == 'N/A':
        return case_ref

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

def getRole(sent_element):
    if sent_element.attrib.get('TYPE') == None:
        return 'NONE'
    return sent_element.attrib.get('TYPE')

def getAlign(sent_element):
    if sent_element.attrib.get('ALIGN') == None:
        return 'NONE'
    return sent_element.attrib.get('ALIGN')

def getText(sent_element):
    wordlist = []
    text = ' '
    for sentences in sent_element:
        if sentences.tag == 'W':
            if sentences.text == None:
                wordlist.append('.')
            else:
                wordlist.append(sentences.text)
        if sentences.tag == 'VG':
            for vg in sentences:
                if vg.text == None:
                    # wordlist.append(' HELP -VG ')
                    print('HELP-VG')
                else:
                    # print('vg')
                    wordlist.append(vg.text)
        if sentences.tag == 'TIMEX':
            for timex in sentences:
                # print('timex')
                if timex.tag == 'PHR':
                    for phr in timex:
                        # print(phr.tag, phr.attrib)
                        wordlist.append(phr.text)
                # if timex.text == None:
                #     # wordlist.append(' HELP -TIMEX ')
                #     print('HELP-TIMEX')
                #     print(timex.tag, timex.attrib)
                else:
                    wordlist.append(timex.text)
        if sentences.tag == 'NUMEX':
            for numex in sentences:
                if numex.tag == 'PHR':
                    for phr in numex:
                        # print(phr.tag, phr.attrib)
                        wordlist.append(phr.text)
                # if numex.text == None:
                #     print('HELP-NUMEX')
                #     print(numex.tag, numex.attrib)
                else:             
                    wordlist.append(numex.text)
        if sentences.tag == 'PHR':
            for phr in sentences:
                if phr.text == None:
                    print('HELP-PHR')
                else:
                    wordlist.append(phr.text)
        if sentences.tag == 'NG':
            for ng in sentences:
                # print('ng')
                if ng.tag == 'W':
                    if ng.text == None:
                        # wordlist.append(' HELP -NG ')  
                        print('HELP-NG')
                    else:
                        wordlist.append(ng.text)  
                for nng in ng:
                    if nng.text == None:
                        # wordlist.append(' HELP -NNG ')  
                        print('HELP-NNG')
                    else:
                        # print('nng')
                        wordlist.append(nng.text)                                   
    text = text.join(wordlist)
    return text

def textReplace(text):
    while '#38;'in text:
        text = text.replace('#38;', '&')
    while '~~#228;' in text:
        text = text.replace('~~#228;', 'ä')
    while '~~#163;' in text:
        text = text.replace('~~#163;', '#')
    if 'Subjectto' in text:
        text = text.replace('Subjectto', 'Subject to')
    if 'inaccordancewith' in text:
        text = text.replace('inaccordancewith', 'in accordance with')
    return text

def adjustText(text):
    while '(' in text:
        text = text.replace('(', '-LRB-')
    while ')' in text:
        text = text.replace(')', '-RRB-')
    while '[' in text:
        text = text.replace('[', '-LSB-')
    while ']' in text:
        text = text.replace(']', '-RSB-')
    return text
         
def getAsmo(asmo, text, new_case):
    filename = 'asmo_' + asmo + '.csv'
    with open('./uob_fp/ASMO_46_corpus/' + filename) as infile:
        reader = csv.DictReader(infile)
        
        asmoret = []
        match = False
        findoutcome = False
        retset= []
        agrret = ''
        no_punct = ''
        text = adjustText(text)
        for char in text:
            if char not in string.punctuation:
                no_punct = no_punct + char
        no_punct = no_punct.replace(' ', '')

        for row in reader:
            if new_case == True:
                majority = row['mj']
                majority = majority.replace(', ', '+')
                return majority, 'no'

            no_punct2 = ''
            for char in row['body']:
                if char not in string.punctuation:
                    no_punct2 = no_punct2 + char
            if 'UnterhaltungsgerÃ¤te' in no_punct2:
                no_punct2 = no_punct2.replace('UnterhaltungsgerÃ¤te', 'Unterhaltungsgeräte')
            no_punct2 = no_punct2.replace(' ', '')
            
            if no_punct in no_punct2:
                if row['relation'] == 'fullagr' and match == False:
                    match = True
                    retset.append(row['to'])
                elif row['relation'] == 'fullagr' and match == True:
                    retset.append(row['to'])
                elif row['relation'] != 'fullagr' and match == True:
                    if len(retset) == 1:
                        agrret = ''.join(retset)
                        findoutcome = True
                        # return ret
                    else:
                        majority = row['mj']
                        majority = majority.split(', ')
                        cnt = 0
                        for v in range(len(majority)):
                            for s in range(len(retset)):
                                if retset[s] == majority[v]:
                                    cnt += 1
                        if cnt == len(majority):
                            agrret = '+'.join(majority)
                            findoutcome = True
                            # return ret
                        agrret = '+'.join(retset)
                        findoutcome = True
                        # return ret
                else:
                    agrret = 'NONE'
                    # return 'NONE'
                if row['relation'] == 'outcome' and findoutcome == True and match == True:
                    outret = 'yes'
                    asmoret = [agrret, outret]
                    return asmoret 
                    # return agrret, outret
                elif row['relation'] != 'outcome' and findoutcome == True and match == True:
                    outret = 'no'
                    asmoret = [agrret, outret]
                    return asmoret 
                    # return agrret, outret
                elif row['relation'] == 'outcome' and match == False:
                    outret = 'yes'
                    asmoret = [agrret, outret]
                    return asmoret 
                    # return agrret, outret
                elif row['relation'] != 'outcome' and match == False:
                    outret = 'no'
                    asmoret = [agrret, outret]
                    return asmoret 
                    # return agrret, outret
            else:
                seq = difflib.SequenceMatcher(None, no_punct, no_punct2).ratio()
                if seq > 0.8:
                    if row['relation'] == 'fullagr' and match == False:
                        match = True
                        retset.append(row['to'])
                    elif row['relation'] == 'fullagr' and match == True:
                        retset.append(row['to'])
                    elif row['relation'] != 'fullagr' and match == True:
                        if len(retset) == 1:
                            agrret = ''.join(retset)
                            findoutcome = True
                            # return ret
                        else:
                            majority = row['mj']
                            majority = majority.split(', ')
                            cnt = 0
                            for v in range(len(majority)):
                                for s in range(len(retset)):
                                    if retset[s] == majority[v]:
                                        cnt += 1
                            if cnt == len(majority):
                                agrret = '+'.join(majority)
                                findoutcome = True
                                # return ret
                            agrret = '+'.join(retset)
                            findoutcome = True
                            # return ret
                    else:
                        agrret = 'NONE'
                        # return 'NONE'
                    if row['relation'] == 'outcome' and findoutcome == True and match == True:
                        outret = 'yes' 
                        asmoret = [agrret, outret]
                        return asmoret 
                        # return agrret, outret
                    elif row['relation'] != 'outcome' and findoutcome == True and match == True:
                        outret = 'no'
                        asmoret = [agrret, outret]
                        return asmoret 
                        # return agrret, outret
                    elif row['relation'] == 'outcome' and match == False:
                        outret = 'yes'
                        asmoret = [agrret, outret]
                        return asmoret 
                        # return agrret, outret
                    elif row['relation'] != 'outcome' and match == False:
                        outret = 'no'
                        asmoret = [agrret, outret]
                        return asmoret 
                        # return agrret, outret
        return 'no match', 'no match'

def appendcsv(case_id, sentence_id, para_id, judge, text, role, align, agree, outcome, fieldnames):
    # with open('./uob_fp/test.csv', 'a', newline='') as out_file: #for quick testing
    with open('./uob_fp/complete_sum.csv', 'a', newline='') as out_file:
        csv_writer = csv.DictWriter(out_file, fieldnames=fieldnames)
        
        csv_writer.writerow({'case_id' : case_id, 'sentence_id' : sentence_id, 'para_id' : para_id, 'judge' : judge, 
                            'text' : text, 'role' : role, 'align' : align, 
                            'agree' : agree, 'outcome' : outcome})

def complete_sum():
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

    asmoCase = ['22', '23', '11', '9',
    '12', '14', '13', '5', '20',
    '3', '2', '21', '7', '4',
    '15', '18', '19', '6', '17',
    '42', '38', '26', '45', '43',
    '31', '35', '36', '32', '40',
    '29', '24', '34', '47', '69',
    '55', '63', '57', '62', '46',
    'N/A', '60', '49', '56', '66',
    '68', '52', '53']

    fieldnames = ['case_id', 'sentence_id', 'para_id', 'judge', 'text', 'role', 'align', 'agree', 'outcome']
    # with open('./uob_fp/test.csv', 'w', newline='') as new_file: #for quick testing
    with open('./uob_fp/complete_sum.csv', 'w', newline='') as new_file:

        csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames)
        csv_writer.writeheader()

    # count = 0 #for quick testing
    for v in range(len(corpusList)):
        #cannot find the corresponding ASMO case
        if corpusList[v] == "2003Jan30regina-1.ling.xml":
            continue

        tree =  ET.parse('./uob_fp/SUM_2005_corpus/' + corpusList[v])
        root = tree.getroot()
        hdr = tree.findall('HDR/')
        body = tree.findall('BODY/')
        asmo = asmoCase[v]

        new_case = True
        case_id = getCase_id(tree)
        sentence_id = '0'
        par_dp = False
        para_id = '0'
        role = '<new-case>'
        align = 'NONE'
        text = ''
        agree = ''
        outcome = ''
        
        judgeList = []
        judge_full = ''
        judgeCount = 0
        judge = 'NONE'
        getJudgelist(root, judgeList)

        #For storing asmo annotations
        asmoval = []

        #Handling broken words not inside a <SENT>
        text_in_par = ''
        textpar_bool = False

        for lords in body:
            if lords.tag == 'LORD':
                judge_full = judgeList[judgeCount]
                judge_full = judge_full.split()
                judge = judge_full[1].lower() #take the string after Lord
                if judge == 'chancellor':
                    for paragraphs in lords:
                        for sentences in paragraphs:
                            tmpname = getText(sentences).split()
                            for v in range(len(tmpname)):
                                if tmpname[v] == 'LORD':
                                    judge = tmpname[v+1].lower()
                                    break                                
                            break
                        break
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
                            if sentence_id != None:
                                role = getRole(sentences)
                                align = getAlign(sentences)
                                text = getText(sentences)
                                text = textReplace(text)
                                asmoval = getAsmo(asmo, text, new_case)
                                agree = asmoval[0]
                                outcome = asmoval[1]
                                appendcsv(case_id, sentence_id, para_id, judge, text, role, align, agree, outcome, fieldnames)
                                # print(case_id, sentence_id, para_id, judge, text, role, align)
                    #print('end of quoteblock')
    
                for sentences in paragraphs:
                    if sentences.tag == 'W':
                        sentence_id = 'N/A'
                        align = 'NONE'
                        agree = 'NONE'
                        outcome = 'no'
                        if sentences.attrib.get('P') == None:
                            role = '<prep-date>'  
                            text = sentences.text
                        elif '.5' in para_id and sentences.text == '...':
                            role = '<separator>'
                            text = sentences.text
                        elif '.5' in para_id:
                            role = '<sub-heading>'
                            text = sentences.text
                        else:
                            text_in_par = text_in_par + sentences.text + ' '
                            textpar_bool = True

                        # if sentences.text == None:
                        #     print('HELP-sentinpar')
                        # else:
                        #     text = sentences.text
                        if textpar_bool == False:
                            appendcsv(case_id, sentence_id, para_id, judge, text, role, align, agree, outcome, fieldnames)
                    
                    if new_case == True:
                        #para_id = '0'
                        text = getRef(tree)
                        asmoval = getAsmo(asmo, text, new_case)
                        agree = asmoval[0]
                        outcome = asmoval[1]
                        tmp = judge
                        judge = 'NONE'
                        appendcsv(case_id, sentence_id, para_id, judge, text, role, align, agree, outcome, fieldnames)
                        # print(case_id, '0', '0', 'NONE', text, '<new-case>', 'NONE')
                        new_case = False
                        judge = tmp
                    
                    sentence_id = getSent_id(sentences)
                    if sentence_id != None:
                        role = getRole(sentences)
                        align = getAlign(sentences)
                        if textpar_bool == True:
                            text = text_in_par + getText(sentences)
                            text = textReplace(text)
                            textpar_bool = False
                            text_in_par = ''
                        else:
                            text = getText(sentences)
                            text = textReplace(text)
                        asmoval = getAsmo(asmo, text, new_case)
                        agree = asmoval[0]
                        outcome = asmoval[1]
                        appendcsv(case_id, sentence_id, para_id, judge, text, role, align, agree, outcome, fieldnames)
                        # print(case_id, sentence_id, para_id, judge, text, role, align)
            judgeCount += 1
        #for quick testing
        # count += 1
        # if count == 1:
        #     break 

complete_sum()