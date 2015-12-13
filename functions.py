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
import itertools
import numpy as np


def readBNFile(input1):
    """
    Reads Bayesian Network structure from input file and returns it in variable graph.
    If any error occurs, it returns -1.

    :param input1: file name string
    :return graph: contains whole BN structure
    """
    graph = Graph()

    with open(input1, 'r') as input1:

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

                print("\nFile %s successfully loaded. %d lines have been read." % (input1.name, lineNo-1))
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



def readQueryFile(input2):
    """
    Reads query file and returns query variable and evidence variables with their assignments.

    :param input2: input file name (string) of the query file (.in)
    :return query: query variable name or alias (string)
    :return evidence: vector of evidence variable names or aliases (string) and their value assignment (string or number)
    """

    with open(input2, 'r') as input2:

        # Initialize query and evidence
        query, evidence = None, None

        lineNo = 0  # Line counter
        for line in input2.readlines():
            lineNo += 1
            if len(line) != 0 and line[0] != '#':   # Skip if empty line or comment
                line = line.strip('\n').split()     # Remove end line
                if line[0] == 'QUERY':
                    if len(line) != 2:              # Check if only one query variable
                        print('ERROR: QUERY line in file %s is incorrect. There can only be 1 query variable.' % input2.name)
                        return query, evidence      # NOTE: if error, query and evidence are None
                    else:
                        query = line[1]             # Get query variable if no error
                elif line[0] == 'EVIDENCE':
                    try:
                        n = int(line[1])            # Try get number of evidence variables
                    except ValueError:
                        print('ERROR: Number of evidence variables in file %s not specified.' % input2.name)
                        return query, evidence

                    if (len(line)-2)/2 != n:        # Check if specified number matches actual number
                        print('ERROR: Number of evidence variables in file %s does not match the specified number or '
                              'one or more evidence variable names or assignments are missing.' % input2.name)
                        return query, evidence

                    evidence = line[2:]             # Get evidence if no error

                    # Restructure evidence into matrix: each variable on new row
                    k = 0
                    tmp = []
                    for i in range(0,len(evidence)-1,2):
                        tmp.append([evidence[i], evidence[i+1]])
                        k += 1
                    evidence = tmp

        # If query or evidence is None, it's missing or not specified correctly
        if query is None:
            print('ERROR: No query specified in file %s.' % input2.name)
        elif evidence is None:
            print('ERROR: No evidence specified in file %s' % input2.name)
        else:
            print('\nFile %s successfully loaded. %d lines have been read.' % (input2.name, lineNo))

    return query, evidence  # None if error


def product(graph, factors, varName):
    """
    Computes the product of a set of factors in tabular form.

    :param graph: Bayesian Network (Graph object)
    :param factors: set of factors in tabular form (list of Factor objects)
    :param varName: name of variable to eliminate (string) -> will be first column of table
    :return factorProduct: product of set of factors, which is a new Factor object
    """

    # If only one factor, no multiplication
    if len(factors) == 1:
        return factors[0]

    # Get all variables involved in the set of factors. NOTE: Variable to eliminate first!
    vars = [varName]
    for factor in factors:
        for var in factor.nodesInvolved:
            if var not in vars:
                vars.append(var)

    # Get all possible values for each variable involved
    values = []
    for nodeName in vars:
        values.append(graph.getNode(nodeName).values)

    # Get ordered list of all possible combinations of values of the variables
    combinations = list(itertools.product(*values))

    # Create factor table
    factorTable = np.zeros([len(combinations), len(factors)])

    # Get probability values corresponding to given combinations of value assignments
    i = 0
    for combination in combinations:
        j = 0
        for factor in factors:
            assignment = []
            for nodeName in factor.nodesInvolved:
                assignment.append(combination[vars.index(nodeName)])
                factorTable[i][j] = factor.getPrVal(assignment)
            j += 1
        i += 1

    # Compute product of factors
    prod = np.ones(len(factorTable))
    for i in range(len(factorTable[0])):
        prod = np.multiply(prod, factorTable[:,i])

    # Store product in Factor object with Conditional Probability Table (CPT) and ordered list of nodes involved
    factorProduct = Factor()
    factorProduct.nodesInvolved = vars

    for i in range(len(prod)):
        row = []
        for value in combinations[i]:
            row.append(value)
        row.append(prod[i])
        factorProduct.CPT.append(row)

    return factorProduct


def marginalization(graph, factorProduct, varName):
    """
    Sums out the variable to eliminate.

    :param graph: Bayesian Network (Graph object)
    :param factorProduct: product of factors, which is a Factor object itself (output from product() function)
    :param varName: name of variable to eliminate (string)
    :return marg: marginalization of the factorProduct w.r.t. the variable to eliminate (also Factor object itself)
    """

    # Get number of possible values of variable over which the sum is computed
    numValues = len(graph.getNode(varName).values)

    # Step between rows that need to be summed
    step = int(len(factorProduct.CPT)/numValues)

    # Store marginalization in Factor object with CPT and variables involved
    marg = Factor()
    marg.nodesInvolved = factorProduct.nodesInvolved
    marg.nodesInvolved.remove(varName)
    for i in range(step):
        marg.CPT.append(factorProduct.CPT[i][1:-1]+[sum([factorProduct.CPT[i+j*step][-1] for j in range(numValues)])])

    # Remove node from graph
    graph.delNode(varName)

    return marg


def eliminateVar(graph, factors, varName, steps):
    """
    Eliminates specified variable by sum-product variable elimination.

    :param graph: Bayesian Network (Graph object)
    :param factors: set of factors in tabular form (list of Factor objects)
    :param varName: name of variable to eliminate (string)
    :param steps: list of steps of the algorithm (strings) to write to output file if -verbose option passed
    :return factors: updated set (list) of factors
    """

    # Get factors in which variable varName is involved
    factors_in = []
    i = 0
    factorNums = []
    for factor in factors:
        i += 1
        if varName in factor.nodesInvolved:
            factors_in.append(factor)
            factorNums.append(str(i))

    # Output steps
    steps.append('\n>> FACTORS INVOLVING VAR '+varName+' (indicated by number):\n\n')
    steps.append(' '.join(factorNums)+'\n')

    # Remove factors_in from set of factors
    for factor in factors_in:
        factors.remove(factor)

    # Compute product of factors in factors_in
    prod = product(graph, factors_in, varName)

    # Output steps
    steps.append('\n>> PRODUCT OF FACTORS '+' '.join(factorNums)+' (tabular form, rounded):\n\n')
    steps.append('VARS: '+' '.join(prod.nodesInvolved)+'\nCPT:\n')
    tmp = deepcopy(prod.CPT)
    for i in range(len(tmp)):
        tmp[i][-1] = '%.5f' % prod.CPT[i][-1]
    for row in tmp:
        steps.append(' '.join(map(str,row))+'\n')

    # Compute marginalization of prod w.r.t. the variable to eliminate, i.e. varName
    marg = marginalization(graph, prod, varName)

    # Output steps
    steps.append('\n>> MARGINALIZATION OF FACTOR PRODUCT W.R.T. '+varName+':\n\n')
    steps.append('VARS: '+' '.join(prod.nodesInvolved)+'\nCPT:\n')
    tmp = deepcopy(marg.CPT)
    for i in range(len(tmp)):
        tmp[i][-1] = '%.5f' % marg.CPT[i][-1]
    for row in tmp:
        steps.append(' '.join(map(str,row))+'\n')

    # Add resulting factor to set of factors
    factors.append(marg)

    # Output steps
    steps.append('\n>> REMOVE FACTORS INVOLVING VAR '+varName+' FROM SET OF FACTORS')
    steps.append('\n>> ADD MARGINALIZATION W.R.T. '+varName+' TO SET OF FACTORS\n')

    return factors


def VE(graph, factors, varsToEliminate, query, evidence, order):
    """
    Main function of the sum-product Variable Elimination (VE) algorithm.

    :param graph: Bayesian Network (Graph object)
    :param factors: set of factors in tabular form (list of Factor objects)
    :param varsToEliminate: list of variable names (strings) to eliminate
    :param query: query variable name (string)
    :param evidence: list of evidence variable names and associated values
    :param order: list specifying the order of variable elimination
    :return PPD_str: solution — the posterior probability density (string format)
    :return steps: list of strings containing a description of the main steps of the VE algorithm, written to output if -verbose specified
    """

    steps = []

    # Sort varsToEliminate according to order
    varsToEliminate = [var for rank, var in sorted(zip(order, varsToEliminate))]

    # Output steps
    steps.append('\nVARIABLES TO ELIMINATE:\n')
    steps.append(' '.join(varsToEliminate))
    steps.append('\n\nHEURISTIC: MIN-NEIGHBOURS\n')

    # Eliminate all variables in varsToEliminate
    i = 0
    for varName in varsToEliminate:
        # output steps
        i += 1
        steps.append('\n\n========== ITERATION %d ==========\n\n' % i)
        steps.append('ELIMINATING VAR: '+varName+'\n')
        steps.append('\n>> SET OF FACTORS (tabular form):\n')
        j = 0
        for factor in factors:
            j += 1
            steps.append('\nFACTOR %d\n' %j)
            steps.append('VARS: '+' '.join(factor.nodesInvolved)+'\nCPT:\n')
            for row in factor.CPT:
                steps.append(' '.join(map(str,row))+'\n')

        # Eliminate variable, get updated set of factors
        factors = eliminateVar(graph, factors, varName, steps)

    # Compute product of remaining factors in set
    prod = product(graph, factors, query)

    # Output steps
    steps.append('\n\n========== WRAP-UP ==========\n')
    steps.append('\n>> PRODUCT OF REMAINING FACTORS:\n\n')
    steps.append('VARS: '+' '.join(prod.nodesInvolved)+'\nCPT:\n')
    tmp = deepcopy(prod.CPT)
    for i in range(len(tmp)):
        tmp[i][-1] = '%.5f' % prod.CPT[i][-1]
    for row in tmp:
        steps.append(' '.join(map(str,row))+'\n')

    # Get Posterior Probability Density (PPD) given the assignment of evidence variables
    PPD = []
    evidenceValues = []

    # Get evidence assignments
    for e in evidence:
        evidenceValues.append(e[-1])

    # Output step
    steps.append('\n>> PROBABILITY VALUES GIVEN THE EVIDENCE:\n\n')

    # Get probability for the possible values of the query variable, given the evidence assignments
    for queryValue in graph.getNode(query).values:
        PPD.append(prod.getPrVal([queryValue]+evidenceValues))

        steps.append(' '.join([queryValue]+['%.5f ' % PPD[-1]]))

    # Normalize probability values and round
    PPD = np.round(PPD/sum(PPD),3)

    # Convert to string for output
    PPD_str = []
    i = 0
    for queryValue in graph.getNode(query).values:
        PPD_str += [str(queryValue), str(PPD[i])]
        i += 1

    # Output steps
    steps.append('\n\n>> NORMALIZE PROBABILITY VALUES\n')
    steps.append('\n>> POSTERIOR PROBABILITY DISTRIBUTION:\n\n')
    steps.append(' '.join(PPD_str))

    return PPD_str, steps


def writeOutput(outputFileName, output):
    """
    Writes solution to output file and steps of the algorithm when asked for (-verbose).

    :param outputFileName: same name as .in file, but with extension .sol (string)
    :param output: list of output lines (strings)
    :return:
    """

    with open(outputFileName, 'w') as outputFile:
        outputFile.writelines(output)

    return 1