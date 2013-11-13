#!/usr/bin/env python

import roslib; roslib.load_manifest('movement')
import rospy
import tf

def transform():
  rospy.init_node('movementtransform')
  
  broadcaster = tf.TransformBroadcaster()

  frequency = 10

  rate = rospy.Rate(frequency)
  #offset variables (change these to adjust for kinect position)
  offsetx = 0.25
  offsety = 0.0
  offsetz = 0.18

  while not rospy.is_shutdown():

    #transform = tf.StampedTransform()
    #transform.setOrigin(tf.Vector3(offsetx, offsety, offsetz))
    
    #q = tf.Quaternion
    #q.setEuler(0.0, 0.0, 0.0) #no rotation needs to be made
    #transform.setRotation(q)

    #transform.frame_id_ = "base_link"
    #transform.child_frame_id_ = "openni_depth_frame"

    frame_id = "base_link"
    child_frame_id = "openni_depth_frame"

    broadcaster.sendTransform((offsetx, offsety, offsetz), tf.transformations.quaternion_from_euler(0,0,0), rospy.Time.now(), frame_id, child_frame_id)

    rate.sleep()

if __name__ == '__main__':
  transform()
