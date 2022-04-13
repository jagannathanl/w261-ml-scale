#!/usr/bin/env python
"""
Reducer to calculate precision and recall as part
of the inference phase of Naive Bayes.
INPUT:
    ID \t true_class \t P(ham|doc) \t P(spam|doc) \t predicted_class
OUTPUT:
    precision \t ##
    recall \t ##
    accuracy \t ##
    F-score \t ##
         
Instructions:
    Complete the missing code to compute these^ four
    evaluation measures for our classification task.
    
    Note: if you have no True Positives you will not 
    be able to compute the F1 score (and maybe not 
    precision/recall). Your code should handle this 
    case appropriately feel free to interpret the 
    "output format" above as a rough suggestion. It
    may be helpful to also print the counts for true
    positives, false positives, etc.
"""
import sys

# initialize counters
FP = 0.0 # false positives
FN = 0.0 # false negatives
TP = 0.0 # true positives
TN = 0.0 # true negatives
NDOCS = 0

# read from STDIN
for line in sys.stdin:
    # parse input
    docID, class_, pHam, pSpam, pred = line.split()
    # emit classification results first
    print(line[:-2], class_ == pred)
    
    # then compute evaluation stats
#################### YOUR CODE HERE ###################
    NDOCS = NDOCS + 1
    if class_ == pred:
        if class_ == '1':
            TP = TP + 1
        else:
            TN = TN + 1
    else:
        if pred == '1':
            FP = FP + 1
        else:
            FN = FN + 1

precision = TP/float(TP+FP) if (TP+FP) != 0.0 else 'n/a'    
recall = TP/float(TP+FN) if (TP+FN) != 0.0 else 'n/a'
accuracy = (TP+TN)/float(TP+FP+TN+FN) if (TP+FP+TN+FN) != 0.0 else 'n/a'
f_score = 2*precision*recall/(precision+recall) if (precision != 'n/a' and recall != 'n/a') != 0.0 else 'n/a'
print(f'# Documenents:\t{NDOCS}')
print(f'True Positives\t{TP}')
print(f'True Negatives:\t{TN}')
print(f'False Positives\t{FP}')
print(f'False Negatives\t{FN}')
print(f'Accuracy\t{accuracy:.4f}')
print(f'Precision\t{precision:.4f}')
print(f'Recall\t{recall:.4f}')
print(f'F_score\t{f_score:.4f}')
#################### (END) YOUR CODE ###################
    