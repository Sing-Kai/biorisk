#!/usr/bin/env python
import roslib; roslib.load_manifest('teleop_twist_keyboard')
import rospy
import math
import tf
import geometry_msgs.msg

from std_msgs.msg import Float64
from random import randint
from reset_position import reset_robot
from navigation_robot import proximity
from navigation_robot import stop
from navigation_robot import backwards


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
oz = 0.0

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

def get_orientation_z(data):

	global oz
	oz = data.data


def leftturn(cmd):

	cmd.linear.x = 1
	cmd.angular.z = 0.5*turn

def rightturn(cmd):

	cmd.linear.x = 1
	cmd.angular.z = -0.5*turn	

def forward(cmd):

	cmd.linear.x = 1


def move_to_goal(goalx, goaly, robotx, roboty, cmd):

	if ((goalx * 0.85) <= robotx <= (goalx * 1.015)) and ((goaly * 0.85) <= roboty <= (goaly * 1.015)):

		cmd.linear.x = 0	

		cmd.angular.z = 0.0 
	else:	

		cmd.linear.x = 1	

def move_to_goal2(goalx, goaly, robotx, roboty, cmd):

	if goalx == robotx and goaly <= roboty:

		cmd.linear.x = 0	

		cmd.angular.z = 0.0 
	else:	

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



	#time = rospy.get_time()

	#print time

	rate = rospy.Rate(1.0)

	#cmd = geometry_msgs.msg.Twist()

	#cmd.linear.x = 1
	#cmd.angular.z = 0.5*turn

	#leftturn(cmd)

	distance = 5.0
	time = rospy.get_time()

	goal_x = 1
	goal_y = 1
	
	r_goal_x = goal_x - 0
	r_goal_y = goal_y - 0

	"quaternion of (0, 0 , sin ((angle of robot wrt global frame - angle drone wrt global frame)/2), cos ((angle of robot wrt global frame - angle drone wrt global frame)/2))."

	while not rospy.is_shutdown():
		r_robot_x = robot_x - 0.0
		r_robot_y = robot_y - 0

		r_robot_goal_x = goal_x - robot_x
		r_robot_goal_y = goal_y - robot_y

		rx = robot_x - goal_x
		ry = robot_y - goal_y
		robot_angle = math.atan2(r_robot_y, r_robot_x) * (180.0/math.pi)
		goal_angle = math.atan2(r_goal_y, r_goal_x) * (180.0/math.pi)
		relative_angle = math.atan2(r_robot_goal_y, r_robot_goal_x) * (180.0/math.pi)
		q_angle = math.atan2(r_robot_goal_y, r_robot_goal_x)


		r_angle = math.atan2(r_robot_goal_x, r_robot_goal_y) * (180.0/math.pi)

		sin = math.sin((robot_angle - goal_angle)/2)
		cos = math.cos((robot_angle - goal_angle)/2)

		quaternion = (0.0, 0.0, sin, cos)
		euler = tf.transformations.euler_from_quaternion(quaternion)

		yaw = euler[2]

		quaternion1 = tf.transformations.quaternion_from_euler(0, 0, q_angle)
		quaternion_z = quaternion1[2]

		robot_oz = round(oz, 1)
		goal_oz = round(quaternion_z, 1)

		#print round(relative_angle, 3), round(robot_face_angle, 3), round(difference, 3)
		#print robot_angle, goal_angle, relative_angle
		#print sin, cos, robot_angle, goal_angle, relative_angle
		#print round(robot_angle), round(yaw), goal_angle, round(oz, 2),  round(quaternion_z, 2) #, sin, cos
		#print yaw, oz, relative_angle, quaternion_z
		#dx = robot_x - 0
		#dy = robot_y - 0
		cmd = geometry_msgs.msg.Twist()
		angularSpeed = 1


		if (goal_oz * 0.9) <= robot_oz <= (goal_oz * 1.01):

			cmd.angular.z = 0.0 

			move_to_goal2(goal_x, goal_y, robot_x, robot_y, cmd)
			#cmd.linear.x = 1
			print "it's facing the robot", robot_oz, goal_oz

		elif robot_oz < goal_oz:

			cmd.angular.z = (0.8)
			cmd.linear.x = 0.5
			print "test1"
		elif robot_oz > goal_oz:

			cmd.angular.z = (-0.8)
			cmd.linear.x = 0.5		
			print "test2"
		elif -(robot_oz) > -(goal_oz):

			cmd.angular.z = (0.8)
			cmd.linear.x = 0.5
			print "test3"		
		else:
			cmd.angular.z = (0.8)
			cmd.linear.x = 0.5
			print "test4"
		pub.publish(cmd)
		

if __name__ == '__main__':
	rospy.Subscriber('robot_position_x', Float64, get_robot_x)		
	rospy.Subscriber('robot_position_y', Float64, get_robot_y)
	rospy.Subscriber('robot_orientation', Float64, get_orientation_z)	
	try:
		robotNavigation()
	except rospy.ROSInterruptException:
		pass