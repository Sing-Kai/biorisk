#!/usr/bin/env python
import rospy
import math
import geometry_msgs.msg

from std_msgs.msg import Float64

robot_x = 0.0
robot_y = 0.0
robot_z = 0.0


def get_robot_x(data):

	global robot_x
	robot_x = data.data

def get_robot_y(data):

	global robot_y
	robot_y = data.data	

def get_robot_z(data):
	
	global robot_z	
	robot_z = data.data

def timer_callback(event):

	print "timer called at " + str(event.current_real)


def batteryTime():

	pub = rospy.Publisher('battery_life',Float64, queue_size = 1)
	rospy.init_node('battery')

	# subcribe to robot position 
	#rospy.Subscriber('robot_position_x', Float64, get_robot_x)		
	#rospy.Subscriber('robot_position_y', Float64, get_robot_y)
	#rospy.Subscriber('robot_position_z', Float64, get_robot_z)

	start_time = rospy.get_time()

	timer = True
	rate = rospy.Rate(5.0)
	
	start = rospy.Time.now()

	while not rospy.is_shutdown():


		timer = rospy.Time.now()
		duration_seconds = rospy.Duration(600) # total battery life of robot
		total = start + duration_seconds

		#print start.secs, timer.secs, three_seconds.secs, count_to_three.secs

		battery_life = (timer - start)/duration_seconds * 100

		#if total <= timer:
		#	print "times up"

		if battery_life <= 100.0:
			pub.publish(battery_life)
			#print battery_life

if __name__ == '__main__':

	try:
		#rospy.Timer(rospy.Duration(2), timer_callback)
		batteryTime()
	except rospy.ROSInterruptException:
		pass