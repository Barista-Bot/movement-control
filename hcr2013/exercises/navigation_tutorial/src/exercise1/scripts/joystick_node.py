#!/usr/bin/env python

# import the rospy library that will allow us to use ROS
import rospy

# import the joystick class 
from common import joystick

# ============= this section is new ===================
# import the JoyAxis message
from exercise1.msg import JoyAxis
# ============= this section is new ===================

# this is our main loop function
def startMainLoop():

    # First initialise the node. 
    # This is *essential* for every ROS node. 
    # the argument is the name of the node, in our case, "joystick_node"
    rospy.init_node("joystick_node")

    # create a new joystick object
    joystick_id = 0 # change this to 1 if you can't seem to control the joystick
    my_joystick = joystick.Joystick(joystick_id)    
    
    # just check that it is initialised
    if not my_joystick.isInit():
        print "Joystick Not Initialised"
        exit()  # exit if it is not ready
        
    # ============= this section is new ===================
    # create a new publisher that publishes JoyAxis messages over 
    # the joystick topic
    pub = rospy.Publisher('joystick', JoyAxis)
    # ============= this section is new ===================   
    
        
    # let's set the rate we want the program to run at 20Hz 
    r = rospy.Rate(20)
    
    # Loop until ros is shutdown
    while not rospy.is_shutdown():

        #we convert the exponential to linear by logging.
        x_val = my_joystick.getXVal()
        y_val = my_joystick.getYVal()

        # ============= this section is new ===================
        # create a new JoyAxis object and populate the data
        jamsg = JoyAxis()
        jamsg.x = x_val
        jamsg.y = y_val
        
        # publish it!
        pub.publish(jamsg)
        # ============= this section is new ===================  


        # log this information
        # ROS will also send this to stdout (print it to the screen)
        # if you are unfamiliar with 
        rospy.loginfo("XY: [" + str(x_val) + ", " + str(y_val) + "]")
        
        # sleep (wait) until it is time to run again (this maintains the 
        # rate of the program at 20Hz)
        r.sleep()


# this is the main function that will run when this python program is executed
if __name__ == '__main__':
    # Start our main loop
    startMainLoop()
