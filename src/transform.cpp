#include <cmath>
#include <ros/ros.h>
#include <tf/transform_broadcaster.h>

int main(int argc, char* argv[])
{
  ros::init(argc, argv, "transform");
  ros::NodeHandle nodeHandle;
  (void)nodeHandle;
  ros::Rate nodeRate(10);

  tf::TransformBroadcaster tfb;

  //change these depending on where the kinect is
  double offsetx = 0.25;
  double offsety = 0.0;
  double offsetz = 0.18;

  while (ros::ok())
  {
    tf::StampedTransform transform;

    transform.setOrigin( tf::Vector3(offsetx, offsety, offsetz));

    tf::Quaternion q;
    q.setEuler(0.0, 0.0, 0.0);
    transform.setRotation(q);

    transform.stamp_ = ros::Time::now(); //timestamp of transform

    transform.frame_id_ = "base_link";
    transform.child_frame_id_ = "openni_depth_frame";

    tfb.sendTransform(transform);

    ros::spinOnce();
    nodeRate.sleep();
  }

  return 0;
}
