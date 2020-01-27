import numpy as np
import csv
import sys

class ml:
    def __init__(self):
        #Target/label
        ##relevance target
        self.rel_y = np.array([])
        ##rhetorical target
        self.rhet_y = np.array([])

        #List of features
        ##for asmo feature-set
        self.agree_X = np.array([])
        self.outcome_X = np.array([])
        ##for location feature-set
        self.loc1_X = np.array([]); self.loc2_X = np.array([]); self.loc3_X = np.array([])
        self.loc4_X = np.array([]); self.loc5_X = np.array([]); self.loc6_X = np.array([])
        self.sentlen_X = np.array([])
        self.rhet_X = np.array([])
        self.tfidf_max_X = np.array([])
        self.tfidf_top20_X = np.array([])
        self.wordlist_X = np.array([])
        self.pasttense_X = np.array([])
        
        #Hachey and Grover's original features
        self.HGloc1_X = np.array([]); self.HGloc2_X = np.array([]); self.HGloc3_X = np.array([])
        self.HGloc4_X = np.array([]); self.HGloc5_X = np.array([]); self.HGloc6_X = np.array([])
        self.tfidf_HGavg_X = np.array([])
        self.HGsentlen_X = np.array([])
        self.qb_X = np.array([])
        self.inq_X = np.array([]) 
        ##for entities feature-set
        self.enamex_X = np.array([])
        self.legalent_X = np.array([])
        # all values are 0, thus non-beneficial in ml 
        # self.caseent_X = np.array([])
        ##for cue phrase feature-set
        self.asp_X = np.array([])
        self.modal_X = np.array([])
        self.voice_X = np.array([])
        self.negcue_X = np.array([])
        self.tense_X = np.array([])

    def classifier_performance(self, X_train, y_train, X_test, y_test, classifier):
        classifier.fit(X_train, y_train)
        predictions = classifier.predict(X_test)

        y_true = y_test
        y_pred = predictions

        from sklearn.metrics import classification_report
        clf_report = classification_report(y_true, y_pred, labels=np.unique(y_pred))
        print(clf_report)
        
        # # Visualize Decision Tree for DTC only
        # from sklearn.tree import export_graphviz

        # # Creates dot file named tree.dot
        # export_graphviz(
        #         classifier,
        #         out_file =  "output.dot",
        #         feature_names = ['loc3_X', 'loc4_X'],
        #         class_names = ['rhet_0', 'rhet_1', 'rhet_2', 'rhet_3', 'rhet_4', 'rhet_5', 'rhet_6'],
        #         filled = True,
        #         rounded = True)

    def classification_report_with_f1_score(self, y_true, y_pred, label):
        from sklearn.metrics import classification_report, f1_score
        print(classification_report(y_true, y_pred, labels=np.unique(y_pred)))
        if label == "multinomial":        
            return f1_score(y_true, y_pred, average='weighted', labels=np.unique(y_pred))
        elif label == "binary":
            return f1_score(y_true, y_pred, average='binary', labels=np.unique(y_pred))   
        else:
            print("Could not detect target type")
            sys.exit()    

    def supervised_ml(self, X, Y, label, feat_names, target_names, mode):
        model = input("Enter anything to use train_test_split, or '1' to use cross_val_score ")
        if model == '1':
            print("Using cross_val_score ")
            from sklearn.model_selection import cross_val_score
        else:
            print("Using train_test_split ")
            from sklearn.model_selection import train_test_split
            X_train, X_test, y_train, y_test = train_test_split(X, Y, shuffle=True, test_size = .1)
        
        rep = ""
        while rep != "done":
            clf, clf_name = mode.select_classifier(label)
            if model == '1':
                from sklearn.metrics import make_scorer
                from sklearn.model_selection import KFold
                cv = KFold(n_splits=10, shuffle=True)
                score = cross_val_score(clf, X=X, y=Y, cv=cv, 
                scoring=make_scorer(self.classification_report_with_f1_score, label=label))
                print(score)
                print(score.mean())
            else:
                self.classifier_performance(X_train, y_train, X_test, y_test, clf)
            print("Classifier:", clf_name, "features:", feat_names, "target:", target_names)  
            rep = input("Enter anything to try again, or 'done' to quit ")
        print('+++++++++++', 'DONE', '+++++++++++')

    #Extract all data and prepare it for ML
    def prep_data(self, filename):
        with open('./uob_fp/' + filename + '.csv', 'r') as infile:
            reader = csv.DictReader(infile)

            for row in reader:
                self.rel_y = np.append(self.rel_y, [float(row['align'])])
                self.agree_X = np.append(self.agree_X, [float(row['agree'])])
                self.outcome_X = np.append(self.outcome_X, [float(row['outcome'])])
                self.loc1_X = np.append(self.loc1_X, [float(row['loc1'])])
                self.loc2_X = np.append(self.loc2_X, [float(row['loc2'])])
                self.loc3_X = np.append(self.loc3_X, [float(row['loc3'])])
                self.loc4_X = np.append(self.loc4_X, [float(row['loc4'])])
                self.loc5_X = np.append(self.loc5_X, [float(row['loc5'])])
                self.loc6_X = np.append(self.loc6_X, [float(row['loc6'])])
                self.HGloc1_X = np.append(self.HGloc1_X, [float(row['HGloc1'])])
                self.HGloc2_X = np.append(self.HGloc2_X, [float(row['HGloc2'])])
                self.HGloc3_X = np.append(self.HGloc3_X, [float(row['HGloc3'])])
                self.HGloc4_X = np.append(self.HGloc4_X, [float(row['HGloc4'])])
                self.HGloc5_X = np.append(self.HGloc5_X, [float(row['HGloc5'])])
                self.HGloc6_X = np.append(self.HGloc6_X, [float(row['HGloc6'])])
                self.sentlen_X = np.append(self.sentlen_X, [float(row['sentlen'])])
                self.HGsentlen_X = np.append(self.HGsentlen_X, [float(row['HGsentlen'])])
                self.qb_X = np.append(self.qb_X, [float(row['quoteblock'])])
                self.inq_X = np.append(self.inq_X, [float(row['inline_q'])])
                self.rhet_X = np.append(self.rhet_X, [float(row['rhet'])])
                self.tfidf_max_X = np.append(self.tfidf_max_X, [float(row['tfidf_max'])])
                self.tfidf_top20_X = np.append(self.tfidf_top20_X, [float(row['tfidf_top20'])])
                self.tfidf_HGavg_X = np.append(self.tfidf_HGavg_X, [float(row['tfidf_HGavg'])])
                self.asp_X = np.append(self.asp_X, [float(row['aspect'])])
                self.modal_X = np.append(self.modal_X, [float(row['modal'])])
                self.voice_X = np.append(self.voice_X, [float(row['voice'])])
                self.negcue_X = np.append(self.negcue_X, [float(row['negation'])])
                self.tense_X = np.append(self.tense_X, [float(row['tense'])])
                self.legalent_X = np.append(self.legalent_X, [float(row['legal entities'])])
                self.enamex_X = np.append(self.enamex_X, [float(row['enamex'])])
                self.rhet_y = np.append(self.rhet_y, [float(row['rhet_target'])])
                self.wordlist_X = np.append(self.wordlist_X, [float(row['wordlist'])])
                self.pasttense_X = np.append(self.pasttense_X, [float(row['past tense'])])

    def exec(self):
        location = self.loc1_X, self.loc2_X, self.loc3_X, self.loc4_X, self.loc5_X, self.loc6_X
        HGlocation = self.HGloc1_X, self.HGloc2_X, self.HGloc3_X, self.HGloc4_X, self.HGloc5_X, self.HGloc6_X
        quotation = self.inq_X, self.qb_X
        entities = self.legalent_X, self.enamex_X
        asmo = self.agree_X, self.outcome_X
        cue_phrase = self.asp_X, self.modal_X, self.voice_X, self.negcue_X, self.tense_X
        sent_length = self.sentlen_X
        HGsent_length = self.HGsentlen_X
        tfidf_max = self.tfidf_max_X
        tfidf_top20 = self.tfidf_top20_X
        tfidf_HGavg = self.tfidf_HGavg_X
        rhet_role = self.rhet_X
        wordlist = self.wordlist_X
        pasttense = self.pasttense_X
        rhet_y = self.rhet_y
        rel_y = self.rel_y
        
        import mode_selector
        mode = mode_selector.mode_selector(location, HGlocation, quotation, entities, asmo,
        cue_phrase, sent_length, HGsent_length, tfidf_max, tfidf_top20, tfidf_HGavg, rhet_role, 
        wordlist, pasttense, rhet_y, rel_y)
        num_of_features = input("how many features? ")
        X, feat_names = mode.select_features(num_of_features)
        Y, label, target_names = mode.select_target()

        self.supervised_ml(X, Y, label, feat_names, target_names, mode)

pipeline = ml()
pipeline.prep_data('MLdata')
# pipeline.prep_data('MLdata_train')
pipeline.exec()