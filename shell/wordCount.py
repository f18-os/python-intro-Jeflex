# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 21:34:27 2018

@author: Phillip
"""

import sys
import string

inFile = sys.argv[1]
outFile = sys.argv[2]

dictionary = {}

with open(inFile) as file:
    for line in file:
        line = line.split()
        for word in line:
            word = "".join(l for l in word if l not in string.punctuation)
            if word:
                if word in dictionary:
                    dictionary[word] += 1
                else:
                    dictionary[word] = 1

with open(outFile, 'w') as out:
    for word in sorted(dictionary):
        out.write(word+' '+str(dictionary[word]))
        out.write('\n')