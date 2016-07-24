#!/usr/bin/env python
import rospy
import math
import geometry_msgs.msg

from std_msgs.msg import Float64

sound_pressure = 0.0

def get_sound_data(data):

	global sound_pressure

	sound_pressure = data.data

def populate_list(list_s, seconds, sound_pressure):

	list_length = len(list_s)

	new_list = []

	if list_length < 5:

		append_list(list_s, seconds, sound_pressure)

	elif list_length == 5:

		new_list = list_s
	print new_list
	return new_list	

def append_list(list_s, data, sound_pressure):

	#if sound_pressure not in list_s and sample_rate(data):

	#	list_s.append(sound_pressure)	
	if sample_rate(data):

		list_s.append(sound_pressure)	


def sample_rate(data):

	if data % 10 == 0:

		return True	

  	return False

def soundSensor():

	pub = rospy.Publisher('sound_score',Float64, queue_size = 1)
	rospy.init_node('sound_sensor')
	rospy.Subscriber('sound_pressure', Float64, get_sound_data)

	rate = rospy.Rate(5.0)

	list_s = []
	final_list = []

	while not rospy.is_shutdown():

		f_time = rospy.get_time()
		seconds = round(f_time)
		
		if seconds != 0.0:
			
			final_list = populate_list(list_s, seconds, sound_pressure)

		#print sound_pressure
		#print final_list

		#pub.publish(sound_pressure)

if __name__ == '__main__':

	try:
		soundSensor()
	except rospy.ROSInterruptException:
		pass