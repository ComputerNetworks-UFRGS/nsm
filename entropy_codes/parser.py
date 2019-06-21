#!/usr/bin/python

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
    monitored_data = open('monitored_data.txt').read().splitlines()
    for i in range(len(monitored_data)):
        monitored_data[i] = map(str, monitored_data[i].split(','))
        current_ip = monitored_data[i].pop(0)
        # Monitored data has now only the values of the ip 'i'
        # Let's convert the values into floats
        monitored_data[i] = map(float, monitored_data[i])
        #print ip
        #print monitored_data[i]
        classifier(current_ip, monitored_data[i])

    #*****************Main Code version**********************
    current_members_OF = list()
    current_members_OF.append(cpu_members_OF)
    current_members_OF.append(str_members_OF)
    current_members_OF.append(net_members_OF)
    print current_members_OF

    #***************** File Writing version *****************
	# Write the files for each class
	# OF
#	members_OF = open('current_members_OF.txt', 'w')
#	members_OF.write(",".join(cpu_members_OF))
#	members_OF.write('\n')
#	members_OF.write(",".join(str_members_OF))
#	members_OF.write('\n')
#	members_OF.write(",".join(net_members_OF))
#	members_OF.write('\n')
#	members_OF.close
#
#	# VL
#	members_VL = open('current_members_OF.txt', 'w')
#	members_VL.write(",".join(cpu_members_VL))
#	members_VL.write('\n')
#	members_VL.write(",".join(str_members_VL))
#	members_VL.write('\n')
#	members_VL.write(",".join(net_members_VL))
#	members_VL.write('\n')
#	members_VL.close
#
#    # LO
#	members_LO= open('current_members_OF.txt', 'w')
#	members_LO.write(",".join(cpu_members_LO))
#	members_LO.write('\n')
#	members_LO.write(",".join(str_members_LO))
#	members_LO.write('\n')
#	members_LO.write(",".join(net_members_LO))
#	members_LO.write('\n')
#	members_LO.close
#
#    # ME
#	members_ME= open('current_members_OF.txt', 'w')
#	members_ME.write(",".join(cpu_members_ME))
#	members_ME.write('\n')
#	members_ME.write(",".join(str_members_ME))
#	members_ME.write('\n')
#	members_ME.write(",".join(net_members_ME))
#	members_ME.write('\n')
#	members_ME.close
#
#    # HI
#	members_HI = open('current_members_OF.txt', 'w')
#	members_HI.write(",".join(cpu_members_HI))
#	members_HI.write('\n')
#	members_HI.write(",".join(str_members_HI))
#	members_HI.write('\n')
#	members_HI.write(",".join(net_members_HI))
#	members_HI.write('\n')
#	members_HI.close
#
#    # VH
#	members_VH = open('current_members_OF.txt', 'w')
#	members_VH.write(",".join(cpu_members_VH))
#	members_VH.write('\n')
#	members_VH.write(",".join(str_members_VH))
#	members_VH.write('\n')
#	members_VH.write(",".join(net_members_VH))
#	members_VH.write('\n')
#	members_VH.close
#
#    # DG
#	members_DG = open('current_members_OF.txt', 'w')
#	members_DG.write(",".join(cpu_members_DG))
#	members_DG.write('\n')
#	members_DG.write(",".join(str_members_DG))
#	members_DG.write('\n')
#	members_DG.write(",".join(net_members_DG))
#	members_DG.write('\n')
#	members_DG.close

