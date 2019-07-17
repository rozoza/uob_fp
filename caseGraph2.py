import csv
import networkx as nx
import pylab as plt
import graphviz as gv
import pydot
import matplotlib.pyplot as plt
from graphviz import Digraph
from networkx.drawing.nx_pydot import write_dot
from networkx.drawing.nx_pydot import to_pydot
from networkx.drawing.nx_agraph import graphviz_layout
#import pygraphviz as pgv
#from networkx.drawing.nx_agraph import graphviz_layout, to_agraph

with open('./ASMO/AS.csv') as file:
    reader = csv.DictReader(file)

    case = input("enter legal case number: ")
    G = Digraph('G', filename='testing.gv')
    count = 0

    for row in reader:
        if int(row['case']) > int(case):
            break

        if int(row['case']) == int(case):

            body = str(row['body'])
            relation = str(row['relation'])


            #if "http" in body:
                #plt.figure(case)
        
            if "fullagr" in relation:
                if "self" in str(row['to']):
                    G.edge(str(row['from']), str(row['from']))
                else:
                    G.edge(str(row['from']), str(row['to']))
        count += 1
        print("count = ", count)

    #nx.draw_networkx(G, node_size=400,font_size=8)
    #plt.draw()
    #fig_name = "case_" + case + ".png"
    #plt.savefig(fig_name)
    #nx.write_dot(G,'graph.dot')
    #plt.show()

    #A = to_agraph(G)
    #print(A)
    #A.layout('dot')
    #A.draw('abcd.png')

    #write_dot(G, 'test.dot')
    #A = to_pydot(G)
    #A.write_png('test.png')

    #node_positions = {node[0]: (node[1]['X'], -node[1]['Y']) for node in G.nodes(data=True)}
    #edge_colors = [e[2]['color'] for e in G.edges(data=True)]
    #plt.figure(figsize=(8, 6))
    #nx.draw(G, pos=node_positions, edge_color=edge_colors, node_size=10, node_color='black')
    #nx.draw(G, node_size=200, node_color='white')
    #plt.title('Test graph', size=15)
    #plt.show()

    #pos = nx.nx_agraph.graphviz_layout(G)
    #nx.draw(G, pos=pos)
    #write_dot(G, 'test.dot')

    G.view()
