import csv
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import write_dot

with open('./ASMO/AS.csv') as file:
    reader = csv.DictReader(file)

    case = input("enter legal case number: ")
    G = nx.MultiDiGraph()
    #count = 0

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
                    G.add_node(str(row['from']))
                    G.add_edge(str(row['from']), str(row['from']))
                else:
                    G.add_edge(str(row['from']), str(row['to']))
        #count += 1
        #print("count = ", count)

    pos = nx.shell_layout(G)
    nodes = nx.draw_networkx_nodes(G, pos=pos, node_size=700, node_color='white', node_shape='o')
    edges = nx.draw_networkx_edges(G, pos=pos, edge_color='black', arrowsize=30)
    labels = nx.draw_networkx_labels(G, pos=pos, font_size=10)
    nodes.set_edgecolor('black')
    plt.draw()
    #write_dot(G, 'test50.dot')
    fig_name = "case_" + case + ".png"
    file_path = "./graphs/"
    plt.savefig(file_path + fig_name)
    #plt.show()
    