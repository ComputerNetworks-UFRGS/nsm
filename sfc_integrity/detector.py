#!/usr/bin/python

import time
import numpy
import math
from collections import Counter

from deepdiff import DeepDiff

import datetime
from datetime import datetime

# VNFFG monitored parameters
vnffg_params = ['vnffg_id', 'connection_points', 'virtual_links', 'vnfs']
# VNF monitored parameters
vnf_params = ['vnf_id', 'connection_points', 'dependencies', 'virtual_links', 'localization', 'vdus']
# VDU monitored parameters
vdu_params = ['vm_id', 'computation_requirement', 'virtual_network_resource_element', 'virtual_network_bandwidth_resource']

# General dictionary of parameters
general_paramenters = dict()

general_paramenters['vnffg'] = vnffg_params
general_paramenters['vnf'] = vnf_params
general_paramenters['vdu'] = vdu_params

# Entropy calculation function
def eta(data, unit='natural'):
	base = {
		'shannon' : 2., # log base
		'natural' : math.exp(1),
		'hartley' : 10. # logarithmic unit which measures information or 
						# entropy - base 10 logarithms and powers of 10
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

# Entropy version alternative = under test (slower)!!!
def entropy(X):
	probs = [numpy.mean(X == c) for c in set(X)]
	return numpy.sum(-p * numpy.log2(p) for p in probs)

# Entropy version 2 = small code
def entropyv2(s):
    p, lns = Counter(s), float(len(s))
    return -sum( count/lns * math.log(count/lns, 2) for count in p.values())

# GENERIC Request data from NFVO
#	info_type: "cataloged" or "monitored"
#	element: "vnffg", "vnf" or "vdu"
# Return: list with the values of each element parameter
def NFVORequestData(info_type, element):
	data_list = list()

	with open(info_type + "_" + element + "_list.dat") as f:

		for line in f:
			read_values = line.split()
			param_index = 1
			param_dict = dict()

			for param in general_paramenters[element]:
				param_dict[param] = read_values[param_index]
				param_index = param_index + 1

			data_list.append(param_dict)

	return data_list

# GENERIC Calculate entropies
# Parameters:
#	info_type: "cataloged" or "monitored"
#	element: "vnffg", "vnf" or "vdu"
# Return: dictionary with element entropies
def Entropies(info_type, element):
	complete_lists = dict()
	entropies = dict()
	data_list = NFVORequestData(info_type,element)

	# Visiting each parameter
	for param in general_paramenters[element]:
		complete_list = list()
		# Visiting each element

		for index in range(0, len(data_list)):
			# Split values separated by comma
			complete_list = complete_list + data_list[index][param].split(",")

		complete_lists[param] = complete_list

	# Now, calculate the entropy of each parameter list
	for param in general_paramenters[element]:
		#entropies[param] = eta(complete_lists[param])
		#entropies[param] = entropy(complete_lists[param])
		entropies[param] = entropyv2(complete_lists[param])

	return entropies

# Send to the NFVO the results of the analysis
# Parameters: report_message = information to be send to NFVO
#				format depends on the format known by the NFVO
def reportNFVO(report_message):
	print report_message

	f = open('log_detector.dat','a')
	f.write(report_message) # python will convert \n to os.linesep
	f.close() # you can omit in most cases as the destructor will call it

# -- Main code --
if __name__ == "__main__":
    # Testing
	max_repetitions = 1 
	polling_interval = 0

	i = 0

	for repetitions in range(0,max_repetitions):
		report_message = str(datetime.now()) + '\n'
		report_message = report_message +  "_____VNFFG_____\n"
		
		i = i+1

		# Measuring the time expended by fucntions
		#start = time.time()

		if (Entropies("cataloged","vnffg") == Entropies("monitored","vnffg")):
			report_message = report_message + "No anomalies found in VNFFG view\n"
			#print str(Entropies("cataloged","vnffg")) + ";" + str(Entropies("monitored","vnffg"))
			# Calculating the elapsed time
			#elapsed = time.time() - start

		else:
			report_message = report_message + "Anomaly detetected!\n"
			# FILTER: Function DeepDiff(o,n) shows the difference betwwen 'o' and 'n', 
			# where o = original and n = new
			report_message = report_message + str(DeepDiff(NFVORequestData("cataloged", "vnffg"), \
															NFVORequestData("monitored", "vnffg")))\
															+ "\n"
			
			# Calculating the elapsed time
			#elapsed = time.time() - start

		report_message = report_message + "_____VNF_____\n"

		if (Entropies("cataloged","vnf") == Entropies("monitored","vnf")):
			report_message = report_message + "No anomalies found in VNF view\n"
			#print str(Entropies("cataloged","vnf")) + ";" + str(Entropies("monitored","vnf"))

		else:
			report_message = report_message + "Anomaly detetected!\n"
			# FILTER: Function DeepDiff(o,n) shows the difference betwwen 'o' and 'n',
			# where o = original and n = new
			report_message = report_message + str(DeepDiff(NFVORequestData("cataloged", "vnf"), \
															NFVORequestData("monitored", "vnf")))\
															+ "\n"

#		report_message = report_message + "_____VDU_____\n"
#
#		if (Entropies("cataloged","vdu") == Entropies("monitored","vdu")):
#			report_message = report_message + "No anomalies found in VDU view\n"
#
#		else:
#			report_message = report_message + "Anomaly detetected!\n"
#			# FILTER: Function DeepDiff(o,n) shows the difference betwwen 'o' and 'n',
#			# where o = original and n = new
#			report_message = report_message + str(DeepDiff(NFVORequestData("cataloged", "vdu"), \
#															NFVORequestData("monitored", "vdu")))\
#															+ "\n"
		# Calculating the elapsed time
#		elapsed = time.time() - start

#		print str(i) + ";" + str(elapsed)

		# IF clause to avoid waiting after the last loop
		if repetitions < max_repetitions -1:
			time.sleep(polling_interval)

		full_entropies = Entropies("monitored","vnffg")

		full_ent_values = full_entropies['virtual_links'] + full_entropies['connection_points'] + full_entropies['vnfs']

		print full_ent_values

#	reportNFVO(report_message)
