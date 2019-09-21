import xml.etree.ElementTree as ET

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

caseList = ['1.19', '1.63', '1.68', 'NA', 
'1.05', '1.02', '1.04', '1.35', '1.39', 
'1.38', '1.42', '1.34', '1.11', '1.15', 
'1.26', '1.28', '1.57', '1.43', '1.55', 
'2.13', '2.18', '2.3', '2.35', '2.34', 
'2.26', '2.24', '2.29', '2.21', '2.23', 
'2.45', '2.47', '2.41', '3.18', '3.21', 
'3.22', '3.07', '3.1', '3.08', '3.02', 
'N/A', '3.44', '3.41', '3.31', '3.32', 
'3.15', '3.14', '3.28']

def count():
    typedict = {}
    for v in range(len(corpusList)):
        if corpusList[v] == "2003Jan30regina-1.ling.xml":
            continue

        count = 0
        tree = ET.parse('./uob_fp/SUM_2005_corpus/' + corpusList[v])
        root = tree.getroot()
        verbslist = []
        # print([elem.tag for elem in root.iter('VG')])

        for sent in root.iter('SENT'):
            if sent.attrib.get('TYPE') == None:
                count += 1
        typedict.update({caseList[v]: count})
    return typedict

def verb_attributes_values():
    for v in range(len(corpusList)):
        if corpusList[v] == "2003Jan30regina-1.ling.xml":
            continue
        tree = ET.parse('./uob_fp/SUM_2005_corpus/' + corpusList[v])
        root = tree.getroot()
        modalList = []
        aspList = []
        voiceList = []
        negList = []
        tenseList = []
        for vg in root.iter('VG'):
            if vg.attrib.get('main') == 'yes':
                aspect = vg.attrib.get('ASP')
                modal = vg.attrib.get('MODAL')
                voice = vg.attrib.get('VOICE')
                negation = vg.attrib.get('NEG')
                tense = vg.attrib.get('TENSE')
            if aspect not in aspList:
                aspList.append(aspect)
            if modal not in modalList:
                modalList.append(modal)
            if voice not in voiceList:
                voiceList.append(voice)
            if negation not in negList:
                negList.append(negation)
            if tense not in tenseList:
                tenseList.append(tense)
    print('asp', aspList)
    print('modal', modalList)
    print('voice', voiceList)
    print('negation', negList)
    print('tense', tenseList)

def get_verb_features(case_id, sentence_id):
    if case_id == 'N/A':
        case_id = 'NA'
    index = caseList.index(case_id)
    tree = ET.parse('./uob_fp/SUM_2005_corpus/' + corpusList[index])
    root = tree.getroot()
    aspect = None
    modal = None
    voice = None
    negation = None
    tense = None
    for sent in root.iter('SENT'):
        if sent.attrib.get('sid') == sentence_id:
            for elem in sent:
                if elem.tag == 'VG':
                    aspect = elem.attrib.get('ASP')
                    modal = elem.attrib.get('MODAL')
                    voice = elem.attrib.get('VOICE')
                    negation = elem.attrib.get('NEG')
                    tense = elem.attrib.get('TENSE')
                    return aspect, modal, voice, negation, tense
    return aspect, modal, voice, negation, tense    

def get_noun_features(case_id, sentence_id):
    if case_id == 'N/A':
        case_id = 'NA'
    index = caseList.index(case_id)    
    tree = ET.parse('./uob_fp/SUM_2005_corpus/' + corpusList[index])
    root = tree.getroot()
    caseent = 0
    legalent = 0
    enamex = 0

    for sent in root.iter('SENT'):
        if sent.attrib.get('sid') == sentence_id:
            for elem in sent.iter('NG'):
                if elem.attrib.get('type') == 'caseent':
                    caseent = 1
                else: 
                    caseent = 0
                if elem.attrib.get('type') == 'legal-ent':
                    legalent = 1
                else:
                    legalent = 0
                if elem.attrib.get('type') == 'enamex-loc' or elem.attrib.get('type') == 'enamex-pers' or \
                elem.attrib.get('type') == 'enamex-org':
                    enamex = 1
                else:
                    enamex = 0
            return caseent, legalent, enamex        