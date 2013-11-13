#!/usr/bin/env python

import roslib; roslib.load_manifest('movement')
import rospy
from math import sqrt, pow, atan2
import tf
from std_msgs.msg import String
from geometry_msgs.msg import Twist, PointStamped
import sys, traceback

from voice_control.srv import *

frequency = 20
timeToUser = 6
minDistance = 0.4
minAngle = 0.09
maxLinearSpeed = 0.3
maxAngularSpeed = 0.52

def publish(linearSpeed, angularSpeed):

  pub = rospy.Publisher('cmd_vel', Twist)
  msg = Twist()

  msg.linear.x = linearSpeed
  msg.angular.z = angularSpeed

  pub.publish(msg)

  print 'Linear Speed ' + str(linearSpeed)
  print 'Angular Speed ' + str(angularSpeed)
  print '------------------------'

  return 0

def computeSpeed(distance, angle):
  #code from tutorials, don't touch that or everything dies
  linearSpeed = 0
  angularSpeed = 0

  if (abs(angle) > minAngle):
    angularSpeed = abs(angle*frequency / timeToUser);
    angularSpeed = min(angularSpeed, maxAngularSpeed)

  if (angle < 0):
    angularSpeed = -angularSpeed

  if (distance > minDistance):
    linearSpeed = distance * frequency / timeToUser
    linearSpeed = min(linearSpeed, maxLinearSpeed)

  return linearSpeed, angularSpeed

def pretendMoveIt():
  print 'wow so lie'
  print 'such pretend'

  frequency = 20
  timeToUser = 6
  minDistance = 0.4
  minAngle = 0.09
  maxLinearSpeed = 0.3
  maxAngularSpeed = 0.52
  
  rate = rospy.Rate(frequency)

  distance = 2
  angle = 0

  while not rospy.is_shutdown():

    linearSpeed, angularSpeed = computeSpeed(distance, angle)

    print 'Distance: ' + str(distance)
    print 'Angle: ' + str(angle)
    print '------------------------'
    
    publish(linearSpeed, angularSpeed)

    if linearSpeed == 0 and angularSpeed == 0:
      #if we're not moving anymore, call voice-control service
      print 'Contacting voice-control'
      rospy.wait_for_service('voice-control')
      srv = rospy.ServiceProxy('voice-control', voice_control)
      try:
        success = voice_control_server()
        print 'Called voice-control, success: ' + str(success)
      except:
        print 'Voice control server failed to respond, call Rich and insult him'

    distance -= 0.1
    rate.sleep()   

  return 0

def moveIt():
  listener = tf.TransformListener()
  
  rate = rospy.Rate(frequency)

  timeout = 0.1
  originFrame = 'torso_1'
  destFrame = 'base_link'

  while not rospy.is_shutdown():
    
    linearSpeed = 0.0
    angularSpeed = 0.0

    now = rospy.Time(0)
     
    try:
      listener.waitForTransform(destFrame, originFrame, now,  rospy.Duration(timeout))
      (trans, rot) = listener.lookupTransform(destFrame, originFrame, now)
    except:
      traceback.print_exc(file=sys.stdout)
      continue

    tInput = PointStamped()
    tOutput = PointStamped()

    tInput.header.frame_id = originFrame
    tInput.header.stamp = rospy.Time(0)

    tInput.point.x = 0.0
    tInput.point.y = 0.0
    tInput.point.z = 0.0

    tOutput = listener.transformPoint(destFrame, tInput)

    distance = sqrt(pow(tOutput.point.x, 2) + pow(tOutput.point.y, 2))
    angle = atan2(tOutput.point.y, tOutput.point.x)

    linearSpeed, angularSpeed = computeSpeed(distance, angle)

    print 'Distance: ' + str(distance)
    print 'Angle: ' + str(angle)
    print '------------------------'
    
    publish(linearSpeed, angularSpeed)

    if linearSpeed == 0 and angularSpeed == 0:
      #if we're not moving anymore, call voice-control service
      rospy.wait_for_service('voice-control')
      srv = rospy.ServiceProxy('voice-control', voice_control)
      try:
        success = voice_control_server()
        print 'Called voice-control, success: ' + str(success)
      except:
        print 'Voice control server failed to respond, call Rich and insult him'

    rate.sleep()

  return 0

if __name__ == '__main__':
  rospy.init_node('movement')

  value = rospy.get_param('~noxtion')
  if value:
    pretendMoveIt()
  else:
    moveIt()
