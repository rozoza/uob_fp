import csv

def join_sumasmo():
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
    
    with open('./ASMO/Complete_Corpus.csv', 'r') as in_file1, open('./uob_fp/complete_sum.csv', 'r') as in_file2:
        asmo_reader = csv.DictReader(in_file1)
        sum_reader = csv.DictReader(in_file2)

        for row in sum_reader:
            print(row)
        # wordlist = text.split()
        # count_token = len(wordlist)
        # maxcount = 0
        # sentence = ''
        # index = ''

        # for row in reader:
        #     count = 0
        #     if new_case == True :
        #         return row['mj']
            
        #     if row['case'] == asmo:
        #         if text in row['body']:
        #             return 'matched'
        # return 'no match'
        #         # for v in range(count_token):
        #         #     if wordlist[v] in row['body']:
        #         #         count += 1
        #         # if count >= maxcount:
        #         #     maxcount = count
        #         #     sentence = row['body']
        #         #     index = row['line']
        #         #     print(index, sentence)

# with open('./uob_fp/join_test.csv', 'a', newline='') as out_file:
#     fieldnames = ['case_id', 'sentence_id', 'para_id', 'judge', 'text', 'role', 'align', 'agree', 'outcome']

#     csv_writer = csv.DictWriter(out_file, fieldnames=fieldnames)

join_sumasmo()