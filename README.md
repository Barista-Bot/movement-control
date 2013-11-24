To run this:
Write the python code you want, then run. Good luck :)

Launch files:
-------------
* main.launch - starts all the nodes intended to run with the main robot: xtion input and calculations, movement commands and filter. The joystick nodes are not included, as they are meant to be ran on a different computer. INCLUDE THIS IN THE MAIN LAUNCH FILE
* joystick.launch - starts all the joystick nodes. RUN THOSE ON THE REMOTE COMPUTER
* runall.launch - starts absolutely everything in one place, used for testing with one laptop on the robot
* controlwithjoystick.launch - starts the robot and makes it follow joystick commands. RUN THIS ON ITS OWN TO MOVE THE ROBOT AROUND


* xtion.launch, filter.launch, p3at.launch - includes, do not run these unless you know what you are doing

Important:
----------
If there is an error with ros:time when running this node, you will need to:  
    * git clone https://github.com/ros/geometry_experimental.git  
into your catkin workspace (hopefully this will be fixed in ros-hydro soon)
