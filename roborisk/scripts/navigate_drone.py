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

	rate = rospy.Rate(10.0)
	while not rospy.is_shutdown():

		angularSpeed = 2.0

		relative_x = robot_x - drone_x
		relative_y = robot_y - drone_y

		relative_x2 = drone_x - robot_x
		relative_y2 = drone_y - robot_y


		relative_angle = math.atan2(relative_y, relative_x)
		quaternion = tf.transformations.quaternion_from_euler(0, 0, relative_angle)
		quaternion_z = quaternion[2]
	

		angular = math.atan2(relative_y, relative_x)

		linear = math.sqrt(relative_x ** 2 + relative_y ** 2) # Distance from Robot


		drone_angle = math.atan2(drone_y, drone_x) * (180.0/math.pi)

		cmd = geometry_msgs.msg.Twist()
		cmd.linear.z = z*0.5				

		"""
		q = (0.0, 0.0, drone_orientation, 0.0)
		euler = tf.transformations.euler_from_quaternion(q)
		roll = euler[0]
		pitch = euler[1]
		yaw = euler[2]

		r_angle = math.radians(yaw)
		"""



		if round(drone_z) == 2:
			z = 0

		robot_qz = round(quaternion_z, 2)
		drone_qz = round(drone_orientation, 2)

		#relative_angle = relative_angle * (180.0/math.pi)

		ninty = robot_qz - 0.01
		hundredten = robot_qz + 0.01


		d_r = robot_qz - drone_qz

		"""
		if robot_qz < 0:
			robot_qz = -robot_qz
		"""
		
		if -0.1 <= d_r <= 0.1:

		#if robot_qz == drone_qz:
			cmd.angular.z = 0.0 
			cmd.linear.x = 0.5
			#print "it's facing the robot"

		elif robot_qz < drone_qz:

			#cmd.angular.z -= angularSpeed
			cmd.angular.z = angularSpeed * (-0.5)
			#cmd.linear.x = 0.8

		elif robot_qz > drone_qz:

			#cmd.angular.z += angularSpeed
			cmd.angular.z = angularSpeed * (0.5)
			#cmd.linear.x = 0.8		

		elif -(robot_qz) > -(drone_qz):

			#cmd.angular.z -= angularSpeed
			cmd.angular.z = angularSpeed * (-0.5)
			#cmd.linear.x = 0.8
		
		else:
			#cmd.angular.z -= angularSpeed
			cmd.angular.z = angularSpeed * (-0.5)

			#cmd.linear.x = 0.8
		


		print robot_qz, drone_qz, relative_angle, d_r

		pub.publish(cmd)

if __name__ == '__main__':

	try:
		#print "test1"
		pursuit()
	except rospy.ROSInterruptException:
		pass