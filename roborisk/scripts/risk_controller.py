#!/usr/bin/env python
import rospy
import math
import geometry_msgs.msg

from std_msgs.msg import Float64

sound_risk = 0.0
distance_risk = 0.0
battery_life = 0.0
speed_risk = 0.0

max_sound = 8.0
max_distance = 14.0
max_speed = 0.6
max_battery = 100

def get_sound_risk(data):

	global sound_risk
	sound_risk = data.data

def get_distance_risk(data):

	global distance_risk
	distance_risk = data.data	

def get_speed_risk(data):

	global speed_risk
	speed_risk = data.data	

def  get_battery_life(data):

	global battery_life
	battery_life = data.data	

def get_percentage(value, max_value):

	percentage = 0.0

	if value > 0.0:
		percentage = value/max_value

	return percentage	

def riskController():

	pub = rospy.Publisher('total_risk',Float64, queue_size = 1)
	rospy.init_node('risk_controller')

	total_risk = 0.0
	rate = rospy.Rate(5.0)
	while not rospy.is_shutdown():

		percentage_sound = get_percentage(sound_risk, max_sound)
		percentage_distance = get_percentage(distance_risk, max_sound)
		percentage_speed = get_percentage(speed_risk, max_speed)
		percentage_battery = get_percentage(battery_life, max_battery)

		# test
		#percentage_sound = get_percentage(4, max_sound)
		#percentage_distance = get_percentage(7, max_sound)
		#percentage_speed = get_percentage(0.3, max_speed)
		#percentage_battery = get_percentage(0.0, max_battery)

		#print round(sound_risk), round(distance_risk), battery_life, speed_risk
		
		total_risk = percentage_sound + percentage_distance + percentage_battery + percentage_speed

		#convert total risk into a overall percentage
		total_risk = (total_risk/4.0) * 100

		print round(percentage_sound, 2), round(percentage_distance, 2), round(percentage_battery, 2), round(percentage_speed, 2), round(total_risk, 2)

		pub.publish(total_risk)

if __name__ == '__main__':

	rospy.Subscriber('sound_risk', Float64, get_sound_risk)
	rospy.Subscriber('distance_risk', Float64, get_distance_risk)
	rospy.Subscriber('speed_risk', Float64, get_speed_risk)	
	rospy.Subscriber('battery_life', Float64, get_battery_life)

	try:
		riskController()
	except rospy.ROSInterruptException:
		pass