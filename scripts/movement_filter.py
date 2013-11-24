#!/usr/bin/env python

import rospy

from movement.msg import Stop
from geometry_msgs.msg import Twist

class MovementFilter(): 

    def __init__(self):
        rospy.init_node('movement_filter')
        
        rospy.Subscriber('xt_cmd_vel', Twist, self.xtionCallback)
        rospy.Subscriber('js_cmd_vel', Twist, self.joystickCallback)
        rospy.Subscriber('stop_movement', Stop, self.stopCallback)
        self.cmd_pub = rospy.Publisher('cmd_vel', Twist)
        self.cmdVel = Twist()
        self.jsCmdVel = Twist()
        self.xtCmdVel = Twist()
        self.stopMovement = []
        self.stopMovement.append(False)
        self.stopMovement.append(False)

    def publishCmdVel(self):
        if abs(self.jsCmdVel.linear.x)>0 or abs(self.jsCmdVel.angular.z)>0:
            self.cmdVel = self.jsCmdVel
        else:
            self.cmdVel = self.xtCmdVel
            self.cmd_pub.publish(self.cmdVel)
        
        if self.cmdVel.linear.x == 0 and self.cmdVel.angular.z == 0:
            self.cmd_pub.publish(self.cmdVel)
        elif self.cmdVel.linear.x < 0 and not self.stopMovement[1]:
            rospy.loginfo('Publishing backward move command')
            self.cmd_pub.publish(self.cmdVel)

        elif (self.cmdVel.linear.x > 0 or abs(self.cmdVel.angular.z) > 0) and not self.stopMovement[0]:
            rospy.loginfo('Publishing forward move command')
            self.cmd_pub.publish(self.cmdVel)
        else:
            rospy.logwarn("Movement is not allowed, staying in position")
    
    def joystickCallback(self, data):
        self.jsCmdVel = data

    def xtionCallback(self, data):
        self.xtCmdVel = data

    def stopCallback(self, stop):
        self.stopMovement[0] = stop.stopFront
        self.stopMovement[1] = stop.stopBack
        rospy.loginfo('Front stop bool updated to ' + str(self.stopMovement[0]) + ' - Back stop bool updated to ' + str(self.stopMovement[1]))

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
