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


graph = readInputFiles(input1, input2)

for node in graph.nodes:
    print(node)

print(graph.getPrVal('A', ['f', 'f', 't']))

print(graph.getFactors('A')[2])