import csv
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import write_dot
#import matplotlib.backends.backend_pdf

with open('./ASMO/Complete_Corpus.csv') as file:
    reader = csv.DictReader(file)

    case = input("enter legal case number: ")
    G = nx.MultiDiGraph()
    color_map = []

    #count = 0

    for row in reader:
        if int(row['case']) > int(case):
            break

        if int(row['case']) == int(case):

            body = str(row['body'])
            relation = str(row['relation'])

            if "http" in body:
                fig = plt.figure(case)
            
            if str(row['from']) != "NAN":
                G.add_node(str(row['from']))
        
            if "fullagr" in relation:
                if "self" in str(row['to']):
                    G.add_edge(str(row['from']), str(row['to']))
                else:
                    G.add_edge(str(row['from']), str(row['to']))
        #count += 1
        #print("count = ", count)

    for node in G:
        if node == "self":
            color_map.append('#EEC76D')
        elif node == "all":
            color_map.append('#BDF7F5')
        else:
            color_map.append('white')


    pos = nx.circular_layout(G, scale=0.1)
    nodes = nx.draw_networkx_nodes(G, pos=pos, node_size=500, node_color=color_map, node_shape='o')
    edges = nx.draw_networkx_edges(G, pos=pos, edge_color='black', arrowsize=20)
    labels = nx.draw_networkx_labels(G, pos=pos, font_size=10)
    nodes.set_edgecolor('black')
    fig_name = "case_" + case + ".pdf"
    fig.suptitle(fig_name, fontsize=14, fontweight='bold')
    plt.draw()
    #write_dot(G, 'test50.dot')

    #pdf = matplotlib.backends.backend_pdf.PdfPages("output.pdf")
    #for fig in range(1, G().number): ## will open an empty extra figure :(
        #pdf.savefig( fig )
        #pdf.close()

    file_path = "./uob_fp/46graphspdf/"
    plt.savefig(file_path + fig_name)
    #plt.show()
    plt.close('all')
    