#!/usr/bin/env python
import roslib; roslib.load_manifest('teleop_twist_keyboard')
import rospy
import math
import tf
import geometry_msgs.msg

from std_msgs.msg import Float64
from random import randint
from reset_position import reset_robot
#from geometry_msgs import PointStamped

"""
speed = .5
turn = 1
max_height = 2.0
drone_z = 0.0
drone_x = 0.0
drone_y = 0.0
drone_orientation = 0.0
"""
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

speed = .5
turn = 1


def leftturn(cmd):

	cmd.linear.x = 1
	cmd.angular.z = 0.5*turn

def rightturn(cmd):

	cmd.linear.x = 1
	cmd.angular.z = -0.5*turn	

def forward(cmd):

	cmd.linear.x = 1

def robotNavigation():

	pub = rospy.Publisher('cmd_vel', geometry_msgs.msg.Twist, queue_size = 1)
	rospy.init_node('teleop_twist_robot')

	# subcribe to drone position 
	#rospy.Subscriber('drone_position_x', Float64, get_drone_x)
	#rospy.Subscriber('drone_position_y', Float64, get_drone_y)
	#rospy.Subscriber('drone_position_z', Float64, get_drone_z)	
	#rospy.Subscriber('drone_orientation', Float64, get_drone_orientation)	

	# subcribe to robot position 
	rospy.Subscriber('robot_position_x', Float64, get_robot_x)		
	rospy.Subscriber('robot_position_y', Float64, get_robot_y)
	#rospy.Subscriber('robot_position_z', Float64, get_robot_z)

	#time = rospy.get_time()

	#print time

	rate = rospy.Rate(1.0)

	#cmd = geometry_msgs.msg.Twist()

	#cmd.linear.x = 1
	#cmd.angular.z = 0.5*turn

	#leftturn(cmd)



	
	while not rospy.is_shutdown():

		cmd = geometry_msgs.msg.Twist()

		dx = robot_x - 0
		dy = robot_y - 0

		distance = math.sqrt(dx ** 2 + dy **2)

		#print distance
		#cmd.linear.x = 1
		#cmd.angular.z = 0.5*turn

		leftturn(cmd)

		#rightturn(cmd)

		#forward(cmd)

		#number = randint(0, 100)

		time = rospy.get_time()
		print time

		"""
		if time % 3 == 0:
			leftturn(cmd)
			rospy.sleep(3)
		else:
			rightturn(cmd)	
		#print number
		"""
		#if number == 10:
		#	leftturn(cmd)
		#elif number == 20:
		#	rightturn(cmd)
		#else:
		#	forward(cmd)	

	
		pub.publish(cmd)

if __name__ == '__main__':

	try:
		robotNavigation()
	except rospy.ROSInterruptException:
		pass