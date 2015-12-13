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
    """
    Models node in BN graph.
    """
    name = ""
    alias = ""
    values = []
    parents = []
    CPT = []

    def __str__(self):
        """
            Prints a formatted text describing the node.
        """
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
        """
        Returns a number of node specified by name or alias.

        :param nameOrAlias: node's name or alias
        :return number: number of node
        """
        for i in range(len(self.nodes)):
            if self.nodes[i].name == nameOrAlias or self.nodes[i].alias == nameOrAlias:
                return i
        print("There is no node of name or alias \"%s\"." % nameOrAlias)
        return -1

    def getNode(self, nameOrAlias):
        """
        Returns a node (object of class 'Node') specified by name or alias.

        :param nameOrAlias: node's name or alias
        :return Node: desired node
        """
        return self.nodes[self.getNodeNo(nameOrAlias)]

    def getPrVal(self, nodename, assignments):
        """
        Returns a value of factor of name or alias 'nodename',
        according to specified assignment of itself and its dependent variables.
        First element of the list 'assignments' corresponds to node's value, next there should be presented values for
        each parent in order presented in 'self.parents' list.
        Example: value = graph.getPrVal('A', ['f', 'f', 't'])

        :param nodename: node's name or alias
        :param assignments: a list of assignments for the node and its dependent variables.
        :return Node: desired node
        """
        if len(assignments) != len(self.nodes[self.getNodeNo(nodename)].parents) + 1:
            print("Variables assignments are not suitable. Specify correct number of assignments.")
            return -1
        for row in self.nodes[self.getNodeNo(nodename)].CPT:
            if row[0:len(assignments)] == assignments:
                return row[len(row)-1]

    def delNode(self, nameOrAlias):
        """
        Deletes a node from the graph.

        :param nameOrAlias: node's name or alias
        """
        self.nodes.pop(self.getNodeNo(nameOrAlias))

    def addNode(self, node):
        """
        Adds a node to the graph.

        :param node: object of class 'Node' to be added
        :return number: -1 if 'node' object is incorrect
        """
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
        """
        Return a list of nodes, that are dependent on variable specified by 'nodename'.

        :param nodename: node's name or alias
        :return factors: list of nodes
        """
        factors = []

        for node in self.nodes:
            if node.name == nodename or node.alias == nodename:
                factors.append(node)
                continue
            for parent in node.parents:
                if self.getNode(parent).name == nodename or self.getNode(parent).alias == nodename:
                    factors.append(node)
        return factors
