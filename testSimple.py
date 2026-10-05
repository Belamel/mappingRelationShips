# import required module
from pathlib import Path
from rdflib import Graph, Literal
import threading
import time

g1 = Graph()
g2 = Graph()
g3 = Graph()

countEquivalent = 0
countInclude =0
countComplementarity = 0
countDisjoint = 0


# with open("rdf.ttl", "r") as f1, open("rdfwithoutMusic.ttl", "r") as f2:
# case equals
with open("scenarios/SparqlGenerate Agency_JSON.ttl", "r") as f1, open(
        "scenarios/Shexml Agency_Calendar_XML.ttl", "r") as f2, open(
    "scenarios/RML Mapping_Agency_CSV.ttl", "r") as f3:
    # case include
    # with open("rdf.ttl", "r") as f1, open("rdfwithoutMusic.ttl", "r") as f2:
    #     print(f1.name)

    l = [

        (g1.parse(file=f1), f1.name.rsplit('/', 1)[-1]),
        (g2.parse(file=f2), f2.name.rsplit('/', 1)[-1]),
        (g3.parse(file=f3), f3.name.rsplit('/', 1)[-1])
    ]

list_pairs = [(l[i], l[j]) for i in range(len(l)) for j in range(i + 1, len(l))]
print('Number of mappings files', len(l))
# print('Pairs to compare : ', list_pairs)
print('Number of mappings pairs', len(list_pairs))


def isInclude(g1, g2):
    graph1_is_included_in_graph2 = True
    for s, p, o in g1[0]:
        if not (s, p, o) in g2[0]:
            graph1_is_included_in_graph2 = False
            break
    return graph1_is_included_in_graph2


def IsComplement(g1, g2):
    complement_graph = g2[0] - g1[0]
    # complement_graph_bytes=(g2[0] - g1[0]).serialize(format="turtle").encode()
    # complement_graph = Graph().parse(data=complement_graph_bytes, format="turtle")
    # print(complement_graph)
    # print(complement_graph.serialize(format="turtle").encode().decode("utf-8")==g1[0])
    if (complement_graph.serialize(format="turtle").encode().decode("utf-8").split("b'\n'") == ['\n']):
        return False
    else:
        if (isInclude(g2, g1)):
            #    print('g1 '+g1[1]+ 'g2 '+g2[1]+ 'true')
            return True
        else:
            return False


def ShowComplement(g1, g2):
    complement_graph = g2[0] - g1[0]
    # print(complement_graph.serialize(format="turtle").encode().decode("utf-8").split("b'\n'")== ['\n'] )
    if (complement_graph.serialize(format="turtle").encode().decode("utf-8").split("b'\n'") == ['\n']):
        print('Any triple exist');
    else:
        # Print the resulting complement graph
        print(complement_graph.serialize(format="turtle").encode())


def AreIndependent(g1, g2):
    # check the independence of the two graphs
    nodes1 = set(g1[0].subjects()).union(set(g1[0].objects()))
    nodes2 = set(g2[0].subjects()).union(set(g2[0].objects()))

    if not nodes1.intersection(nodes2):
        print("The two graphs are independent.")
    else:
        print("The two graphs are not independent.")


def compareGraphs(graph1, graph2):
    if graph1[0].isomorphic(graph2[0]):
        print(graph1[1] + " is equivalent to " + graph2[1] + '\n')
        global countEquivalent
        countEquivalent = countEquivalent + 1

    else:
        if isInclude(graph1, graph2):
            print("The RDF graph in " + graph1[1] + " is included in " + graph2[1] + '\n')
            print("The RDF graph in " + graph2[1] + " is complement to " + graph1[1] + '\n')
            global countInclude
            global countComplementarity
            countInclude = countInclude + 1
            countComplementarity = countComplementarity + 1

        else:
            if isInclude(graph2, graph1):
                print("The RDF graph in " + graph2[1] + " is included in " + graph1[1] + '\n')
                print("The RDF graph in " + graph1[1] + " is complement to " + graph2[1] + '\n')
                # print(IsComplement(graph2, graph1))
                # ShowComplement(graph2, graph1)
            else:
                print("The RDF graph in " + graph1[1] + " is disjoint with graph RDF in " + graph2[1] + '\n')
                global countDisjoint
                countDisjoint = countDisjoint + 1

                # if(IsComplement(graph2, graph1)): # ShowComplement(graph2, graph1) print("The RDF graph in " +
                # graph1[1] + " is complement to " + graph2[1] +'\n') else: if(IsComplement(graph1, graph2)): #
                # ShowComplement(graph1, graph2) print("The RDF graph in " + graph2[1] + " is complement to " +
                # graph1[1]+'\n') else: print("The RDF graph in " + graph1[1] + " is contradictory with graph RDF in
                # " + graph2[1]+'\n')

                # print("The RDF graph in "+graph1[1]+" is not included in "+graph2[1])

    # AreIndependent(graph1,graph2)


# compare graphs
# compareGraphs(g1,g2)

threads = []
start = time.time()
for graph1, graph2 in list_pairs:
    thread = threading.Thread(target=compareGraphs, args=(graph1, graph2))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
# print('time of execution is :',time.time() - start,' ms')
print('Number of Equivalence is : ', countEquivalent)
print('Number of Inclusion is : ', countInclude)
print('Number of Complementarity is : ', countComplementarity)
print('Number of Disjoint is : ', countDisjoint)