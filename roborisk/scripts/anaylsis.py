#!/usr/bin/env python

import rospy
import inspect
import sys
import os
import re
import math

model_file = 'testdata'

listtoplot = []
tempNumList = []
numberList = []
set_list = []

current_set = 'Current set: '
final_time = 'Simulation Finished '
proximity = 'Execute Proximity '
protean = 'Excute Protean fleeing '
captured = 'Robot captured whilst fleeing '
final_distance = 'Final Relative Distance '
proximity_distance = 'Initiated Proximity Distance '
protean_distance = 'Initiated Protean Distance '
reached_goal = 'Main goal accomplished '


# find all set numbers 
for i, line in enumerate(open(model_file +'.txt', 'r')): # All global variables

	if re.search(proximity,line):
		newline = line
		number = re.findall(r'\d+', newline)
		tempNumList.append(number[0])
		print number


for i in tempNumList:
	int_number = int(i)
	numberList.append(int_number)
		
[int(s) for s in tempNumList]


print numberList

"""
Current set: 2
Execute Proximity  17.0
Initiated Proximity Distance 16.9219328306
Reached fleeing goal
Execute Proximity  28.0
Initiated Proximity Distance 17.407387003
Reached fleeing goal
Execute Proximity  37.0
Initiated Proximity Distance 18.1064208094
Reached fleeing goal
Execute Proximity  77.0
Initiated Proximity Distance 5.09407837127
Reached fleeing goal
Excute Protean fleeing 99.0
Initiated Protean Distance 2.04538626823
Protean flight 3 5 -10 8 0
Robot captured whilst fleeing 102.0
Captured
Simulation Finished 102.0
Final Relative Distance 1.69612293292
escape speed: 1.0 7.5
base speed: 0.5 7.5
"""