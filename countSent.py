import csv

with open('uob_fp/complete_sum.csv', 'r') as infile:
    reader = csv.DictReader(infile)

    count = 0
    case = ''
    for row in reader:
        if row['role'] == '<prep-date>' or row['role'] == '<sub-heading>' \
        or row['role'] == '<separator>' or row['role'] == '<new-case>':
            continue
        if case == '':
            case = row['case_id']
        if case != row['case_id']:
            print(case, count)
            case = row['case_id']
            count = 0
        if case == row['case_id']:
            count+=1
