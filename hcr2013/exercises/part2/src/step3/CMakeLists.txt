cmake_minimum_required(VERSION 2.8.3)
project(step3)

#===============================================================================
# FIND PACKAGE DEPENDENCIES
#===============================================================================
# List C++ dependencies on ros packages
set( ROS_CXX_DEPENDENCIES roscpp tf geometry_msgs sensor_msgs)


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

add_executable(flies_generator "src/other_code/FliesGenerator.cpp" )
add_dependencies(flies_generator ${catkin_EXPORTED_TARGETS})
target_link_libraries(flies_generator  ${catkin_LIBRARIES})

add_executable( ${PROJECT_NAME} "src/Main.cpp" )
add_dependencies( ${PROJECT_NAME} ${catkin_EXPORTED_TARGETS})
target_link_libraries( ${PROJECT_NAME}  ${catkin_LIBRARIES})

#===============================================================================
# INSTALLATION
#===============================================================================
# For binaries...
install(TARGETS ${PROJECT_NAME} flies_generator
    RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION} )

# For launch files
install(DIRECTORY launch
    DESTINATION "${CATKIN_PACKAGE_SHARE_DESTINATION}")
