#!/usr/bin/env python

import roslib; roslib.load_manifest('movement')
import rospy
from math import sqrt, pow, atan2
import tf
from std_msgs.msg import String
from geometry_msgs.msg import Twist, PointStamped
import sys, traceback

from voice_control.srv import *

class robot():
    """docstring for robot"""
    def __init__(self, frequency=20, timeToUser=6, minDistance=0.4, 
        minAngle=0.09, maxLinearSpeed=0.3, maxAngularSpeed=0.52):

        super(robot, self).__init__()
        self.frequency = frequency
        self.timeToUser = timeToUser
        self.minDistance = minDistance
        self.minAngle = minAngle
        self.maxLinearSpeed = maxLinearSpeed
        self.maxAngularSpeed = maxAngularSpeed
        
        self.linearSpeed = 0.0
        self.angularSpeed = 0.0

        rospy.init_node('movement')

        self.HasCamera = rospy.get_param('~noxtion')



    def publish(self, linearSpeed, angularSpeed):
        pub = rospy.Publisher('cmd_vel', Twist)
        msg = Twist()

        msg.linear.x = linearSpeed
        msg.angular.z = angularSpeed

        pub.publish(msg)

        print 'Linear Speed ' + str(linearSpeed)
        print 'Angular Speed ' + str(angularSpeed)
        print '------------------------'

        return 0

    def computeSpeed(self, distance, angle):
        if (abs(angle) > self.minAngle):
            self.angularSpeed = abs(angle*self.frequency/self.timeToUser)
            self.angularSpeed = min(angularSpeed, self.maxAngularSpeed)

        if (angle < 0):
            self.angularSpeed = -self.angularSpeed

        if (distance > self.minDistance):
            self.linearSpeed = distance * self.frequency / self.timeToUser
            self.linearSpeed = min(self.linearSpeed, self.maxLinearSpeed)

    def followPerson(self):
        return

    def moveToTarget(self):
        return

    def orientRobot(self):
        return

    def moveIt(self):
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
              rospy.wait_for_service('voice_control')
              srv = rospy.ServiceProxy('voice_control', voice_control)
              try:
                success = voice_control_server()
                print 'Called voice-control, success: ' + str(success)
              except:
                print 'Voice control server failed to respond, call Rich and insult him'

            rate.sleep()

        return 0

    def pretendMoveIt():
        print 'wow so lie'
        print 'such pretend'

      
        rate = rospy.Rate(frequency)

        distance = 2
        angle = 0

        while not rospy.is_shutdown():
            self.linearSpeed, self.angularSpeed = computeSpeed(distance, angle)

            print 'Distance: ' + str(distance)
            print 'Angle: ' + str(angle)
            print '------------------------'
        
            publish(self.linearSpeed, self.angularSpeed)

            if self.linearSpeed == 0 and self.angularSpeed == 0:
                #if we're not moving anymore, call voice-control service
                print 'Contacting voice-control'
                rospy.wait_for_service('voice_control')
                srv = rospy.ServiceProxy('voice_control', voice_control)
                try:
                    success = voice_control_server()
                    print 'Called voice-control, success: ' + str(success)
                except:
                    print 'Voice control server failed to respond, call Rich and insult him'

            distance -= 0.1
            rate.sleep()   

        return 0




