To run this:
Write the python code you want, then run. Good luck :)

Launch files:
-------------
* main.launch - starts all the nodes intended to run with the main robot: xtion input and calculations, movement commands and filter. The joystick nodes are not included, as they are meant to be ran on a different computer. INCLUDE THIS IN THE MAIN LAUNCH FILE (note: we now run openni_tracker manually, because it needs to be restarted once in a while)  
* joystick.launch - starts all the joystick nodes. RUN THOSE ON THE REMOTE COMPUTER
* runall.launch - starts absolutely everything in one place, used for testing with one laptop on the robot
* controlwithjoystick.launch - starts the robot and makes it follow joystick commands. RUN THIS ON ITS OWN TO MOVE THE ROBOT AROUND


* xtion.launch, filter.launch, p3at.launch - includes, do not run these unless you know what you are doing

Important:
----------
If there is an error with ros:time when running this node, you will need to:  
    
    git clone https://github.com/ros/geometry_experimental.git  
into your catkin workspace and run catkin_make  

Every time the robot is plugged in, you will need to run:  

    sudo chmod 777 /dev/ttyUSB0  
Replace 0 by whatever device you need if necessary (and set the correct one in p3at.launch)  
