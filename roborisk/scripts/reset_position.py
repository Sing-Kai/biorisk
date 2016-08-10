#!/usr/bin/env python

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

robot_drone_distance = 0.0
robot_goal_distance = 0.0

# test below list
#set 1
#random.seed(40) # goal: 9.2 3.3, goal distance: 11.0, robot to drone: 15.0
#set 2
#random.seed(20) # goal: -4.8 2.7,  goal distance: 13.0,  robot to drone: 5.0 # check if too close
#set 3
#random.seed(96) # goal: 6.4 5.2,  goal distance: 9.0,  robot to drone: 14.0
#set 4
#random.seed(33) # goal: 3.0 7.8,  goal distance: 5.0,  robot to drone: 9.0 # check if too close
#set 5
#random.seed(30) # goal: -5.8 -4.9,  goal distance: 7.0,  robot to drone: 13.0,
#set 6
#random.seed(75) # goal: 3.5 3.4,  goal distance: 7.0,  robot to drone: 11.0
#set 7
#random.seed(58) # goal: -9.2 -1.0,  goal distance: 12.0,  robot to drone: 15.0
#set 8
#random.seed(63) # goal: -8.3 5.0,  goal distance: 12.0,  robot to drone: 10.0
#set 9
#random.seed(12) # goal: -9.8 -2.5,  goal distance: 11.0, robot to drone: 11.0
#set 10
random.seed(88) # goal: 0.5 3.9,  goal distance: 10.0,  robot to drone: 13.0

#list of seeds and coordinates
"""
random.seed( 0 ) #  robot: 6.9 5.2  drone: -1.6 -4.8  goal: 0.2 -1.9  goal distance: 10.0  robot to drone: 13.0
random.seed( 7 ) #  robot: -3.5 -7.0  drone: 3.0 -8.6  goal: 0.7 -2.7  goal distance: 6.0  robot to drone: 7.0
random.seed( 8 ) #  robot: -5.5 9.2  drone: -7.5 4.1  goal: -8.3 -5.1  goal distance: 15.0  robot to drone: 5.0
random.seed( 9 ) #  robot: -0.7 -2.5  drone: -7.2 7.3  goal: -9.9 0.1  goal distance: 10.0  robot to drone: 12.0
random.seed( 12 ) #  robot: -0.5 3.1  drone: 3.3 -7.1  goal: -9.8 -2.5  goal distance: 11.0  robot to drone: 11.0
random.seed( 13 ) #  robot: -4.8 3.7  drone: 3.7 7.0  goal: -6.3 -5.4  goal distance: 9.0  robot to drone: 9.0
random.seed( 14 ) #  robot: -7.9 4.1  drone: 3.0 8.8  goal: -4.6 -4.9  goal distance: 10.0  robot to drone: 12.0
random.seed( 17 ) #  robot: 0.4 6.1  drone: 9.2 -4.2  goal: 5.3 4.1  goal distance: 5.0  robot to drone: 14.0
random.seed( 18 ) #  robot: -6.4 3.2  drone: -3.3 -6.0  goal: -0.2 -0.1  goal distance: 7.0  robot to drone: 10.0
random.seed( 19 ) #  robot: 3.5 5.7  drone: 0.4 0.2  goal: -2.1 9.9  goal distance: 7.0  robot to drone: 6.0
random.seed( 20 ) #  robot: 8.1 3.7  drone: 5.3 8.1  goal: -4.8 2.7  goal distance: 13.0  robot to drone: 5.0
random.seed( 24 ) #  robot: 4.2 6.8  drone: -6.3 10.0  goal: -6.1 3.4  goal distance: 11.0  robot to drone: 11.0
random.seed( 27 ) #  robot: 3.0 4.0  drone: 9.1 -6.1  goal: -8.7 6.5  goal distance: 12.0  robot to drone: 12.0
random.seed( 28 ) #  robot: -7.7 -7.4  drone: 1.9 -6.4  goal: -7.4 -0.7  goal distance: 7.0  robot to drone: 10.0
random.seed( 30 ) #  robot: 0.8 -4.2  drone: -9.4 3.1  goal: -5.8 -4.9  goal distance: 7.0  robot to drone: 13.0
random.seed( 32 ) #  robot: -8.5 -5.7  drone: -3.9 8.0  goal: -0.1 4.4  goal distance: 13.0  robot to drone: 14.0
random.seed( 33 ) #  robot: 1.4 2.6  drone: 6.3 -4.5  goal: 3.0 7.8  goal distance: 5.0  robot to drone: 9.0
random.seed( 34 ) #  robot: 0.6 1.7  drone: 6.9 8.0  goal: 7.6 -2.7  goal distance: 8.0  robot to drone: 9.0
random.seed( 36 ) #  robot: -3.4 9.7  drone: 9.2 8.4  goal: 5.8 7.5  goal distance: 9.0  robot to drone: 13.0
random.seed( 40 ) #  robot: -0.8 7.6  drone: -9.4 -4.4  goal: 9.2 3.3  goal distance: 11.0  robot to drone: 15.0
random.seed( 41 ) #  robot: -2.4 -5.4  drone: -6.7 8.3  goal: 1.6 3.8  goal distance: 10.0  robot to drone: 14.0
random.seed( 42 ) #  robot: 2.8 -9.5  drone: -4.5 -5.5  goal: 4.7 3.5  goal distance: 13.0  robot to drone: 8.0
random.seed( 43 ) #  robot: -9.2 3.9  drone: -7.1 -0.7  goal: 3.4 5.9  goal distance: 13.0  robot to drone: 5.0
random.seed( 44 ) #  robot: -1.8 0.8  drone: 7.2 -6.5  goal: -5.5 -9.4  goal distance: 11.0  robot to drone: 12.0
random.seed( 46 ) #  robot: 7.8 -2.0  drone: 1.8 7.2  goal: -5.4 0.3  goal distance: 13.0  robot to drone: 11.0
random.seed( 49 ) #  robot: -8.7 -1.7  drone: -7.8 5.0  goal: 0.2 -9.0  goal distance: 12.0  robot to drone: 7.0
random.seed( 52 ) #  robot: 9.6 -8.9  drone: 4.5 -0.3  goal: 8.8 -1.9  goal distance: 7.0  robot to drone: 10.0
random.seed( 56 ) #  robot: 9.3 1.2  drone: -0.5 0.5  goal: 5.4 9.8  goal distance: 9.0  robot to drone: 10.0
random.seed( 58 ) #  robot: 1.6 -5.9  drone: 2.8 8.9  goal: -9.2 -1.0  goal distance: 12.0  robot to drone: 15.0
random.seed( 63 ) #  robot: -1.1 -4.1  drone: 8.2 -0.3  goal: -8.3 5.0  goal distance: 12.0  robot to drone: 10.0
random.seed( 64 ) #  robot: -0.5 2.6  drone: -1.9 8.4  goal: -9.7 9.8  goal distance: 12.0  robot to drone: 6.0
random.seed( 65 ) #  robot: -1.7 -4.2  drone: 6.9 -1.1  goal: 0.6 1.0  goal distance: 6.0  robot to drone: 9.0
random.seed( 71 ) #  robot: -3.5 2.4  drone: -9.8 9.7  goal: 6.4 10.0  goal distance: 12.0  robot to drone: 10.0
random.seed( 73 ) #  robot: -4.4 0.0  drone: 1.3 -0.8  goal: 1.7 -0.3  goal distance: 6.0  robot to drone: 6.0
random.seed( 75 ) #  robot: -1.0 -1.3  drone: -9.2 5.4  goal: 3.5 3.4  goal distance: 7.0  robot to drone: 11.0
random.seed( 76 ) #  robot: -2.6 9.0  drone: -6.0 -4.1  goal: -1.6 -5.3  goal distance: 14.0  robot to drone: 14.0
random.seed( 78 ) #  robot: 6.3 -8.1  drone: 8.5 4.6  goal: -4.9 -1.5  goal distance: 13.0  robot to drone: 13.0
random.seed( 82 ) #  robot: -7.1 -0.2  drone: 0.1 9.4  goal: 6.2 5.8  goal distance: 15.0  robot to drone: 12.0
random.seed( 83 ) #  robot: -0.1 7.1  drone: -8.2 -2.4  goal: -9.0 3.0  goal distance: 10.0  robot to drone: 12.0
random.seed( 88 ) #  robot: -2.1 -6.2  drone: 8.0 2.5  goal: 0.5 3.9  goal distance: 10.0  robot to drone: 13.0
random.seed( 90 ) #  robot: -5.9 -8.1  drone: 3.2 1.7  goal: 2.7 -2.9  goal distance: 10.0  robot to drone: 13.0
random.seed( 94 ) #  robot: 0.9 -7.5  drone: -4.4 -1.4  goal: -9.7 -0.0  goal distance: 13.0  robot to drone: 8.0
random.seed( 96 ) #  robot: -2.6 8.2  drone: -2.1 -5.9  goal: 6.4 5.2  goal distance: 9.0  robot to drone: 14.0
"""
def create_random():

	global robot_x, robot_y
	global drone_x, drone_y
	global goal_x, goal_y

	robot_x = random.uniform(-10, 10) 
	robot_y = random.uniform(-10, 10)

	drone_x = random.uniform(-10, 10)
	drone_y = random.uniform(-10, 10)

	goal_x = random.uniform(-10, 10) 
	goal_y = random.uniform(-10, 10)

	robot_x = round(robot_x, 1)
	robot_y = round(robot_y, 1)

	drone_x = round(drone_x, 1)
	drone_y = round(drone_y, 1)

	goal_x = round(goal_x, 1)
	goal_y = round(goal_y, 1)

	#print robot_x, robot_y, drone_x, drone_y, goal_x, goal_y

def reset_robot():
	setmodel = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)	
	setmodel(ModelState('jackal',Pose(Point(robot_x,robot_y, 0.0),Quaternion(0.0,0.0,0.0,1.0)),Twist(Vector3(0.0,0.0,0.0),Vector3(0.0,0.0,0.0)),'world'))
	setmodel(ModelState('quadrotor',Pose(Point(drone_x, drone_y, 0.0),Quaternion(0.0,0.0,0.0,1.0)),Twist(Vector3(0.0,0.0,0.0),Vector3(0.0,0.0,0.0)),'world'))

def distanceCheck():

	global robot_drone_distance, robot_goal_distance

	dx = drone_x - robot_x
	dy = drone_y - robot_y

	gx = goal_x - robot_x
	gy = goal_y - robot_y

	robot_drone_distance = math.sqrt(dx ** 2 + dy ** 2)
	robot_goal_distance = math.sqrt(gx ** 2 + gy ** 2)

	#print "drone to robot", round(robot_drone_distance)
	#print "robot to goal", round(robot_goal_distance)

def generateList():

	randomSeedList = []

	for i in range(100):

		random.seed(i)		
		create_random()
		distanceCheck()		

		if (5.0 <= robot_goal_distance <= 15.0) and (5.0 <= robot_drone_distance <= 15.0):
			#print " "
			#print "Keep random seed: ", i
			#print robot_x, robot_y, drone_x, drone_y, goal_x, goal_y
			#print "distance value", robot_goal_distance, robot_drone_distance
			print "random.seed(", i, ")", "# ", "robot:", robot_x, robot_y, " drone:", drone_x, drone_y, " goal:", goal_x, goal_y, " goal distance:", round(robot_goal_distance), " robot to drone:", round(robot_drone_distance)
			#randomSeedList.append(i)

	#print randomSeedList		

def selectRandomSeed():

	seedList = [0, 7, 8, 9, 12, 13, 14, 17, 18, 19, 20, 24, 27, 28, 30, 32, 33, 34, 36, 40, 41, 42, 43, 44, 46, 49, 52, 56, 58, 63, 64, 65, 71, 73, 75, 76, 78, 82, 83, 88, 90, 94, 96]

	for i in range(10):

		element = random.choice(seedList)
		print "random.seed(", element, ")"

if __name__ == '__main__':
	
	try:
		create_random()
		#generateList()
		#selectRandomSeed()
		reset_robot()
	except rospy.ROSInterruptException:
		pass

#random list of seeds that fullfil criteria
"""[0, 7, 8, 9, 12, 13, 14, 17, 18, 19, 20, 24, 27, 28, 30, 32, 33, 34, 36, 40, 41, 42, 43, 44, 46, 49, 52, 56, 58, 63, 64, 65, 71, 73, 75, 76, 78, 82, 83, 88, 90, 94, 96]"""
