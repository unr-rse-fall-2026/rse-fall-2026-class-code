"""File for joystick/keyboard control, for RSE[2][1]."""

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

    ttk = Node(
        package="teleop_twist_keyboard",
        executable="teleop_twist_keyboard",
        name="TTK",
        output="screen",
        prefix = 'xterm -e',
        parameters=[],
    )

    joy = Node(
        package="joy",
        executable="joy_node",
        name="joy_node",
        output="screen",
    )


    return LaunchDescription(
        [
            ttk,
            joy
        ]
    )
