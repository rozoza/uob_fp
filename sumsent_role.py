import csv
import sumVerbs

# Cases that Oliver initially needed
# caseList = ['1.19', '3.22', '1.11','1.55','2.21','2.3','2.35','2.45','2.47','3.02','3.08','3.1',
# '3.14','3.28','3.44', '2.23']

#Complete 46 cases
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

missingdict = sumVerbs.count()
for v in range(len(caseList)):
    filename = caseList[v]
    with open('./uob_fp/comsum_corpus/comsum_' + filename + '.csv', 'r') as infile:
        reader = csv.DictReader(infile)

        count_none = 0
        count_textual = 0
        count_disposal = 0
        count_framing = 0
        count_background = 0
        count_proceedings = 0
        count_fact = 0
        missing_type = str(missingdict.get(filename))

        for row in reader:

            if row['role'] == 'NONE':
                count_none += 1
            if row['role'] == 'TEXTUAL':
                count_textual += 1
            if row['role'] == 'DISPOSAL':
                count_disposal += 1
            if row['role'] == 'FRAMING':
                count_framing += 1
            if row['role'] == 'BACKGROUND':
                count_background += 1
            if row['role'] == 'PROCEEDINGS':
                count_proceedings += 1
            if row['role'] == 'FACT':
                count_fact += 1
        print('(' + filename + ', ' + '[' + str(count_none), ',', str(count_textual), ',', str(count_fact), ',',
        str(count_proceedings), ',', str(count_background), ',', str(count_framing), ',', str(count_disposal) + 
        ']' + ', ' + missing_type + ')')


