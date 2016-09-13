#!/usr/bin/env python

# simulated sensor node that subscibes to the environmental cue of sound, node takes a sample of data every 1 seconds

import rospy
import math
import geometry_msgs.msg

from std_msgs.msg import Float64

sound_pressure = 0.0
list_s = []
total_length = 5

def get_sound_data(data):

	global sound_pressure

	sound_pressure = data.data

def populate_list(list_s, sound_pressure):

	list_length = len(list_s)

	global total_length

	new_list = []

	if list_length < total_length:

		append_list(list_s, sound_pressure)


def append_list(list_s, sound_pressure):

	list_s.append(sound_pressure)	

def check_seconds(sec, old_sec, sound_pressure):

	if sec > old_sec:		
		old_sec = sec
		populate_list(list_s, sound_pressure)		

	return sec

# NOT associated with whole of program yet, just need to populate the list
def find_slope(list_temp):
	
	ylist = list(list_s)

	slope = 0.0
	sum_square_x_final = 0
	xy_sum = 0.0

	xlist = []
	dx_list = []
	dy_list = []
	sum_square_x = []
	dx_dy = []

	xlist = create_x_list(ylist)

	mean_y = find_mean(ylist)
	mean_x = find_mean(xlist)

	dx_list = value_minus_mean(xlist, mean_x)
	dy_list = value_minus_mean(ylist, mean_y)

	dx_dy = dx_times_dy(dx_list, dy_list)

	sum_square_x = dx_list

	sum_square_x_final = sum_square(sum_square_x)

	xy_sum = sum(dx_dy)

	slope = float(xy_sum)/sum_square_x_final

	#print ylist, xlist, slope

	return slope


def dx_times_dy(dx_list, dy_list):

	i = 0
	total = 0
	temp_list = []

	while i < len(dy_list):
		new_element = 0
		new_element = dx_list[i] * dy_list[i]
		new_element = new_element
		temp_list.append(new_element)
		i += 1

	return temp_list	

def find_mean(temp_list):

	total = 0
	mean = 0

	for i in temp_list:
		total += i

	mean = total/len(temp_list)

	return mean	

def value_minus_mean(temp_list, mean):

	d_list = []
	d_list = temp_list
	d_list[:] = [x - mean for x in d_list]

	return d_list

def create_x_list(alist):

	x_list = []
	i = 0
	j = 0

	while j < len(alist):
		i += 1
		x_list.append(i)
		j += 1 	

	#print x_list

	return x_list	

def sum_square(sum_square_x):

	total = 0.0
	temp_list = sum_square_x

	temp_list[:] = [x ** 2 for x in temp_list]

	total = sum(temp_list)

	#print total

	return total

def soundSensor():

	pub = rospy.Publisher('sound_risk',Float64, queue_size = 1)
	rospy.Subscriber('sound_pressure', Float64, get_sound_data)
	rospy.init_node('sound_sensor')

	rate = rospy.Rate(5.0)

	global total_length

	#list_s = []
	final_list = []
	intial_seconds = 0


	while not rospy.is_shutdown():

		f_time = rospy.get_time()
		seconds = round(f_time)
		intial_seconds = check_seconds(seconds, intial_seconds, sound_pressure)
		
		if len(list_s) == total_length:
			sound_risk = find_slope(list_s)

			pub.publish(sound_risk)
			rospy.sleep(1.0)

			del list_s[:]
			#print "list is empty", list_s



if __name__ == '__main__':

	try:
		soundSensor()
	except rospy.ROSInterruptException:
		pass