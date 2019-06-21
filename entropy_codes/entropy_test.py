#!/usr/bin/python

import pandas as pd
import scipy.stats as scstats

import math
from collections import Counter

# 1 - Without panda
def eta(data, unit='natural'):
    base = {
        'shannon' : 2., # log base
        'natural' : math.exp(1),
        'hartley' : 10. # logarithmic unit which measures information or entropy, based on base 10 logarithms and powers of 10
    }

    if len(data) <= 1:
        return 0

    counts = Counter()

    for d in data:
        counts[d] += 1

    probs = [float(c) / len(data) for c in counts.values()]
    probs = [p for p in probs if p > 0.]

    ent = 0

    for p in probs:
        if p > 0.:
            ent -= p * math.log(p, base[unit])

    return ent

# 2 - Input a pandas series 
def ent(data):
	p_data= data.value_counts()/len(data) # calculates the probabilities
	entropy=scstats.entropy(p_data)  # input probabilities to get the entropy
	return entropy


if __name__ == "__main__":
	## Defining a panda series
	#print ent(pd.Series(['a', 'b', 'c']))
	#print ent(pd.Series(['a', 'b', 'd']))
	# Version 1 (only using math)
	A = ['a', 'b', 'm', 'b']
	B = ['a', 'b', 'm', 'a']
	print eta(A)
	print eta(B)
	
	#print list((Counter(A)-Counter(B)).elements())
