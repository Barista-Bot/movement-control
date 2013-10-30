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
#include <sensor_msgs/PointCloud.h>

// README: In this exercise we will learn to transform points from a
// point cloud to another frame of coordinates.
// The objective is to log the coordinates of all the flies (represented by a
// point in the point cloud) with repect to the right hand of the user.
class Step3
{
private:
    tf::TransformListener tfl_;

    static inline geometry_msgs::PointStamped extractPoint(
            const sensor_msgs::PointCloud::ConstPtr& pc,
            unsigned int i)
    {
        geometry_msgs::PointStamped result;

        //Copy useful parts of header
        result.header.frame_id = pc->header.frame_id;
        result.header.stamp = pc->header.stamp;

        const geometry_msgs::Point32 p = pc->points.at(i);

        result.point.x = p.x;
        result.point.y = p.y;
        result.point.z = p.z;

        return result;
    }

public:

    // README: This is the only function you will have to modify
    void callback(const sensor_msgs::PointCloud::ConstPtr& msg)
    {
        const std::string destFrame = "right_hand_1";
        const std::string originFrame = "openni_depth_frame";
        const double timeout = 1; // Maximum time for transform to be available

        // TODO: Wait till transform between openni_depth_frame and
        // right_hand is available. Return if not available.
        // HINT: Look at solution of tf_tutorial/step1 if you are unsure
        bool okay = tfl_.waitForTransform(
                    destFrame,
                    originFrame,
                    ros::Time(0),
                    ros::Duration(timeout)
                    );

        if (! okay)
            return;

        for( unsigned int i = 0; i < msg->points.size(); ++i )
        {
            geometry_msgs::PointStamped input = extractPoint(msg, i);
            geometry_msgs::PointStamped output;

            // Ensure we use latest transform
            input.header.stamp = ros::Time(0);

            // TODO: Verify that the frame of reference of the point is
            // openni_depth_frame, otherwise ignore point.
            // HINT: Pseudo-code with the structure of PointStamped
            // http://docs.ros.org/api/geometry_msgs/html/msg/PointStamped.html
            if ( input.header.frame_id != originFrame )
                continue;

            // TODO: The arguments of this function are not in the right order.
            // Can you rearrange them? Do you understand what the function does?
            tfl_.transformPoint(destFrame, input, output);

            // TODO: Verify the transformed point coordinates are expressed in
            // terms of the user's right hand, otherwise log an error
            if ( output.header.frame_id != destFrame )
                ROS_ERROR_STREAM("transformPoint() did not work as expected!");

            // TODO: Complete function below so that the coordinates are logged
            ROS_INFO_STREAM(
                        "Fly " << i
                        <<" position with respect to right hand [x,y,z]: ["
                        << output.point.x << ", "
                        << output.point.y << ", "
                        << output.point.z
                        << "]"
                        );
        }
    }
};

// README: This time around main is complete
int main(int argc, char* argv[])
{
    // Initialise ROS
    ros::init(argc, argv, "tf_tutorial_3");
    ros::NodeHandle nodeHandle;
    Step3 s3;

    ros::Subscriber subscriber = nodeHandle.subscribe<sensor_msgs::PointCloud>(
                "flies", //topic
                10, // size of buffer
                &Step3::callback, //callback member function
                &s3 //Instance on which to call the callback
                );

    (void) subscriber; //Get rid of unused subscriber method

    ros::spin();
    return 0;
}
