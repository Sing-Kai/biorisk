#!/usr/bin/env python
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

def findDistance():

	rospy.init_node('capture_robot')
	capture = rospy.Publisher('capture_signal',Bool, queue_size = 1)
	rate = rospy.Rate(5.0)

	capture_signal = False
	
	#rospy.sleep(5)

	while not rospy.is_shutdown():

		getState = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
		droneState = getState(model_name="quadrotor")
		robotState = getState(model_name="jackal")

		# robot coordinates and orientatoin in gazebo
		robot_z = robotState.pose.position.z
		robot_x = robotState.pose.position.x
		robot_y = robotState.pose.position.y
		robot_oz = robotState.pose.orientation.z           
		
		# drone coordinates and orientatoin in gazebo
		drone_x = droneState.pose.position.x
		drone_y = droneState.pose.position.y
		drone_z = droneState.pose.position.z

		dx = drone_x - robot_x
		dy = drone_y - robot_y

		robot_range = findRange(dx, dy)
		now = rospy.Time.now()

		five_seconds = rospy.Duration(5)
		count_to_five = now + five_seconds

		while robot_range < 1.0:
			timer = rospy.Time.now()
			dx = drone_x - robot_x
			dy = drone_y - robot_y
			robot_range = findRange(dx, dy)

			if count_to_five <= timer:
				
				capture_signal = True
				capture.publish(capture_signal)
				print "Successful capture", capture_signal
									
			#print now.secs, timer.secs, count_to_three.secs
			capture_signal = False

		#if capture_signal:
		#	print "Failed to capture robot"

if __name__ == '__main__':

	# subcribe to drone position 
	#rospy.Subscriber('drone_position_x', Float64, get_drone_x)
	#rospy.Subscriber('drone_position_y', Float64, get_drone_y)
	#rospy.Subscriber('drone_position_z', Float64, get_drone_z)	

	# subcribe to robot position 
	#rospy.Subscriber('robot_position_x', Float64, get_robot_x)		
	#rospy.Subscriber('robot_position_y', Float64, get_robot_y)
	#rospy.Subscriber('robot_position_z', Float64, get_robot_z)

	try:
		findDistance()
	except rospy.ROSInterruptException:
		pass