#!/usr/bin/env python

import rospy
import inspect
import sys
import os
import re
import math

model_file = 'tempdata'

listtoplot = []
tempNumList = []
finaSimTime = []
proximityList = []
proteanList = []
set_list = []

current_set = 'Current set: '
final_time = 'Simulation Finished '
proximity = 'Execute Proximity '
protean = 'Excute Protean fleeing '
captured_fleeing = 'Robot captured whilst fleeing '
final_distance = 'Final Relative Distance '
proximity_distance = 'Initiated Proximity Distance '
protean_distance = 'Initiated Protean Distance '
reached_goal = 'Main goal accomplished only'
captured_goal = "Robot captured whilst navigating to main goal"
reached_goal_fleed = 'Main goal accomplished and fled'
max_time = "Simulation time is up"

def convert(tempNumList):

	finalResult = []

	for i in tempNumList:
		int_number = int(i)
		finalResult.append(int_number)
			
	return finalResult

def findData():

	finaSimTime = []
	proximityList = []
	proteanList = []
	proximity_distanceList = []
	protean_distanceList = []

	proximity_count = 0
	protean_count = 0

	result_captured_fleeing = 0
	result_captured_goal = 0
	result_goal = 0
	result_sim_end = 0
	result_reached_goal_fled = 0
	result_time_up = 0


	for i, line in enumerate(open(model_file +'.txt', 'r')): # All global variables

		# final sim time
		if re.search(final_time,line):
			newline = line
			number = re.findall(r'\d+', newline)
			finaSimTime.append(number[0])
		# proxmity excution
		if re.search(proximity,line):
			newline = line
			number = re.findall(r'\d+', newline)
			proximityList.append(number[0])
			proximity_count += 1

		if re.search(proximity_distance, line):
			newline = line
			number = re.findall(r'\d+', newline)
			proximity_distanceList.append(number[0])			
		# proximity distance
		if re.search(protean,line):
			newline = line
			number = re.findall(r'\d+', newline)
			proteanList.append(number[0])
			protean_count += 1

		if re.search(protean_distance, line):
			newline = line
			number = re.findall(r'\d+', newline)
			protean_distanceList.append(number[0])	

		if re.search(captured_fleeing,line):
			result_captured_fleeing += 1

		if re.search(reached_goal, line):
			result_goal += 1	

		if re.search(captured_goal, line):
			result_captured_goal += 1

		if re.search(reached_goal_fleed, line):
			result_reached_goal_fled += 1	

		if re.search(max_time, line):
			result_time_up += 1	


	print "Final sim time =", convert(finaSimTime)
	print "Proximity List =", convert(proximityList)
	print "Proximity count =", proximity_count
	print "Proximity distance =", convert(proximity_distanceList)
	print "ProteanList =", convert(proteanList)
	print "protean_count =", protean_count
	print "Protean distance =", convert(protean_distanceList)
	print "Total reached goal =", result_goal
	print "Total captured_fleeing =", result_captured_fleeing
	print "Total captured_goal =", result_captured_goal
	print "Total reach goal fleeing =", result_reached_goal_fled
	print "Total reach max_time =", result_time_up

	#print "final sim time", convert(finaSimTime)	

if __name__ == '__main__':

	try:
		findData()
	except rospy.ROSInterruptException:
		pass