"""Launch the RSE warehouse, Stage-compatible bridge, and robot TF model."""

from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    package_share = Path(get_package_share_directory("rse_gazebo"))
    ros_gz_share = Path(get_package_share_directory("ros_gz_sim"))

    world_file = package_share / "worlds" / "rse_warehouse.sdf"
    bridge_file = package_share / "config" / "bridge.yaml"
    robot_xacro = package_share / "urdf" / "rse_bot.urdf.xacro"
    rviz_config = package_share / "rviz" / "rse_bot.rviz"
    model_path = package_share / "models"

    use_sim_time = LaunchConfiguration("use_sim_time")
    start_rviz = LaunchConfiguration("rviz")

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            str(ros_gz_share / "launch" / "gz_sim.launch.py")
        ),
        launch_arguments={"gz_args": f"-r {world_file}"}.items(),
    )

    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        name="rse_gz_bridge",
        output="screen",
        parameters=[{"config_file": str(bridge_file)}],
    )

    robot_description = Command(["xacro ", str(robot_xacro)])
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[
            {"robot_description": robot_description},
            {"use_sim_time": use_sim_time},
        ],
    )

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", str(rviz_config)],
        parameters=[{"use_sim_time": use_sim_time}],
        condition=IfCondition(start_rviz),
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "use_sim_time",
                default_value="true",
                description="Use Gazebo's /clock for ROS nodes.",
            ),
            DeclareLaunchArgument(
                "rviz",
                default_value="false",
                description="Start RViz with a preconfigured robot view.",
            ),
            # The world includes model://rse_bot. Keep all custom assets local.
            SetEnvironmentVariable("GZ_SIM_RESOURCE_PATH", str(model_path)),
            gazebo,
            bridge,
            robot_state_publisher,
            rviz,
        ]
    )
