#!/usr/bin/env python
import roslib; roslib.load_manifest('movement')

import sys

import rospy
from movement.srv import *

def movement_client():
  rospy.wait_for_service('movement')
  try:
    movementServer = rospy.ServiceProxy('movement', movement)
    return movementServer(1)
  except rospy.ServiceException, e:
    print "Service call failed: %s"%e

if __name__ == '__main__':
  movement_client()
