#!/usr/bin/env python

# python node to simulate the distance between the sound of drone

from __future__ import division
import rospy
import math
import geometry_msgs.msg
import numpy

from std_msgs.msg import Float64


relative_distance = 1.0
decibel = 60.0
source = 0.1
sound_pressure = 0.0


def get_distance(data):

	global relative_distance
	relative_distance = data.data

def get_ratio(r_dist):

	ratio = 0.0
	ratio = 1.0/(r_dist)

	return ratio


def soundSimulator():

	pub = rospy.Publisher('sound_pressure',Float64, queue_size = 1)
	rospy.init_node('sound_simulator')
	rospy.Subscriber('relative_distance', Float64, get_distance)

	rate = rospy.Rate(5.0)
	ratio = 0.0
	while not rospy.is_shutdown():

		r_distance = round(relative_distance, 1)

		print r_distance

		ratio = 1/r_distance

		sound_pressure = decibel * ratio

		#print sound_pressure

		pub.publish(sound_pressure)

if __name__ == '__main__':

	try:
		soundSimulator()
	except rospy.ROSInterruptException:
		pass