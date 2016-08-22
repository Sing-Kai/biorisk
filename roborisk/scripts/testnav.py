#!/usr/bin/env python
import rospy
import math
import tf
import time

import random
from std_msgs.msg import Float64, Bool
from gazebo_msgs.srv import GetModelState
from geometry_msgs.msg import Twist, Vector3

max_time = 180

escape_angularSpeed = 1.0
escape_linearSpeed = 1.0

goal_angularSpeed = 1.0
goal_linearSpeed = 0.5

robot_orientation = 0.0
robot_x = 0.0
robot_y = 0.0
distance = 0.0

drone_x = 0.0
drone_y = 0.0

capture_signal = False
sim_time = 0.0
total_risk = 0.0

relative_distance = 0.0

proximity_para_x = 3
proximity_para_y = 3

flight_count = 0


def moveuntilreached(x,y):

	global goal_angularSpeed, goal_linearSpeed, sim_time

	getmodel = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
	data = getmodel('jackal','')
	pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1,latch=True)
	phi = math.atan2(2*(data.pose.orientation.w*data.pose.orientation.z + data.pose.orientation.x*data.pose.orientation.y), 1 - 2*(math.pow(data.pose.orientation.y,2)+math.pow(data.pose.orientation.z,2)))
	keepLoop = True

	angularSpeed = goal_angularSpeed
	linearSpeed = goal_linearSpeed

	while (abs(y - data.pose.position.y) > 0.5 or abs(x - data.pose.position.x) > 0.5) and keepLoop:

		if capture_signal:
			print "Robot captured whilst navigating to main goal", sim_time
			pub.publish(Vector3(0.0,0.0,0.0),Vector3(0.0,0.0,0.0))
			keepLoop = False		

		# risk test this must match parameters in the mainGoal() function
		if 9.9 < total_risk :
			pub.publish(Vector3(0.0,0.0,0.0),Vector3(0.0,0.0,0.0))
			keepLoop = False
		#Correct angle
		while round(abs(math.atan2(y - data.pose.position.y,x - data.pose.position.x) - phi),1) > 0.2 : 

			testnum = abs(math.atan2(y - data.pose.position.y,x - data.pose.position.x)- phi)

			print testnum #, abs(math.atan2(y - data.pose.position.y,x - data.pose.position.x)) * (180.0/2), phi

			if math.atan2(y - data.pose.position.y,x - data.pose.position.x)  > 0 and phi > 0:
				if math.atan2(y - data.pose.position.y,x - data.pose.position.x) > phi:
					pub.publish(Vector3(0.0,0.0,0.0),Vector3(0.0,0.0,angularSpeed))
					rospy.sleep(0.25)
				else: 
					pub.publish(Vector3(0.0,0.0,0.0),Vector3(0.0,0.0,-angularSpeed))
					rospy.sleep(0.25)
			elif math.atan2(y - data.pose.position.y,x - data.pose.position.x) < 0 and phi < 0:
				if abs(math.atan2(y - data.pose.position.y,x - data.pose.position.x)) > abs(phi):
					pub.publish(Vector3(0.0,0.0,0.0),Vector3(0.0,0.0,-angularSpeed))
					rospy.sleep(0.25)
				else:
					pub.publish(Vector3(0.0,0.0,0.0),Vector3(0.0,0.0,angularSpeed))
					rospy.sleep(0.25)
			elif math.atan2(y - data.pose.position.y,x - data.pose.position.x) > 0 and phi < 0:
				if abs(math.atan2(y - data.pose.position.y,x - data.pose.position.x)) > 1.5 and abs(phi) > 1.5:
					pub.publish(Vector3(0.0,0.0,0.0),Vector3(0.0,0.0,-angularSpeed))
					rospy.sleep(0.25)
				elif abs(math.atan2(y - data.pose.position.y,x - data.pose.position.x)) < 1.5 and abs(phi) < 1.5:
					pub.publish(Vector3(0.0,0.0,0.0),Vector3(0.0,0.0,angularSpeed))
					rospy.sleep(0.25)
				else:
					pub.publish(Vector3(0.0,0.0,0.0),Vector3(0.0,0.0,angularSpeed))
					rospy.sleep(0.25)
			else:
				if abs(math.atan2(y - data.pose.position.y,x - data.pose.position.x)) > 1.5 and abs(phi) > 1.5:
					pub.publish(Vector3(0.0,0.0,0.0),Vector3(0.0,0.0,angularSpeed))
					rospy.sleep(0.25)
				elif abs(math.atan2(y - data.pose.position.y,x - data.pose.position.x)) < 1.5 and abs(phi) < 1.5:
					pub.publish(Vector3(0.0,0.0,0.0),Vector3(0.0,0.0,-angularSpeed))
					rospy.sleep(0.25)
				else:
					pub.publish(Vector3(0.0,0.0,0.0),Vector3(0.0,0.0,angularSpeed))
					rospy.sleep(0.25)
			getmodel = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
			data = getmodel('jackal','')
			phi = math.atan2(2*(data.pose.orientation.w*data.pose.orientation.z + data.pose.orientation.x*data.pose.orientation.y), 1 - 2*(math.pow(data.pose.orientation.y,2)+math.pow(data.pose.orientation.z,2)))
		#Then advance for a bit
		for i in range(0,1):
			pub.publish(Vector3(linearSpeed,0.0,0.0),Vector3(0.0,0.0,0.0))
			rospy.sleep(0.1)

		getmodel = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
		data = getmodel('jackal','')

if __name__ == '__main__':

	pub = rospy.Publisher('cmd_vel', Twist, queue_size = 1)
	rospy.init_node('teleop_twist_robot')

#	rospy.Subscriber('drone_position_x', Float64, get_drone_x)
#	rospy.Subscriber('drone_position_y', Float64, get_drone_y)
#	rospy.Subscriber('robot_position_x', Float64, get_robot_x)		
#	rospy.Subscriber('robot_position_y', Float64, get_robot_y)
#	rospy.Subscriber('robot_orientation', Float64, get_robot_orientation)
#	rospy.Subscriber('sim_time', Float64, get_sim_time)
#	rospy.Subscriber('capture_signal', Bool, callback_capture)
#	rospy.Subscriber('total_risk', Float64, get_risk)
#	rospy.Subscriber('relative_distance', Float64, get_relative_distance)
	
	try:

		moveuntilreached(5, 0)
	except rospy.ROSInterruptException:
		pass