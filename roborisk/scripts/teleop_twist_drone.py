#!/usr/bin/env python
import roslib; roslib.load_manifest('teleop_twist_keyboard')
import rospy
import math
import tf
import geometry_msgs.msg

from std_msgs.msg import Float64


speed = .5
turn = 1
max_height = 2.0
drone_z = 0.0
drone_x = 0.0
drone_y = 0.0
drone_orientation = 0.0
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

def get_drone_orientation(data):
	
	global drone_orientation
	drone_orientation = data.data


def pursuit():

	pub = rospy.Publisher('/drone/cmd_vel', geometry_msgs.msg.Twist, queue_size = 1)
	rospy.init_node('teleop_twist_drone')

	# subcribe to drone position 
	rospy.Subscriber('drone_position_x', Float64, get_drone_x)
	rospy.Subscriber('drone_position_y', Float64, get_drone_y)
	rospy.Subscriber('drone_position_z', Float64, get_drone_z)	
	rospy.Subscriber('drone_orientation', Float64, get_drone_orientation)	

	# subcribe to robot position 
	rospy.Subscriber('robot_position_x', Float64, get_robot_x)		
	rospy.Subscriber('robot_position_y', Float64, get_robot_y)
	rospy.Subscriber('robot_position_z', Float64, get_robot_z)

	x = 0
	y = 0
	z = 1
	th = 0

	origin_x = 0
	origin_y = 0

	rate = rospy.Rate(5.0)
	while not rospy.is_shutdown():

		angularSpeed = 5.0

		relative_x = robot_x - drone_x
		relative_y = robot_y - drone_y

		relative_angle = math.atan2(relative_y, relative_x)
		quaternion = tf.transformations.quaternion_from_euler(0, 0, relative_angle)
		quaternion_z = quaternion[2]

		angular = math.atan2(relative_y, relative_x)

		linear = math.sqrt(relative_x ** 2 + relative_y ** 2) # Distance from Robot


		cmd = geometry_msgs.msg.Twist()
		cmd.linear.z = z*0.5				

		if round(drone_z) == 2:
			z = 0

		robot_qz = round(quaternion_z, 1)
		drone_qz = round(drone_orientation, 1)

		if robot_qz == drone_qz:

			cmd.angular.z = 0.0 
			cmd.linear.x = 1
			print "it's facing the robot"

		elif robot_qz < drone_qz:

			cmd.angular.z = angularSpeed * (-0.8)
			cmd.linear.x = 0.8

		elif robot_qz > drone_qz:

			cmd.angular.z = angularSpeed * (0.8)
			cmd.linear.x = 0.8		

		elif -(robot_qz) > -(drone_qz):

			cmd.angular.z = angularSpeed * (-0.8)
			cmd.linear.x = 0.8
		
		else:
			cmd.angular.z = angularSpeed * (-0.8)
			cmd.linear.x = 0.8

		pub.publish(cmd)

if __name__ == '__main__':

	try:
		#print "test1"
		pursuit()
	except rospy.ROSInterruptException:
		pass