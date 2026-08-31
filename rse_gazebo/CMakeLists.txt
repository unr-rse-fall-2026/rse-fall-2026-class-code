cmake_minimum_required(VERSION 3.8)
project(rse_gazebo)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY config launch models rviz urdf worlds
  DESTINATION share/${PROJECT_NAME}
)

install(
  PROGRAMS
    scripts/install_dependencies.sh
    scripts/lab_environment.sh
    scripts/smoke_test.sh
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
