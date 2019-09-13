import numpy as np
# def tfidf(word, document, corpus):
#     # TFIDF(w,d,D) = TF(w,d) * IDF(w,D)

#     # N = the number of times the word w occurs in document d
#     with open(document, 'r') as infile:
#         str = infile.read().replace

#     # M = the number of (all occurrences of all) words in document d

#     # TF(w,d) = N / M 

#     # P is the number of documents that contain the word d (at least once)

#     # Q is the number of documents in the set D

#     # IDF(w,D) = log (Q / P)


# tfidf_score = {}

# for word in corpus[0].split():
#     tfidf_score.update({word : tfidf(word,corpus[0], corpus)})
#     pass
class tfidf_calc:
    def __init__(self):
        self.path = './uob_fp/46txt_corpus/'
        self.corpus = [self.path+'1.19.txt', self.path+'1.63.txt', self.path+'1.68.txt', self.path+'NA.txt', 
        self.path+'1.05.txt', self.path+'1.02.txt', self.path+'1.04.txt', self.path+'1.35.txt', self.path+'1.39.txt', 
        self.path+'1.38.txt', self.path+'1.42.txt', self.path+'1.34.txt', self.path+'1.11.txt', self.path+'1.15.txt', 
        self.path+'1.26.txt', self.path+'1.28.txt', self.path+'1.57.txt', self.path+'1.43.txt', self.path+'1.55.txt', 
        self.path+'2.13.txt', self.path+'2.18.txt', self.path+'2.3.txt', self.path+'2.35.txt', self.path+'2.34.txt', 
        self.path+'2.26.txt', self.path+'2.24.txt', self.path+'2.29.txt', self.path+'2.21.txt', self.path+'2.23.txt', 
        self.path+'2.45.txt', self.path+'2.47.txt', self.path+'2.41.txt', self.path+'3.18.txt', self.path+'3.21.txt', 
        self.path+'3.22.txt', self.path+'3.07.txt', self.path+'3.1.txt', self.path+'3.08.txt', self.path+'3.02.txt', 
        self.path+'3.44.txt', self.path+'3.41.txt', self.path+'3.31.txt', self.path+'3.32.txt', 
        self.path+'3.15.txt', self.path+'3.14.txt', self.path+'3.28.txt']
        from sklearn.feature_extraction.text import TfidfVectorizer
        # self.vectorizer = TfidfVectorizer(input='filename')
        self.vectorizer = TfidfVectorizer(input='filename', stop_words='english')
        self.vectorizer.fit(self.corpus)
        self.dictionary = self.vectorizer.vocabulary_
        self.keys = self.dictionary.keys()

    def get_doc(self, document):
        caseList = ['1.19', '1.63', '1.68', 'NA', 
        '1.05', '1.02', '1.04', '1.35', '1.39', 
        '1.38', '1.42', '1.34', '1.11', '1.15', 
        '1.26', '1.28', '1.57', '1.43', '1.55', 
        '2.13', '2.18', '2.3', '2.35', '2.34', 
        '2.26', '2.24', '2.29', '2.21', '2.23', 
        '2.45', '2.47', '2.41', '3.18', '3.21', 
        '3.22', '3.07', '3.1', '3.08', '3.02', 
        '3.44', '3.41', '3.31', '3.32', 
        '3.15', '3.14', '3.28']
        if document == 'N/A':
            document = 'NA'
        self.document = caseList.index(document)

        # encode document
        self.vector = self.vectorizer.transform([self.corpus[self.document]])
        self.tfidf_array = self.vector.toarray()

        # #mean seems to be incorrect
        # return np.mean(self.tfidf_array)

    def get_sent_features(self, text):
        self.textarray = text.split(' ')
        self.highest_score = 0
        # self.individual_tfidfList = []
        # self.mean = 0
        
        for i in self.textarray:
            self.index = self.dictionary.get(i.lower())
            if self.index != None:
                # self.individual_tfidfList.append(self.tfidf_array[0, self.index])
                self.highest_score = max(self.highest_score, self.tfidf_array[0, self.index])
        return self.highest_score
        # from statistics import mean
        # if self.highest_score != 0:
        #     self.mean = mean(self.individual_tfidfList)
        # return self.mean, self.highest_score