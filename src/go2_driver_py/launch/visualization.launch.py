"""Launch the chapter 5 visualization stack without the chapter 6 bridge."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    go2_description_pkg = get_package_share_directory("go2_description")
    go2_driver_pkg = get_package_share_directory("go2_driver_py")

    use_rviz = DeclareLaunchArgument(
        "use_rviz",
        default_value="true",
        description="Whether to start RViz for chapter 5 visualization.",
    )

    return LaunchDescription(
        [
            use_rviz,
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(go2_description_pkg, "launch", "display.launch.py")
                ),
                launch_arguments={"use_joint_state_publisher": "false"}.items(),
            ),
            Node(
                package="rviz2",
                executable="rviz2",
                arguments=[
                    "-d",
                    os.path.join(go2_driver_pkg, "rviz", "display.rviz"),
                ],
                condition=IfCondition(LaunchConfiguration("use_rviz")),
            ),
            Node(
                package="tf2_ros",
                executable="static_transform_publisher",
                arguments=["--frame-id", "radar", "--child-frame-id", "utlidar_lidar"],
            ),
            Node(
                package="go2_driver_py",
                executable="driver",
                parameters=[os.path.join(go2_driver_pkg, "params", "driver.yaml")],
            ),
        ]
    )
