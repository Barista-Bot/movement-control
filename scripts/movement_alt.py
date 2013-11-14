import robot_control

frequency = 20
timeToUser = 6
minDistance = 0.4
minAngle = 0.09
maxLinearSpeed = 0.3
maxAngularSpeed = 0.52

if __name__ == "__main__":
    p3at = robot(frequency=frequency, timeToUser=timeToUser, minDistance=minDistance,
            minAngle=minAngle, maxLinearSpeed=maxLinearSpeed, maxAngularSpeed=maxAngularSpeed)

    rospy.init_node('movement')

    value = rospy.get_param('~noxtion')
    if value:
        p3at.pretendMoveIt()
    else:
        p3at.moveIt()