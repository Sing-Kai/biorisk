#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Snippet of code on how to send a navigation goal and how to get the current robot position in map

Navigation actionserver: /move_base/goal
Type of message: move_base_msgs/MoveBaseActionGoal

Actual robot pose topic: /amcl_pose
Type of message: geometry_msgs/PoseWithCovarianceStamped

"""

import rospy
import actionlib
import random
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import PoseWithCovarianceStamped, Quaternion, Twist
from tf.transformations import quaternion_from_euler, euler_from_quaternion
from math import radians, degrees

def create_nav_goal(x, y, yaw):
    """Create a MoveBaseGoal with x, y position and yaw rotation (in degrees).
Returns a MoveBaseGoal"""
    mb_goal = MoveBaseGoal()
    mb_goal.target_pose.header.frame_id = '/map' # Note: the frame_id must be map
    mb_goal.target_pose.pose.position.x = x
    mb_goal.target_pose.pose.position.y = y
    mb_goal.target_pose.pose.position.z = 0.0 # z must be 0.0 (no height in the map)

    # Orientation of the robot is expressed in the yaw value of euler angles
    angle = radians(yaw) # angles are expressed in radians
    quat = quaternion_from_euler(0.0, 0.0, angle) # roll, pitch, yaw
    mb_goal.target_pose.pose.orientation = Quaternion(*quat.tolist())

    return mb_goal

def callback_pose(data):
    """Callback for the topic subscriber.
Prints the current received data on the topic."""
    x = data.pose.pose.position.x
    y = data.pose.pose.position.y
    roll, pitch, yaw = euler_from_quaternion([data.pose.pose.orientation.x,
                                             data.pose.pose.orientation.y,
                                             data.pose.pose.orientation.z,
                                             data.pose.pose.orientation.w])
    rospy.loginfo("Current robot pose: x=" + str(x) + "y=" + str(y) + " yaw=" + str(degrees(yaw)) + "º")
    #print "Current robot pose: x=" + str(x) + "y=" + str(y) + " yaw=" + str(degrees(yaw)) + "º"
    

def random_number():

    number = random.randint(-5, 5)

    return number

def send_goal(nav_gal):

    nav_as.send_goal(nav_goal)
    nav_as.wait_for_result()
    nav_res = nav_as.get_result()

def protean():

    """
    x = random_number()
    y = random_number()

    print x, y

    nav_goal = create_nav_goal(x, y, 0.0)
    send_goal(nav_goal)
    nav_state = nav_as.get_state()

    if nav_state == 3:
        nav_goal = create_nav_goal(0.5, 0.0, 0.0)
        nav_as.send_goal(nav_goal)
        nav_state = nav_as.get_state()
    """
    for i in range(3):

        x = random_number()
        y = random_number()
        print x, y
        nav_goal = create_nav_goal(x, y, 0.0)
        nav_as.send_goal(nav_goal)
        nav_as.wait_for_result()
        nav_res = nav_as.get_result()
        nav_state = nav_as.get_state()
        print "Nav state: ", str(nav_state), i

if __name__=='__main__':
    rospy.init_node("navigation_snippet")

    # Read the current pose topic
    rospy.Subscriber("/amcl_pose", PoseWithCovarianceStamped, callback_pose)

    # Connect to the navigation action server
    nav_as = actionlib.SimpleActionClient('/move_base', MoveBaseAction)
    rospy.loginfo("Connecting to /move_base AS...")
    nav_as.wait_for_server()
    rospy.loginfo("Connected.")

    rospy.loginfo("Creating navigation goal...")

    nav_goal = create_nav_goal(5.5, 0.0, 0.0)#4.72333594438, -0.377168390489, 45) # 3.925197124481201, -3.026911973953247, 0.6259599924087524 livingroom
    nav_as.send_goal(nav_goal)

    rospy.loginfo("Waiting for result...")
    nav_as.wait_for_result()
    nav_res = nav_as.get_result()
    nav_state = nav_as.get_state()
    rospy.loginfo("Done!")
    print "Result: ", str(nav_res) # always empty, be careful
    print "Nav state: ", str(nav_state) # use this, 3 is SUCCESS, 4 is ABORTED (couldnt get there), 5 REJECTED (the goal is not attainable)  

    protean()

    """
    if nav_state == 3:
        nav_goal = create_nav_goal(0.5, 0.0, 0.0)
        nav_as.send_goal(nav_goal)
        nav_state = nav_as.get_state()
        print "2nd Goal Nav state: ", str(nav_state)
    """