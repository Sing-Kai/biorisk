#!/usr/bin/env python

"""
This script has tracks the locatons of the robots and drone within gazebo and hand location. 
Created by Sing-Kai Chiu, July 2016.
"""

import rospy
import tf

from gazebo_msgs.srv import GetModelState
from gazebo_msgs.msg import ModelState
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Point
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Vector3
from std_msgs.msg import Float64
from std_msgs.msg import String


def gtracker():

   rospy.init_node('get_robot_location')
   location_x = rospy.Publisher('robot_position_x', Float64, queue_size=10)
   location_z = rospy.Publisher('robot_position_z', Float64, queue_size=10)
   location_y = rospy.Publisher('robot_position_y', Float64, queue_size=10)


   rate = rospy.Rate(10) # 10hz

   while not rospy.is_shutdown():

      getstate = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
      rospy.wait_for_service("/gazebo/get_model_state")
      robotState = getstate(model_name="jackal")

      #print "\nBelow is the Pose"        
      #print robotState.pose.position

      position_z = robotState.pose.position.z
      position_x = robotState.pose.position.x
      position_y = robotState.pose.position.y

      #print position_z
      location_z.publish(position_z)
      location_y.publish(position_y)      
      location_x.publish(position_x)

      rate.sleep()

if __name__ == '__main__':
   try:
      gtracker()
   except rospy.ROSInterruptException:
      pass
