#!/usr/bin/python

import time
import numpy
import math
from collections import Counter

cpu_members_OF = list()
cpu_members_VL = list()
cpu_members_LO = list()
cpu_members_ME = list()
cpu_members_HI = list()
cpu_members_VH = list()
cpu_members_DG = list()

str_members_OF = list()
str_members_VL = list()
str_members_LO = list()
str_members_ME = list()
str_members_HI = list()
str_members_VH = list()
str_members_DG = list()

net_members_OF = list()
net_members_VL = list()
net_members_LO = list()
net_members_ME = list()
net_members_HI = list()
net_members_VH = list()
net_members_DG = list()

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
			entropies_to_add[i] = numpy.mean(column(historical_entropies,i))
		else:
			# If not anomalous
			print 'Ok'
			entropies_to_add[i] = current_entropies[i]

	################### HISTORIC: ENTROPIES ########################
	# Every execution is updating the historical knowledge.
	# This approach should be discussed.
	historical_entropies.append(entropies_to_add)

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
    # CPU
    if values[0] == 0:
        cpu_members_OF.append(ip)
    elif values[0] < 21:
        cpu_members_VL.append(ip)
    elif values[0] < 41:
        cpu_members_LO.append(ip)
    elif values[0] < 61:
        cpu_members_ME.append(ip)
    elif values[0] < 81:
        cpu_members_HI.append(ip)
    elif values[0] < 95:
        cpu_members_VH.append(ip)
    else:
        cpu_members_DG.append(ip)

	# STR
    if values[1] == 0:
        str_members_OF.append(ip)
    elif values[1] < 21:
        str_members_VL.append(ip)
    elif values[1] < 41:
        str_members_LO.append(ip)
    elif values[1] < 61:
        str_members_ME.append(ip)
    elif values[1] < 81:
        str_members_HI.append(ip)
    elif values[1] < 95:
        str_members_VH.append(ip)
    else:
        str_members_DG.append(ip)

	# NET
    if values[2] == 0:
        net_members_OF.append(ip)
    elif values[2] < 21:
        net_members_VL.append(ip)
    elif values[2] < 41:
        net_members_LO.append(ip)
    elif values[2] < 61:
        net_members_ME.append(ip)
    elif values[2] < 81:
        net_members_HI.append(ip)
    elif values[2] < 95:
        net_members_VH.append(ip)
    else:
        net_members_DG.append(ip)

if __name__ == "__main__":
	# Execution Loop - Inserted for testing
	for rep in range(0,1):

		# MONITORING INTERVAL
		#time.sleep(5)
	
		# First, let's create the historical lists for each class
		historical_entropies_OF = list()
		historical_entropies_VL = list()
		historical_entropies_LO = list()
		historical_entropies_ME = list()
		historical_entropies_HI = list()
		historical_entropies_VH = list()
		historical_entropies_DG = list()
		
		# We also must define the lists of each class
		current_members_OF = list()
		current_members_VL = list()
		current_members_LO = list()
		current_members_ME = list()
		current_members_HI = list()
		current_members_VH = list()
		current_members_DG = list()
	
		# Finally, we define the current entropies list
		current_entropies_OF = list()
		current_entropies_VL = list()
		current_entropies_LO = list()
		current_entropies_ME = list()
		current_entropies_HI = list()
		current_entropies_VH = list()
		current_entropies_DG = list()

		############################# MONITOR ###########################
		monitored_data = open('monitored_data.txt').read().splitlines()
		# For each IP address
		for i in range(len(monitored_data)):
			monitored_data[i] = map(str, monitored_data[i].split(','))
			current_ip = monitored_data[i].pop(0)
			# Monitored data has now only the values of the ip 'i'
			# Let's convert the values into floats
			monitored_data[i] = map(float, monitored_data[i])
		############################ CLASSIFFIER #########################
			classifier(current_ip, monitored_data[i])

		# Composing the classes
		# OF
		current_members_OF.append(cpu_members_OF)
		current_members_OF.append(str_members_OF)
		current_members_OF.append(net_members_OF)
		
		# VL
		current_members_VL.append(cpu_members_VL)
		current_members_VL.append(str_members_VL)
		current_members_VL.append(net_members_VL)

		# LO
		current_members_LO.append(cpu_members_LO)
		current_members_LO.append(str_members_LO)
		current_members_LO.append(net_members_LO)
		
		# ME
		current_members_ME.append(cpu_members_ME)
		current_members_ME.append(str_members_ME)
		current_members_ME.append(net_members_ME)

		# HI
		current_members_HI.append(cpu_members_HI)
		current_members_HI.append(str_members_HI)
		current_members_HI.append(net_members_HI)
		
		# VH
		current_members_VH.append(cpu_members_VH)
		current_members_VH.append(str_members_VH)
		current_members_VH.append(net_members_VH)

		# DG
		current_members_DG.append(cpu_members_DG)
		current_members_DG.append(str_members_DG)
		current_members_DG.append(net_members_DG)

		# OLD - for testes using files
		############################ CLASSIFFIER #########################
		## The IPs are already classifyed in the .txt files, so the
		## monitor is reading the IPs belowing to their respective classes
		##************************* Just testing *************************
		#current_members_VL = getCurrentMembers('current_members_VL.txt')
		#current_members_LO = getCurrentMembers('current_members_LO.txt')
		#current_members_ME = getCurrentMembers('current_members_ME.txt')
		#current_members_HI = getCurrentMembers('current_members_HI.txt')
		#current_members_VH = getCurrentMembers('current_members_VH.txt')
		#print current_members_VL
		#****************************************************************
		#################################################################
	
		###################### HISTORIC: ENTROPIES ######################
		#************************* Just testing *************************
		historical_entropies_OF = readFloatFile('hist_entropy_OF.txt')
		historical_entropies_VL = readFloatFile('hist_entropy_VL.txt')
		historical_entropies_LO = readFloatFile('hist_entropy_LO.txt')
		historical_entropies_ME = readFloatFile('hist_entropy_ME.txt')
		historical_entropies_HI = readFloatFile('hist_entropy_HI.txt')
		historical_entropies_VH = readFloatFile('hist_entropy_VH.txt')
		historical_entropies_DG = readFloatFile('hist_entropy_DG.txt')
		#****************************************************************
		#################################################################
	
		##################### DETECTOR: CALCULATOR ######################
		# For each class we must perform the analysis
		
		######################### Offline (OF) #######################
		# Current entropies calculation for each resource (i)
		for i in range (len(current_members_OF)):
			current_entropies_OF.append(eta(current_members_OF[i]))

		######################### Very Low (VL) #######################
		# Current entropies calculation for each resource (i)
		for i in range (len(current_members_VL)):
			current_entropies_VL.append(eta(current_members_VL[i]))
		
		########################### Low (LO) ##########################
		# Current entropies calculation for each resource (i)
		for i in range (len(current_members_LO)):
			current_entropies_LO.append(eta(current_members_LO[i]))
		
		######################### Medium (ME) #########################
		# Current entropies calculation for each resource (i)
		for i in range (len(current_members_ME)):
			current_entropies_ME.append(eta(current_members_ME[i]))
		
		########################## High (HI) ##########################
		# Current entropies calculation for each resource (i)
		for i in range (len(current_members_HI)):
			current_entropies_HI.append(eta(current_members_HI[i]))
		
		######################### Very High (VH) ######################
		# Current entropies calculation for each resource (i)
		for i in range (len(current_members_VH)):
			current_entropies_VH.append(eta(current_members_VH[i]))
		
		######################### Danger (DG) ######################
		# Current entropies calculation for each resource (i)
		for i in range (len(current_members_DG)):
			current_entropies_DG.append(eta(current_members_DG[i]))

		##################### DETECTOR: ANALYZER ######################
		print 'Analysis %i:' % rep
		anomalyDetection(current_entropies_OF, historical_entropies_OF)
		anomalyDetection(current_entropies_VL, historical_entropies_VL)
		anomalyDetection(current_entropies_LO, historical_entropies_LO)
		anomalyDetection(current_entropies_ME, historical_entropies_ME)
		anomalyDetection(current_entropies_HI, historical_entropies_HI)
		anomalyDetection(current_entropies_VH, historical_entropies_VH)
		anomalyDetection(current_entropies_DG, historical_entropies_DG)
