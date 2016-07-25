#!/usr/bin/env python
import rospy
import math
import geometry_msgs.msg

from std_msgs.msg import Float64

relative_distance = 0.0
list_d = []


def get_distance_data(data):

	global relative_distance

	relative_distance = data.data

def populate_list(list_d, relative_distance):

	list_length = len(list_d)

	new_list = []

	if list_length < 5:

		append_list(list_d, relative_distance)


def append_list(list_d, relative_distance):

	list_d.append(relative_distance)	

def check_seconds(sec, old_sec, relative_distance):

	if sec > old_sec:		
		old_sec = sec
		populate_list(list_d, relative_distance)		

	return sec

def find_slope(list_temp):
	
	ylist = list(list_d)

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

	print ylist, xlist, slope

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

	return x_list	

def sum_square(sum_square_x):

	total = 0.0
	temp_list = sum_square_x

	temp_list[:] = [x ** 2 for x in temp_list]

	total = sum(temp_list)

	return total

def distanceSensor():

	pub = rospy.Publisher('distance_risk',Float64, queue_size = 1)
	rospy.init_node('distance_sensor')

	rate = rospy.Rate(5.0)


	final_list = []
	old_seconds = 0

	while not rospy.is_shutdown():

		f_time = rospy.get_time()
		seconds = round(f_time)
		old_seconds = check_seconds(seconds, old_seconds, relative_distance)
		
		if len(list_d) == 5:
			distance_risk = find_slope(list_d)
			print list_d, distance_risk

			pub.publish(distance_risk)
			rospy.sleep(1.0)

			del list_d[:]
			print "list is empty", list_d
		
		#pub.publish(relative_distance)

if __name__ == '__main__':

	rospy.Subscriber('relative_distance', Float64, get_distance_data)

	try:
		distanceSensor()
	except rospy.ROSInterruptException:
		pass