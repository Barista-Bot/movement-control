#!/usr/bin/env python

import rospy

from std_msgs.msg import Bool
from geometry_msgs.msg import Twist

class MovementFilter(): 

    def __init__(self):
        rospy.init_node('movement_filter')
        
        rospy.Subscriber('js_cmd_vel', Twist, self.cmdVelCallback)
        rospy.Subscriber('stop_movement', Bool, self.stopCallback)
        self.cmd_pub = rospy.Publisher('cmd_vel', Twist)
        self.stopAllMovement = 0

    def cmdVelCallback(self, data):
        if not self.stopAllMovement:
            self.cmd_pub.publish(data)
        else:
            rospy.logerr("STOPPING ALL MOVEMENT")

    def stopCallback(self, stop):
        self.stopAllMovement = stop

    def runFilter(self, rate=10):
        rospy.loginfo("Starting movement filter")
        r = rospy.Rate(rate)
        try:
            while not rospy.is_shutdown():
                r.sleep()
        except rospy.ROSInterruptException:
            pass

            return

if __name__ == '__main__':
    mf = MovementFilter()
    mf.runFilter()
