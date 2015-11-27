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


def readInputFiles(input1, input2):

    VARS = dict()

    with open(input1,'r') as input1:
        for line in input1:
            if not line=='\n':
                print(line.strip('\n'))

    return 1