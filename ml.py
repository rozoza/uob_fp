import numpy as np
import csv

class ml:
    def __init__(self):
        #Target/label
        #relevance target
        self.y = np.array([])
        #rhetorical target
        self.rhet_y = np.array([])

        #List of features
        self.agree_X = np.array([])
        self.outcome_X = np.array([])
        self.loc1_X = np.array([]); self.loc2_X = np.array([]); self.loc3_X = np.array([])
        self.loc4_X = np.array([]); self.loc5_X = np.array([]); self.loc6_X = np.array([])
        self.sentlen_X = np.array([])
        self.qb_X = np.array([])
        self.inq_X = np.array([])
        self.cue_X = np.array([])
        self.tfidf_X = np.array([])
        self.rhet_X = np.array([])
        
        # no more used
        # neg_X = np.array([])
        
        ##for cue phrase feature-set
        self.asp_X = np.array([])
        self.modal_X = np.array([])
        self.voice_X = np.array([])
        self.negcue_X = np.array([])
        self.tense_X = np.array([])
        
        ##for entities feature-set
        self.enamex_X = np.array([])
        self.legalent_X = np.array([])
        # all values are 0, thus non-beneficial in ml 
        # self.caseent_X = np.array([])

    def classifier_performance(self, X_train, y_train, X_test, y_test, classifier, clf_name):
        classifier.fit(X_train, y_train)
        predictions = classifier.predict(X_test)

        # # Visualize Decision Tree
        # from sklearn.tree import export_graphviz

        # # Creates dot file named tree.dot
        # export_graphviz(
        #         classifier,
        #         out_file =  "output.dot",
        #         feature_names = ['agree_X', 'outcome_X', 'loc1_X', 'loc2_X', 'loc3_X', 'loc4_X', 'loc5_X', 'loc6_X', 'inq_X', 'qb_X', 'sentlen_X', 'rhet_X'],
        #         class_names = ['align_0', 'align_1'],
        #         filled = True,
        #         rounded = True)
        
        # from subprocess import check_call
        # check_call(['dot','-Tpng','output.dot','-o','output.png'])
        # import pydot

        # (graph,) = pydot.graph_from_dot_file('output.dot')
        # graph.write_png('output.png')
        
        y_true = y_test
        y_pred = predictions
        from sklearn.metrics import recall_score
        recall = recall_score(y_true, y_pred, average='weighted', labels=np.unique(y_pred))
        # recall = recall_score(y_true, y_pred, average='binary', labels=np.unique(y_pred))
        from sklearn.metrics import precision_score
        precision = precision_score(y_true, y_pred, average='weighted', labels=np.unique(y_pred))
        # precision = precision_score(y_true, y_pred, average='binary', labels=np.unique(y_pred))
        from sklearn.metrics import f1_score
        f_score = f1_score(y_true, y_pred, average='weighted', labels=np.unique(y_pred))
        # f_score = f1_score(y_true, y_pred, average='binary', labels=np.unique(y_pred))

        print('-----------', clf_name, '-----------')
        print('precision_score:', precision)
        print('recall_score:', recall)
        print('f1_score:', f_score)

    def supervised_ml(self, X_train, y_train, X_test, y_test, setname):
        print('+++++++++++', setname, '+++++++++++')
        from sklearn.naive_bayes import ComplementNB
        compNB_clf = ComplementNB()
        self.classifier_performance(X_train, y_train, X_test, y_test, compNB_clf, 'compNB_clf')

        from sklearn.linear_model import LogisticRegression
        LR_clf = LogisticRegression(solver='lbfgs', multi_class='auto', max_iter=1000)
        # LR_clf = LogisticRegression(class_weight='balanced', solver='liblinear', multi_class='auto')
        self.classifier_performance(X_train, y_train, X_test, y_test, LR_clf, 'LR_clf')

        from sklearn.svm import SVC
        SVC_clf = SVC(gamma='scale', decision_function_shape='ovo')
        # SVC_clf = SVC(gamma='scale', class_weight='balanced', decision_function_shape='ovo')
        self.classifier_performance(X_train, y_train, X_test, y_test, SVC_clf, 'SVC_clf')

        from sklearn.tree import DecisionTreeClassifier
        # DTC_clf = DecisionTreeClassifier(max_features=None, class_weight='balanced', max_depth=None, min_samples_leaf=1)
        DTC_clf = DecisionTreeClassifier(max_features=None, max_depth=None, min_samples_leaf=1)
        self.classifier_performance(X_train, y_train, X_test, y_test, DTC_clf, 'DTC_clf')

        from sklearn.neighbors import KNeighborsClassifier
        KN_clf = KNeighborsClassifier(algorithm='auto')
        self.classifier_performance(X_train, y_train, X_test, y_test, KN_clf, 'KN_clf')
        print('+++++++++++', 'DONE', '+++++++++++')

    def prep_data(self):
        with open('./uob_fp/MLdata.csv', 'r') as infile:
            reader = csv.DictReader(infile)

            for row in reader:
                self.y = np.append(self.y, [float(row['align'])])
                self.agree_X = np.append(self.agree_X, [float(row['agree'])])
                self.outcome_X = np.append(self.outcome_X, [float(row['outcome'])])
                self.loc1_X = np.append(self.loc1_X, [float(row['loc1'])])
                self.loc2_X = np.append(self.loc2_X, [float(row['loc2'])])
                self.loc3_X = np.append(self.loc3_X, [float(row['loc3'])])
                self.loc4_X = np.append(self.loc4_X, [float(row['loc4'])])
                self.loc5_X = np.append(self.loc5_X, [float(row['loc5'])])
                self.loc6_X = np.append(self.loc6_X, [float(row['loc6'])])
                self.sentlen_X = np.append(self.sentlen_X, [float(row['sentlen'])])
                self.qb_X = np.append(self.qb_X, [float(row['quoteblock'])])
                self.inq_X = np.append(self.inq_X, [float(row['inline_q'])])
                self.rhet_X = np.append(self.rhet_X, [float(row['rhet'])])
                self.tfidf_X = np.append(self.tfidf_X, [float(row['tfidf'])])
                self.asp_X = np.append(self.asp_X, [float(row['aspect'])])
                self.modal_X = np.append(self.modal_X, [float(row['modal'])])
                self.voice_X = np.append(self.voice_X, [float(row['voice'])])
                self.negcue_X = np.append(self.negcue_X, [float(row['negation'])])
                self.tense_X = np.append(self.tense_X, [float(row['tense'])])
                self.legalent_X = np.append(self.legalent_X, [float(row['legal entities'])])
                self.enamex_X = np.append(self.enamex_X, [float(row['enamex'])])
                self.rhet_y = np.append(self.rhet_y, [float(row['rhet_target'])])

    def exec(self):
        location = self.loc1_X, self.loc2_X, self.loc3_X, self.loc4_X, self.loc5_X, self.loc6_X
        quotation = self.inq_X, self.qb_X
        entities = self.legalent_X, self.enamex_X
        asmo = self.agree_X, self.outcome_X
        cue_phrase = self.asp_X, self.modal_X, self.voice_X, self.negcue_X, self.tense_X
        X = np.vstack((*location, *asmo, *entities)).T
        # self.rhet_X = np.vstack((self.rhet_X, *location, *quotation, *entities)).T
        # self.rhet_X = self.rhet_X.reshape(-1, 1)
        self.asmo_X = np.vstack((*asmo, *location)).T
        self.loc_X = np.vstack((*location,)).T
        self.quo_X = np.vstack((*quotation, *location, *asmo, *entities)).T
        self.sentlen_X = np.vstack((self.sentlen_X, *location, *asmo, *entities)).T
        # self.sentlen_X = self.sentlen_X.reshape(-1, 1)
        # neg_X = neg_X.reshape(-1, 1)
        self.tfidf_X = np.vstack((self.tfidf_X, *location, *asmo, *entities)).T
        # self.tfidf_X = self.tfidf_X.reshape(-1, 1)
        self.cue_X = np.vstack((*cue_phrase, *location, *asmo, *entities)).T
        self.ent_X = np.vstack((*entities, *location, *asmo)).T

        # ML train and test
        # from sklearn.model_selection import cross_val_score
        # from sklearn.model_selection import cross_validate
        # from sklearn.naive_bayes import ComplementNB
        # compNB_clf = ComplementNB()
        # print('ASMO compNB_clf: ', cross_val_score(compNB_clf, asmo_X, y, cv=10, scoring='f1').mean())
        # print('location compNB_clf: ', cross_val_score(compNB_clf, loc_X, y, cv=10, scoring='f1').mean())
        # print('cumulative NB_clf: ', cross_val_score(compNB_clf, X, y, cv=10, scoring='f1').mean())
        # from sklearn.linear_model import LogisticRegression
        # LR_clf = LogisticRegression(class_weight='balanced', solver='liblinear', multi_class='auto')
        # print('ASMO LR_clf: ', cross_val_score(LR_clf, asmo_X, y, cv=10, scoring='f1').mean())
        # print('location LR_clf: ', cross_val_score(LR_clf, loc_X, y, cv=10, scoring='f1').mean())
        # print('cumulative LR_clf: ', cross_val_score(LR_clf, X, y, cv=10, scoring='f1').mean())
        # from sklearn.svm import SVC
        # SVC_clf = SVC(gamma='scale', class_weight='balanced', decision_function_shape='ovo')
        # svc_score = cross_validate(SVC_clf, X, self.y, groups=None, scoring=('precision', 'recall', 'f1'), cv=10)
        # print('SVC')
        # print('precision:', svc_score['test_precision'])
        # print('recall:', svc_score['test_recall'])
        # print('f1:', svc_score['test_f1'])
        # print('---------')
        # print('ASMO SVC_clf: ', cross_val_score(SVC_clf, asmo_X, y, cv=10, scoring='f1').mean())
        # print('location SVC_clf: ', cross_val_score(SVC_clf, loc_X, y, cv=10, scoring='f1').mean())
        # print('cumulative SVC_clf: ', cross_val_score(SVC_clf, X, y, cv=10, scoring='f1').mean())
        # from sklearn.tree import DecisionTreeClassifier
        # DTC_clf = DecisionTreeClassifier(max_features=None, class_weight='balanced', max_depth=None, min_samples_leaf=1)
        # dtc_score = cross_validate(DTC_clf, X, self.y, groups=None, scoring=('precision', 'recall', 'f1'), cv=10)
        # print('DTC')
        # print('precision:', dtc_score['test_precision'])
        # print('recall:', dtc_score['test_recall'])
        # print('f1:', dtc_score['test_f1'])
        # print('---------')
        # print('ASMO DTC_clf: ', cross_val_score(DTC_clf, asmo_X, y, cv=10, scoring='f1').mean())
        # print('location DTC_clf: ', cross_val_score(DTC_clf, loc_X, y, cv=10, scoring='f1').mean())
        # print('cumulative DTC_clf: ', cross_val_score(DTC_clf, X, y, cv=10, scoring='f1').mean())


        from sklearn.model_selection import train_test_split
        # X_train, X_test, y_train, y_test = train_test_split(self.asmo_X, self.rhet_y, random_state=42, shuffle=True, test_size = .1)
        # self.supervised_ml(X_train, y_train, X_test, y_test, 'asmo_individual')
        # X_train, X_test, y_train, y_test = train_test_split(self.loc_X, self.rhet_y, random_state=42, shuffle=True, test_size = .1)
        # self.supervised_ml(X_train, y_train, X_test, y_test, 'location_individual')
        # X_train, X_test, y_train, y_test = train_test_split(self.sentlen_X, self.rhet_y, random_state=42, shuffle=True, test_size = .1)
        # self.supervised_ml(X_train, y_train, X_test, y_test, 'sent_len_individual')
        # X_train, X_test, y_train, y_test = train_test_split(self.quo_X, self.rhet_y, random_state=42, shuffle=True, test_size = .1)
        # self.supervised_ml(X_train, y_train, X_test, y_test, 'quotation_individual')
        # X_train, X_test, y_train, y_test = train_test_split(neg_X, y, random_state=42, shuffle=True, test_size = .1)
        # supervised_ml(X_train, y_train, X_test, y_test, 'neg_expr_individual')
        # X_train, X_test, y_train, y_test = train_test_split(self.tfidf_X, self.rhet_y, random_state=42, shuffle=True, test_size = .1)
        # self.supervised_ml(X_train, y_train, X_test, y_test, 'tfidf_individual')
        # X_train, X_test, y_train, y_test = train_test_split(self.cue_X, self.rhet_y, random_state=42, shuffle=True, test_size = .1)
        # self.supervised_ml(X_train, y_train, X_test, y_test, 'cue_individual')
        # X_train, X_test, y_train, y_test = train_test_split(self.ent_X, self.rhet_y, random_state=42, shuffle=True, test_size = .1)
        # self.supervised_ml(X_train, y_train, X_test, y_test, 'ent_individual')
        # X_train, X_test, y_train, y_test = train_test_split(self.rhet_X, self.y, random_state=42, shuffle=True, test_size = .1)
        # self.supervised_ml(X_train, y_train, X_test, y_test, 'rhetorical_individual')
        X_train, X_test, y_train, y_test = train_test_split(X, self.rhet_y, shuffle=True, test_size = .1)
        self.supervised_ml(X_train, y_train, X_test, y_test, 'cumulative')
    
    # def cumulative_tests(self, X):
    #     from sklearn.model_selection import train_test_split
    #     with open('./uob_fp/ML_Summary_bestset.csv', 'w', newline='') as outfile:
    #         fieldnames = ['P(NB)'


    #         for v in range(20):
    #             X_train, X_test, y_train, y_test = train_test_split(X, self.y, shuffle=True, test_size = .1)
    #             self.supervised_ml(X_train, y_train, X_test, y_test, 'cumulative')

pipeline = ml()
pipeline.prep_data()
pipeline.exec()