#!/usr/bin/env python
import rospy
import math
import geometry_msgs.msg

from std_msgs.msg import Float64

sound_risk = 0.0
distance_risk = 0.0
battery_life = 0.0

def get_sound_risk(data):

	global sound_risk
	sound_risk = data.data

def get_distance_risk(data):

	global distance_risk
	distance_risk = data.data	

def  get_battery_life(data):

	global battery_life
	battery_life = data.data		

def riskController():

	pub = rospy.Publisher('total_risk',Float64, queue_size = 1)
	rospy.init_node('risk_controller')

	rate = rospy.Rate(5.0)
	while not rospy.is_shutdown():

		print sound_risk, distance_risk

		#pub.publish(relative_distance)

if __name__ == '__main__':

	rospy.Subscriber('sound_risk', Float64, get_sound_risk)
	rospy.Subscriber('distance_risk', Float64, get_distance_risk)
	rospy.Subscriber('battery_life', Float64, get_distance_risk)

	try:
		riskController()
	except rospy.ROSInterruptException:
		pass