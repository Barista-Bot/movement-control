To run this:
Write the python code you want, then run. Good luck :)

Launch files:
    main.launch - starts all the nodes intended to run with the main robot: xtion input and calculations, movement commands and filter. The joystick nodes are not included, as they are meant to be ran on a different computer. Include this in the main launch file.
    runall.launch - starts absolutely everything in one place, used for testing with one laptop on the robot.
    xtion.launch - starts the xtion nodes: openni_tracker, movement_alt and transforms
    joystick.launch - starts the joystick nodes
    filter.launch - starts the filter that handles all movement commands (this is needed when running joystick or xtion alone)
    p3at.launch - starts the motors, allows the computer to control the robot
