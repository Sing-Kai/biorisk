#!/usr/bin/env python
import rospy

from std_msgs.msg import Float64

def risk_test():

	pub = rospy.Publisher('risk_score',Float64, queue_size = 1)
	rospy.init_node('test_risk')

	rate = rospy.Rate(20)

	while not rospy.is_shutdown():

		risk_score = 4
		#print "risk score is ", risk_score
		pub.publish(risk_score)

if __name__ == '__main__':

	try:
		risk_test()
	except rospy.ROSInterruptException:
		pass