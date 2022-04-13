#!/usr/bin/env python

import os
import sys                                                  
import numpy as np  

#################### YOUR CODE HERE ###################
# confirm that we have access to the model file
assert 'NBmodel.txt' in os.listdir('.'), "ERROR: can't find NBmodel.txt"

# load the model into a dictionary for easy access
unique_words = set()
for record in open('NBmodel.txt', 'r').readlines():
    word = record.split('\t')[0]
    if word == 'ClassPriors':
        continue
    if word is not unique_words:
        unique_words.add(word)
        
        
    
c0_total = None
c1_total = None
c0_wordtotal = None
c1_wordtotal = None
uniquewc = len(unique_words)

current_word = None
ham_count = 0
spam_count = 0
ham_prob = 0.0
spam_prob = 0.0

for line in sys.stdin:
    # parse input
    pk, word, c0_n, c1_n = line.split('\t')
    c0_n = int(c0_n)
    c1_n = int(c1_n)
    if word == current_word:
        spam_count = spam_count + c1_n
        ham_count = ham_count + c0_n
    else:
        if word[0] == '*':
            if word == '*doccount':
                if c0_total == None:
                    c0_total = c0_n
                    c1_total = c1_n
                else:
                    c0_total = c0_total + c0_n
                    c1_total = c1_total + c1_n
            if word == '*wordcount':
                if c0_wordtotal == None:
                    c0_wordtotal = c0_n
                    c1_wordtotal = c1_n
                else:
                    c0_wordtotal = c0_wordtotal + c0_n
                    c1_wordtotal = c1_wordtotal + c1_n                     
        elif current_word == None:
            current_word, ham_count, spam_count  = word, c0_n, c1_n
        else:
            ham_prob = (ham_count+1)/(float(c0_wordtotal)+float(uniquewc))
            spam_prob = (spam_count+1)/(float(c1_wordtotal)+float(uniquewc))
            #print(f'{current_word}\t{ham_count}\t{spam_count}\t{ham_prob}\t{spam_prob}')
            print(f'{current_word}\t{ham_count},{spam_count},{ham_prob},{spam_prob}')
            current_word, ham_count, spam_count  = word, c0_n, c1_n
            
if c0_wordtotal != None and c1_wordtotal != None:
    ham_prob = (ham_count+1)/(float(c0_wordtotal)+float(uniquewc))
    spam_prob = (spam_count+1)/(float(c1_wordtotal)+float(uniquewc))        
    #print(f'{current_word}\t{ham_count}\t{spam_count}\t{ham_prob}\t{spam_prob}')
    #print(f'{"ClassPriors"}\t{c0_total}\t{c1_total}\t{c0_total/(c0_total+c1_total)}\t{c1_total/(c0_total+c1_total)}')
    print(f'{current_word}\t{ham_count},{spam_count},{ham_prob},{spam_prob}')
    print(f'{"ClassPriors"}\t{c0_total},{c1_total},{c0_total/(c0_total+c1_total)},{c1_total/(c0_total+c1_total)}')
#################### (END) YOUR CODE ###################