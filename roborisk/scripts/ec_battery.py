#!/usr/bin/env python

# Ros node to simulate battery life of robot

import rospy
import math
import time
import geometry_msgs.msg

from std_msgs.msg import Float64

def batteryTime():

	pub = rospy.Publisher('battery_life',Float64, queue_size = 1)
	rospy.init_node('battery')
	#timer = True
	rate = rospy.Rate(5.0)

	time_start = time.time()

	batter_time = 0.0

	#print time_start
	total_battery_life = 600

	while not rospy.is_shutdown():

		if batter_time < total_battery_life:
			time.sleep(1)
			batter_time += 1.0
			percentage = batter_time/total_battery_life *100
			#print percentage
			pub.publish(percentage)
		else:
			#print percentage
			pub.publish(percentage)

if __name__ == '__main__':

	try:
		#rospy.Timer(rospy.Duration(2), timer_callback)
		batteryTime()
	except rospy.ROSInterruptException:
		pass