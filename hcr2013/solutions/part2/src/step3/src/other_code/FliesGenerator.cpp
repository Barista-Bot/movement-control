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
#include <sensor_msgs/PointCloud.h>

namespace
{

//returns a random double between 0 and 1
inline double randomDouble()
{
    return static_cast<double>(std::rand() ) / static_cast<double>(RAND_MAX);
}

//Returns random angle between 0 and 2pi
inline double randomAngle()
{
    return randomDouble() * 2 * M_PI;
}

inline double randomRadius(double maxRadius)
{
    return randomDouble() * maxRadius;
}

}// End of anonymous namespace

int main(int argc, char* argv[])
{
    // Initialise ROS
    ros::init(argc, argv, "flies_generator");
    ros::NodeHandle nodeHandle;
    ros::Rate nodeRate(20); //Run at 20Hz

    ros::Publisher publisher =
            nodeHandle.advertise<sensor_msgs::PointCloud>("flies", 10);

    //Initialise random generator
    srand( ros::Time::now().toNSec() );

    while ( ros::ok() )
    {

        sensor_msgs::PointCloud msg;
        msg.header.frame_id = "openni_depth_frame";
        msg.header.stamp = ros::Time::now();

        //Once in every ten frames send a point cloud in the wrong frame
        if (rand() % 10 == 0)
            msg.header.frame_id = "wrong_frame";

        for (unsigned int i = 0; i < 10; ++i)
        {
            double radius = randomRadius(0.5);
            double angle = randomAngle();

            geometry_msgs::Point32 p;
            p.x = 0.5;
            p.y = radius*cos(angle);
            p.z = radius*sin(angle);
            msg.points.push_back( p );
        }

        //Send message
        publisher.publish(msg);

        ros::spinOnce();
        nodeRate.sleep();
    }
    return 0;
}
