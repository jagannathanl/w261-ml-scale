#!/usr/bin/env python
"""
Reducer aggregates word counts by class and emits frequencies.
INPUT:                                                    
    partitionKey \t word \t class0_partialCount \t class1_partialCount                
OUTPUT:
    word \t class0_count \t class1_count \t class0_conditional_prob \t class1_conditional_prob 
    
    
Instructions:
    Again, you are free to design a solution however you see 
    fit as long as your final model meets our required format
    for the inference job we designed in Question 8. Please
    comment your code clearly and concisely.
    
    A few reminders: 
    1) Don't forget to emit Class Priors (with the right key).
    2) In python2: 3/4 = 0 and 3/float(4) = 0.75
"""
import sys
##################### YOUR CODE HERE ####################
c0_total = None
c1_total = None
c0_wordtotal = None
c1_wordtotal = None

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
            ham_prob = ham_count/float(c0_wordtotal)
            spam_prob = spam_count/float(c1_wordtotal)
            print(f'{current_word}\t{ham_count}\t{spam_count}\t{ham_prob}\t{spam_prob}')
            current_word, ham_count, spam_count  = word, c0_n, c1_n
            
if c0_wordtotal != None and c1_wordtotal != None:
    ham_prob = ham_count/float(c0_wordtotal)
    spam_prob = spam_count/float(c1_wordtotal)        
    print(f'{current_word}\t{ham_count}\t{spam_count}\t{ham_prob}\t{spam_prob}')
    print(f'{"ClassPriors"}\t{c0_total}\t{c1_total}\t{c0_total/(c0_total+c1_total)}\t{c1_total/(c0_total+c1_total)}')

##################### (END) CODE HERE ####################