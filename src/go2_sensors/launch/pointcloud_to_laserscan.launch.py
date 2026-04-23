"""Launch timestamp fixing and 3D-to-2D laser scan conversion for chapter 11."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    pkg_share = get_package_share_directory("go2_sensors")
    params_file = os.path.join(pkg_share, "config", "pointcloud_to_laserscan_params.yaml")

    return LaunchDescription(
        [
            Node(
                package="go2_sensors",
                executable="pointcloud_timestamp_fix",
                name="pointcloud_timestamp_fix",
                parameters=[
                    {
                        "input_topic": "/utlidar/cloud_deskewed",
                        "output_topic": "/utlidar/cloud_fixed",
                    }
                ],
                output="screen",
            ),
            Node(
                package="pointcloud_to_laserscan",
                executable="pointcloud_to_laserscan_node",
                name="pointcloud_to_laserscan_node",
                parameters=[params_file],
                remappings=[
                    ("cloud_in", "/utlidar/cloud_fixed"),
                    ("scan", "/scan"),
                ],
                output="screen",
            ),
        ]
    )
