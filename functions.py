########################################################################################################################
#
#   File:           functions.py
#   Authors:        Maciej Przydatek & Giliam Datema
#   Created:        27/11/2015
#
#   Course:         Artificial Intelligence & Decision Systems
#   Assignment:     3
#   Institution:    Instituto Superior Técnico Lisboa
#
########################################################################################################################

"""
This file contains all functions used in the main file bn_inference.py, notably the sum-product variable elimination
(VE) algorithm.
"""
from classes import *
from copy import deepcopy


def readInputFiles(input1):
    """
    Reads Bayesian Network structure from input file and returns it in variable graph.
    If any error occures, it returns -1.

    :param input1: file name string
    :return graph: contains whole BN structure
    """
    graph = Graph()

    input1 = open(input1, 'r')

    lineNo = 0  # line number indicator

    ifVAR = False   # temporary variable indicating, if we currently are in VAR section of file
    ifCPT = False   # temporary variable indicating, if we currently are in CPT section of file

    nodeNo = -1     # temporary variable, stores number of node we currently work with

    ifTable = False # temporary variable indicating, if we currently are in table of CPT section of the file
    tableLine = []  # temporary variable, stores whole table in single line

    tmp = Node()    # temporary variable, stores object of class Node

    while True:
        lineNo += 1
        line = input1.readline()

        if len(line) == 0:  # means, that we reached the end of the file
            if not ifTable: # means, that we ended reading a CPT section and didn't find table
                print("CPT statement without a table! Check entry ending at line %d." % (lineNo-1))
                return -1

            nRows = len(graph.nodes[nodeNo].values)
            for parent in graph.nodes[nodeNo].parents:
                nRows *= len(graph.nodes[graph.getNodeNo(parent)].values)

            nCols = len(graph.nodes[nodeNo].parents) + 2

            if nRows*nCols != len(tableLine):   # if read assignments number is not as expected
                print("Number of CPT entries is not as expected. Check CPT entry ending at line %d." % (lineNo-1))
                print("Expected number of entries: ",nCols, ", got: ", len(tableLine))
                return -1

            graph.nodes[nodeNo].CPT = [[] for i in range(nRows)]

            for i in range(nRows):
                first = i*nCols
                graph.nodes[nodeNo].CPT[i] = tableLine[first:first+nCols]
            for i in range(nRows):
                graph.nodes[nodeNo].CPT[i][len(graph.nodes[nodeNo].CPT[i])-1] = float(graph.nodes[nodeNo].CPT[i][len(graph.nodes[nodeNo].CPT[i])-1])

            for i in range(len(graph.nodes)):
                for j in range(len(graph.nodes[i].parents)):
                    graph.nodes[i].parents[j] = graph.getNode(graph.nodes[i].parents[j]).name

            input1.close()

            print("File successfully loaded. %d lines have been read." % (lineNo-1))
            return graph

        if line[0] != '\n':
            line = line.strip('\n').split(" ")

        if line[0] == '#':
            continue

        if line[0] == 'VAR':  # new VAR section found
            if ifVAR:
                print("Started new VAR definition before finishing last one. Check line %d." % lineNo)
                return -1
            if not ifCPT:
                tmp.name = ""
                tmp.alias = ""
                tmp.values = []
                tmp.parents = []
                tmp.CPT = []
                ifVAR = True
                continue
            print("VAR inside CPT in input file (remember about blank lines!)")
            return -1

        if line[0] == 'CPT':    # new CPT section found
            if ifCPT:
                print("Started new CPT definition before finishing last one. Check line %d." % lineNo)
                return -1
            if not ifVAR:
                ifCPT = True
                continue
            print("CPT inside VAR in input file (remember about blank lines!)")
            return -1

        if line[0] == '\n':     # end of section or more than one blank line one after another
            if ifVAR:   # if VAR statement is active, then it will end here
                if tmp.name == "":
                    print("VAR without name detected! Check VAR ending at %d line." % (lineNo-1))
                    return -1
                if len(tmp.values) == 0:
                    print("VAR without values detected! Check VAR ending at %d line." % (lineNo-1))
                    return -1
                graph.nodes.append(deepcopy(tmp))
                ifVAR = False
                continue
            if ifCPT:   # if CPT statement is active, then it will end here
                if not ifTable:     # means, that we ended reading a CPT section and didn't find table
                    print("CPT statement without a table! Check entry ending at line %d." % (lineNo-1))
                    return -1

                nRows = len(graph.nodes[nodeNo].values)
                for parent in graph.nodes[nodeNo].parents:
                    nRows *= len(graph.nodes[graph.getNodeNo(parent)].values)

                nCols = len(graph.nodes[nodeNo].parents) + 2

                if nRows*nCols != len(tableLine):   # if read assignments number is not as expected
                    print("Number of CPT entries is not as expected. Check CPT entry ending at line %d." % (lineNo-1))
                    print("Expected number of entries: ",nCols, ", got: ", len(tableLine))
                    return -1

                graph.nodes[nodeNo].CPT = [[] for i in range(nRows)]

                for i in range(nRows):
                    first = i*nCols
                    graph.nodes[nodeNo].CPT[i] = tableLine[first:first+nCols]
                for i in range(nRows):
                    graph.nodes[nodeNo].CPT[i][len(graph.nodes[nodeNo].CPT[i])-1] = float(graph.nodes[nodeNo].CPT[i][len(graph.nodes[nodeNo].CPT[i])-1])
                nodeNo = -1
                tableLine = []
                ifTable = False
                ifCPT = False
                continue
            continue
        # a this point we know, that we are inside either a VAR or a CPT section
        if ifVAR:
            if line[0] == 'name':
                try:
                    tmp.name = line[1]
                except IndexError:
                    print("There is no VAR name in line %d." % lineNo)
                    return -1
                continue
            if line[0] == 'values':
                for i in range(1,len(line)):
                    tmp.values.append(line[i])
                continue
            if line[0] == 'alias':
                try:
                    tmp.alias = line[1]
                except IndexError:
                    print("There is no VAR alias in line %d." % lineNo)
                    return -1
                continue
            if line[0] == 'parents':
                for i in range(1,len(line)):
                    tmp.parents.append(line[i])
                continue

        if ifCPT:
            #return graph
            if line[0] == 'var':
                try:
                    nodeNo = graph.getNodeNo(line[1])
                except IndexError:
                    print("There is no var name or alias in line %d." % lineNo)
                    return -1
                if nodeNo == -1:
                    print("All nodes should be defined before first CPT statement.\n"
                          "Check line %d." % lineNo)
                    return -1
                continue
            if line[0] == 'table':
                ifTable = True
                for i in range(1, len(line)):
                    tableLine.append(line[i])
                continue
            tableLine.extend(line)
            continue