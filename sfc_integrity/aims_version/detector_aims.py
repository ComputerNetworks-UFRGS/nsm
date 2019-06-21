#!/usr/bin/python

import time
import numpy
import math
from collections import Counter

from deepdiff import DeepDiff

import datetime
from datetime import datetime

import copy

# Policy parameters
policy_params = ['ar', 'id', 'customer_id', 'customer_bw', 'ip_src-dst', 'vnffg']
# Customer parameters
customer_params = ['id', 'vnffgs']
# VNFFG/SFC parameters
vnffg_params = ['id', 'customer_id', 'cusotmer_bw', 'ip_src-dst', 'vnfs']

# General dictionary of parameters
general_paramenters = dict()

general_paramenters['policy'] = policy_params
general_paramenters['customer'] = customer_params
general_paramenters['vnffg'] = vnffg_params

# Entropy version 2 = small code
def entropyv2(s):
	p, lns = Counter(s), float(len(s))
	return -sum( count/lns * math.log(count/lns, 2) for count in p.values())

# GENERIC Request data from NFVO
#	info_type: "cataloged" or "monitored"
#	element: "policy", "customer", or "vnffg" 
# Return: list with the values of each element parameter
def NFVORequestData(info_type, element):
	data_list = list()

	with open(info_type + "_" + element + "_list.txt") as f:

		for line in f:
			read_values = line.split()
			param_index = 1
			param_dict = dict()

			for param in general_paramenters[element]:
				param_dict[param] = read_values[param_index]
				param_index = param_index + 1

			# The code bellow was inserted to work with the new data set.
			# After the 6th element, SFCs may present different sizes.
			# So this part is to read SFCs with different sizes in each
			# line of the data set.
			param_index_2 = param_index
			while len(read_values) > param_index_2:
				param_dict[param] = param_dict[param] + read_values[param_index_2]
				param_index_2 = param_index_2 + 1

			data_list.append(param_dict)

	return data_list

# GENERIC Calculate entropies
# Parameters:
#	info_type: "cataloged" or "monitored"
#	element: "policy", "customer", or "vnffg" 
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
		entropies[param] = entropyv2(complete_lists[param])

	return entropies

if __name__ == "__main__":

###################### OLD VERSION ###########################
# Acquires all information and calculates separated entropies
# It is not good to detect small changes in each information.
##############################################################

#	requested_data = NFVORequestData("cataloged", "policy")
#	requested_data = NFVORequestData("monitored", "policy")
	#print str(requested_data)

	#cataloged_ent = Entropies('cataloged', 'policy')
	#monitored_ent = Entropies('monitored', 'policy')

#	print cataloged_ent
#	print monitored_ent

	#if cataloged_ent != monitored_ent:
	#	print "Anomaly!"

###################### NEW VERSION ###########################
# Merges both cataloged and monitored information and compares
# the entropy of ther merged info with the entropy of cataloged
# info. Better results in detecting small changes.
# This version does not use all acquired information, but
# customers VNFFGs.
##############################################################

	cataloged_data = NFVORequestData("cataloged", "policy")
	monitored_data = NFVORequestData("monitored", "policy")
	
	# Creating a dictionary of customers, each one with a list
	# of SFCs.
	cataloged_customers_vnffgs = dict()
	monitored_customers_vnffgs = dict()

	for row in cataloged_data:
			if row['customer_id'] not in cataloged_customers_vnffgs:
				cataloged_customers_vnffgs[row['customer_id']] = list()
			cataloged_customers_vnffgs[row['customer_id']].append(row['vnffg'])

	# Deepcopy creates a perfect copy of the dictionary
	merged_customers_vnffgs = copy.deepcopy(cataloged_customers_vnffgs)

	for row in monitored_data:
			if row['customer_id'] not in cataloged_customers_vnffgs:
				print "ERROR: Missing customer! " + row['customer_id']
			if row['customer_id'] not in monitored_customers_vnffgs:
				monitored_customers_vnffgs[row['customer_id']] = list()
			merged_customers_vnffgs[row['customer_id']].append(row['vnffg'])
			monitored_customers_vnffgs[row['customer_id']].append(row['vnffg'])

	merged_entropies = dict()
	cataloged_entropies = dict()

	for customer in cataloged_customers_vnffgs:
		merged_entropies[customer] = entropyv2(merged_customers_vnffgs[customer])
		cataloged_entropies[customer] = entropyv2(cataloged_customers_vnffgs[customer])

		# Detector
		if (cataloged_entropies[customer] != merged_entropies[customer]):
			print "ANOMALY! " + customer
			# Filtering
			print str(DeepDiff(cataloged_customers_vnffgs[customer], monitored_customers_vnffgs[customer]))

	print cataloged_entropies
	print merged_entropies


###################### VERSION 3 ###########################
# All VNFFGs (not differing Customers!
# Not 100% correct yet!!!!
##############################################################


#	cataloged_data = NFVORequestData("cataloged", "policy")
#	monitored_data = NFVORequestData("monitored", "policy")
#	
#	# Creating a list of SFCs.
#	cataloged_vnffgs = list()
#	monitored_vnffgs = list()
#
#	for row in cataloged_data:
#		cataloged_vnffgs.append(row['vnffg'])
#
#	# Deepcopy creates a perfect copy of the dictionary
#	merged_vnffgs = copy.deepcopy(cataloged_vnffgs)
#
#	for row in monitored_data:
#		merged_vnffgs.append(row['vnffg'])
#		monitored_vnffgs.append(row['vnffg'])
#
#	merged_entropies = dict()
#	cataloged_entropies = dict()
#
#	merged_entropy = entropyv2(merged_vnffgs)
#	cataloged_entropy = entropyv2(cataloged_vnffgs)
#
#	# Detector
#	print cataloged_entropy
#	print merged_entropy
#
#	if (cataloged_entropy != merged_entropy):
#		print "ANOMALY! "
#		# Filtering
#		print str(DeepDiff(cataloged_vnffgs, monitored_vnffgs))
#
