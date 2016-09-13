#!/usr/bin/env python

# node to capture the robot, also has the condition in which drone gives up pursuit

import rospy
import math
import geometry_msgs.msg
from gazebo_msgs.srv import GetModelState
from std_msgs.msg import Float64, Bool


#drone_z = 0.0
#drone_x = 0.0
#drone_y = 0.0
#robot_x = 0.0
#robot_y = 0.0
#robot_z = 0.0

drone_z = 0.0
drone_x = 0.0
drone_y = 0.0
robot_x = 0.0
robot_y = 0.0
robot_z = 0.0
robot_range = 0.0

stopCap = False

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

def findRange(dx, dy):

	global robot_range

	robot_range = 0.0

	robot_range = math.sqrt(dx ** 2 + dy ** 2)

	return robot_range

def hiding(data):

	global stopCap
	stopCap = data.data


# captures robot if in range, drone quites if robot escapes set range
def findDistance():

	rospy.init_node('capture_robot')
	capture = rospy.Publisher('capture_signal',Bool, queue_size = 1)
	quit = rospy.Publisher('quit_signal',Bool, queue_size = 1)
	rospy.Subscriber('capture_stop', Bool, hiding)

	rate = rospy.Rate(5.0)

	capture_signal = False
	capture_attempt = False
	robot_escape = False
	first_attempt = False
	second_attempt = False
	#rospy.sleep(5)

	while not rospy.is_shutdown():

		dx = drone_x - robot_x
		dy = drone_y - robot_y

		robot_range = findRange(dx, dy)
		now = rospy.Time.now()

		#seconds taken to capture robot
		total_seconds = rospy.Duration(1)
		count_sec = now + total_seconds

		# initialize attempt to capture
		if robot_range < 3.0:
			capture_attempt = True
			print "Attempting to capture", robot_range, capture_attempt

		# if robot escapes range then stop drone navigation
		if capture_attempt and (robot_range >= 3.0):
			first_attempt = True
			quit.publish(first_attempt)
			print "first attempt", first_attempt

		# check to see if robot is in range and time to be capture
		if stopCap:
			capture_signal = False
			capture.publish(capture_signal)
		else:
			while robot_range < 2.5:
				timer = rospy.Time.now()
				dx = drone_x - robot_x
				dy = drone_y - robot_y
				robot_range = findRange(dx, dy)	

				print "in robot_range", robot_range
				
				if count_sec <= timer:				
					capture_signal = True
					capture.publish(capture_signal)
					print "Successful capture", capture_signal
										
				#print now.secs, timer.secs, count_to_three.secs
				capture_signal = False		


		#	print "Failed to capture robot"

if __name__ == '__main__':

	# subcribe to drone position 
	rospy.Subscriber('drone_position_x', Float64, get_drone_x)
	rospy.Subscriber('drone_position_y', Float64, get_drone_y)
	rospy.Subscriber('drone_position_z', Float64, get_drone_z)	

	# subcribe to robot position 
	rospy.Subscriber('robot_position_x', Float64, get_robot_x)		
	rospy.Subscriber('robot_position_y', Float64, get_robot_y)
	rospy.Subscriber('robot_position_z', Float64, get_robot_z)

	try:
		findDistance()
	except rospy.ROSInterruptException:
		pass