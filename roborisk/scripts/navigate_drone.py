#!/usr/bin/env python
import roslib; roslib.load_manifest('teleop_twist_keyboard')
import rospy
import math
import tf
import geometry_msgs.msg

from std_msgs.msg import Float64, Bool
from gazebo_msgs.srv import GetModelState


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
quit = False

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

def drone_quit(data):

	global quit
	quit = data.data

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

	# subscribe to quit signal
	rospy.Subscriber('quit_signal', Bool, drone_quit)
	height_speed_z = 1

	rate = rospy.Rate(10.0)
	while not rospy.is_shutdown():

		getState = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
		droneState = getState(model_name="quadrotor")

		relative_x = robot_x - drone_x
		relative_y = robot_y - drone_y

		relative_x2 = drone_x - robot_x
		relative_y2 = drone_y - robot_y

		relative_angle = math.atan2(relative_y, relative_x)
		quaternion = tf.transformations.quaternion_from_euler(0, 0, relative_angle)
		quaternion_z = quaternion[2]

		quaternion = (
		droneState.pose.orientation.x,
		droneState.pose.orientation.y,
		droneState.pose.orientation.z,
		droneState.pose.orientation.w)
		euler = tf.transformations.euler_from_quaternion(quaternion)
		roll = euler[0]
		pitch = euler[1]
		yaw = euler[2]

		yaw = yaw * (180.0/math.pi)
		relative_angle = relative_angle * (180.0/math.pi)
		angle_difference = relative_angle - yaw
	
		cmd = geometry_msgs.msg.Twist()
		cmd.linear.z = height_speed_z * 0.5				
		angularSpeed = 0.4
		linearSpeed = 0.5
		linearRotationSpeed = 0.3

		if quit:
			angularSpeed = 0.0
			linearSpeed = 0.0
			linearRotationSpeed = 0.0
			print quit

		# limit drone height
		if round(drone_z) == 2:
			height_speed_z = 0

		# drone navigation - move towards robot it is facing it else rotate until it faces robot
		if angle_difference <= -300 or 300 <= angle_difference:
			#print "edge case" 
			cmd.angular.z = 0.0 
			cmd.linear.x = linearSpeed

		else:

			if relative_angle - 5 <= yaw <= relative_angle + 5:
				#print "heading towards main goal"
				cmd.angular.z = 0.0 
				cmd.linear.x = linearSpeed

			elif relative_angle < yaw:
				cmd.angular.z = angularSpeed * (-1.0)
				cmd.linear.x = linearRotationSpeed

			elif relative_angle > yaw:
				cmd.angular.z = angularSpeed * (1.0)
				cmd.linear.x = linearRotationSpeed		

			elif -(relative_angle) > -(yaw):
				cmd.angular.z = angularSpeed * (-1.0)
				cmd.linear.x = linearRotationSpeed			
			else:
				cmd.angular.z = angularSpeed * (-1.0)
				cmd.linear.x = linearRotationSpeed

		#print robot_qz, drone_qz, relative_angle, d_r

		pub.publish(cmd)

if __name__ == '__main__':

	try:
		pursuit()
	except rospy.ROSInterruptException:
		pass