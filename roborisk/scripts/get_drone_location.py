#!/usr/bin/env python

"""
This script has tracks the locatons of the robots and drone within gazebo and hand location. 
Created by Sing-Kai Chiu, July 2016.
"""

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
   location_x = rospy.Publisher('drone_position_x', Float64, queue_size=10)
   location_z = rospy.Publisher('drone_position_z', Float64, queue_size=10)
   location_y = rospy.Publisher('drone_position_y', Float64, queue_size=10)
   orientation_z = rospy.Publisher('drone_orientation', Float64, queue_size=10)

   rate = rospy.Rate(5) # 10hz

   while not rospy.is_shutdown():

      getstate = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
      #rospy.wait_for_service("/gazebo/get_model_state")
      robotState = getstate(model_name="quadrotor")

      #print "\nBelow is the Drone Pose"      
      #print robotState.pose.position

      #print "\nBelow is the Drone Twist - linear"      
      #print robotState.twist.linear

      #print "\nBelow is the Drone Twist - angular"      
      #print robotState.twist.angular

      #print "\nBelow is the Drone Orientation"      
      print robotState.pose.orientation.z


      x = robotState.pose.orientation.x
      y = robotState.pose.orientation.y
      w = robotState.pose.orientation.w
      oz = robotState.pose.orientation.z      

      yaw = math.asin(2*x*y + 2*oz*w)

      pi = math.pi
      degree = yaw *(180.0/pi)

      if degree < 0:
         degree += 360

      #print degree, z, yaw


      #z = obotState.pose.orientation.z
      #sinz = sin(z)

      #print "\nBelow is the Drone Vector"
      #print robotState.Vector3


      position_z = robotState.pose.position.z
      position_x = robotState.pose.position.x
      position_y = robotState.pose.position.y
      #rospy.loginfo(position_z)

      #print position_z
      location_z.publish(position_z)
      location_y.publish(position_y)      
      location_x.publish(position_x)
      orientation_z.publish(oz)


      #print "return x postion:", robotState.pose.position.x
      #print "return y postion:", robotState.pose.position.y
      #print "return z postion:", robotState.pose.position.z     
      #print "return x linear:", robotState.twist.linear.x
      #print "return y linear:", robotState.twist.linear.y
      #print "return z linear:", robotState.twist.linear.z

      #rospy.loginfo(hello_str)
      #hello_str = "hello world %s" % rospy.get_time()      
      #pub.publish(hello_str)

      rate.sleep()

if __name__ == '__main__':
   try:


      gtracker()
   except rospy.ROSInterruptException:
      pass
