#!/usr/bin/env python
import rospy
import math
import geometry_msgs.msg

from std_msgs.msg import Float64

relative_distance = 0.0
speed = 0.0
list_d = []

def get_distance_data(data):

	global relative_distance

	relative_distance = data.data

def populate_list(list_d, speed):

	list_length = len(list_d)

	new_list = []

	if list_length < 5:

		append_list(list_d, speed)


def append_list(list_d, speed):

	list_d.append(speed)	

# checks for time difference and populates a list for analysis
def check_seconds(sec, old_sec, speed):

	if sec > old_sec:		
		old_sec = sec
		populate_list(list_d, speed)		

	return sec

# analyse sample list data to check return slope
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

	return x_list	

def sum_square(sum_square_x):

	total = 0.0
	temp_list = sum_square_x

	temp_list[:] = [x ** 2 for x in temp_list]

	total = sum(temp_list)

	return total

def speedSensor():

	pub = rospy.Publisher('speed_risk',Float64, queue_size = 1)
	rospy.init_node('speed_sensor')

	rate = rospy.Rate(5.0)

	final_list = []
	intial_seconds = 0

	while not rospy.is_shutdown():

		#estimate speed of by calculating speed difference in distance every two seconds 
		first_distance = relative_distance
		total_seconds = 2.0
		rospy.sleep(total_seconds)
		second_distance = relative_distance
		distance_difference = round(first_distance - second_distance)
		speed = distance_difference/total_seconds

		#print first_distance, second_distance, distance_difference, speed

		f_time = rospy.get_time()
		current_seconds = round(f_time)

		# checks for time difference and populates a list for analysis
		intial_seconds = check_seconds(current_seconds, intial_seconds, speed)
		
		# once 5 samples have been taken the analyse the slope of data to see if this is increase or decreasing
		if len(list_d) == 5:
			speed_risk = find_slope(list_d)
			#print speed_risk #list_d, 

			pub.publish(speed_risk)
			rospy.sleep(1.0)

			# empty list 
			del list_d[:]


if __name__ == '__main__':

	rospy.Subscriber('relative_distance', Float64, get_distance_data)

	try:
		speedSensor()
	except rospy.ROSInterruptException:
		pass