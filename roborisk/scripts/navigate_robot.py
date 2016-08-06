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
from gazebo_msgs.srv import GetModelState
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import GoalID
from geometry_msgs.msg import PoseWithCovarianceStamped, Quaternion, Twist
from tf.transformations import quaternion_from_euler, euler_from_quaternion
from math import radians, degrees
from std_msgs.msg import Float64, Bool

risk_score = 0
capture_signal = False

gazebo_x = 0.0
gazebo_y = 0.0

# robot intial start point to calculate relative gmap ordinates 
intial_x = 0.0
intial_y = 0.0

robot_x = 0.0
robot_y = 0.0

drone_x = 0.0
drone_y = 0.0

#parameters for gmapping
max_x = 0.0
max_y = 0.0

mid_x = 0.0
mid_y = 0.0

min_x = 0.0
min_y = 0.0

#goal for gmapping, update to give robot goal
goal_x = 0.0
goal_y = 0.0
goal_z = 0.0

distance = 0.0

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

def callback_capture(data):

    global capture_signal

    capture_signal = data.data

# get risk scoring from risk controller
def callback_risk(data):

    global risk_score

    risk_score = data.data

def get_robot_x(data):

    global robot_x
    robot_x = data.data

#   return robot_x

def get_robot_y(data):

    global robot_y
    robot_y = data.data 

# test purpose
def get_distance(data):

    global distance
    distance = data.data 

def get_drone_x(data):

    global drone_x
    drone_x = data.data

def get_drone_y(data):

    global drone_y
    drone_y = data.data 

# generate random number
def random_number():

    number = random.randint(-5, 5)

    return number

def send_goal(nav_gal):

    nav_as.send_goal(nav_goal)
    nav_as.wait_for_result()
    nav_res = nav_as.get_result()

# protean fleeing behaviour, currently changes random direction 3 times
def protean(risk_score):

    #for i in range(1):

        #x = random_number()
        #y = random_number()

    x, y = directionGoal()
    
    print "robot location", robot_x, robot_y
    print "fleeing goal", x, y

    d_goal = create_nav_goal(x, y, 0.0)
    defence.send_goal(d_goal)
    dnav_state = 1

    while (dnav_state != 3):
        dnav_state = defence.get_state()

        if distance >= 4:
            defence.cancel_all_goals()
            dnav_state = 3

        if capture_signal:
            print "captured, mission failed"
            defence.cancel_all_goals()
            dnav_state = 3

    print "fleeing complete"
    return True    

def cancel_all_goal(goal):

    if capture_signal:
        print "captured"
        goal.cancel_all_goals()    

# translate initial gazebo coordinates parameters to gmapping coordinates parameters
def get_parameters():

    global max_x, max_y, min_x, min_y, mid_x, mid_y
    global intial_x, intial_y

    max_x = 10 - intial_x
    max_y = 10 - intial_y
    min_x = -10 - intial_x
    min_y = -10 - intial_y
    mid_x = 5 - intial_x
    mid_y = 5 - intial_y

    print max_x, max_y, min_x, min_y
 
def navigationMission(goal_x, goal_y, goal_z):

    rospy.Subscriber("/amcl_pose", PoseWithCovarianceStamped, callback_pose)
    print "navigate to main goal"
    nav_goal = create_nav_goal(goal_x, goal_y, goal_z)
    nav_as.send_goal(nav_goal)

    nav_state = 1
    #print "nav_state", nav_state

    while (nav_state != 3):
        #print sx, sy
        nav_state = nav_as.get_state()
        #print nav_state, risk_score

        start_defence_complete = False

        # initialize protean behaviour
        #if risk_score == 4:
        if distance <= 2:
            print "abandon mission, implementing fleeing"
            #nav_as.cancel_all_goals()    
            start_defence_complete = protean(risk_score)              
        
        # once defence is complete return to pursing original goal
        if distance > 2 and start_defence_complete:

            print "returning to mission", goal_x, goal_y
            nav_goal = create_nav_goal(goal_x, goal_y, goal_z)
            nav_as.send_goal(nav_goal)

        if capture_signal:
            print "captured, mission failed"
            nav_as.cancel_all_goals()
            nav_state = 3
    
    if nav_state == 3 and capture_signal == False:

        print "Mission accomplished", nav_state

    #print robot_x, robot_y, drone_x, drone_y

def directionGoal():

    print robot_x, robot_y, drone_x, drone_y

    selectAxis = 0

    proximity_x = 4
    proximity_y = 4

    # if 0 false keep y constant and if 1 true then keey x constant
    selectAxis = randomXYaxis()

    dx = drone_x - robot_x
    dy = drone_y - robot_y

    proximity_goal_x = 0
    proximity_goal_y = 0 

    if (-1 <= dx <= 1) and drone_y > robot_y:
        print "scenario 5, -ve y"   
        proximity_y = -(proximity_y)
        selectAxis = 0
        proximity_goal_x, proximity_goal_y = proximityXY(proximity_x, proximity_y, selectAxis)

    #if round(drone_x) == round(robot_x) and drone_y < robot_y:
    elif (-1 <= dx <= 1) and drone_y < robot_y:
        print "scenario 6, +ve y"
        selectAxis = 0
        proximity_goal_x, proximity_goal_y = proximityXY(proximity_x, proximity_y, selectAxis)

    elif drone_x > robot_x and (-1 <= dy <= 1):
        print "scenario 7, -ve x"
        proximity_x = -(proximity_x)
        selectAxis = 1
        proximity_goal_x, proximity_goal_y = proximityXY(proximity_x, proximity_y, selectAxis)

    elif drone_x < robot_x and (-1 <= dy <= 1): 
        print "scenario 8 +ve x"
        selectAxis = 1
        proximity_goal_x, proximity_goal_y = proximityXY(proximity_x, proximity_y, selectAxis)

    elif drone_x < robot_x and drone_y < robot_y:
        print "scenario 1, +ve x or +ve y"
        proximity_goal_x, proximity_goal_y = proximityXY(proximity_x, proximity_y, selectAxis)

    elif drone_x > robot_x and drone_y > robot_y:
        print "scenario 2, -ve x or -ve y"
        proximity_x = -(proximity_x)
        proximity_y = -(proximity_y)
        proximity_goal_x, proximity_goal_y = proximityXY(proximity_x, proximity_y, selectAxis)

    elif drone_x < robot_x and drone_y > robot_y:       
        print "scenario 3, +ve x or -ve y"  
        proximity_y = -(proximity_y) 
        proximity_goal_x, proximity_goal_y = proximityXY(proximity_x, proximity_y, selectAxis)

    elif drone_x > robot_x and drone_y < robot_y:
        print "scenario 4, -ve x or +ve y"  
        proximity_x = -(proximity_x)
        proximity_goal_x, proximity_goal_y = proximityXY(proximity_x, proximity_y, selectAxis)

    #print "these are still showing as float!", int(proximity_goal_x), int(proximity_goal_y)
    return int(proximity_goal_x), int(proximity_goal_y)

#selects x or y axises for fleeing
def randomXYaxis():

    number = random.randint(0, 1)

    print number

    return number    

def proximityXY(proximity_x, proximity_y, selectAxis):

    global intial_x, intial_y
    #proximity_x = -2
    #proximity_y = 2

    #off set current robot location proximity
    x = int(robot_x) + proximity_x # robot location
    y = int(robot_y) + proximity_y

    rx = round(robot_x)
    ry = round(robot_y)
    # produce random y coordinates with fixed x  
    if selectAxis: # test randomXYais function

        y_min = ry - proximity_y
        y_max = ry + proximity_y

        y_min, y_max = switch(y_min, y_max)

        #print y_min, y_max
        print "keep x constant and vary y"
        y = random.randint(y_min, y_max)

        
        #print x, y, x - intial_x, y -intial_y

    # produce random y coordinates with fixed x
    else:
        x_min = rx - proximity_x
        x_max = rx + proximity_x

        x_min, x_max = switch(x_min, x_max)

        #print x_min, x_max
        print "keep y constant and vary x"
        x = random.randint(x_min, x_max)
        

    print x, y, x - intial_x, y -intial_y
    return x - intial_x, y -intial_y

def switch(min_v, max_v):

    temp_v = 0

    if min_v > max_v:
        temp_v = max_v
        max_v = min_v
        min_v = temp_v

    #print min_v, max_v    
    return min_v, max_v

if __name__=='__main__':
    rospy.init_node("navigation_mission")

    # Read the current pose topic
    #rospy.Subscriber("/amcl_pose", PoseWithCovarianceStamped, callback_pose)
    rospy.Subscriber('capture_signal', Bool, callback_capture)
    rospy.Subscriber('risk_score', Float64, callback_risk)

    rospy.Subscriber('robot_position_x', Float64, get_robot_x)      
    rospy.Subscriber('robot_position_y', Float64, get_robot_y)
    rospy.Subscriber('drone_position_x', Float64, get_drone_x)
    rospy.Subscriber('drone_position_y', Float64, get_drone_y)
    rospy.Subscriber('relative_distance', Float64, get_distance)

    # get drone and robot positions
    """
    getState = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
    robotState = getState(model_name="jackal")
    droneState = getState(model_name="quadrotor")   

    robot_x = robotState.pose.position.x
    robot_y = robotState.pose.position.y
     
    drone_x = droneState.pose.position.x
    drone_y = droneState.pose.position.y
    """

    intial_x = 4.0
    intial_y = 4.0

    #print robot_x, robot_y, drone_x, drone_y
    get_parameters()

    # Connect to the navigation action server
    nav_as = actionlib.SimpleActionClient('/move_base', MoveBaseAction)
    defence = actionlib.SimpleActionClient('/move_base', MoveBaseAction)

    rospy.loginfo("Connecting to /move_base AS...")
    nav_as.wait_for_server()
    rospy.loginfo("Connected.")
    rospy.loginfo("Creating navigation goal...")

    print "goal location is", goal_x, goal_y
    navigationMission(goal_x, goal_y, goal_z)
    #directionGoal()
    #randomXYaxis()
    #proximityXY()
    #switch(2, 6)
