#!/usr/bin/env python

import roslib; roslib.load_manifest('movement')
# Load (import) rospy
import rospy

# Load sonarArray message from p2os
from p2os_driver.msg import SonarArray

# Load PointCloud from sensor_msgs
from movement.msg import Stop

class SonarStop:

    #Sonar positions
    #(hardcoded, but maybe they should be determined at runtime)


    # the CLASS initialization code
    def __init__(self, x_scale = 1.0, y_scale = 1.0):

        self.sonar_positions = [
            +1.570796326794897,
            +0.872664625997165,
            +0.523598775598299,
            +0.174532925199433,
            -0.174532925199433,
            -0.523598775598299,
            -0.872664625997165,
            -1.570796326794897,
            -1.570796326794897,
            -2.268928027592628,
            -2.617993877991494,
            -2.967059728390360,
            +2.967059728390360,
            +2.617993877991494,
            +2.268928027592628,
            +1.570796326794897
        ]
        # initialize the node with the name 'joystick_to_cmd_vel'
        rospy.init_node('sonar_stopper')

        # set up a publisher to topic 'cmd_vel' publishing Twist messages
        self.pub = rospy.Publisher('stop_movement', Stop)

        # The following line creates a subcriber to the joystick topic
        # it has 3 arguments:
        #  1. the topic to subscribe to
        #  2. the message type
        #  3. the "callback" function to run when a message is received
        rospy.Subscriber('sonar', SonarArray, self.sonarCallback)

    # this is the callback function
    # it is run whenever a new SonarArray message is received
    def sonarCallback(self, data):

        stopFront = False
        stopBack = False

        sonar_stop = Stop()

        print "Sonar Data Ranges", data.ranges
        
        for r in data.ranges[2:5]:
            if r < 0.5:
                stopFront = True
        for r in data.ranges[10:13]:
            if r  < 0.5:
                stopBack = True

        sonar_stop.stopFront = stopFront
        sonar_stop.stopBack = stopBack
        # Publish the new cmd message using publish
        self.pub.publish(sonar_stop)


    # call this function to start the listener
    def startListener(self):
        # the rospy.spin() member function starts the callbacks
        rospy.spin()


# our main function
if __name__ == '__main__':
    try:
        # instantiate the class and start the listener
        stopper = SonarStop()
        stopper.startListener()
    except rospy.ROSInterruptException:
        pass
