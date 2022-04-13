#!/usr/bin/env python
"""
Mapper reads in text documents and emits word counts by class.
INPUT:                                                    
    DocID \t true_class \t subject \t body                
OUTPUT:                                                   
    partitionKey \t word \t class0_partialCount,class1_partialCount       
    

Instructions:
    You know what this script should do, go for it!
    (As a favor to the graders, please comment your code clearly!)
    
    A few reminders:
    1) To make sure your results match ours please be sure
       to use the same tokenizing that we have provided in
       all the other jobs:
         words = re.findall(r'[a-z]+', text-to-tokenize.lower())
         
    2) Don't forget to handle the various "totals" that you need
       for your conditional probabilities and class priors.
       
Partitioning:
    In order to send the totals to each reducer, we need to implement
    a custom partitioning strategy.
    
    We will generate a list of keys based on the number of reduce tasks 
    that we read in from the environment configuration of our job.
    
    We'll prepend the partition key by hashing the word and selecting the
    appropriate key from our list. This will end up partitioning our data
    as if we'd used the word as the partition key - that's how it worked
    for the single reducer implementation. This is not necessarily "good",
    as our data could be very skewed. However, in practice, for this
    exercise it works well. The next step would be to generate a file of
    partition split points based on the distribution as we've seen in 
    previous exercises.
    
    Now that we have a list of partition keys, we can send the totals to 
    each reducer by prepending each of the keys to each total.
       
"""

import re                                                   
import sys                                                  
import numpy as np      

from operator import itemgetter
import os

#################### YOUR CODE HERE ###################

class1_doc_count, class0_doc_count = 0, 0
class1_word_count, class0_word_count = 0, 0

def inverse_hash1(c):
    c = c.lower()
    if ord(c)<ord('i'):
        return 0
    elif ord(c)<ord('o'):
        return 1
    else:
        return 2
    
if os.getenv('mapreduce_job_reduces') == None:
    N = 3
else:
    N = int(os.getenv('mapreduce_job_reduces'))
    

alpha = 'abcdefghijklmnopqrstuvwxyz'
n = int(len(alpha)/N)
parts = [alpha[i*n-1] for i in range(1, N+1)]

def inverse_hash(c):
    c = c.lower()
    m = len(parts)
    for i in range(0, m):
        if ord(c)<=ord(parts[i]):
            return i
    return m-1
    
def makeIndex(key, num_reducers = N):
    """
    Mimic the Hadoop string-hash function.
    
    key             the key that will be used for partitioning
    num_reducers    the number of reducers that will be configured
    """
    byteof = lambda char: int(format(ord(char), 'b'), 2)
    current_hash = 0
    for c in key:
        current_hash = (current_hash * 31 + byteof(c))
    return current_hash % num_reducers

def makeKeyFile(num_reducers = N):
    KEYS = list(map(chr, range(ord('A'), ord('Z')+1)))[:num_reducers]
    partition_keys = sorted(KEYS, key=lambda k: makeIndex(k,num_reducers))

    return partition_keys


# call your helper function to get partition keys
pKeys = makeKeyFile()

for line in sys.stdin:
    # parse input and tokenize
    docID, _class, subject, body = line.lower().split('\t')
    words = re.findall(r'[a-z]+', subject + ' ' + body)
    
    if _class == '1':
        class1_doc_count = class1_doc_count + 1
    else:
        class0_doc_count = class0_doc_count + 1

    for w in words:
        if _class == '1':
            print(str(inverse_hash(w[:1]))+'\t'+w+'\t'+'0'+'\t'+'1')
            class1_word_count = class1_word_count + 1
        else:
            print(str(inverse_hash(w[:1]))+'\t'+w+'\t'+'1'+'\t'+'0')
            class0_word_count = class0_word_count + 1
            
for i in range(N):
    print(str(i)+'\t'+'*doccount'+'\t'+str(class0_doc_count)+'\t'+str(class1_doc_count))
    print(str(i)+'\t'+'*wordcount'+'\t'+str(class0_word_count)+'\t'+str(class1_word_count))
#################### (END) YOUR CODE ###################