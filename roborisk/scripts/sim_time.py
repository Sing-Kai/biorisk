#!/usr/bin/env python

# node only used for testing purposes

import rospy
import math
import time
import geometry_msgs.msg

from std_msgs.msg import Float64, Bool

def simulationTime():

	pub = rospy.Publisher('sim_time',Float64, queue_size = 1)
	rospy.init_node('sim_time')
	#timer = True
	rate = rospy.Rate(5.0)

	timer = 0.0

	stop_sim = False
	
	#total time for simulation
	simulation_time = 10.0

	while not rospy.is_shutdown():

		time.sleep(1)
		timer += 1.0
		#print timer
		pub.publish(timer)

if __name__ == '__main__':

	try:
		simulationTime()
	except rospy.ROSInterruptException:
		pass