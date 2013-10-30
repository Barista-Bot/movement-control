/*
 * Copyright (c) 2012, 2013 Miguel Sarabia del Castillo
 * Imperial College London
 *
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 *
 */

#include <ros/ros.h>
#include <tf/transform_listener.h>
#include <bullet/LinearMath/btMatrix3x3.h>
#include <bullet/LinearMath/btQuaternion.h>


// This function is slightly involved due to the way ROS represents quaternions.
// Don't worry if you don't understand it!
std::string printYawPitchRoll(const tf::Quaternion& q)
{
    std::stringstream out;

    btScalar yaw, pitch, roll;
    btQuaternion btQuat( q.getX(), q.getY(), q.getZ(), q.getW() );
    btMatrix3x3(btQuat).getEulerYPR(yaw, pitch, roll);

    out << "[" << yaw << ", " << pitch << ", " << roll << "]";

    return out.str();
}

// README: The objective of this code is to find the parameters of the transform
// between the kinect and the user's torso.

int main(int argc, char* argv[])
{
    // Initialise ROS
    ros::init(argc, argv, "tf_tutorial_1");
    ros::NodeHandle nodeHandle;
    (void)nodeHandle; //Get rid of "unused variable" warning
    ros::Rate nodeRate(1); //Node runs at 1Hz

    // TODO: Modify parameters below as required
    const double timeout = 1; // Maximum time for transform to be available
    const std::string originFrame = "openni_depth_frame";
    const std::string destFrame = "torso_1";


    tf::TransformListener tfl;

    while( ros::ok() )
    {
        // TODO: This code is supposed to wait till a transform from origin to
        // dest is available. However there is one error.
        // Can you spot it and fix it?
        // HINT: Section 1.4.1 of
        // http://www.ros.org/wiki/tf/Overview/Using%20Published%20Transforms
        bool okay = tfl.waitForTransform(
                    destFrame,
                    originFrame,
                    ros::Time(0), //Use latest transform
                    ros::Duration(timeout)
                    );

        // TODO: if the previous call does not succeed we should log a warning
        // and try again (continue).
        if (! okay )
        {
            ROS_WARN_STREAM(
                        "Transformation between " << originFrame
                        << " and " << destFrame << " not found"
                        );
            continue;
        }

        //Variable to hold transform
        tf::StampedTransform transform;

        // TODO: obtain the transform between originFrame and destFrame
        // HINT: You will need the StampedTransform declared above
        // HINT: Arguments are similar to those of waitForTransform()
        // HINT: Section 1.5 and 1.5.1 of
        // http://www.ros.org/wiki/tf/Overview/Using%20Published%20Transforms
        tfl.lookupTransform(
                    destFrame,
                    originFrame,
                    ros::Time(0),
                    transform
                    );

        // TODO: Complete the call below so that the translation values of the
        // transformation are also logged
        // HINT: Translations are stored in getOrigin()
        ROS_INFO_STREAM( "Transformation between " << originFrame
                         << " and " << destFrame
                         << "Translation [x,y,z]: ["
                         << transform.getOrigin().x() << ", "
                         << transform.getOrigin().y() << ", "
                         << transform.getOrigin().z()
                         << "] Rotation [yaw, pitch, roll]: "
                         << printYawPitchRoll( transform.getRotation() )
                         );

        // TODO: Modify code so that program prints the transformation between
        // the user's left foot and the right hand

        // SOLUTION: Simply change
        //   const std::string destFrame = "torso_1";
        // to
        //   const std:string destFrame = "right_hand_1";
        // and
        //   const std::string originFrame = "openni_depth_camera";
        // to
        //   const std::string originFrame = "left_foot_1";

        ros::spinOnce();
        nodeRate.sleep();
    }

    return 0;
}
