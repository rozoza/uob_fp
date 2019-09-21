import sklearn
import csv
import numpy as np
import math

def get_end_par_in_lord(judge, case, current_paragraph):
    filename = 'comsum_' + case + '.csv'
    if case == 'N/A':
        filename = 'comsum_' + 'NA' + '.csv'
    with open('./uob_fp/comsum_corpus/' + filename, 'r') as infile:
        reader = csv.DictReader(infile)

        ret = '' 
        for row in reader:
            if row['judge'] == judge:
                if row['para_id'] == '0.5':
                    rowpar = '0'
                elif '.5' in row['para_id']:
                    rowpar = row['para_id'].replace('.5', '')
                else:
                    rowpar = row['para_id']
                if int(rowpar) >= int(current_paragraph):
                    ret = rowpar
        return ret

def get_end_sent_in_lord(judge, case, current_sentence):
    filename = 'comsum_' + case + '.csv'
    if case == 'N/A':
        filename = 'comsum_' + 'NA' + '.csv'
    with open('./uob_fp/comsum_corpus/' + filename, 'r') as infile:
        reader = csv.DictReader(infile)

        ret = ''
        for row in reader:
            if row['agree'] == 'no match' or row['role'] == '<prep-date>'\
            or row['role'] == '<sub-heading>' or row['role'] == '<separator>' or row['role'] == '<new-case>':
                continue
            if row['judge'] == judge:
                if int(row['sentence_id']) >= int(current_sentence):
                    ret = row['sentence_id']
        return ret

def get_end_sent_in_par(par, case, current_sentence):
    filename = 'comsum_' + case + '.csv'
    if case == 'N/A':
        filename = 'comsum_' + 'NA' + '.csv'
    with open('./uob_fp/comsum_corpus/' + filename, 'r') as infile:
        reader = csv.DictReader(infile)
        
        ret = ''
        for row in reader:
            if row['agree'] == 'no match' or row['role'] == '<prep-date>'\
            or row['role'] == '<sub-heading>' or row['role'] == '<separator>' or row['role'] == '<new-case>':
                continue
            if row['para_id'] == '0.5':
                rowpar = '0'
            elif '.5' in row['para_id']:
                rowpar = row['para_id'].replace('.5', '')
            else:
                rowpar = row['para_id']
            if rowpar == par:
                if int(row['sentence_id']) >= int(current_sentence):
                    ret = row['sentence_id']
        return ret

def storeFeatures(case_flag, sent_flag, y, agree_X, outcome_X, loc1_X, loc2_X, loc3_X, loc4_X, loc5_X, loc6_X,
sentlen_X, qb_X, inq_X, rhet_X, tfidf_X, asp_X, modal_X, voice_X, negcue_X, tense_X, caseent_X, legalent_X, enamex_X, rhet_y):
    with open('./uob_fp/MLdata.csv', 'w', newline='') as outfile:
        fieldnames = ['case_id', 'sent_id', 'align', 'agree', 'outcome', 'loc1', 'loc2', 'loc3', 
        'loc4', 'loc5', 'loc6', 'sentlen', 'quoteblock', 'inline_q', 'rhet', 'tfidf', 'aspect', 'modal',
        'voice', 'negation', 'tense', 'case entities', 'legal entities', 'enamex', 'rhet_target']        

        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for v in range(len(y)):
            writer.writerow({'case_id': case_flag[v], 'sent_id': sent_flag[v], 'align': y[v], 'agree': agree_X[v],
            'outcome': outcome_X[v], 'loc1': loc1_X[v], 'loc2': loc2_X[v], 'loc3': loc3_X[v], 'loc4': loc4_X[v], 
            'loc5': loc5_X[v], 'loc6': loc6_X[v], 'sentlen': sentlen_X[v], 'quoteblock': qb_X[v], 'inline_q': inq_X[v], 
            'rhet': rhet_X[v], 'tfidf': tfidf_X[v], 'aspect': asp_X[v], 'modal': modal_X[v], 'voice': voice_X[v],
            'negation': negcue_X[v], 'tense': tense_X[v], 'case entities': caseent_X[v],
            'legal entities': legalent_X[v], 'enamex': enamex_X[v], 'rhet_target': rhet_y[v]})

#Target/label
#relevance target
y = np.array([])
#rhetorical role target
rhet_y = np.array([])

#List of features
agree_X = np.array([])
outcome_X = np.array([])
loc1_X = np.array([]); loc2_X = np.array([]); loc3_X = np.array([])
loc4_X = np.array([]); loc5_X = np.array([]); loc6_X = np.array([])
sentlen_X = np.array([])
qb_X = np.array([])
inq_X = np.array([])
rhet_X = np.array([])

#for cue phrase feature-set
asp_X = np.array([])
modal_X = np.array([])
voice_X = np.array([])
negcue_X = np.array([])
tense_X = np.array([])
cue_X = np.array([])

#for entities feature-set
caseent_X = np.array([])
legalent_X = np.array([])
enamex_X = np.array([])

import tfidf_feature
tfidf = tfidf_feature.tfidf_calc()
tfidf_X = np.array([])

#for storing Xs values
case_flag = []
sent_flag = []

with open('uob_fp/complete_sum.csv', 'r') as infile:
    reader = csv.DictReader(infile)

    #for location features
    judge = ''
    case = ''
    par = ''
    loc1 = 0; loc2 = 0; loc3 = 0; loc4 = 0; loc5 = 0; loc6 = 0

    #for quotations
    qb_bool = False
    quoteblock = 0
    inquotes = False
    word_inq = 0
    
    # cnt = 0 #for quick test
    for row in reader:
        # if row['case_id'] != '1.63': #quick test on first case
        #     continue
        # if row['case_id'] == 'N/A': #quick test on first 3 cases
        #     break

        if row['agree'] == 'no match' or row['role'] == '<prep-date>'\
        or row['role'] == '<sub-heading>' or row['role'] == '<separator>' or row['role'] == '<new-case>':
            continue

        case_flag.append(row['case_id'])
        sent_flag.append(row['sentence_id'])

        import nvGroups
        asp, modal, voice, negation, tense = nvGroups.get_verb_features(row['case_id'], row['sentence_id'])
        if asp == 'SIMPLE':
            asp_X = np.append(asp_X, [1])
        elif asp == 'PERF':
            asp_X = np.append(asp_X, [2/3])
        elif asp == 'PROG':
            asp_X = np.append(asp_X, [1/3])
        else:
            asp_X = np.append(asp_X, [0])
        if modal == 'NO':
            modal_X = np.append(modal_X, [1])
        elif modal == 'YES':
            modal_X = np.append(modal_X, [1/2])
        else:
            modal_X = np.append(modal_X, [0])
        if voice == 'ACT':
            voice_X = np.append(voice_X, [1])
        elif voice == 'PASS':
            voice_X = np.append(voice_X, [1/2])
        else:
            voice_X = np.append(voice_X, [0])
        if negation == 'yes':
            negcue_X = np.append(negcue_X, [1])
        else:
            negcue_X = np.append(negcue_X, [0])
        if tense == 'PRES':
            tense_X = np.append(tense_X, [1])
        elif tense == 'PRESorBASE':
            tense_X = np.append(tense_X, [3/4])
        elif tense == 'PAST':
            tense_X = np.append(tense_X, [2/4])
        elif tense == 'INF':
            tense_X = np.append(tense_X, [1/4])
        else:
            tense_X = np.append(tense_X, [0])

        caseent, legalent, enamex = nvGroups.get_noun_features(row['case_id'], row['sentence_id'])
        caseent_X = np.append(caseent_X, [caseent])
        legalent_X = np.append(legalent_X, [legalent])
        enamex_X = np.append(enamex_X, [enamex])

        tfidf.get_doc(row['case_id'])
        sent_max_tfidf = tfidf.get_sent_features(row['text'])
        tfidf_X = np.append(tfidf_X, [sent_max_tfidf])

        tmptxt = row['text'].split()
        if '.5' in row['para_id']:
            if tmptxt[0] == '"':
                quoteblock = 1
                qb_bool = True
            if qb_bool == True:
                quoteblock = 1
            if tmptxt[-1] == '"' and qb_bool == True or '" .' in row['text'] and qb_bool == True:
                quoteblock = 1
                qb_bool = False
        else:
            quoteblock = 0
            qb_bool = False
        qb_X = np.append(qb_X, [quoteblock])        
        
        if tmptxt[0] == '"':
            tmptxt[0] = ''
            if tmptxt[-1] == '"':
                tmptxt[-1] == ''
            if '" .' in row['text']:
                tmptxt[:-3]
        word_inq = 0
        for v in range(len(tmptxt)):
            if tmptxt[v] == '"' and inquotes == False:
                inquotes = True
            elif tmptxt[v] == '"' and inquotes == True:
                inquotes = False
            if inquotes == True and tmptxt[v] != '"':
                word_inq += 1
        if word_inq == 0:
            inq = 0
        else:
            inq = word_inq / len(row['text'])
        inq_X = np.append(inq_X, [inq])            

        sent_len = len(row['text'].split())
        sent_len = math.log(sent_len,625)
        sentlen_X = np.append(sentlen_X, [sent_len])
          
        current_case = row['case_id']
        current_judge = row['judge']
        current_paragraph = row['para_id']
        if current_paragraph == '0.5':
            current_paragraph = '0'
        elif '.5' in current_paragraph:
            current_paragraph = current_paragraph.replace('.5', '')
        current_sentence = row['sentence_id']

        if case != current_case:
            case = current_case
            start_lord_par = 0 #for every new lord, get current paragraph
            start_lord_sent = 0 #for every new lord, get current sentence
            start_par_sent = 0 #for every new paragraph, get current sentence
            end_lord_paragraphs = 0 #total paragraphs in a lord
            end_lord_sentences = 0 #total sentences in a lord
            end_par_sentences = 0 #total sentences in a paragraph

        if judge != current_judge:
            judge = current_judge
            start_lord_par = int(current_paragraph)
            start_lord_sent = int(current_sentence)
            end_lord_paragraphs = int(get_end_par_in_lord(judge, case, current_paragraph))
            end_lord_sentences = int(get_end_sent_in_lord(judge, case, current_sentence))
        
        if par != current_paragraph:
            par = current_paragraph
            start_par_sent = int(current_sentence)
            end_par_sentences = int(get_end_sent_in_par(par, case, current_sentence))
        
        loc1 = math.log(1+ int(current_paragraph) - start_lord_par, 81)
        loc2 = math.log(1+ end_lord_paragraphs - int(current_paragraph), 81)
        loc3 = math.log(1+ int(current_sentence) - start_lord_sent, 625)
        loc4 = math.log(1+ end_lord_sentences - int(current_sentence), 625)
        loc5 = math.log(1+ int(current_sentence) - start_par_sent, 16)
        loc6 = math.log(1+ end_par_sentences - int(current_sentence), 16)       
        
        #norm attempt-1
        # loc1 = (int(current_paragraph) - start_lord_par)/(end_lord_paragraphs - start_lord_par + 1)
        # loc2 = (end_lord_paragraphs - int(current_paragraph))/(end_lord_paragraphs - start_lord_par + 1)
        # loc3 = (int(current_sentence) - start_lord_sent)/(end_lord_sentences - start_lord_sent + 1)
        # loc4 = (end_lord_sentences - int(current_sentence))/(end_lord_sentences - start_lord_sent + 1)
        # loc5 = (int(current_sentence) - start_par_sent)/(end_par_sentences - start_par_sent + 1)
        # loc6 = (end_par_sentences - int(current_sentence))/(end_par_sentences - start_par_sent + 1)

        #un-normalised
        # loc1 = int(current_paragraph) - start_lord_par
        # loc2 = end_lord_paragraphs - int(current_paragraph)
        # loc3 = int(current_sentence) - start_lord_sent
        # loc4 = end_lord_sentences - int(current_sentence)
        # loc5 = int(current_sentence) - start_par_sent
        # loc6 = end_par_sentences - int(current_sentence)
        
        loc1_X = np.append(loc1_X, [loc1]); loc2_X = np.append(loc2_X, [loc2]); loc3_X = np.append(loc3_X, [loc3])
        loc4_X = np.append(loc4_X, [loc4]); loc5_X = np.append(loc5_X, [loc5]); loc6_X = np.append(loc6_X, [loc6])
        
        if row['align'] == 'NONE':
            tmp = np.array([0])
            y = np.hstack([y, tmp])
        else:
            tmp = np.array([1])
            y = np.hstack([y, tmp])
        
        if row['agree'] == 'NONE':
            tmp = np.array([0])
            agree_X = np.hstack([agree_X, tmp])
        else:
            tmp = np.array([1])
            agree_X = np.hstack([agree_X, tmp])    
        if row['outcome'] == 'no':
            tmp = np.array([0])
            outcome_X = np.hstack([outcome_X, tmp])
        else:
            tmp = np.array([1])
            outcome_X = np.hstack([outcome_X, tmp])

        if row['role'] == 'FACT':
            rhet_y = np.append(rhet_y, [2])        
            rhet_X = np.append(rhet_X, [2/6])        
        if row['role'] == 'PROCEEDINGS':
            rhet_y = np.append(rhet_y, [3])        
            rhet_X = np.append(rhet_X, [3/6])        
        if row['role'] == 'BACKGROUND':
            rhet_y = np.append(rhet_y, [4])        
            rhet_X = np.append(rhet_X, [4/6])        
        if row['role'] == 'FRAMING':
            rhet_y = np.append(rhet_y, [5])        
            rhet_X = np.append(rhet_X, [5/6])        
        if row['role'] == 'DISPOSAL':
            rhet_y = np.append(rhet_y, [6])        
            rhet_X = np.append(rhet_X, [1])        
        if row['role'] == 'TEXTUAL':
            rhet_y = np.append(rhet_y, [1])        
            rhet_X = np.append(rhet_X, [1/6])        
        if row['role'] == 'NONE':
            rhet_y = np.append(rhet_y, [0])   
            rhet_X = np.append(rhet_X, [0])   
        
        # #for quick test
        # cnt +=1
        # if cnt == 3:
        #     break

storeFeatures(case_flag, sent_flag, y, agree_X, outcome_X, loc1_X, loc2_X, loc3_X, loc4_X, loc5_X, loc6_X,
sentlen_X, qb_X, inq_X, rhet_X, tfidf_X, asp_X, modal_X, voice_X, negcue_X, tense_X, caseent_X, legalent_X, enamex_X, rhet_y)