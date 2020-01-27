import numpy as np
import csv

class tfidf_calc:
    def __init__(self):
        self.path = './uob_fp/68txt_corpus/'
        # self.corpus = [self.path+'1.19.txt', self.path+'1.63.txt', self.path+'1.68.txt', self.path+'NA.txt', 
        # self.path+'1.05.txt', self.path+'1.02.txt', self.path+'1.04.txt', self.path+'1.35.txt', self.path+'1.39.txt', 
        # self.path+'1.38.txt', self.path+'1.42.txt', self.path+'1.34.txt', self.path+'1.11.txt', self.path+'1.15.txt', 
        # self.path+'1.26.txt', self.path+'1.28.txt', self.path+'1.57.txt', self.path+'1.43.txt', self.path+'1.55.txt', 
        # self.path+'2.13.txt', self.path+'2.18.txt', self.path+'2.3.txt', self.path+'2.35.txt', self.path+'2.34.txt', 
        # self.path+'2.26.txt', self.path+'2.24.txt', self.path+'2.29.txt', self.path+'2.21.txt', self.path+'2.23.txt', 
        # self.path+'2.45.txt', self.path+'2.47.txt', self.path+'2.41.txt', self.path+'3.18.txt', self.path+'3.21.txt', 
        # self.path+'3.22.txt', self.path+'3.07.txt', self.path+'3.1.txt', self.path+'3.08.txt', self.path+'3.02.txt', 
        # self.path+'3.44.txt', self.path+'3.41.txt', self.path+'3.31.txt', self.path+'3.32.txt', 
        # self.path+'3.15.txt', self.path+'3.14.txt', self.path+'3.28.txt']
        self.corpus = []
        self.case_ids = []
        with open("./uob_fp/complete_sum.csv", "r") as infile:
            reader = csv.DictReader(infile)

            for row in reader:
                if row["case_id"] not in self.case_ids:
                    self.case_ids.append(row["case_id"])
        
        for v in range(len(self.case_ids)):
            if self.case_ids[v] == "N/A":
                self.corpus.append(self.path + "NA" + ".txt")
            else:
                self.corpus.append(self.path + self.case_ids[v] + ".txt")

        from sklearn.feature_extraction.text import TfidfVectorizer
        self.vectorizer = TfidfVectorizer(input='filename', stop_words='english')
        self.vectorizer.fit(self.corpus)
        self.dictionary = self.vectorizer.vocabulary_
        self.keys = self.dictionary.keys()

    def get_doc(self, document):
        # caseList = ['1.19', '1.63', '1.68', 'NA', 
        # '1.05', '1.02', '1.04', '1.35', '1.39', 
        # '1.38', '1.42', '1.34', '1.11', '1.15', 
        # '1.26', '1.28', '1.57', '1.43', '1.55', 
        # '2.13', '2.18', '2.3', '2.35', '2.34', 
        # '2.26', '2.24', '2.29', '2.21', '2.23', 
        # '2.45', '2.47', '2.41', '3.18', '3.21', 
        # '3.22', '3.07', '3.1', '3.08', '3.02', 
        # '3.44', '3.41', '3.31', '3.32', 
        # '3.15', '3.14', '3.28']
        # self.document = caseList.index(document)
        self.document = self.case_ids.index(document)
        if document == 'N/A':
            document = 'NA'

        # encode document
        self.vector = self.vectorizer.transform([self.corpus[self.document]])
        self.tfidf_array = self.vector.toarray()

        # get top 20 tfidf score for current document
        self.top20_score = []
        count = 0
        self.sorted_tfidf_array = np.sort(self.tfidf_array)
        self.sorted_tfidf_array = self.sorted_tfidf_array[:,::-1]
        for row in self.sorted_tfidf_array:
            for val in row:
                self.top20_score.append(val)
                count += 1
                if count == 20:
                    break
            if count == 20:
                break

    def get_sent_features(self, text):
        self.textarray = text.split(' ')
        self.highest_score = 0
        self.individual_tfidfList = []
        hits = 0
        
        for i in self.textarray:
            self.index = self.dictionary.get(i.lower())
            
            if self.index != None:
                self.individual_tfidfList.append(self.tfidf_array[0, self.index])
                self.highest_score = max(self.highest_score, self.tfidf_array[0, self.index])

        for s in self.individual_tfidfList:
            for v in self.top20_score:
                if s == v:
                    hits += 1
                    break
        
        import math
        self.in_top20 = math.log(hits+1, 16)

        from statistics import mean
        if len(self.individual_tfidfList) == 0:
            self.average_tfidf = 0
        else:
            self.average_tfidf = mean(self.individual_tfidfList)

        return self.highest_score, self.in_top20, self.average_tfidf
