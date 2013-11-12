#include <ros/ros.h>
#include <tf/transform_listener.h>
#include <geometry_msgs/Twist.h>

int main(int argc, char* argv[])
{
  const double frequency = 20;
  const double timeToUser = 6;
  const double minDistance = 0.4;
  const double minAngle = 0.09;
  const double maxLinearSpeed = 0.3;
  const double maxAngularSpeed = 0.52;

  ros::init(argc, argv, "movement");
  ros::NodeHandle nodeHandle;
  ros::Rate nodeRate(frequency);

  ros::Publisher pub = nodeHandle.advertise<geometry_msgs::Twist>("cmd_vel", 10);

  const double timeout = 0.1;
  const std::string originFrame = "torso_1";
  const std::string destFrame = "base_link";

  tf::TransformListener tfl;

  while (ros::ok())
  {
    double linearSpeed = 0.0;
    double angularSpeed = 0.0;

    bool okay = tfl.waitForTransform(destFrame, originFrame, ros::Time::now() - ros::Duration(timeout), ros::Duration(timeout));

    if (okay)
    {
      geometry_msgs::PointStamped input;
      geometry_msgs::PointStamped output;

      input.header.frame_id = originFrame;
      input.header.stamp = ros::Time(0);

      input.point.x = 0.0;
      input.point.y = 0.0;
      input.point.z = 0.0;

      tfl.transformPoint(destFrame, input, output);

      //compute distance between robot and torso
      double distance = std::sqrt(output.point.x * output.point.x + output.point.y * output.point.y);

      double angle = std::atan2(output.point.y, output.point.x);

      ROS_INFO_STREAM("DISTANCE = " << distance << " ANGLE = " << angle);

      if (std::abs(angle) > minAngle)
      {
        angularSpeed = std::abs(angle*frequency / timeToUser);
        if (angularSpeed > maxAngularSpeed)
          angularSpeed = maxAngularSpeed;

        if (angle < 0)
          angularSpeed = -angularSpeed;
      }
      if (distance > minDistance)
      {
        linearSpeed = distance * frequency / timeToUser;
        if (linearSpeed > maxLinearSpeed)
        {
          linearSpeed = maxLinearSpeed;
        }
      }
    }

    //send info as a Twist message
    geometry_msgs::Twist msg;

    ROS_INFO_STREAM("SENDING " << okay);
    msg.linear.x = linearSpeed;
    msg.angular.z = angularSpeed;

    pub.publish(msg);

    ros::spinOnce();
    nodeRate.sleep();
  }

  return 0;
}
