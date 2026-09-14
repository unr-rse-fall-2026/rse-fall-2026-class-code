cmake_minimum_required(VERSION 3.8)
project(rse_teleop)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY config launch
  DESTINATION share/${PROJECT_NAME}
)

install(
  FILES README.md LICENSE
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
