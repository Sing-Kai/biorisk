#!/usr/bin/env python

# node only used for presentation demo

import rospy
import math
import tf
import time

import random
from std_msgs.msg import Float64, Bool
from gazebo_msgs.srv import GetModelState
from geometry_msgs.msg import Twist, Vector3

set_number = 1
main_goal_x, main_goal_y = 1.6, 3.8

#hide_goal_x, hide_goal_y =  1.1 , -2.3

#set_number = 2
#main_goal_x, main_goal_y = 0.9, -2.5
#hide_goal_x, hide_goal_y =  4.8 , 3.7

#set_number = 3
#main_goal_x, main_goal_y =  0.5, 3.9
#hide_goal_x, hide_goal_y =  7.0 , 3.7

#set_number = 4
#main_goal_x, main_goal_y = 2.3, 0.5
#hide_goal_x, hide_goal_y =  8.8 , -4.3

#set_number = 5
#main_goal_x, main_goal_y = -1.0, 2.5
#hide_goal_x, hide_goal_y =  4.7 , 6.1

#set_number = 6
#main_goal_x, main_goal_y = -0.0, 2.2
#hide_goal_x, hide_goal_y =  9.8 , -4.1

#set_number = 7
#main_goal_x, main_goal_y = 2.1, -7.6	
#hide_goal_x, hide_goal_y =  -1.7 , -9.9

#set_number = 8
#main_goal_x, main_goal_y = -7.9, -4.3
#hide_goal_x, hide_goal_y =  -3.2 , 9.6

#set_number = 9
#main_goal_x, main_goal_y = 9.6, -5.5
#hide_goal_x, hide_goal_y =  7.3 , -8.7

#set_number = 10
#main_goal_x, main_goal_y = -1.8, 7.5
#hide_goal_x, hide_goal_y =  0.7 , -2.5

#set_number = 11
#main_goal_x, main_goal_y = 4.7, 7.4 
#hide_goal_x, hide_goal_y =  -4.8 , -1.3

#set_number = 12
#main_goal_x, main_goal_y = 0.6, 4.2 
#hide_goal_x, hide_goal_y =  -0.7 , 1.9

#set_number = 13
#main_goal_x, main_goal_y = 4.7, -4.1
#hide_goal_x, hide_goal_y =  -3.7 , 4.3

#set_number = 14
#main_goal_x, main_goal_y = 3.9, 7.1
#hide_goal_x, hide_goal_y =  -2.5 , 1.1	

#set_number = 15
#main_goal_x, main_goal_y = 2.6, -5.4
#hide_goal_x, hide_goal_y =  9.3 , 9.8

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

proximity_para_x = 2
proximity_para_y = 2

#hide_goal_x = 0.0
#hide_goal_y = 0.0

flight_count = 0

# log details of experiment
def printSimulationDetails():

	global escape_linearSpeed, escape_angularSpeed, sim_time
	global goal_linearSpeed, goal_angularSpeed, relative_distance

	print "Simulation Finished", sim_time
	print "Final Relative Distance", relative_distance
	print "escape speed:", escape_linearSpeed, escape_angularSpeed
	print "base speed:", goal_linearSpeed, goal_angularSpeed
	print " "

def finalDetails():

	printSimulationDetails()

def get_risk(data):

	global total_risk	
	total_risk = data.data	

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

def get_relative_distance(data):

	global relative_distance
	relative_distance = data.data

def get_robot_orientation(data):
	
	global robot_orientation
	robot_orientation = data.data

def get_sim_time(data):

	global sim_time
	sim_time = data.data

def get_distance(data):

	global distance
	distance = data.data 

def callback_capture(data):

   global capture_signal

   capture_signal = data.data


# decides on the direction and the magnitue of proximity maintenance
def directionGoal(x, y):

	#print robot_x, robot_y, drone_x, drone_y

	selectAxis = 0

	proximity_x = x
	proximity_y = y

	# if 0 false keep y constant and if 1 true then keey x constant
	selectAxis = randomXYaxis()

	dx = drone_x - robot_x
	dy = drone_y - robot_y

	proximity_goal_x = 0
	proximity_goal_y = 0 

	if (-1 <= dx <= 1) and drone_y > robot_y:
		#print "scenario 5, -ve y"   
		proximity_y = -(proximity_y)
		selectAxis = 0
		proximity_goal_x, proximity_goal_y = proximityXY(proximity_x, proximity_y, selectAxis)

	elif (-1 <= dx <= 1) and drone_y < robot_y:
		#print "scenario 6, +ve y"
		selectAxis = 0
		proximity_goal_x, proximity_goal_y = proximityXY(proximity_x, proximity_y, selectAxis)

	elif drone_x > robot_x and (-1 <= dy <= 1):
		#print "scenario 7, -ve x"
		proximity_x = -(proximity_x)
		selectAxis = 1
		proximity_goal_x, proximity_goal_y = proximityXY(proximity_x, proximity_y, selectAxis)

	elif drone_x < robot_x and (-1 <= dy <= 1): 
		#print "scenario 8 +ve x"
		selectAxis = 1
		proximity_goal_x, proximity_goal_y = proximityXY(proximity_x, proximity_y, selectAxis)

	elif drone_x < robot_x and drone_y < robot_y:
		#print "scenario 1, +ve x or +ve y"
		proximity_goal_x, proximity_goal_y = proximityXY(proximity_x, proximity_y, selectAxis)

	elif drone_x > robot_x and drone_y > robot_y:
		#print "scenario 2, -ve x or -ve y"
		proximity_x = -(proximity_x)
		proximity_y = -(proximity_y)
		proximity_goal_x, proximity_goal_y = proximityXY(proximity_x, proximity_y, selectAxis)

	elif drone_x < robot_x and drone_y > robot_y:   
		#print "scenario 3, +ve x or -ve y"  
		proximity_y = -(proximity_y) 
		proximity_goal_x, proximity_goal_y = proximityXY(proximity_x, proximity_y, selectAxis)

	elif drone_x > robot_x and drone_y < robot_y:
		#print "scenario 4, -ve x or +ve y"  
		proximity_x = -(proximity_x)
		proximity_goal_x, proximity_goal_y = proximityXY(proximity_x, proximity_y, selectAxis)

	#print "these are still showing as float!", int(proximity_goal_x), int(proximity_goal_y)
	return int(proximity_goal_x), int(proximity_goal_y)


# random protean fleeing 
def proteanGoal():

	for i in range(2):
		randx = random.randint(2, 3)
		randy = random.randint(2, 3)

		subgoalx, subgoaly = directionGoal(randx, randy)

		print "Protean flight", randx, randy, subgoalx, subgoaly, i
		proximity_goal(subgoalx, subgoaly)

#selects x or y axises for fleeing
def randomXYaxis():

	number = random.randint(0, 1)

	return number

def randomXY(robot_x, robot_y):

	min_x = robot_x + 1
	max_x = robot_x + 6
	x = random.randint(1,6)
	y = random.randint(1,6)
	return x, y

# function used for selecting random postional goal for proximty maintenance and protean fleeing
def proximityXY(proximity_x, proximity_y, selectAxis):

	#off set current robot location proximity
	x = int(robot_x) + proximity_x # robot location
	y = int(robot_y) + proximity_y

	rx = round(robot_x)
	ry = round(robot_y)
	# produce random y coordinates with fixed x  
	if selectAxis: # test randomXYais function

		y_min = ry - proximity_y
		y_max = ry + proximity_y

		y_min, y_max = switch(y_min, y_max)

	#print y_min, y_max
		#print "keep x constant and vary y"
		y = random.randint(y_min, y_max)

	# produce random y coordinates with fixed x
	else:
		x_min = rx - proximity_x
		x_max = rx + proximity_x

		x_min, x_max = switch(x_min, x_max)

		#print x_min, x_max
		#print "keep y constant and vary x"
		x = random.randint(x_min, x_max)

	#print x, y
	return x, y

def switch(min_v, max_v):

	temp_v = 0

	if min_v > max_v:
		temp_v = max_v
		max_v = min_v
		min_v = temp_v

	return min_v, max_v

def goalCheck(goal_distance):

	if goal_distance < 0.5:
		return True

	return False		

# check if robot has reached goal or has been captured
def checkMainGoal():

	getmodel = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
	data = getmodel('jackal','')

	robot_x = data.pose.position.x
	robot_y = data.pose.position.y

	relative_x = main_goal_x - robot_x
	relative_y = main_goal_y - robot_y
	goal_distance = math.sqrt(relative_x ** 2 + relative_y ** 2) # Distance from Robot

	if goal_distance <= 0.5:
		print "Main goal accomplished"
		finalDetails()
		return True

	elif capture_signal is True:
		print "Captured"
		finalDetails()
		return True

	elif checkTime() is False:
		print "Simulation time is up"	
		finalDetails()
		return True

	return False	

def stopNav():

	return 0.0, 0.0

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
		if 5.9 < total_risk :
			pub.publish(Vector3(0.0,0.0,0.0),Vector3(0.0,0.0,0.0))
			keepLoop = False
		#Correct angle
		while abs(math.atan2(y - data.pose.position.y,x - data.pose.position.x) - phi) > 0.1 : 
			
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
	
def proximity_goal(x, y):

	global escape_angularSpeed, escape_linearSpeed, sim_time, flight_count

	getmodel = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
	data = getmodel('jackal','')
	pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1,latch=True)
	phi = math.atan2(2*(data.pose.orientation.w*data.pose.orientation.z + data.pose.orientation.x*data.pose.orientation.y), 1 - 2*(math.pow(data.pose.orientation.y,2)+math.pow(data.pose.orientation.z,2)))
	keepLoop = True

	angularSpeed = escape_angularSpeed
	linearSpeed = escape_linearSpeed

	flight_count += 1

	while (abs(y - data.pose.position.y) > 0.5 or abs(x - data.pose.position.x) > 0.5) and keepLoop:

		if capture_signal:
			print "Robot captured whilst fleeing", sim_time
			pub.publish(Vector3(0.0,0.0,0.0),Vector3(0.0,0.0,0.0))
			keepLoop = False		

		#Correct angle
		while round(abs(math.atan2(y - data.pose.position.y,x - data.pose.position.x) - phi),1) > 0.2 : 

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
	

# checks how many times robot has flight response, once reached a threshold permantly increase base speed
def flight_counter():

	global flight_count, goal_linearSpeed

	if 2 <= flight_count:
		goal_linearSpeed = 1.0


def checkTime():

	global sim_time, max_time

	if sim_time <= max_time:	
		return True
	#print "time is up"
	return False		

def mainGoal():

	global main_goal_x, main_goal_y, relative_distance, set_number

	print "Current set:", set_number

	stop = False

	while not stop:

		#stop = checkTime()
		
		flight_counter()
		subgoalx, subgoaly = main_goal_x, main_goal_y
		moveuntilreached(0.0, 0.0)

		#test hiding:
		# testing protean fleeing
#		if 5 < total_risk < 10:
#			subgoalx, subgoaly = directionGoal(proximity_para_x, proximity_para_y)
#			print "Execute Proximity ", sim_time
#			print "Initiated Proximity Distance", relative_distance
#			proximity_goal(subgoalx, subgoaly)

		if 6 < total_risk:
			print "Excute Protean fleeing", sim_time
			print "Initiated Protean Distance", relative_distance
			proteanGoal()

		stop = checkMainGoal()
		#print stop

if __name__ == '__main__':

	pub = rospy.Publisher('cmd_vel', Twist, queue_size = 1)
	rospy.init_node('teleop_twist_robot')

	rospy.Subscriber('drone_position_x', Float64, get_drone_x)
	rospy.Subscriber('drone_position_y', Float64, get_drone_y)
	rospy.Subscriber('robot_position_x', Float64, get_robot_x)		
	rospy.Subscriber('robot_position_y', Float64, get_robot_y)
	rospy.Subscriber('robot_orientation', Float64, get_robot_orientation)
	rospy.Subscriber('sim_time', Float64, get_sim_time)
	rospy.Subscriber('capture_signal', Bool, callback_capture)
	rospy.Subscriber('total_risk', Float64, get_risk)
	rospy.Subscriber('relative_distance', Float64, get_relative_distance)
	
	try:

		mainGoal()
	except rospy.ROSInterruptException:
		pass