#!/usr/bin/env python

# ROS node which produced the random seeds for hiding location

import rospy
import random
import math
from gazebo_msgs.srv import SetModelState
from gazebo_msgs.msg import ModelState
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Point
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Vector3

robot_x = 0.0 
robot_y = 0.0

drone_x = 0.0
drone_y = 0.0

goal_x = 0.0 
goal_y = 0.0

hide_goal_x = 0.0
hide_goal_y = 0.0

robot_drone_distance = 0.0
robot_goal_distance = 0.0
drone_goal_distance = 0.0
goal_hide_distance = 0.0

# test below list
# set 1
random.seed(41) #  robot: -2.4 -5.4  drone: -6.7 8.3  goal: 1.6 3.8  robot to goal: 10.0  robot to drone: 14.0 drone to goal: 9.0

# set 2
#random.seed(72) #  robot: -8.5 1.9  drone: 9.8 -3.1  goal: 0.9 -2.5  robot to goal: 10.0  robot to drone: 19.0 drone to goal: 9.0

# set 3
#random.seed(88) #  robot: -2.1 -6.2  drone: 8.0 2.5  goal: 0.5 3.9  robot to goal: 10.0  robot to drone: 13.0 drone to goal: 8.0

#set 4
#random.seed(121) #  robot: -8.3 1.7  drone: -2.0 8.3  goal: 2.3 0.5  robot to goal: 11.0  robot to drone: 9.0 drone to goal: 9.0

# set 5
#random.seed(147) #  robot: 2.1 -7.0  drone: 8.9 -1.2  goal: -1.0 2.5  robot to goal: 10.0  robot to drone: 9.0 drone to goal: 11.0

# set 6
#random.seed(162) #  robot: -8.9 8.1  drone: -5.9 -6.0  goal: -0.0 2.2  robot to goal: 11.0  robot to drone: 14.0 drone to goal: 10.0

# set 7
#random.seed(164) #  robot: -8.1 -4.0  drone: 8.9 -0.7  goal: 2.1 -7.6  robot to goal: 11.0  robot to drone: 17.0 drone to goal: 10.0

# set 8
#random.seed(219) #  robot: 4.0 -3.2  drone: -9.2 4.3  goal: -7.9 -4.3  robot to goal: 12.0  robot to drone: 15.0 drone to goal: 9.0

# set 9
#random.seed(253) #  robot: 0.8 -2.4  drone: 7.3 3.0  goal: 9.6 -5.5  robot to goal: 9.0  robot to drone: 8.0 drone to goal: 9.0

# set 10
#random.seed(286) #  robot: -0.2 -3.7  drone: -8.6 4.2  goal: -1.8 7.5  robot to goal: 11.0  robot to drone: 12.0 drone to goal: 8.0

# set 11
#random.seed(347) #  robot: -3.0 -0.6  drone: 7.8 -0.1  goal: 4.7 7.4  robot to goal: 11.0  robot to drone: 11.0 drone to goal: 8.0

# set 12
#random.seed(372) #  robot: -7.7 9.6  drone: 4.9 -5.2  goal: 0.6 4.2  robot to goal: 10.0  robot to drone: 19.0 drone to goal: 10.0

# set 13
#random.seed(416) #  robot: -4.9 -9.8  drone: 1.6 3.3  goal: 4.7 -4.1  robot to goal: 11.0  robot to drone: 15.0 drone to goal: 8.0

# set 14
#random.seed(453) #  robot: -5.3 0.7  drone: 3.3 -2.3  goal: 3.9 7.1  robot to goal: 11.0  robot to drone: 9.0 drone to goal: 9.0

# set 15
#random.seed(455) #  robot: 8.1 4.5  drone: -2.4 1.3  goal: 2.6 -5.4  robot to goal: 11.0  robot to drone: 11.0 drone to goal: 8.0


def create_random():

	global robot_x, robot_y
	global drone_x, drone_y
	global goal_x, goal_y
	global hide_goal_x, hide_goal_y

	robot_x = random.uniform(-10, 10) 
	robot_y = random.uniform(-10, 10)

	drone_x = random.uniform(-10, 10)
	drone_y = random.uniform(-10, 10)

	goal_x = random.uniform(-10, 10) 
	goal_y = random.uniform(-10, 10)

	hide_goal_x = random.uniform(-10, 10)
	hide_goal_y = random.uniform(-10, 10)

	robot_x = round(robot_x, 1)
	robot_y = round(robot_y, 1)

	drone_x = round(drone_x, 1)
	drone_y = round(drone_y, 1)

	goal_x = round(goal_x, 1)
	goal_y = round(goal_y, 1)

#	hide_goal_x = round(hide_goal_x, 1)	
#	hide_goal_y = round(hide_goal_y, 1)

	#print robot_x, robot_y, drone_x, drone_y, goal_x, goal_y

def reset_robot():
	setmodel = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)	
	setmodel(ModelState('jackal',Pose(Point(robot_x,robot_y, 0.0),Quaternion(0.0,0.0,0.0,1.0)),Twist(Vector3(0.0,0.0,0.0),Vector3(0.0,0.0,0.0)),'world'))
	setmodel(ModelState('quadrotor',Pose(Point(drone_x, drone_y, 0.0),Quaternion(0.0,0.0,0.0,1.0)),Twist(Vector3(0.0,0.0,0.0),Vector3(0.0,0.0,0.0)),'world'))

def distanceCheck():

	global robot_drone_distance, robot_goal_distance, drone_goal_distance, goal_hide_distance

#	dx = drone_x - robot_x
#	dy = drone_y - robot_y#

#	gx = goal_x - robot_x
#	gy = goal_y - robot_y#

#	dgx = goal_x - drone_x
#	dgy = goal_y - drone_y

	dhx = goal_x - hide_goal_x
	dhy = goal_y - hide_goal_y

#	robot_drone_distance = math.sqrt(dx ** 2 + dy ** 2)
#	robot_goal_distance = math.sqrt(gx ** 2 + gy ** 2)
#	drone_goal_distance = math.sqrt(dgx ** 2 + dgy ** 2)
	goal_hide_distance = math.sqrt(dhx ** 2 + dhy ** 2)

	#print "drone to robot", round(robot_drone_distance)
	#print "robot to goal", round(robot_goal_distance)

def generateList():

	randomSeedList = []

	for i in range(500):

		random.seed(i)		
		create_random()
		distanceCheck()		
		"""
		if (6.0 <= goal_hide_distance <= 11.0):
			#print " "
			print "Keep random seed: ", i
			#print robot_x, robot_y, drone_x, drone_y, goal_x, goal_y
			#print "distance value", robot_goal_distance, robot_drone_distance
			#print "#random.seed(", i, ")", "# ", "robot:", robot_x, robot_y, " drone:", drone_x, drone_y, " goal:", goal_x, goal_y, " robot to goal:", round(robot_goal_distance), " robot to drone:", round(robot_drone_distance), "drone to goal:", round(drone_goal_distance)
			print "random hide goal is:", hide_goal_x, hide_goal_y, goal_hide_distance
			randomSeedList.append(i)
		"""

		print i, "hide_goal_x, hide_goal_y = ", round(hide_goal_x, 1), ",", round(hide_goal_y, 1)
	#print randomSeedList		

# select random seeds that fulfill critera
def selectRandomSeed():

	seedList = [0, 7, 8, 9, 12, 13, 14, 17, 18, 19, 20, 24, 27, 28, 30, 32, 33, 34, 36, 40, 41, 42, 43, 44, 46, 49, 52, 56, 58, 63, 64, 65, 71, 73, 75, 76, 78, 82, 83, 88, 90, 94, 96]

	for i in range(10):

		element = random.choice(seedList)
		print "random.seed(", element, ")"


if __name__ == '__main__':
	
	try:
		#create_random()
		generateList()
		#selectRandomSeed()
		#reset_robot()
	except rospy.ROSInterruptException:
		pass

