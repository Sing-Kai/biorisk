#!/usr/bin/env python
import rospy
import math
import numpy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64

twist = Twist()

# percentage of increase in velocity
vel_increase = 1
angular_speed = 1
risk_score = 0.0

def callback_risk(data):

    global risk_score

    risk_score = data.data

# adjust velocity according to risk_scoring
def change_vel(risk_score):

	global vel_increase 

	if risk_score <= 3:
		vel_increase = 1.5

	elif risk_score > 3:
		vel_increase = 2.5

	else:
		vel_increase = 2.0

def get_velocity(data):

	global twist
	x = data.linear.x
	y = data.linear.y
	z = data.linear.z
	angular_z = data.angular.z
	twist.linear.x = x * vel_increase
	twist.linear.y = y
	twist.linear.z = z
	twist.angular.z = angular_z * angular_speed

def move_base_velocity():
	rospy.Subscriber('move_base/cmd_vel', Twist, get_velocity)
	rospy.Subscriber('risk_score', Float64, callback_risk)
	pub = rospy.Publisher('cmd_vel',Twist, queue_size = 1)
	rospy.init_node('move_base_vel_update')

	rate = rospy.Rate(20.0)

	#change_vel(1.5)

	while not rospy.is_shutdown():

		change_vel(risk_score)

		#print risk_score, vel_increase

		#print twist.linear.x, twist.angular.z

		pub.publish(twist)

if __name__ == '__main__':
	
	try:
		move_base_velocity()
	except rospy.ROSInterruptException:
		pass