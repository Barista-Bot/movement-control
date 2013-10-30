/*
 * Copyright (c) 2012 Miguel Sarabia del Castillo
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

#include <cmath>
#include <ros/ros.h>
#include <tf/transform_broadcaster.h>


int main(int argc, char* argv[])
{
    // Initialise ROS
    ros::init(argc, argv, "tf_tutorial_2");
    ros::NodeHandle nodeHandle;
    (void)nodeHandle; //Get rid of "unused variable" warning
    ros::Rate nodeRate(20); //Node runs at 20Hz


    // README: The objective of this module is to create a hat frame on top
    // of the head of the user.
    // HINT: Visualise results in rviz

    tf::TransformBroadcaster tfb;

    while( ros::ok() )
    {

        tf::StampedTransform transform;

        // TODO: Modify the vector below so that the hat frame is above the head
        // of the user
        // HINT: Use rviz to check which way is "up" on the head frame of
        // coordinates
        transform.setOrigin( tf::Vector3(0.0, 0.2, 0.0) );

        // Create the rotation quaternion from yaw, pitch, roll
        tf::Quaternion q;
        q.setEuler(0.0, 0.0, 0.0);
        transform.setRotation( q );

        // TODO: This timestamp is incorrect, do you know why?
        // How can it be fixed?
        transform.stamp_ = ros::Time::now();

        // TODO: This specifies the frame on which origin and rotation are
        // defined. Should it be "head_1" or "hat"? Why?
        transform.frame_id_ = "head_1";

        // TODO: This is the name of the new coordinate.
        // Should it be "head_1" or "hat"? Why?
        transform.child_frame_id_ = "hat";

        //Finally send the transform
        tfb.sendTransform( transform );


        // TODO [EXTRA]: Modify code so that the hat moves sinusoidally around
        // the head of the user

        // SOLUTION: We will change the pitch of the transformation.
        // Add the following code (you can change the frequency):
        //   double frequency = 10;
        //   double pitch = sin(2*M_PI * ros::Time::now().toSec() / frequency);
        // Then replace:
        //   q.setEuler(0.0, 0.0, 0.0);
        // by:
        //   q.setEuler(0.0, pitch, 0.0);
        //
        // NOTE: This is only one of the many ways of solving the task

        ros::spinOnce();
        nodeRate.sleep();
    }

    return 0;
}
