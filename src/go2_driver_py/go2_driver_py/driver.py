"""Publish standard odom, TF and joint states for Unitree Go2."""

import rclpy
from geometry_msgs.msg import TransformStamped
from nav_msgs.msg import Odometry
from rclpy.node import Node
from sensor_msgs.msg import JointState
from tf2_ros import TransformBroadcaster
from unitree_go.msg import LowState, SportModeState


JOINT_NAMES = [
    "FL_hip_joint",
    "FL_thigh_joint",
    "FL_calf_joint",
    "FR_hip_joint",
    "FR_thigh_joint",
    "FR_calf_joint",
    "RL_hip_joint",
    "RL_thigh_joint",
    "RL_calf_joint",
    "RR_hip_joint",
    "RR_thigh_joint",
    "RR_calf_joint",
]


class Driver(Node):
    """Standardize Go2 state topics for RViz and downstream packages."""

    def __init__(self) -> None:
        super().__init__("driver_py")

        self.declare_parameter("odom_frame", "odom")
        self.declare_parameter("base_frame", "base")
        self.declare_parameter("publish_tf", "true")

        self.odom_frame = str(self.get_parameter("odom_frame").value)
        self.base_frame = str(self.get_parameter("base_frame").value)
        publish_tf_raw = self.get_parameter("publish_tf").value
        self.publish_tf = str(publish_tf_raw).lower() not in ("false", "0", "no")

        self.odom_publisher = self.create_publisher(Odometry, "odom", 10)
        self.joint_publisher = self.create_publisher(JointState, "joint_states", 10)
        self.transform_broadcaster = TransformBroadcaster(self)

        self.create_subscription(
            SportModeState,
            "/lf/sportmodestate",
            self.mode_callback,
            10,
        )
        self.create_subscription(
            LowState,
            "/lf/lowstate",
            self.state_callback,
            10,
        )

    def state_callback(self, state: LowState) -> None:
        """Convert the Go2 low-level state into JointState."""
        joint_state = JointState()
        joint_state.header.stamp = self.get_clock().now().to_msg()
        joint_state.name = JOINT_NAMES
        joint_state.position = [float(state.motor_state[i].q) for i in range(12)]
        self.joint_publisher.publish(joint_state)

    def mode_callback(self, mode: SportModeState) -> None:
        """Convert the Go2 sport mode state into Odometry and TF."""
        odom = Odometry()
        odom.header.stamp = self.get_clock().now().to_msg()
        odom.header.frame_id = self.odom_frame
        odom.child_frame_id = self.base_frame

        odom.pose.pose.position.x = float(mode.position[0])
        odom.pose.pose.position.y = float(mode.position[1])
        odom.pose.pose.position.z = float(mode.position[2])

        odom.pose.pose.orientation.w = float(mode.imu_state.quaternion[0])
        odom.pose.pose.orientation.x = float(mode.imu_state.quaternion[1])
        odom.pose.pose.orientation.y = float(mode.imu_state.quaternion[2])
        odom.pose.pose.orientation.z = float(mode.imu_state.quaternion[3])

        odom.twist.twist.linear.x = float(mode.velocity[0])
        odom.twist.twist.linear.y = float(mode.velocity[1])
        odom.twist.twist.linear.z = float(mode.velocity[2])
        odom.twist.twist.angular.z = float(mode.yaw_speed)

        self.odom_publisher.publish(odom)

        if not self.publish_tf:
            return

        transform = TransformStamped()
        transform.header.stamp = odom.header.stamp
        transform.header.frame_id = self.odom_frame
        transform.child_frame_id = self.base_frame
        transform.transform.translation.x = odom.pose.pose.position.x
        transform.transform.translation.y = odom.pose.pose.position.y
        transform.transform.translation.z = odom.pose.pose.position.z
        transform.transform.rotation = odom.pose.pose.orientation
        self.transform_broadcaster.sendTransform(transform)


def main() -> None:
    rclpy.init()
    node = Driver()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
