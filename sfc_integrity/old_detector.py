#!/usr/bin/python

import time
import numpy
import math
from collections import Counter

## Dictionaries creation
#vdu_dic = {}
#vdu_params_dic = {}
#vnf_dic = {}
#vnffg_dic = {}

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

# Dynamic VDU dictionary creation
#for param_name in vdu_params:
#    vdu_params_dic[param_name] = list()

# Dynamic VNF dictionary creation
#for param_name in vnf_params:
#	vnf_dic[param_name] = dict()

## Dynamic VNF dictionary creation
#for vnffg_param_name in vnffg_params:
#	vnffg_dic[vnffg_param_name] = dict()
#	for vnf_param_name in vnf_params:
#		vnffg_dic[vnffg_param_name][vnf_param_name] = dict()
#		for vdu_param_name in vdu_params:
#			vnffg_dic[vnffg_param_name][vnf_param_name][vdu_param_name] = dict()

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

## This function send a request to NFVO asking for current information
## regarding VNFFGs operation
## Version #1 - creates an unified structure with VNFFG -> VNF -> VDU
#def getNFVOMonitoredVNFFGData():
#	vdu_list = list()
#	vnf_params_dict = dict()
#
#	with open("monitored_vdu_list.dat") as f:
#		for line in f:
#			vdu_read_values = line.split()
#			param_index = 1
#			vdu_params_dict = dict()
#			for vdu_param in vdu_params:
#				vdu_params_dict[vdu_param] = vdu_read_values[param_index]
#				param_index = param_index + 1
#			vdu_list.append(vdu_params_dict)
#	
#	for vnf_param in vnf_params:
#		vnf_params_dict[vnf_param] = list()
#	vnf_params_dict['vdus'] = vdu_list
#
#	vnf_list = list()
#	vnf_list.append(vnf_params_dict)
#
#	vnffg_params_dict = dict()
#
#	for vnffg_param in vnffg_params:
#		vnffg_params_dict[vnffg_param] = list()
#	vnffg_params_dict['vnfs'] = vnf_list
#
#	vnffg_list = list()
#	vnffg_list.append(vnffg_params_dict)
#	return vnffg_list
#
## This function sends a request to NFVO asking for registered information
## regarding VNFFGs operation
## Version #1 - creates an unified structure with VNFFG -> VNF -> VDU
#def getNFVOCatalogedVNFFGData():
#	vdu_list = list()
#	vnf_params_dict = dict()
#
#	with open("cataloged_vdu_list.dat") as f:
#		for line in f:
#			vdu_read_values = line.split()
#			param_index = 1
#			vdu_params_dict = dict()
#			for vdu_param in vdu_params:
#				vdu_params_dict[vdu_param] = vdu_read_values[param_index]
#				param_index = param_index + 1
#			vdu_list.append(vdu_params_dict)
#	
#	for vnf_param in vnf_params:
#		vnf_params_dict[vnf_param] = list()
#	vnf_params_dict['vdus'] = vdu_list
#
#	vnf_list = list()
#	vnf_list.append(vnf_params_dict)
#
#	vnffg_params_dict = dict()
#
#	for vnffg_param in vnffg_params:
#		vnffg_params_dict[vnffg_param] = list()
#	vnffg_params_dict['vnfs'] = vnf_list
#
#	vnffg_list = list()
#	vnffg_list.append(vnffg_params_dict)
#	return vnffg_list

# Generic request data
def NFVORequestData(data_origin, data_type):
	data_list = list()

	with open(data_origin + "_" + data_type + "_list.dat") as f:
		for line in f:
			read_values = line.split()
			param_index = 1
			param_dict = dict()
			for param in general_paramenters[data_type]:
				param_dict[param] = read_values[param_index]
				param_index = param_index + 1
			data_list.append(param_dict)
	return data_list

## Version 2: get cataloged VDU list information only
## Paramenter: data_type = "cataloged" or "monitored"
## Return: VDU information list
#def NFVORequestVDUData(data_type):
#	vdu_list = list()
#
#	with open(data_type + "_vdu_list.dat") as f:
#		for line in f:
#			vdu_read_values = line.split()
#			param_index = 1
#			vdu_params_dict = dict()
#			for vdu_param in vdu_params:
#				vdu_params_dict[vdu_param] = vdu_read_values[param_index]
#				param_index = param_index + 1
#			vdu_list.append(vdu_params_dict)
#	return vdu_list
#
## Version 2: get VNF list information only
## Paramenter: data_type = "cataloged" or "monitored"
## Return: VNF information list
#def NFVORequestVNFData(data_type):
#	vnf_list = list()
#
#	with open(data_type + "_vnf_list.dat") as f:
#		for line in f:
#			vnf_read_values = line.split()
#			param_index = 1
#			vnf_params_dict = dict()
#			for vnf_param in vnf_params:
#				vnf_params_dict[vnf_param] = vnf_read_values[param_index]
#				param_index = param_index + 1
#			vnf_list.append(vnf_params_dict)
#	return vnf_list

## Version 2: get cataloged VNFFG list information only
## Paramenter: data_type = "cataloged" or "monitored"
## Return: VNFFG information list
#def NFVORequestVNFFGData(data_type):
#	vnffg_list = list()
#
#	with open(data_type + "_vnffg_list.dat") as f:
#		for line in f:
#			vnffg_read_values = line.split()
#			param_index = 1
#			vnffg_params_dict = dict()
#			for vnffg_param in vnffg_params:
#				vnffg_params_dict[vnffg_param] = vnffg_read_values[param_index]
#				param_index = param_index + 1
#			vnffg_list.append(vnffg_params_dict)
#	return vnffg_list

## Calculate VNFFG entropies
## Parameter: info_type: "cataloged" or "monitored"
## Return: dictionary with VNFFG entropies
#def VNFFGEntropies(data_type,other):
#
#	vnffg_complete_lists = dict()
#	vnffg_entropies = dict()
#	vnffg_list = NFVORequestData(data_type,other)
#	# visits each parameter
#	for vnffg_param in vnffg_params:
#		complete_list = list()
#		# visits each VNFFG
#		for vnffg_index in range(0, len(vnffg_list)):
#			# Split values separated by comma
#			complete_list = complete_list + vnffg_list[vnffg_index][vnffg_param].split(",")
#		vnffg_complete_lists[vnffg_param] = complete_list
#
#	# Now, calculate the entropy of each parameter list
#	for vnffg_param in vnffg_params:
#		vnffg_entropies[vnffg_param] = eta(vnffg_complete_lists[vnffg_param])
#	return vnffg_entropies
#
## Calculate VNF entropies
## Parameter: info_type: "cataloged" or "monitored"
## Return: dictionary with VNF entropies
#def VNFEntropies(data_type, other):
#
#	vnf_complete_lists = dict()
#	vnf_entropies = dict()
#	vnf_list = NFVORequestData(data_type,other)
#	# visits each parameter
#	for vnf_param in vnf_params:
#		complete_list = list()
#		# visits each VNF
#		for vnf_index in range(0, len(vnf_list)):
#			# Split values separated by comma
#			complete_list = complete_list + vnf_list[vnf_index][vnf_param].split(",")
#		vnf_complete_lists[vnf_param] = complete_list
#
#	# Now, calculate the entropy of each parameter list
#	for vnf_param in vnf_params:
#		vnf_entropies[vnf_param] = eta(vnf_complete_lists[vnf_param])
#	return vnf_entropies
#
## Calculate vdu entropies
## Parameter: info_type: "cataloged" or "monitored"
## Return: dictionary with vdu entropies
#def VDUEntropies(data_type, other):
#
#	vdu_complete_lists = dict()
#	vdu_entropies = dict()
##	vdu_list = NFVORequestVDUData(data_type)
#	vdu_list = NFVORequestData(data_type,other)
#	# visits each parameter
#	for vdu_param in vdu_params:
#		complete_list = list()
#		# visits each vdu
#		for vdu_index in range(0, len(vdu_list)):
#			# Split values separated by comma
#			complete_list = complete_list + vdu_list[vdu_index][vdu_param].split(",")
#		vdu_complete_lists[vdu_param] = complete_list
#
#	# Now, calculate the entropy of each parameter list
#	for vdu_param in vdu_params:
#		vdu_entropies[vdu_param] = eta(vdu_complete_lists[vdu_param])
#	return vdu_entropies

# GENERIC Calculate entropies
# Parameters:
#	info_type: "cataloged" or "monitored"
#	element: "vnffg", "vnf" or "vdu"
# Return: dictionary with element entropies
def Entropies(data_type, element):

	complete_lists = dict()
	entropies = dict()
	data_list = NFVORequestData(data_type,element)
	# visits each parameter
	for param in general_paramenters[element]:
		complete_list = list()
		# visits each vdu
		for index in range(0, len(data_list)):
			# Split values separated by comma
			complete_list = complete_list + data_list[index][param].split(",")
		complete_lists[param] = complete_list

	# Now, calculate the entropy of each parameter list
	for param in general_paramenters[element]:
		entropies[param] = eta(complete_lists[param])
	return entropies

# -- Main code --
if __name__ == "__main__":
# Version 1 tests:
#	print getNFVOMonitoredVNFFGData()
#	print getNFVOCatalogedVNFFGData()

# Version 2 tests:
#	print getNFVOCatalogedVDUData()
#	print "___"
#	print getNFVOCatalogedVNFData()
#	print "___"
#	print getNFVOCatalogedVNFFGData()

	#print VNFFGEntropies("cataloged")
	#print VNFFGEntropies("monitored")

#	total_connection_points = list()
#	vnffg_list = getNFVOCatalogedVNFFGData()
#	for vnffg_index in range(0, len(vnffg_list)):
#		print vnffg_list[vnffg_index]['connection_points'].split(",")
#		total_connection_points = total_connection_points + vnffg_list[vnffg_index]['connection_points'].split(",")
#	print total_connection_points
#	print eta(vnffg_list[vnffg_index]['connection_points'])
#	print eta(total_connection_points)
	print "_____VNFFG_____"
	print Entropies("cataloged","vnffg")
	print Entropies("monitored","vnffg")
	print "_____VNF_____"
	print Entropies("cataloged","vnf")
	print Entropies("monitored","vnf")
	print "_____VDU_____"
	print Entropies("cataloged", "vdu")
	print Entropies("monitored", "vdu")
