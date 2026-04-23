import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description() -> LaunchDescription:
    go2_description_pkg = get_package_share_directory("go2_description")

    use_joint_state_publisher = DeclareLaunchArgument(
        "use_joint_state_publisher",
        default_value="true",
        description="Start a dummy joint_state_publisher when no real joint data exists.",
    )
    urdf_path = DeclareLaunchArgument(
        "urdf_path",
        default_value=os.path.join(go2_description_pkg, "urdf", "go2_description.urdf"),
        description="Path to the Go2 URDF file.",
    )

    robot_description = ParameterValue(
        Command(["xacro ", LaunchConfiguration("urdf_path")]),
        value_type=str,
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description}],
    )
    joint_state_publisher = Node(
        package="joint_state_publisher",
        executable="joint_state_publisher",
        condition=IfCondition(LaunchConfiguration("use_joint_state_publisher")),
    )

    return LaunchDescription(
        [
            urdf_path,
            use_joint_state_publisher,
            robot_state_publisher,
            joint_state_publisher,
        ]
    )
