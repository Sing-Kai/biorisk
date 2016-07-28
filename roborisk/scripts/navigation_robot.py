#!/usr/bin/env python

import rospy
import geometry_msgs.msg

from gazebo_msgs.srv import SetModelState
from gazebo_msgs.msg import ModelState
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Point
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Vector3

cmd = geometry_msgs.msg.Twist()
pub = rospy.Publisher('cmd_vel', geometry_msgs.msg.Twist, queue_size = 1)

def proximity(distance):

	if distance == 10:
		cmd.linear.x = 1

	if distance < 10:
		cmd.linear.x = -1

	pub.publish(cmd)

def stop(distance):

	if distance == 0:
		cmd.linear.x = 0
		cmd.linear.y = 0
		cmd.linear.z = 0
	pub.publish(cmd)

def backwards():

	cmd.linear.x = -1
	pub.publish(cmd)	

if __name__ == '__main__':
	
	try:
		reset_robot()
	except rospy.ROSInterruptException:
		pass
