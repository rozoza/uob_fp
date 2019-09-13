import csv

comsumCase = ['1.19','1.63', '1.68', 'N/A', 
    '1.05', '1.02', '1.04', '1.35', '1.39',
    '1.38', '1.42', '1.34', '1.11', '1.15',
    '1.26', '1.28', '1.57', '1.43', '1.55',
    '2.13', '2.18', '2.3', '2.35', '2.34',
    '2.26', '2.24', '2.29', '2.21', '2.23',
    '2.45', '2.47', '2.41', '3.18', '3.21',
    '3.22', '3.07', '3.1', '3.08', '3.02',
    '3.44', '3.41', '3.31', '3.32', '3.15', 
    '3.14', '3.28']

fieldnames = ['case_id', 'sentence_id', 'para_id', 'judge', 'text', 'role', 'align', 'agree', 'outcome']

for v in range(len(comsumCase)):    
    filename = 'comsum_' + comsumCase[v] + '.csv'
    if comsumCase[v] == 'N/A':
        filename = 'comsum_' + 'NA' + '.csv'
    with open('./uob_fp/comsum_corpus/' + filename, 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
    with open('./uob_fp/complete_sum.csv', 'r') as infile, \
    open('./uob_fp/comsum_corpus/' + filename, 'a', newline='') as outfile:
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        for row in reader:
            if row['case_id'] == comsumCase[v]:
                writer.writerow({'case_id': row['case_id'], 'sentence_id': row['sentence_id'], \
                'para_id': row['para_id'], 'judge': row['judge'], 'text': row['text'], \
                'role': row['role'], 'align': row['align'], 'agree': row['agree'], 'outcome': row['outcome']})