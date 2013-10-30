execute_process(COMMAND "/home/human/hcr2013/exercises/ros_intro/build/common/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/human/hcr2013/exercises/ros_intro/build/common/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
