#!/usr/bin/env python


# reset drone and robot location, only used for demostration

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

drone_x = -5.0
drone_y = -5.0


def reset_robot():
	setmodel = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)	
	setmodel(ModelState('jackal',Pose(Point(robot_x,robot_y, 0.0),Quaternion(0.0,0.0,0.0,1.0)),Twist(Vector3(0.0,0.0,0.0),Vector3(0.0,0.0,0.0)),'world'))
	setmodel(ModelState('quadrotor',Pose(Point(drone_x, drone_y, 0.0),Quaternion(0.0,0.0,0.0,1.0)),Twist(Vector3(0.0,0.0,0.0),Vector3(0.0,0.0,0.0)),'world'))

if __name__ == '__main__':
	
	try:
		reset_robot()
	except rospy.ROSInterruptException:
		pass

