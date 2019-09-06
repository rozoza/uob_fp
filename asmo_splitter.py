import csv

asmoCase = ['22', '23', '11', '9',
    '12', '14', '13', '5', '20',
    '3', '2', '21', '7', '4',
    '15', '18', '19', '6', '17',
    '42', '38', '26', '45', '43',
    '31', '35', '36', '32', '40',
    '29', '24', '34', '47', '69',
    '55', '63', '57', '62', '46',
    'N/A', '60', '49', '56', '66',
    '68', '52', '53']

# string 'ï»¿' was generated by microsoft excel when modifying Complete_Corpus
fieldnames = ['ï»¿', 'case', 'line', 'body', 'from', 'to', 'relation', 'pos', 'mj']

for v in range(len(asmoCase)):
    if asmoCase[v] == 'N/A':
        continue
    
    filename = 'asmo_' + asmoCase[v] + '.csv'
    with open('./uob_fp/ASMO_46_corpus/' + filename, 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
    with open('./uob_fp/Complete_Corpus.csv', 'r') as infile, \
    open('./uob_fp/ASMO_46_corpus/' + filename, 'a', newline='') as outfile:
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        for row in reader:
            if row['case'] == asmoCase[v]:
                writer.writerow({'ï»¿': row['ï»¿'], 'case': row['case'], 'line': row['line'],\
                'body': row['body'], 'from': row['from'], 'to': row['to'], 'relation': row['relation'],\
                'pos': row['pos'], 'mj': row['mj']})