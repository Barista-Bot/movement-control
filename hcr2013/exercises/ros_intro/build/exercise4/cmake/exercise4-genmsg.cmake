# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "exercise4: 1 messages, 0 services")

set(MSG_I_FLAGS "-Iexercise4:/home/human/hcr2013/exercises/ros_intro/src/exercise4/msg;-Istd_msgs:/opt/ros/hydro/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(genlisp REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(exercise4_generate_messages ALL)

#
#  langs = gencpp;genlisp;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(exercise4
  "/home/human/hcr2013/exercises/ros_intro/src/exercise4/msg/JoyAxis.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/exercise4
)

### Generating Services

### Generating Module File
_generate_module_cpp(exercise4
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/exercise4
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(exercise4_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(exercise4_generate_messages exercise4_generate_messages_cpp)

# target for backward compatibility
add_custom_target(exercise4_gencpp)
add_dependencies(exercise4_gencpp exercise4_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS exercise4_generate_messages_cpp)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(exercise4
  "/home/human/hcr2013/exercises/ros_intro/src/exercise4/msg/JoyAxis.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/exercise4
)

### Generating Services

### Generating Module File
_generate_module_lisp(exercise4
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/exercise4
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(exercise4_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(exercise4_generate_messages exercise4_generate_messages_lisp)

# target for backward compatibility
add_custom_target(exercise4_genlisp)
add_dependencies(exercise4_genlisp exercise4_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS exercise4_generate_messages_lisp)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(exercise4
  "/home/human/hcr2013/exercises/ros_intro/src/exercise4/msg/JoyAxis.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/exercise4
)

### Generating Services

### Generating Module File
_generate_module_py(exercise4
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/exercise4
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(exercise4_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(exercise4_generate_messages exercise4_generate_messages_py)

# target for backward compatibility
add_custom_target(exercise4_genpy)
add_dependencies(exercise4_genpy exercise4_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS exercise4_generate_messages_py)


debug_message(2 "exercise4: Iflags=${MSG_I_FLAGS}")


if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/exercise4)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/exercise4
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
add_dependencies(exercise4_generate_messages_cpp std_msgs_generate_messages_cpp)

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/exercise4)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/exercise4
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
add_dependencies(exercise4_generate_messages_lisp std_msgs_generate_messages_lisp)

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/exercise4)
  install(CODE "execute_process(COMMAND \"/usr/bin/python\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/exercise4\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/exercise4
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
add_dependencies(exercise4_generate_messages_py std_msgs_generate_messages_py)
