import csv
from gensim.models import KeyedVectors

wvecs = KeyedVectors.load_word2vec_format("word2vec.6B.100d.txt", binary=False)

sentences = []

with open("complete_sum.csv", "r") as infile:
    reader = csv.DictReader(infile)
    count = 0
    for row in reader:
        if row['agree'] == 'no match' or row['role'] == '<prep-date>'\
        or row['role'] == '<sub-heading>' or row['role'] == '<separator>' or row['role'] == '<new-case>':
            continue
        # text = ""
        # tp_text = tuple(text.join(row["text"]))
        # text = text.join(row["text"])
        text = row["text"].split()
        sentences.append(text)
        count += 1 
        if count == 20:
            break

# tp_sentences = tuple(sentences)

from fse.models import SIF
from fse import IndexedList
model = SIF(wvecs)
sents = IndexedList(sentences)
model.train(sents)

# f = open("sent_embed.csv", "w")
import numpy as np

array = []
for i in range(len(model.sv)):
    for n in model.sv[i]:
        tmp = n
        print(round(tmp, 7))
        exit()
    array.append(model.sv[i])

np.savetxt(f, array, delimiter=",")
# [f.write(i) for i in model.sv]

f.close()
# print(model.sv.most_similar(5, indexable=sents.items))
# model.save("sent_embed")