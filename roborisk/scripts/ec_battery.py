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
	rospy.Subscriber('robot_position_x', Float64, get_robot_x)		
	rospy.Subscriber('robot_position_y', Float64, get_robot_y)
	rospy.Subscriber('robot_position_z', Float64, get_robot_z)

	start_time = rospy.get_time()

	timer = True
	rate = rospy.Rate(1.0)

	while timer:

		current_time = rospy.get_time()

		seconds = current_time - start_time

		#print seconds

		if seconds > 10:
			print seconds
			timer = False


		percentage = (seconds/10.0) * 100

		battery_life = 100 - percentage

		print battery_life

		#relative_distance = math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
		#rospy.Timer(rospy.Duration(2), timer_callback)
		pub.publish(battery_life)

if __name__ == '__main__':

	try:
		#rospy.Timer(rospy.Duration(2), timer_callback)
		batteryTime()
	except rospy.ROSInterruptException:
		pass