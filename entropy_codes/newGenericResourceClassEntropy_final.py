#!/usr/bin/python

import time
import numpy
import math
from collections import Counter

# Dictionary of member of each class of each resource
resource_classes_members = dict()
# Dictionary of each class of each resource
resource_classes = dict()

# Classes list
classes_list = ['OF', 'VL', 'LO', 'ME', 'HI', 'VH', 'DG']
# Resources list
resources_list = ['cpu', 'str', 'net']

# Creation of the dictionary of dictionaries of lists
for resource_name in resources_list:
    resource_classes_members[resource_name] = dict()
    for class_name in classes_list:
        resource_classes_members[resource_name][class_name] = list()

# Entropy calculation - Using simple python list (no panda)
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

# Function to extract a column from a multidimensional list
def column(matrix, i):
	return [row[i] for row in matrix]

# Functions for detecting anomaly - ANALYZER MODULE
def anomalyDetection(current_entropies, historical_entropies):
	# First, we create an auxiliary list for updating the historical values
	# with the same size of the current entropies
	entropies_to_add = list(range(len(current_entropies)))

	# Visit all entropies (each resource)
	for i in range(len(current_entropies)):
		# Now we verify if the current value is out of the norm, ie
		# greater/lower than mean +/- std_dev
		hist_entropy_mean = round(numpy.mean(column(historical_entropies,i)),6)
		hist_entropy_std_dev = round(numpy.std(column(historical_entropies,i)),6)
		if (round(current_entropies[i],6) > hist_entropy_mean + hist_entropy_std_dev) or \
			(round(current_entropies[i],6) < hist_entropy_mean - hist_entropy_std_dev):
			################################ ALERT #############################
			print 'ANOMALY - Resource index = %d, Value: %f' % (i, current_entropies[i])
			# The current anomalous entropy must not be inserted in
			# the historical knowledge, so we add the historial mean
			# instead, guaranteeing not interfering in the knowledge
			###################################################################
			entropies_to_add[i] = hist_entropy_mean
		else:
			# If not anomalous
			print 'Ok'
			entropies_to_add[i] = current_entropies[i]

	################### HISTORIC: ENTROPIES ########################
	# Every execution is updating the historical knowledge.
	# This approach should be discussed.
	historical_entropies.append(entropies_to_add)
	################################################################
# Function for reading float values from a file, composing a list
def readFloatFile(file_name):
	my_list = open(file_name).read().splitlines()

	# Convert each element in the lists of the list into float
	for i in range(len(my_list)):
		my_list[i] = map(float, my_list[i].split(','))

	return my_list

# Function to get the current members of each class.
# This version assumes the members are placed in a file.
def getCurrentMembers(file_name):
	current_members = open(file_name).read().splitlines()
	# For each members list read
	for i in range (len(current_members)):
		# Separetes each element in a single string
		current_members[i] = current_members[i].split(",")
	return current_members

############################ CLASSIFFIER #########################
# Values in the if statements represent the boudaries of each class
def classifier(ip, values):

	i = 0
	for resource_name in resources_list:
		if values[i] == 0:
			resource_classes_members[resource_name]['OF'].append(ip)
		elif values[i] < 21:
			resource_classes_members[resource_name]['VL'].append(ip)
		elif values[i] < 41:
			resource_classes_members[resource_name]['LO'].append(ip)
		elif values[i] < 61:
			resource_classes_members[resource_name]['ME'].append(ip)
		elif values[i] < 81:
			resource_classes_members[resource_name]['HI'].append(ip)
		elif values[i] < 95:
			resource_classes_members[resource_name]['VH'].append(ip)
		else:
			resource_classes_members[resource_name]['DG'].append(ip)
		i = i + 1
#################################################################

if __name__ == "__main__":
	# Execution Loop - Inserted for testing
	for rep in range(0,1):

		# MONITORING INTERVAL
		#time.sleep(5)
	
		# First, let's create the historical lists for each class
		historical_entropies = dict()
		for class_name in classes_list:
			historical_entropies[class_name] = list()
		
		# We also must define the lists of each class
		current_members = dict()
		for class_name in classes_list:
			current_members[class_name] = list()
	
		# Finally, we define the current entropies list
		current_entropies = dict()
		for class_name in classes_list:
			current_entropies[class_name] = list()

		############################# MONITOR ###########################
		monitored_data = open('monitored_data.txt').read().splitlines()
		# For each IP address
		for i in range(len(monitored_data)):
			monitored_data[i] = map(str, monitored_data[i].split(','))
			current_ip = monitored_data[i].pop(0)
			# Monitored data has now only the values of the ip 'i'
			# Let's convert the values into floats
			monitored_data[i] = map(float, monitored_data[i])
			#################################################################
			############################ CLASSIFFIER ########################
			classifier(current_ip, monitored_data[i])

		# Composing the classes
		for class_name in classes_list:
			for resouce_name in resources_list:
				current_members[class_name].append(resource_classes_members[resource_name][class_name])
		#################################################################

		###################### HISTORIC: ENTROPIES ######################
		#************************* Just testing *************************
		for class_name in classes_list:
			historical_entropies[class_name] = readFloatFile('hist_entropy_{0}.txt'.format(class_name))
		#****************************************************************
		#################################################################
	
		##################### DETECTOR: CALCULATOR ######################
		# For each class we must perform the analysis
		for class_name in classes_list:
			for i in range (len(current_members[class_name])):
				current_entropies[class_name].append(eta(current_members[class_name][i]))
		#################################################################

		##################### DETECTOR: ANALYZER ########################
		print 'Analysis %i:' % rep
		for class_name in classes_list:
			anomalyDetection(current_entropies[class_name], historical_entropies[class_name])
		#################################################################
