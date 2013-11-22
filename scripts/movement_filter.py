#!/usr/bin/env python

import rospy

from std_msgs.msg import Bool
from geometry_msgs.msg import Twist

class MovementFilter(): 

    def __init__(self):
        rospy.init_node('movement_filter')
        
        rospy.Subscriber('xt_cmd_vel', Twist, self.xtionCallback)
        rospy.Subscriber('js_cmd_vel', Twist, self.joystickCallback)
        rospy.Subscriber('stop_movement', Bool, self.stopCallback)
        self.cmd_pub = rospy.Publisher('cmd_vel', Twist)
        self.cmdVel = Twist()
        self.jsCmdVel = Twist()
        self.xtCmdVel = Twist()
        self.stopAllMovement = 0

    def publishCmdVel(self):
        if not self.stopAllMovement:
            if not (self.jsCmdVel.linear.x == 0 and self.jsCmdVel.angular.z == 0):
                self.cmdVel = self.jsCmdVel
            else:
                self.cmdVel = self.xtCmdVel
            self.cmd_pub.publish(self.cmdVel)
        else:
            rospy.logerr("STOPPING ALL MOVEMENT")
    
    def joystickCallback(self, data):
        self.jsCmdVel = data

    def xtionCallback(self, data):
        self.xtCmdVel = data

    def stopCallback(self, stop):
        self.stopAllMovement = stop

    def runFilter(self, rate=10):
        rospy.loginfo("Starting movement filter")
        r = rospy.Rate(rate)
        try:
            while not rospy.is_shutdown():
                self.publishCmdVel()
                r.sleep()
        except rospy.ROSInterruptException:
            pass

            return

if __name__ == '__main__':
    mf = MovementFilter()
    mf.runFilter()
