#!/usr/bin/env python
import rospy
import math
import tf
import geometry_msgs.msg
import random
from std_msgs.msg import Float64
from gazebo_msgs.srv import GetModelState

speed = .5
turn = 1
max_height = 2.0
drone_z = 0.0
drone_x = 0.0
drone_y = 0.0
robot_orientation = 0.0
robot_x = 0.0
robot_y = 0.0
robot_z = 0.0
distance = 0.0
main_goal_x = 3.0
main_goal_y = -3.0

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

def get_robot_orientation(data):
	
	global robot_orientation
	robot_orientation = data.data

def get_distance(data):

	global distance
	distance = data.data 

def directionGoal(x, y):

	print robot_x, robot_y, drone_x, drone_y

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
		print "scenario 5, -ve y"   
		proximity_y = -(proximity_y)
		selectAxis = 0
		proximity_goal_x, proximity_goal_y = proximityXY(proximity_x, proximity_y, selectAxis)

	#if round(drone_x) == round(robot_x) and drone_y < robot_y:
	elif (-1 <= dx <= 1) and drone_y < robot_y:
		print "scenario 6, +ve y"
		selectAxis = 0
		proximity_goal_x, proximity_goal_y = proximityXY(proximity_x, proximity_y, selectAxis)

	elif drone_x > robot_x and (-1 <= dy <= 1):
		print "scenario 7, -ve x"
		proximity_x = -(proximity_x)
		selectAxis = 1
		proximity_goal_x, proximity_goal_y = proximityXY(proximity_x, proximity_y, selectAxis)

	elif drone_x < robot_x and (-1 <= dy <= 1): 
		print "scenario 8 +ve x"
		selectAxis = 1
		proximity_goal_x, proximity_goal_y = proximityXY(proximity_x, proximity_y, selectAxis)

	elif drone_x < robot_x and drone_y < robot_y:
		print "scenario 1, +ve x or +ve y"
		proximity_goal_x, proximity_goal_y = proximityXY(proximity_x, proximity_y, selectAxis)

	elif drone_x > robot_x and drone_y > robot_y:
		print "scenario 2, -ve x or -ve y"
		proximity_x = -(proximity_x)
		proximity_y = -(proximity_y)
		proximity_goal_x, proximity_goal_y = proximityXY(proximity_x, proximity_y, selectAxis)

	elif drone_x < robot_x and drone_y > robot_y:   
		print "scenario 3, +ve x or -ve y"  
		proximity_y = -(proximity_y) 
		proximity_goal_x, proximity_goal_y = proximityXY(proximity_x, proximity_y, selectAxis)

	elif drone_x > robot_x and drone_y < robot_y:
		print "scenario 4, -ve x or +ve y"  
		proximity_x = -(proximity_x)
		proximity_goal_x, proximity_goal_y = proximityXY(proximity_x, proximity_y, selectAxis)

	#print "these are still showing as float!", int(proximity_goal_x), int(proximity_goal_y)
	return int(proximity_goal_x), int(proximity_goal_y)

def proteanGoal():

	for i in range(1):
		randx = random.randint(3, 5)
		randy = random.randint(3, 5)

		subgoalx, subgoaly = directionGoal(randx, randy)

		print "protean flight", randx, randy, subgoalx, subgoaly, i
		proximity_goal(subgoalx, subgoaly)


#selects x or y axises for fleeing
def randomXYaxis():

	number = random.randint(0, 1)

	print number

	return number

def randomXY(robot_x, robot_y):

	min_x = robot_x + 1
	max_x = robot_x + 6
	x = random.randint(1,6)
	y = random.randint(1,6)
	return x, y

def proximityXY(proximity_x, proximity_y, selectAxis):

	#proximity_x = -2
	#proximity_y = 2

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
		print "keep x constant and vary y"
		y = random.randint(y_min, y_max)


	#print x, y, x - intial_x, y -intial_y

	# produce random y coordinates with fixed x
	else:
		x_min = rx - proximity_x
		x_max = rx + proximity_x

		x_min, x_max = switch(x_min, x_max)

		#print x_min, x_max
		print "keep y constant and vary x"
		x = random.randint(x_min, x_max)

	print x, y
	return x, y

def switch(min_v, max_v):

	temp_v = 0

	if min_v > max_v:
		temp_v = max_v
		max_v = min_v
		min_v = temp_v

	#print min_v, max_v
	return min_v, max_v

def goalCheck(goal_distance):

	if goal_distance < 0.5:

		return True

	return False		

def checkMainGoal():

	relative_x = main_goal_x - robot_x
	relative_y = main_goal_y - robot_y
	goal_distance = math.sqrt(relative_x ** 2 + relative_y ** 2) # Distance from Robot

	if goal_distance < 0.5:

		print "Main goal accomplished"


def stopNav():

	return 0.0, 0.0

def riskCheck(distance):

	temp = distance

	flee = False

	if temp < 4:
		print "drone is close by", temp
		flee = True

	return flee	

def navigate_goal(goal_x, goal_y):

	#rospy.Subscriber('drone_position_x', Float64, get_drone_x)
	#rospy.Subscriber('drone_position_y', Float64, get_drone_y)
	#rospy.Subscriber('robot_position_x', Float64, get_robot_x)		
	#rospy.Subscriber('robot_position_y', Float64, get_robot_y)
	#rospy.Subscriber('robot_position_z', Float64, get_robot_z)
	#rospy.Subscriber('robot_orientation', Float64, get_robot_orientation)
	#rospy.Subscriber('relative_distance', Float64, get_distance)

	rate = rospy.Rate(10.0)
	keepLoop = True

	while keepLoop:

		getState = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
		robotState = getState(model_name="jackal")

		relative_x = goal_x - robot_x
		relative_y = goal_y - robot_y
		relative_angle = math.atan2(relative_y, relative_x)
		quaternion = tf.transformations.quaternion_from_euler(0, 0, relative_angle)
		quaternion_z = quaternion[2]	

		quaternion = (
		robotState.pose.orientation.x,
		robotState.pose.orientation.y,
		robotState.pose.orientation.z,
		robotState.pose.orientation.w)
		euler = tf.transformations.euler_from_quaternion(quaternion)
		roll = euler[0]
		pitch = euler[1]
		yaw = euler[2]

		yaw = yaw * (180.0/math.pi)
		relative_angle = relative_angle * (180.0/math.pi)
		angle_difference = relative_angle - yaw

		#print round(yaw), round(relative_angle), round(angle_difference)

		goal_distance = math.sqrt(relative_x ** 2 + relative_y ** 2) # Distance from Robot

		cmd = geometry_msgs.msg.Twist()			

		angularSpeed = 4.0
		linearSpeed = 0.5

		# test risk

		if distance <= 4:
			print "drone nearby"
			angularSpeed, linearSpeed = stopNav()
			keepLoop = False

		# checks if goal has been reach and stops process
		
		if goalCheck(goal_distance):
			print "reached goal"
			angularSpeed, linearSpeed = stopNav()
			keepLoop = False


		# edge case when relative again is 180 or -180
		if angle_difference <= -300 or 300 <= angle_difference:
			print "edge case" 
			cmd.angular.z = 0.0 
			cmd.linear.x = linearSpeed

		else:

			if relative_angle - 5 <= yaw <= relative_angle + 5:
				print "heading towards main goal"
				cmd.angular.z = 0.0 
				cmd.linear.x = linearSpeed

			elif relative_angle < yaw:
				cmd.angular.z = angularSpeed * (-0.2)
				#cmd.linear.x = 0.5

			elif relative_angle > yaw:
				cmd.angular.z = angularSpeed * (0.2)
				#cmd.linear.x = 0.5		

			elif -(relative_angle) > -(yaw):
				cmd.angular.z = angularSpeed * (-0.2)
				#cmd.linear.x = 0.5			
			else:
				#cmd.angular.z -= angularSpeed
				cmd.angular.z = angularSpeed * (-0.2)

				#cmd.linear.x = 0.5

		#cmd = nav_direction(cmd, relative_angle, yaw, angle_difference)	
		pub.publish(cmd)

def proximity_goal(goal_x, goal_y):

	rate = rospy.Rate(10.0)
	keepLoop = True

	while keepLoop:

		getState = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
		robotState = getState(model_name="jackal")

		relative_x = goal_x - robot_x
		relative_y = goal_y - robot_y
		relative_angle = math.atan2(relative_y, relative_x)
		quaternion = tf.transformations.quaternion_from_euler(0, 0, relative_angle)
		quaternion_z = quaternion[2]

		quaternion = (
		robotState.pose.orientation.x,
		robotState.pose.orientation.y,
		robotState.pose.orientation.z,
		robotState.pose.orientation.w)
		euler = tf.transformations.euler_from_quaternion(quaternion)
		roll = euler[0]
		pitch = euler[1]
		yaw = euler[2]

		yaw = yaw * (180.0/math.pi)
		relative_angle = relative_angle * (180.0/math.pi)
		angle_difference = relative_angle - yaw

		#print round(yaw), round(relative_angle), round(angle_difference)

		goal_distance = math.sqrt(relative_x ** 2 + relative_y ** 2) # Distance from Robot

		cmd = geometry_msgs.msg.Twist()			

		angularSpeed = 5.0
		linearSpeed = 2.0

		# checks if goal has been reach and stops process
		
		if goalCheck(goal_distance):

			print "reached goal"
			angularSpeed, linearSpeed = stopNav()
			keepLoop = False
		
		# edge case when relative again is 180 or -180
		if angle_difference <= -300 or 300 <= angle_difference:

			print "edge case" 

			cmd.angular.z = 0.0 
			cmd.linear.x = linearSpeed

		else:

			if relative_angle - 5 <= yaw <= relative_angle + 5:

				print "Fleeing mode"
				cmd.angular.z = 0.0 
				cmd.linear.x = linearSpeed

			elif relative_angle < yaw:

				cmd.angular.z = angularSpeed * (-0.2)
				#cmd.linear.x = 0.5

			elif relative_angle > yaw:

				cmd.angular.z = angularSpeed * (0.2)
				#cmd.linear.x = 0.5		

			elif -(relative_angle) > -(yaw):

				cmd.angular.z = angularSpeed * (-0.2)
				#cmd.linear.x = 0.5
			
			else:
				#cmd.angular.z -= angularSpeed
				cmd.angular.z = angularSpeed * (-0.2)

				#cmd.linear.x = 0.5		
		pub.publish(cmd)

def mainGoal():

	global main_goal_x, main_goal_y, distance
	rospy.Subscriber('relative_distance', Float64, get_distance)
	print "starting main goal"
	while not rospy.is_shutdown():

		rospy.sleep(1)

		global distance
		#angularSpeed = 2.0
		#linearSpeed = 0.5

		subgoalx, subgoaly = main_goal_x, main_goal_y
		navigate_goal(subgoalx, subgoaly)

		#print "stopped main", distance

		
		if distance <= 1:
			print "initiate proximity ", distance	

			subgoalx, subgoaly = directionGoal(2, 2)
			proximity_goal(subgoalx, subgoaly)

		if distance <= 4:
			"""
			randx = random.randint(3, 5)
			randy = random.randint(3, 5)

			subgoalx, subgoaly = directionGoal(randx, randy)

			print "protean flight", randx, randy, subgoalx, subgoaly
			proximity_goal(subgoalx, subgoaly)
			"""
			proteanGoal()

		checkMainGoal()	
		
	checkMainGoal(main_goal_x, main_goal_y, robot_x, robot_y)

if __name__ == '__main__':

	pub = rospy.Publisher('cmd_vel', geometry_msgs.msg.Twist, queue_size = 1)
	rospy.init_node('teleop_twist_robot')

	rospy.Subscriber('drone_position_x', Float64, get_drone_x)
	rospy.Subscriber('drone_position_y', Float64, get_drone_y)
	rospy.Subscriber('robot_position_x', Float64, get_robot_x)		
	rospy.Subscriber('robot_position_y', Float64, get_robot_y)
	rospy.Subscriber('robot_position_z', Float64, get_robot_z)
	rospy.Subscriber('robot_orientation', Float64, get_robot_orientation)
	rospy.Subscriber('relative_distance', Float64, get_distance)
	print distance
	try:
		#print "test1"
		mainGoal()
	except rospy.ROSInterruptException:
		pass