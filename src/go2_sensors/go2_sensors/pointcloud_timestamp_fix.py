#!/usr/bin/env python3
"""Rewrite UTlidar point cloud timestamps to the current ROS clock time."""

import rclpy
from rclpy.duration import Duration
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, HistoryPolicy, QoSProfile, ReliabilityPolicy
from sensor_msgs.msg import PointCloud2


class PointCloudTimestampFix(Node):
    """Fix delayed point cloud timestamps before laser scan conversion."""

    def __init__(self) -> None:
        super().__init__("pointcloud_timestamp_fix")

        self.declare_parameter("input_topic", "/utlidar/cloud_deskewed")
        self.declare_parameter("output_topic", "/utlidar/cloud_fixed")
        self.declare_parameter("backdate_sec", 0.05)

        input_topic = str(self.get_parameter("input_topic").value)
        output_topic = str(self.get_parameter("output_topic").value)
        self.backdate_sec = float(self.get_parameter("backdate_sec").value)
        self.backdate_duration = Duration(seconds=self.backdate_sec)

        sub_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE,
            history=HistoryPolicy.KEEP_LAST,
            depth=5,
        )
        pub_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.VOLATILE,
            history=HistoryPolicy.KEEP_LAST,
            depth=5,
        )

        self.subscription = self.create_subscription(
            PointCloud2,
            input_topic,
            self.on_cloud,
            sub_qos,
        )
        self.publisher = self.create_publisher(
            PointCloud2,
            output_topic,
            pub_qos,
        )

        self.get_logger().info("时间戳修复节点已启动")
        self.get_logger().info(f"订阅: {input_topic}")
        self.get_logger().info(f"发布: {output_topic}")
        self.get_logger().info(f"回拨时间戳: {self.backdate_sec:.3f} 秒")

        self.message_count = 0

    def on_cloud(self, msg: PointCloud2) -> None:
        """Copy the incoming cloud and replace its timestamp with 'now'."""
        stamp_time = self.get_clock().now() - self.backdate_duration

        if self.message_count == 0:
            original_time = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9
            adjusted_time = stamp_time.nanoseconds * 1e-9
            delay_seconds = adjusted_time - original_time
            self.get_logger().info(
                "原始时间戳 %.3fs, 修正后时间 %.3fs, 时间差 %.3fs"
                % (original_time, adjusted_time, delay_seconds)
            )

        fixed_msg = PointCloud2()
        fixed_msg.header = msg.header
        fixed_msg.height = msg.height
        fixed_msg.width = msg.width
        fixed_msg.fields = msg.fields
        fixed_msg.is_bigendian = msg.is_bigendian
        fixed_msg.point_step = msg.point_step
        fixed_msg.row_step = msg.row_step
        fixed_msg.data = msg.data
        fixed_msg.is_dense = msg.is_dense
        fixed_msg.header.stamp = stamp_time.to_msg()

        self.publisher.publish(fixed_msg)
        self.message_count += 1


def main(args=None) -> None:
    rclpy.init(args=args)
    node = PointCloudTimestampFix()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
