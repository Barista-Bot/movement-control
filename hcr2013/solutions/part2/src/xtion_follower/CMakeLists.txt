cmake_minimum_required(VERSION 2.8.3)
project(xtion_follower)

#===============================================================================
# FIND PACKAGE DEPENDENCIES
#===============================================================================
# List C++ dependencies on ros packages
set( ROS_CXX_DEPENDENCIES roscpp tf geometry_msgs)


# Find catkin, ros c++ deps as well as boost
find_package(catkin REQUIRED COMPONENTS ${ROS_CXX_DEPENDENCIES})

#===============================================================================
# CATKIN PACKAGE
#===============================================================================
# This package only creates nodes, so no need to export any information
catkin_package()

#===============================================================================
# INCLUDES
#===============================================================================
include_directories( ${catkin_INCLUDE_DIRS} )

#===============================================================================
# COMPILATION
#===============================================================================

add_executable(tf_broadcaster "src/tf_broadcaster/Main.cpp" )
add_dependencies(tf_broadcaster  ${catkin_EXPORTED_TARGETS})
target_link_libraries(tf_broadcaster ${catkin_LIBRARIES})

add_executable( xtion_follower "src/xtion_follower/Main.cpp" )
add_dependencies( xtion_follower ${catkin_EXPORTED_TARGETS})
target_link_libraries( xtion_follower  ${catkin_LIBRARIES})

#===============================================================================
# INSTALLATION
#===============================================================================
# For binaries...
install(TARGETS xtion_follower tf_broadcaster
    RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION} )

# For script files...
install(DIRECTORY scripts/
    DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
    USE_SOURCE_PERMISSIONS)

# For launch files
install(DIRECTORY launch
    DESTINATION "${CATKIN_PACKAGE_SHARE_DESTINATION}")
