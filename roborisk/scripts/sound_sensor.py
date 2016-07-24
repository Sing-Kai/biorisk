#!/usr/bin/env python
import rospy
import math
import geometry_msgs.msg

from std_msgs.msg import Float64

sound_pressure = 0.0

def get_sound_data(data):

	global sound_pressure
	sound_pressure = data.data


def populate_list(list_s, seconds):

	#list_s = []

	list_length = len(list_s)
	#sample_data = 0
	#print list_length
	

	if list_length == 0:

		list_s.append(seconds)

	elif list_length <= 5:

		check_duplicate(list_s, seconds)
		#sample_data = sample_rate(data_s)
		#list_s.append(sample_data)

		print list_s	
		

def check_duplicate(list_s, data):

	if data not in list_s and sample_rate(data):

		list_s.append(data)
		

def sample_rate(data):

	#sample_data = 0

	if data % 2 == 0:
		return True
		
  	return False

def soundSensor():

	pub = rospy.Publisher('sound_score',Float64, queue_size = 1)
	rospy.init_node('sound_simulator')
	rospy.Subscriber('sound_pressure', Float64, get_sound_data)

	rate = rospy.Rate(5.0)

	list_s = []

	while not rospy.is_shutdown():

		#list_s = [1, 2, 3]

		f_time = rospy.get_time()
		seconds = round(f_time)

		#final_list = populate_list(list_s, seconds)

		
		if seconds != 0.0:
			populate_list(list_s, seconds)


		#print seconds #, final_list
		print list_s
		"""
		if seconds % 2 == 0:
			print seconds, "this is divisble by 2"
		"""
		#print round(time)

		pub.publish(sound_pressure)

if __name__ == '__main__':

	try:
		soundSensor()
	except rospy.ROSInterruptException:
		pass