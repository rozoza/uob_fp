import sklearn
import csv
import numpy as np

def classifier_performance(X_train, y_train, X_test, y_test, classifier, clf_name):
    classifier.fit(X_train, y_train)
    predictions = classifier.predict(X_test)
    
    y_true = y_test
    y_pred = predictions
    from sklearn.metrics import accuracy_score
    accuracy = accuracy_score(y_true, y_pred)
    from sklearn.metrics import recall_score
    recall = recall_score(y_true, y_pred, average='weighted')
    from sklearn.metrics import precision_score
    precision = precision_score(y_true, y_pred, average='weighted')
    from sklearn.metrics import f1_score
    f_score = f1_score(y_true, y_pred, average='weighted')

    print('-----------', clf_name, '-----------')
    print('accuracy_score:', accuracy)
    print('recall_score:', recall)
    print('precision_score:', precision)
    print('f1_score:', f_score)

y = np.array([])
agree_X = np.array([])
outcome_X = np.array([])

with open('uob_fp/complete_sum.csv', 'r') as infile:
    reader = csv.DictReader(infile)

    for row in reader:
        if row['agree'] == 'no match':
            continue
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
asmo_X = np.vstack((agree_X, outcome_X)).T
# print(asmo_X.ndim, asmo_X.shape)
# print(len(y), len(asmo_X))
# agree_X = agree_X.reshape(-1, 1)

# print(y, asmo_X)
# for v in range(len(y)):
#     print(y[v])

# ML train and test
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(asmo_X, y, test_size = .5)

from sklearn.naive_bayes import BernoulliNB
BernNB_clf = BernoulliNB()
classifier_performance(X_train, y_train, X_test, y_test, BernNB_clf, 'BernNB_clf')

from sklearn.linear_model import LogisticRegressionCV
LR_clf = LogisticRegressionCV(cv=10)
classifier_performance(X_train, y_train, X_test, y_test, LR_clf, 'LR_clf')

from sklearn.svm import SVC
SVC_clf = SVC(gamma='scale')
classifier_performance(X_train, y_train, X_test, y_test, SVC_clf, 'SVC_clf')

from sklearn.tree import DecisionTreeClassifier
DTC_clf = DecisionTreeClassifier()
classifier_performance(X_train, y_train, X_test, y_test, DTC_clf, 'DTC_clf')