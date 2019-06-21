#!/usr/bin/python

import numpy
import math
from collections import Counter

# Entropy calculation - Using simple python list (no panda)
def eta(data, unit='natural'):
    base = {
        'shannon' : 2., # log base
        'natural' : math.exp(1),
        'hartley' : 10. # logarithmic unit which measures information or 
						# entropy, based on base 10 logarithms and powers of 10
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

# Function to extract a column from a multidimensional list
def column(matrix, i):
    return [row[i] for row in matrix]

if __name__ == "__main__":
	
	# First, let's create the historical lists for each class
	historical_entropies_VL = list()
	#historical_sum_list_LO = list()
	#historical_sum_list_ME = list()
	#historical_sum_list_HI = list()
	#historical_sum_list_VH = list()
	
	########## **** Just testing *** #############
	# Indexes:							CPU				STR			NET
	historical_entropies_VL.append([1.09861228867,0.69314718056,1.38629436112])
	historical_entropies_VL.append([1.09861228867,0.69314718056,1.38629436112])
	historical_entropies_VL.append([1.09861228867,0.69314718056,1.38629436112])
	##############################################
	
	# First, let's define the resource usage classes:
	# - Offline (OF)(0)
	# - Very Low (VL) [1 - 20]
	# - Low (LO) [21 - 40]
	# - Medium (ME) [41 - 60]
	# - High (HI) [61 - 80]
	# - Very High (VH) [80 - 95]
	# - Danger (DG) [> 95]

	# The following blocks are just examples of filled classes.
	# These lists will be filled with current measurements obtained
	# throught resource monitoring. A classification process will fill
	# the classes with the respective hosts.
	#cpu_OF = ['x', 'y', 'z']
	cpu_VL = ['a', 'b', 'c', 'd', 'e']		# eta = 1.60943791243
	#cpu_LO = ['b', 'c']
	#cpu_ME = ['d', 'e', 'f', 'g', 'h']
	#cpu_HI = ['i', 'j' 'k']
	#cpu_VH = ['l']
	#cpu_DG = []
	
	#str_OF = ['x', 'y', 'z']
	str_VL = ['a', 'b']						# eta = 0.69314718056
	#str_LO = ['b', 'c']
	#str_ME = ['d', 'e', 'f', 'g', 'h']
	#str_HI = ['i', 'j' 'k']
	#str_VH = ['l']
	#str_DG = []
	
	#net_OF = ['x', 'y', 'z']
	net_VL = ['a', 'b', 'c', 'd']			# eta = 1.38629436112
	#net_LO = ['b', 'c']
	#net_ME = ['d', 'e', 'f', 'g', 'h']
	#net_HI = ['i', 'j' 'k']
	#net_VH = ['l']
	#net_DG = []
			
	# Calculate the current entropies 	CPU		STR		NET
	current_entropies_VL = [eta(cpu_VL), eta(str_VL), eta(net_VL)]
	
	# Now we verify if the current value is out of the norm, ie
	#	greater or lower than mean +- std_dev
	
	#For loop inserted for testing
	for i in range (1,2):
		# Visit all entropies (each resource)
		
		for i in range(len(current_entropies_VL)):
			print current_entropies_VL[i]
			if (round(current_entropies_VL[i]) > round(numpy.mean(column(historical_entropies_VL,i)) + numpy.std(column(historical_entropies_VL,i)))) or \
				(round(current_entropies_VL[i]) < round(numpy.mean(column(historical_entropies_VL,i)) - numpy.std(column(historical_entropies_VL,i)))):
				print 'VL anomaly: Index %d, Value: %f' % (i, current_entropies_VL[i])
				# The current anomalous entropy must not be inserted in
				# the historical knowledge, so we add the historial mean
				# instead, guaranteeing not interfering in the knowledge
				current_entropies_VL[i] = numpy.mean(column(historical_entropies_VL,i))
			else:
				# If not anomalous, we push the current sum in the historic list
				print 'Ok'
				historical_entropies_VL.append(current_entropies_VL)
	print historical_entropies_VL
