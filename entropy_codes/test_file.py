#!/usr/bin/python

def readFloatFile(file_name):
	my_list = open(file_name).read().splitlines()

	for i in range(len(my_list)):
		my_list[i] = map(float, my_list[i].split(','))

	return my_list

if __name__ == "__main__":

	list_ent = readFloatFile('histEntropy.txt')
	
	historical_entropies_VL = list()

	historical_entropies_VL.append([1.09861228867,0.69314718056,1.38629436112])
	historical_entropies_VL.append([1.13861228867,0.67314718056,1.30629436112])
	historical_entropies_VL.append([1.06861228867,0.71314718056,1.36294361121])

	print list_ent
	print historical_entropies_VL
