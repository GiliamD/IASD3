########################################################################################################################
#
#   File:           classes.py
#   Authors:        Maciej Przydatek & Giliam Datema
#   Created:        27/11/2015
#
#   Course:         Artificial Intelligence & Decision Systems
#   Assignment:     3
#   Institution:    Instituto Superior Técnico Lisboa
#
########################################################################################################################

"""
This file contains all classes used in the main file bn_inference.py.
"""


class Node:
    name = ""
    alias = ""
    values = []
    parents = []
    CPT = []

    def __str__(self):
        message = "\nName:    " + str(self.name) + "\nAlias:   " + str(self.alias) + "\nValues:  "
        for value in self.values:
            message += str(value) + ", "
        message += "\nParents: "
        for parent in self.parents:
            message += str(parent) + ", "
        message += "\nCPT:\n"
        for row in self.CPT:
            message += str(row) + "\n"
        return message


class Graph:
    nodes = []

    def getNodeNo(self, nameOrAlias):
        for i in range(len(self.nodes)):
            if self.nodes[i].name == nameOrAlias or self.nodes[i].alias == nameOrAlias:
                return i
        print("There is no node of name or alias \"%s\"." % nameOrAlias)
        return -1

    def getNode(self, nameOrAlias):
        return self.nodes[self.getNodeNo(nameOrAlias)]

    def getPrVal(self, nodename, assignments):
        if len(assignments) != len(self.nodes[self.getNodeNo(nodename)].parents) + 1:
            print("Variables assignments are not suitable. Specify correct number of assignments.")
            return -1
        for row in self.nodes[self.getNodeNo(nodename)].CPT:
            if row[0:len(assignments)] == assignments:
                return row[len(row)-1]

    def delNode(self, nameOrAlias):
        self.nodes.pop(self.getNodeNo(nameOrAlias))

    def addNode(self, node):
        try:
            if node.name == "":
                print("Node name must be specified.")
                return -1
            if len(node.values) == 0:
                print("Node values must be specified.")
                return -1
        except AttributeError:
            print("This is not a proper node.")
            return -1
        self.nodes.append(node)

    def getFactors(self, nodename):
        factors = []

        for node in self.nodes:
            if node.name == nodename or node.alias == nodename:
                factors.append(node)
                continue
            for parent in node.parents:
                if self.getNode(parent).name == nodename or self.getNode(parent).alias == nodename:
                    factors.append(node)
        return factors