#!/usr/bin/env python
"""
This script reads word counts from STDIN and aggregates
the counts for any duplicated words.

INPUT & OUTPUT FORMAT:
    word \t count
USAGE (standalone):
    python aggregateCounts_v2.py < yourCountsFile.txt

Instructions:
    For Q7 - Your solution should not use a dictionary or store anything   
             other than a single total count - just print them as soon as  
             you've added them. HINT: you've modified the framework script 
             to ensure that the input is alphabetized; how can you 
             use that to your advantage?
"""

# imports
import sys


################# YOUR CODE HERE #################

current_key = None
current_val = None

for line in sys.stdin:
    # extract words & counts
    word, count  = line.split()

    if current_key == word:
        current_value = current_value + int(count)
    else:
        if current_key != None:
            print("{}\t{}".format(current_key, current_value))
        current_key = word
        current_value = int(count)
            
if current_key != None:
    print("{}\t{}".format(current_key, current_value))






################ (END) YOUR CODE #################
