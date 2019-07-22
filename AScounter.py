import csv

with open('./ASMO/AS.csv') as file:
    reader = csv.DictReader(file)

    count = 0
    case = 0

    for row in reader:
        if case != int(row['case']):
            case = int(row['case'])
            count += 1
    print(count)