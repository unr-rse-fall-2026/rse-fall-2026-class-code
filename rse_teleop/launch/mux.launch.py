"""Start only the command multiplexer for keyboard or conflict demos."""

from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    package_share = Path(get_package_share_directory("rse_teleop"))
    output_topic = LaunchConfiguration("output_topic")

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "output_topic",
                default_value="/cmd_vel",
                description="Topic receiving the command selected by twist_mux.",
            ),
            Node(
                package="twist_mux",
                executable="twist_mux",
                name="twist_mux",
                parameters=[str(package_share / "config" / "twist_mux.yaml")],
                remappings=[("cmd_vel_out", output_topic)],
                output="screen",
            ),
        ]
    )
