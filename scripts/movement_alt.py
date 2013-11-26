#!/usr/bin/env python

import roslib; roslib.load_manifest('movement')
import rospy
import robot_control

if __name__ == "__main__":
    
    rospy.init_node('movement')
    p3at = robot_control.Robot()
    p3at.moveIt()
