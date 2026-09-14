"""Start the gamepad input and gamepad-to-Twist conversion nodes."""

from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    package_share = Path(get_package_share_directory("rse_teleop"))

    return LaunchDescription(
        [
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
        ]
    )
