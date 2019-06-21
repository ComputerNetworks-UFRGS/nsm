#!/usr/bin/python

import numpy
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
	
	# First, let's create the historical lists for each class
	historical_sum_list_VL = list()
	#historical_sum_list_LO = list()
	#historical_sum_list_ME = list()
	#historical_sum_list_HI = list()
	#historical_sum_list_VH = list()
	
	########## **** Just testing *** #############
	historical_sum_list_VL.append(2.0794415416798357)
	##############################################
	
	# First, let's define the resource usage classes:
	# - Offline (OF)(0)
	# - Very Low (VL) [1 - 20]
	# - Low (LO) [21 - 40]
	# - Medium (ME) [41 - 60]
	# - High (HI) [61 - 80]
	# - Very High (VH) [80 - 95]
	# - Danger (DG) [> 95]

	# The following blocks are just examples of filled classes
	# These lists will be filled with current measurements obtained
	#	throught resource monitoring
	#cpu_OF = ['x', 'y', 'z']
	cpu_VL = ['a', 'b']
	#cpu_LO = ['b', 'c']
	#cpu_ME = ['d', 'e', 'f', 'g', 'h']
	#cpu_HI = ['i', 'j' 'k']
	#cpu_VH = ['l']
	#cpu_DG = []
	
	#str_OF = ['x', 'y', 'z']
	str_VL = ['a', 'b']
	#str_LO = ['b', 'c']
	#str_ME = ['d', 'e', 'f', 'g', 'h']
	#str_HI = ['i', 'j' 'k']
	#str_VH = ['l']
	#str_DG = []
	
	#net_OF = ['x', 'y', 'z']
	net_VL = ['a', 'b']
	#net_LO = ['b', 'c']
	#net_ME = ['d', 'e', 'f', 'g', 'h']
	#net_HI = ['i', 'j' 'k']
	#net_VH = ['l']
	#net_DG = []
	
	# Creating current entropy lists for CPU, STR and NET
	# Indexes: CPU, STR, NET
	all_VL = [eta(cpu_VL), eta(str_VL), eta(net_VL)]
	#all_LO = [eta(cpu_LO), eta(str_LO), eta(net_LO)]
	#all_ME = [eta(cpu_ME), eta(str_ME), eta(net_ME)]
	#all_HI = [eta(cpu_HI), eta(str_HI), eta(net_HI)]
	#all_VH = [eta(cpu_VH), eta(str_VH), eta(net_VH)]
	
	print '___'
	
	# Now we sum the results to create an unified descriptor	
	current_sum_VL = numpy.sum(all_VL)
	#current_sum_LO = numpy.sum(all_LO)
	#current_sum_ME = numpy.sum(all_ME)
	#current_sum_HI = numpy.sum(all_HI)
	#current_sum_VH = numpy.sum(all_VH)
	
	# Now we verify if the current value is out of the norm, ie
	#	greater or lower than mean +- std_dev
	
	#For loop inserted for testing
	for i in range (1,4):
		if (round(current_sum_VL, 5) > round(numpy.mean(historical_sum_list_VL) + numpy.std(historical_sum_list_VL), 5)) or (round(current_sum_VL, 5) < round(numpy.mean(historical_sum_list_VL) - numpy.std(historical_sum_list_VL), 5)):
			print 'VL Anomaly'
			break
		else:
			# If not anomalous, we push the current sum in the historic list
			historical_sum_list_VL.append(current_sum_VL)
			#historical_sum_list_LO.append(current_sum_LO)
			#historical_sum_list_ME.append(current_sum_ME)
			#historical_sum_list_HI.append(current_sum_HI)
			#historical_sum_list_VH.append(current_sum_VH)
			print historical_sum_list_VL
	
	# Statistic operations test
	#A_rank = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
	# Statistic operations
	#print 'Sum: %f' % numpy.sum(A_rank)			# sum
	#print 'Mean: %f' % numpy.mean(A_rank)		# mean
	#print 'Pop Std dev: %f' % numpy.std(A_rank)	# population std dev
	
	# Subtracting a list from another (considering repetitions)
	#print list((Counter(A)-Counter(B)).elements())
