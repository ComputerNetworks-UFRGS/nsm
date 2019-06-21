#!/usr/bin/python

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

if __name__ == "__main__":
	A = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
	B = ['2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
	print eta(A)
	print eta(B)
        print eta(A) - eta(B)
