import sklearn
import xml.etree.ElementTree as ET
import numpy

tree =  ET.parse('./uob_fp/2001Apr04eastbrn-1.ling.xml')
sentence = tree.findall('BODY/LORD/P/')
paragraph = tree.findall('BODY/LORD/')
lord = tree.findall('BODY/LORD')

# get labels/targets as y for ML train and test
y = []
for p in paragraph:
    if p.tag == 'quoteblock':
        for i in p:
            for s in i:
                sentence_attributes = s.attrib
                align_value = s.attrib.get('ALIGN')
                if align_value == 'NONE' or align_value == None:
                    y.append(0)
                else:
                    y.append(float(align_value))
    else:
        for s in p:
            sentence_attributes = s.attrib
            align_value = s.attrib.get('ALIGN')
            if align_value == 'NONE' or align_value == None:
                y.append(0)
            else:
                y.append(float(align_value))

# get features as x used in ML train and test:

# #get location feature
loc_feature = []

def count_par_in_lord(param_lord):
    count = 0
    for p in param_lord:
        count += 1
    return count

def count_sent_in_lord(param_lord):
    count = 0
    for p in param_lord:
        for s in p:
            count += 1
    return count

def count_sent_in_par(param_par):
    count = 0
    for s in param_par:
        count += 1
    return count 

def par_after_beglord(current_paragraph, start_lord_par):
    value = current_paragraph - start_lord_par
    return value

def par_before_endlord(current_paragraph, sum_lord_paragraphs):
    value = sum_lord_paragraphs - current_paragraph
    return value

def sent_after_beglord(current_sentence, start_lord_sent):
    value = current_sentence - start_lord_sent
    return value

def sent_before_endlord(current_sentence, sum_lord_sentences):
    value = sum_lord_sentences - current_sentence
    return value

def sent_after_begpar(current_sentence, start_par_sent):
    value = current_sentence - start_par_sent
    return value

def sent_before_endpar(current_sentence, sum_par_sentences):
    value = sum_par_sentences - current_sentence
    return value

def get_encoded_value(current_paragraph, start_lord_par, sum_lord_paragraphs, current_sentence, start_lord_sent, sum_lord_sentences, start_par_sent, sum_par_sentences):
    encoded_value = (par_after_beglord(current_paragraph, start_lord_par) + par_before_endlord(current_paragraph, sum_lord_paragraphs) +  
    sent_after_beglord(current_sentence, start_lord_sent) + sent_before_endlord(current_sentence, sum_lord_sentences) + 
    sent_after_begpar(current_sentence, start_par_sent) + sent_before_endpar(current_sentence, sum_par_sentences))
    return encoded_value

def get_location_feature(lord):
    current_paragraph = 0
    current_sentence = 0
    sum_lord_paragraphs = 0
    sum_lord_sentences = 0
    sum_par_sentences = 0

    for l in lord:
        new_lord = True
        sum_lord_paragraphs += count_par_in_lord(l)
        sum_lord_sentences += count_sent_in_lord(l)
        for p in l:
            if p.tag == 'quoteblock':
                for i in p:
                    new_paragraph = True
                    current_paragraph += 1
                    sum_par_sentences += count_sent_in_par(p)
                    if new_lord == True:
                        start_lord_par = current_paragraph
                    for s in i:
                        current_sentence += 1
                        if new_lord == True:
                            start_lord_sent = current_sentence
                        if new_paragraph == True:
                            start_par_sent = current_sentence
                        loc_feature.append(get_encoded_value(current_paragraph, start_lord_par, sum_lord_paragraphs, current_sentence, 
                            start_lord_sent, sum_lord_sentences, start_par_sent, sum_par_sentences))
                        new_paragraph = False
                        new_lord = False
            else:
                new_paragraph = True
                current_paragraph += 1
                sum_par_sentences += count_sent_in_par(p)
                if new_lord == True:
                    start_lord_par = current_paragraph
                for s in p: 
                    current_sentence += 1
                    if new_lord == True:
                        start_lord_sent = current_sentence
                    if new_paragraph == True:
                        start_par_sent = current_sentence
                    loc_feature.append(get_encoded_value(current_paragraph, start_lord_par, sum_lord_paragraphs, current_sentence, 
                        start_lord_sent, sum_lord_sentences, start_par_sent, sum_par_sentences))
                    new_paragraph = False
                    new_lord = False

get_location_feature(lord)
#print(loc_feature)

# #get thematic words feature using tfidf

# #get sentence length feature
sent_len_feature = []

def get_sent_len_feature(lord):
    for p in paragraph:
        if p.tag == 'quoteblock':
            for i in p:
                for s in i:
                    count = 0
                    for w in s:
                        if w.tag == 'W':
                            count += 1
                    sent_len_feature.append(count)
        else:
            for s in p:
                count = 0
                for w in s:
                    if w.tag == 'W':
                        count += 1
                sent_len_feature.append(count)

get_sent_len_feature(lord)
#print(sent_len_feature)

# #get quotation feature
quotation_feature = []

def find_inline_quotes(param_sent, quoteblock):
        in_quote = False
        count_word = 0
        word_in_quote = 0
        for w in param_sent:
            if w.tag == 'W':
                count_word += 1
            if w.tag == 'W' and w.attrib.get('C') == 'LQUOTE':
                in_quote = True
            if in_quote == True:
                word_in_quote += 1
            if w.tag == 'W' and w.attrib.get('C') == 'RQUOTE':
                in_quote = False
        if word_in_quote == 0:
            senttokens_in_quote = 0
        else:
            senttokens_in_quote = word_in_quote / count_word
        if quoteblock == True:
            value = 1 + senttokens_in_quote
        else:
            value = 0 + senttokens_in_quote
        quotation_feature.append(value)

def get_quotation_feature(lord):
    for p in paragraph:
        quoteblock = False
        if p.tag == 'quoteblock':
            for i in p:
                quoteblock = True
                for s in i:
                    find_inline_quotes(s, quoteblock)
        else:
            for s in p:
                find_inline_quotes(s, quoteblock)

get_quotation_feature(lord)
#print(quotation_feature)

x = []
n = len(y)
for v in range (0, n):
    value = numpy.array([loc_feature[v], sent_len_feature[v], quotation_feature[v]], dtype=float)
    # value = [loc_feature[v], sent_len_feature[v], quotation_feature[v]]
    x.append(value)

# ML train and test
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = .5)

# from sklearn.model_selection import KFold
# cv = KFold(n_splits = 10)
# for train_index, test_index in cv.split(x):
#     X_train, X_test, y_train, y_test = x[train_index], x[test_index], y[train_index], y[test_index]

from sklearn.naive_bayes import MultinomialNB
my_classifier = MultinomialNB()

# from sklearn.linear_model import LogisticRegressionCV
# my_classifier = LogisticRegressionCV(cv=10)

my_classifier.fit(X_train, y_train)

predictions = my_classifier.predict(X_test)

from sklearn.metrics import accuracy_score
print(accuracy_score(y_test, predictions))