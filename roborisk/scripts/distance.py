#!/usr/bin/env python
import rospy
import math
import geometry_msgs.msg

from std_msgs.msg import Float64


drone_z = 0.0
drone_x = 0.0
drone_y = 0.0
robot_x = 0.0
robot_y = 0.0
robot_z = 0.0

def get_drone_z(data):

	global drone_z
	drone_z = data.data

def get_drone_x(data):

	global drone_x
	drone_x = data.data

def get_drone_y(data):

	global drone_y
	drone_y = data.data	

def get_robot_x(data):

	global robot_x
	robot_x = data.data

def get_robot_y(data):

	global robot_y
	robot_y = data.data	

def get_robot_z(data):
	
	global robot_z	
	robot_z = data.data

def findDistance():

	pub = rospy.Publisher('relative_distance',Float64, queue_size = 1)
	rospy.init_node('relative_distance_manager')

	# subcribe to drone position 
	rospy.Subscriber('drone_position_x', Float64, get_drone_x)
	rospy.Subscriber('drone_position_y', Float64, get_drone_y)
	rospy.Subscriber('drone_position_z', Float64, get_drone_z)	
	#rospy.Subscriber('drone_orientation', Float64, get_drone_orientation)	

	# subcribe to robot position 
	rospy.Subscriber('robot_position_x', Float64, get_robot_x)		
	rospy.Subscriber('robot_position_y', Float64, get_robot_y)
	rospy.Subscriber('robot_position_z', Float64, get_robot_z)

	rate = rospy.Rate(5.0)
	while not rospy.is_shutdown():

		dx = drone_x - robot_x
		dy = drone_y - robot_y
		dz = drone_z - robot_z

		relative_distance = math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
		#print relative_distance

		pub.publish(relative_distance)

if __name__ == '__main__':

	try:
		findDistance()
	except rospy.ROSInterruptException:
		pass