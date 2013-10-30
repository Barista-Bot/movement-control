#!/usr/bin/env python

from movement.srv import *
import rospy
from math import sqrt, pow, atan2
import tf2_ros
from std_msgs.msg import String
from geometry_msgs.msg import Twist, PointStamped

def moveIt(i):
  frequency = 20
  timeToUser = 6
  minDistance = 0.4
  minAngle = 0.09
  maxLinearSpeed = 0.3
  maxAngularSpeed = 0.52

  buf = tf2_ros.Buffer()
  listener = tf2_ros.TransformListener(buf)

  pub = rospy.Publisher('cmd_vel', Twist)
  
  rate = rospy.Rate(frequency)
  rospy.Time()

  timeout = 0.1
  originFrame = 'torso_1'
  destFrame = 'base_link'

  while not rospy.is_shutdown():
    
    linearSpeed = 0.0
    angularSpeed = 0.0
    
    okay = buf.lookup_transform(destFrame, originFrame, rospy.Time.now() - rospy.Duration(timeout), rospy.Duration(timeout))

    if okay:
      transformInput = PointStamped()
      transformOutput = PointStamped()

      transformInput.header.frame_id = originFrame
      transformInput.header.stamp = rospy.Time(0)

      transformInput.point.x = 0.0
      transformInput.point.y = 0.0
      transformInput.point.z = 0.0

      listener.transformPoint(destFrame, transformInput, transformOutput)

      distance = sqrt(pow(output.point.x, 2) + pow(output.point.y, 2))

      angle = atan2(output.point.y, output.point.x)

      #code from tutorials, don't touch that or everything dies
      if (abs(angle) > minAngle):
        angularSpeed = abs(angle*frequency / timeToUser);

        angularSpeed = min(angularSpeed, maxAngularSpeed)

        if (angle < 0):
          angularSpeed = -angularSpeed

      if (distance > minDistance):
        linearSpeed = distance * frequency / timeToUser

        linearSpeed = min(linearSpeed, maxLinearSpeed)

    msg = Twist()

    msg.linear.x = linearSpeed
    msg.angular.z = angularSpeed

  return movementResponse(okay, 'DONE MAYBE BUT NO PROMISES')

def movement_server():
  rospy.init_node('movement')
  rospy.Service('movement', movement, moveIt)

  rospy.spin()

if __name__ == '__main__':
  movement_server()
