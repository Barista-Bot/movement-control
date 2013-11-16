#!/usr/bin/env python

import robot_control

if __name__ == "__main__":
    p3at = robot_control.robot()

    if p3at.HasCamera:
        p3at.pretendMoveIt()
    else:
        p3at.moveIt()
