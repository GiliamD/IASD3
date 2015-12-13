########################################################################################################################
#
#   File:           bn_inference.py
#   Authors:        Maciej Przydatek & Giliam Datema
#   Created:        27/11/2015
#
#   Course:         Artificial Intelligence & Decision Systems
#   Assignment:     3
#   Institution:    Instituto Superior Técnico Lisboa
#
########################################################################################################################

"""
This program is an implementation of a probabilistic reasoner based on Bayesian Networks (BN). It computes the posterior
probability distribution P(X|e) for a query variable X, given a particular observed event e, using the sum-product
variable elimination (VE) algorithm.

The program can be executed from the command line as follows:

$ bn_inference.py input1.bn input2.in [-verbose]

where the input file with extension .bn defines the Bayesian Network and the input file with extension .in defines the
query and evidence. The optional argument -verbose can be used to print all the steps of the VE algorithm.
"""

from functions import *
import sys

# Get names of input files if specified correctly
try:
    input1 = sys.argv[1]
    input2 = sys.argv[2]

# Quit and return error message if one or both input files are not specified
except IndexError:
    print('ERROR: Specify input files <input1>.bn (Bayesian Network) and <input2>.in (Query & Evidence).')
    input1 = ''
    input2 = ''
    quit()

# Quit and return error message if one or both input files are not found
except FileNotFoundError:
    print('ERROR: One or both specified files could not be found.')
    input1 = ''
    input2 = ''
    quit()

# Set verbose to True if optional -verbose argument is passed
try:
    if sys.argv[3]=='-verbose':
        verbose = True
    # If wrong third argument passed, set verbose to False
    else:
        verbose = False

# If no third argument passed, set verbose to False
except IndexError:
    verbose = False

# Read Bayesian Network and store in graph
graph = readBNFile(input1)

# Read query and evidence
query, evidence = readQueryFile(input2)

# If any error, quit
if graph == -1 or query == None or evidence == None:
    quit()

# Initialize set of factors
factors = []
for node in graph.nodes:
    factor = Factor()

    # Initial factors are simply the CPDs, hence only the node itself and its parents are involved
    factor.nodesInvolved.append(node.name)
    for parent in node.parents:
        factor.nodesInvolved.append(parent)

    factor.CPT = node.CPT

    # Add factor to set
    factors.append(factor)

# Get variables to eliminate
varsToEliminate = []
for node in graph.nodes:
    varsToEliminate.append(node.name)
varsToEliminate.remove(query)
for e in evidence:
    varsToEliminate.remove(e[0])

# Get number of neighbours in

query_dist, steps = VE(graph, factors, varsToEliminate, query, evidence, order=[])
evidence = [item for sublist in evidence for item in sublist]

output = [query, evidence, query_dist]
output = [' '.join(sublist) if not isinstance(sublist,str) else sublist for sublist in output]
output[0] = 'QUERY ' + output[0] + '\n'
output[1] = 'EVIDENCE ' + output[1] + '\n'
output[2] = 'QUERY_DIST ' + output[2] + '\n'
output.insert(0, '########## SOLUTION ##########\n')

if verbose:
    output.append('########## STEPS ##########\n')
    output += steps

outputFileName = input2.replace('.in','.sol')
writeOutput(outputFileName, output)
