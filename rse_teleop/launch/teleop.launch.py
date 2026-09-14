"""Start the joystick control path and command multiplexer.

Keyboard teleoperation intentionally runs in a separate terminal because it
requires direct terminal input.
"""

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
                package="joy",
                executable="joy_node",
                name="joy_node",
                parameters=[str(package_share / "config" / "joy.yaml")],
                output="screen",
            ),
            Node(
                package="teleop_twist_joy",
                executable="teleop_node",
                name="teleop_node",
                parameters=[
                    str(package_share / "config" / "teleop_twist_joy.yaml")
                ],
                remappings=[("cmd_vel", "/cmd_vel/joystick")],
                output="screen",
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
