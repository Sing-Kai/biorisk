#!/usr/bin/env python

## node that controls the navigation of the drone, also contains method to check if robot is hding

import rospy
import math
import tf
import geometry_msgs.msg

from std_msgs.msg import Float64, Bool
from gazebo_msgs.srv import GetModelState


# assumption hiding locaiton of robot is known to drone
#set_number = 1
#hide_x, hide_y =  1.1 , -2.3

#set_number = 2
#hide_x, hide_y =  4.8 , 3.7

#set_number = 3
#hide_x, hide_y =  7.0 , 3.7

#set_number = 4
#hide_x, hide_y =  8.8 , -4.3

#set_number = 5
#hide_x, hide_y =  4.7 , 6.1

#set_number = 6
#hide_x, hide_y =  9.8 , -4.1

#set_number = 7
#hide_x, hide_y =  -1.7 , -9.9

#set_number = 8
#hide_x, hide_y =  -3.2 , 9.6

#set_number = 9
#hide_x, hide_y =  7.3 , -8.7

#set_number = 10
#hide_x, hide_y =  0.7 , -2.5

#set_number = 11
#hide_x, hide_y =  -4.8 , -1.3

#set_number = 12
#hide_x, hide_y =  -0.7 , 1.9

#set_number = 13
#hide_x, hide_y =  -3.7 , 4.3

#set_number = 14
#hide_x, hide_y =  -2.5 , 1.1	

set_number = 15
#hide_x, hide_y =  9.3 , 9.8

hide_x, hide_y =  50.0 , 50.0  # default setting when not testing hiding 

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
robot_hiding = False
leave = False

def is_hiding(data):

	global robot_hiding
	robot_hiding = data.data

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

# check if drone has reached robot hiding location
def robot_reached_hiding():

	global robot_x, robot_y, hide_x, hide_y

	reached_hiding_location = False

	hidingGoal = math.sqrt((hide_x - robot_x) ** 2 + (hide_y - robot_y) ** 2)

	if hidingGoal < 0.5:
		reached_hiding_location = True

	return reached_hiding_location	

#check if robot has reached location of robot
def drone_reached_robot():

	global robot_x, robot_y, drone_x, drone_y

	reachedRobot = False

	distacne = math.sqrt((drone_x - robot_x) ** 2 + (drone_y - robot_y) ** 2)

	if distacne < 2:

		reachedRobot = True

	return reachedRobot

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

	#stop capture if robot is hiding
	stop_capture = rospy.Publisher('capture_stop',Bool, queue_size = 1)

	rospy.Subscriber('hiding', Bool, is_hiding)

	# subscribe to quit signal
	rospy.Subscriber('quit_signal', Bool, drone_quit)
	height_speed_z = 1

	rate = rospy.Rate(10.0)

	leave = False

	while not rospy.is_shutdown():

		getState = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
		droneState = getState(model_name="quadrotor")
		
		reach_hiding = False
		reach_hiding = robot_reached_hiding()
		reachedRobot = drone_reached_robot()

		# activate when robot is hiding
		if robot_hiding and reach_hiding: #and reachedRobot:
			#print "time to call it quits"
			leave = True
			#rospy.sleep(3)
			stop_capture.publish(True)
		
		if leave:
			nav_x, nav_y = 15, 15

		else:
			nav_x, nav_y = robot_x, robot_y

		#print nav_x, nav_y
		
		#	activate for no hiding robot
#		nav_x = robot_x
#		nav_y = robot_y

		relative_x = nav_x - drone_x
		relative_y = nav_y - drone_y

		relative_angle = math.atan2(relative_y, relative_x)
		quaternion = tf.transformations.quaternion_from_euler(0, 0, relative_angle)
		quaternion_z = quaternion[2]

		quaternion = (
		droneState.pose.orientation.x,
		droneState.pose.orientation.y,
		droneState.pose.orientation.z,
		droneState.pose.orientation.w)

		# transformation for quaternions to euler
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


		# stops drone navigation if recieves quit signal
		if quit:
			angularSpeed = 0.0
			linearSpeed = 0.0
			linearRotationSpeed = 0.0

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