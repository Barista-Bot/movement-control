#!/usr/bin/env python

from movement.srv import *
import rospy
from math import sqrt, pow, atan2
from tf import TransformListener
from std_msgs.msg import String
from geometry_msgs.msg import Twist, PointStamped

def main():
  frequency = 20
  timeToUser = 6
  minDistance = 0.4
  minAngle = 0.09
  maxLinearSpeed = 0.3
  maxAngularSpeed = 0.52

  rospy.init_node('movement')

  listener = tf.TransformListener()

  pub = rospy.Publisher('cmd_vel', Twist)
  
  rate = rospy.Rate(frequency)

  timeout = 0.1
  originFrame = 'torso_1'
  destFrame = 'base_link'

  while not rospy.is_shutdown():
    
    linearSpeed = 0.0
    angularSpeed = 0.0
    
    okay = listener.waitForTransform(destFrame, originFrame, rospy.Time.now() - rospy.Duration(timeout), ros.Duration(timeout))

    if okay:
      transformInput = PointStamped()
      transformOutput = PointStamped()

      transformInput.header.frame_id = originFrame
      transformInput.header.stamp = rospy.Time(0)

      transformInput.point.x = 0.0
      transformInput.point.y = 0.0
      transformInput.point.z = 0.0

      listener.transformPoint(destFrame, transformInput, transformOutput)

      distance = sqrt(pow(output.point.x, 2) + pow(output.point.y, 2)

      angle = atan2(output.point.y, output.point.x)

      if (abs(angle) > minAngle):
        angularSpeed = abs(angle*frequency / timeToUser);

        angularSpeed = min(angularSpeed, maxAngularSpeed)

        if (angle < 0)
          angularSpeed = -angularSpeed

      if (distance > minDistance):
        linearSpeed = distance * frequency / timeToUser

        linearSpeed = min(linearSpeed, maxLinearSpeed)

    msg = Twist()

    msg.linear.x = linearSpeed
    msg.angular.z = angularSpeed

    rospy.spin()
    rate.sleep()

if __name__ == '__main__':
  main()
