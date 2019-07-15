import csv
import networkx as nx
import matplotlib.pyplot as plt

with open('./ASMO/AS.csv') as file:
    reader = csv.DictReader(file)

    case = input("enter legal case number: ")
    G = nx.MultiDiGraph()
    count = 0

    for row in reader:
        if int(row['case']) > int(case):
            break

        if int(row['case']) == int(case):

            body = str(row['body'])
            relation = str(row['relation'])


            if "http" in body:
                plt.figure(case)
        
            if "fullagr" in relation:
                if "self" in str(row['to']):
                    G.add_edge(str(row['from']), str(row['from']))
                else:
                    G.add_edge(str(row['from']), str(row['to']))
        count += 1
        print("count = ", count)

    nx.draw_networkx(G, node_size=400,font_size=8)
    plt.draw()
    #fig_name = "case_" + case + ".png"
    #plt.savefig(fig_name)
    plt.show()
