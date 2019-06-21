This file is just to describe the composition of the text files

1. Historical entropies:
 - Each line represents a measurement;
 - Each column represents a resource;
 - In the code, the historical_entropies variable is a list of measurements.
   Each measurement is a list of a measurement of each resource, ie, a list
   of lists.
 - Example:
   									RESOURCE
   						CPU				STR			NET
   MEASUREMENT
   		1			1.09861228867,0.69314718056,1.38629436112
		2			1.13861228867,0.67314718056,1.30629436112
		3			1.06861228867,0.71314718056,1.36294361121


. Current members:
 - Each line represents a resource of that class;
 - In the code, the current_members is a list of resource members list (ie a
   list of lists too).
 - Example:
				MEMBERS
 	RESOURCE
		cpu		a,b,c,d,e
		str		a,b
		net		a,b,c,d
