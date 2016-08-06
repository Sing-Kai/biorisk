#!/usr/bin/env python
import rospy
import math
import geometry_msgs.msg

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

def get_drone_z(data):

	global drone_z
	drone_z = data.data

#	return drone_z

def get_drone_x(data):

	global drone_x
	drone_x = data.data
#	return drone_x

def get_drone_y(data):

	global drone_y
	drone_y = data.data	

#	return drone_y

def get_robot_x(data):

	global robot_x
	robot_x = data.data

#	return robot_x

def get_robot_y(data):

	global robot_y
	robot_y = data.data	

#	return robot_y

def get_robot_z(data):
	
	global robot_z	
	robot_z = data.data

#	return robot_z

# returns boolean if drone is within distance and time frame of robot
def capture_range(robot_rangex):

	#now = rospy.Time.now()

	global robot_range

	capture_distance = robot_range
	start_counter = True
	capture_robot = False
	#capture_distance = 2

	if robot_range < 3.0:

		now = rospy.Time.now()

		print "in range", robot_range
		while start_counter:

			timer = rospy.Time.now()
			three_seconds = rospy.Duration(5)
			count_to_three = now + three_seconds

			print "robot range is ", robot_range

			if count_to_three < timer:
				#print "time up"
				start_counter = False
				capture_robot = True
			#print now.secs, timer.secs, three_seconds.secs, count_to_three.secs, robot_range

	return capture_robot

def findRange(dx, dy):

	global robot_range

	robot_range = 0.0

	robot_range = math.sqrt(dx ** 2 + dy ** 2)

	return robot_range

def findDistance():

	rospy.init_node('capture_robot')
	capture = rospy.Publisher('capture_signal',Bool, queue_size = 1)
	rate = rospy.Rate(5.0)

	capture_signal = False


	#rospy.sleep(5)

	while not rospy.is_shutdown():

		dx = drone_x - robot_x
		dy = drone_y - robot_y

		robot_range = findRange(dx, dy)
		now = rospy.Time.now()

		three_seconds = rospy.Duration(5)
		count_to_three = now + three_seconds

		while robot_range < 3:
			timer = rospy.Time.now()
			dx = drone_x - robot_x
			dy = drone_y - robot_y
			robot_range = findRange(dx, dy)

			if count_to_three <= timer:
				
				capture_signal = True
				capture.publish(capture_signal)
				print "Successful capture", capture_signal
				
					
			print now.secs, timer.secs, count_to_three.secs
			capture_signal = False

		if capture_signal:
			print "Failed to capture robot"

if __name__ == '__main__':

	# subcribe to drone position 
	rospy.Subscriber('drone_position_x', Float64, get_drone_x)
	rospy.Subscriber('drone_position_y', Float64, get_drone_y)
	#rospy.Subscriber('drone_position_z', Float64, get_drone_z)	

	# subcribe to robot position 
	rospy.Subscriber('robot_position_x', Float64, get_robot_x)		
	rospy.Subscriber('robot_position_y', Float64, get_robot_y)
	#rospy.Subscriber('robot_position_z', Float64, get_robot_z)

	try:
		findDistance()
	except rospy.ROSInterruptException:
		pass