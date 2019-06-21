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

	# Numbre of times the program will execute
	interactions = 0

	# Number of times the monitored data will be used to compose
	# the historical entropies dictionary
	training_loop = 3

	###################### AIMS VERSION #############################
	# Merges both cataloged and monitored information and compares	#
	# the entropy of ther merged info with the entropy of cataloged	#
	# info. Better results in detecting small changes.				#
	# This version does not use all acquired information, but		#
	# customers VNFFGs.												#
	#################################################################

	cataloged_data = NFVORequestData("cataloged", "policy")
	
	# Creating a dictionary of customers, each one with a list
	# of bws.
	cataloged_customers_bw = dict()
	monitored_customers_bw = dict()

	for row in cataloged_data:
		if row['customer_id'] not in cataloged_customers_bw:
			cataloged_customers_bw[row['customer_id']] = list()
		cataloged_customers_bw[row['customer_id']].append(row['customer_bw'])

	# Creating dictionaries for the current entropies
	cataloged_entropies = dict()
	monitored_entropies = dict()

	# Dictionary for historical entropies.
	# The first entropies added to this dictionary should be measuread in
	# normal condictions, ie, withou anomalies, since they will be used
	# as baseline to the upcoming detections.
	historic_entropies = dict()

	# Entropies are calculated per customer
	# This loop is to load the historic entropies.
	# During the "historic learning" phase, the historic entropies are composed by
	# cataloged entripies and 'n' monitored entropies.
	# Such monitored entropies should be guaranteed normal ones!
	for customer in cataloged_customers_bw:
		cataloged_entropies[customer] = entropyv2(cataloged_customers_bw[customer])
		historic_entropies[customer] = list()
		historic_entropies[customer].append(entropyv2(cataloged_customers_bw[customer]))

	for training in range (0, training_loop):

		training_customers_bw = dict()

		print "Training phase"
		# Calculate n monitored entropies and add to the historic
		# Assuming that during training there are no anomalies,
		# there is no verification being conducted here.
		
		# Retrieve monitored data
		training_data = NFVORequestData("training_" + str(training) , "policy")

		for row in training_data:
			# Is the customer present in the cataloged information?
			if row['customer_id'] not in cataloged_customers_bw:
				print "ERROR: Missing customer! " + row['customer_id']
			if row['customer_id'] not in training_customers_bw:
				training_customers_bw[row['customer_id']] = list()
			# Add info to the monitored dictionary
			training_customers_bw[row['customer_id']].append(row['customer_bw'])
	
		for customer in cataloged_customers_bw:
			historic_entropies[customer].append(entropyv2(training_customers_bw[customer]))

	while interactions < 1:

		# Retrieve monitored data
		monitored_data = NFVORequestData("monitored", "policy")

		for row in monitored_data:
			# Is the customer present in the cataloged information?
			if row['customer_id'] not in cataloged_customers_bw:
				print "ERROR: Missing customer! " + row['customer_id']
			if row['customer_id'] not in monitored_customers_bw:
				monitored_customers_bw[row['customer_id']] = list()
			# Add info to the monitored dictionary
			monitored_customers_bw[row['customer_id']].append(row['customer_bw'])
	
		# Bandwidth detection: entropy should be between [mean - std; mean + std]
		for customer in cataloged_customers_bw:
			monitored_entropies[customer] = entropyv2(monitored_customers_bw[customer])
			# Detector
			if (round(monitored_entropies[customer]) > round(numpy.mean(historic_entropies[customer])) + round(numpy.std(historic_entropies[customer]))) or \
			(round(monitored_entropies[customer]) < round(numpy.mean(historic_entropies[customer])) - round(numpy.std(historic_entropies[customer]))):
				print "ANOMALY! " + customer
				print "monitored entropy " + str(round(monitored_entropies[customer]))
				print "mean " + str(round(numpy.mean(historic_entropies[customer])))
				print "std " + str(round(numpy.std(historic_entropies[customer])))

				# Filtering
				# BW filtering compares monitored and cataloged info. In this way,
				# it may show many differences that are not the anomaly.
				# ie, even small changes will be highligthed
				print str(DeepDiff(cataloged_customers_bw[customer], monitored_customers_bw[customer]))
			else:
				# Append the new value on the historic
				historic_entropies[customer].append(monitored_entropies[customer])
	
		print cataloged_entropies
		print monitored_entropies

		interactions = interactions + 1

