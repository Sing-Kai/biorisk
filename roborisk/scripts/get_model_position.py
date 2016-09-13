#!/usr/bin/env python

#This script  tracks the locatons of the robots and drone within gazebo and hand drone_location. 
#Created by Sing-Kai Chiu, July 2016.


import rospy
import math
from gazebo_msgs.srv import GetModelState
from gazebo_msgs.msg import ModelState
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Point
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Vector3
from std_msgs.msg import String 
from std_msgs.msg import Float64

def gtracker():

   rospy.init_node('get_drone_location')

   # gets drone postion in gazebo world
   drone_position_x = rospy.Publisher('drone_position_x', Float64, queue_size=0)
   drone_position_z = rospy.Publisher('drone_position_z', Float64, queue_size=0)
   drone_position_y = rospy.Publisher('drone_position_y', Float64, queue_size=0)
   drone_orientation_z = rospy.Publisher('drone_orientation', Float64, queue_size=0)


   # gets robot postion in gazebo world
   robot_position_x = rospy.Publisher('robot_position_x', Float64, queue_size=0)
   robot_position_z = rospy.Publisher('robot_position_z', Float64, queue_size=0)
   robot_position_y = rospy.Publisher('robot_position_y', Float64, queue_size=0)
   robot_orientation_z = rospy.Publisher('robot_orientation', Float64, queue_size=0)

   rate = rospy.Rate(10)

   while not rospy.is_shutdown():

      #variable to receive model information from gazebo
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
      drone_oz = droneState.pose.orientation.z 

      # publish robot data
      robot_position_y.publish(robot_y)      
      robot_position_x.publish(robot_x)
      robot_position_z.publish(robot_z)      
      robot_orientation_z.publish(robot_oz)

      # publish drone data
      drone_position_z.publish(drone_z)
      drone_position_y.publish(drone_y)      
      drone_position_x.publish(drone_x)
      drone_orientation_z.publish(drone_oz)

      #print robot_x, robot_y, drone_x, drone_y
      #print robotState.pose.position.x, robotState.pose.position.y
      rate.sleep()

if __name__ == '__main__':
   try:

      gtracker()
   except rospy.ROSInterruptException:
      pass
