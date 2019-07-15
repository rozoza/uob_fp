import csv
import networkx as nx
import matplotlib.pyplot as plt

with open('./ASMO/AS.csv') as file:
    reader = csv.DictReader(file)

    case = 0
    judge = 0
    G = nx.MultiDiGraph()
    judgeList = []
    count = 1
    new_judge = False


    for row in reader:
        if case == 21:
            break

        body = str(row['body'])
        relation = str(row['relation'])

        if new_judge == True:
            judgeList.append([body, judge])
            new_judge = False

        if "http" in body:
            if case > 0:
                #for x in range(len(judgeList)):
                #   print(judgeList[x])
                nx.draw_networkx(G, node_size=400, font_size=8)
                plt.draw()
                G.clear()
                judgeList.clear()
                judge == 0
                count == 1
            
            #judgeList.append(["name", "number", "to"])
            case += 1
            plt.figure(case)

        if "------------- NEW JUDGE ---------------" in body:
            judge += 1
            new_judge = True
        
        if "fullagr" in relation:
            count += 1
            G.add_edge(str(row['from']), str(row['to']))
            #judgeList.append([str(row['from']), judge, str(row['to'])])

    nx.draw_networkx(G, node_size=400, font_size=8)
    plt.draw()

    plt.show()