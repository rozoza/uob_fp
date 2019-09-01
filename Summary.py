import csv

def countlines(case, parreader):
    count = 1
    for lines in parreader:
        if int(lines['case']) == case:
            count += 1
        if int(lines['case']) > case:
            break
    return count


with open('./ASMO/Complete_Corpus.csv') as file:
    reader = csv.DictReader(file)
    current_lord = ''
    name = ''
    filename = ''
    lines = 0
    fullagr = True
    
    try:
        for row in reader:
            if int(row['case']) == 300:
                if int(row['line']) == 0:
                    '''Need to know how to open different reader 
                    and countlines so we know the begining and ending of each case and lord
                    case using row[('case')]
                    maybe use new judge for the lord'''
                    #lines = countlines(int(row['case']), reader)
                    #print(lines)
                    name = 'summary_' + 'case_' + row['case'] + '_ASMO'
                    filename = './uob_fp/Summary/' + name + '.txt'
                    f = open(filename, 'w+')
                    f.write(name + '\n')
                    f.write('from ' + row['body'] + '\n')
                    f.write('majority opinion: ' + row['mj'] + '\n')

                if 'LORD' in row['body'] or 'BARONESS' in row['body']:
                    if fullagr == False:
                        f.write(current_lord + 'is assumed to fully agree only with his/her own reasonings ' + '\n')                        
                    current_lord = row['body']
                    fullagr = False
                    f.write('\n' + '--' + current_lord + '--' + '\n')

                if row['relation'] == 'fullagr':
                    fullagr = True
                    if row['to'] == 'all':
                        f.write(row['from'] + ' agrees with all judges' + '\n')
                    elif row['to'] == 'self':  
                        f.write(row['from'] + ' states the importance of his/her own reasonings' + '\n')
                    else:                  
                        f.write(row['from'] + ' has a full agreement with ' + row['to'] + '\n')
                
                if row['relation'] == 'outcome':
                    f.write('outcome: ' + '\n')
                    f.write(row['body'] + '\n')

            # if int(row['case']) == 100:
            #     print('hello')
            #     break

    except Exception as e:
        print(e)
    finally:
        f.close()
