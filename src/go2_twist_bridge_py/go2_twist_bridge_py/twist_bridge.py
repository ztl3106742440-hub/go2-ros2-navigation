"""Bridge geometry_msgs/Twist commands to Unitree Go2 Request messages."""

import json

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from unitree_api.msg import Request

from .sport_model import ROBOT_SPORT_API_IDS


class TwistBridge(Node):
    """Translate standard cmd_vel messages into Go2 sport requests."""

    def __init__(self) -> None:
        super().__init__("twist_bridge")

        self.declare_parameter("cmd_vel_topic", "cmd_vel")
        self.declare_parameter("request_topic", "/api/sport/request")
        self.declare_parameter("max_linear_speed", 0.30)
        self.declare_parameter("max_angular_speed", 0.50)
        self.declare_parameter("linear_deadband", 0.02)
        self.declare_parameter("angular_deadband", 0.05)

        self.max_linear_speed = float(self.get_parameter("max_linear_speed").value)
        self.max_angular_speed = float(self.get_parameter("max_angular_speed").value)
        self.linear_deadband = float(self.get_parameter("linear_deadband").value)
        self.angular_deadband = float(self.get_parameter("angular_deadband").value)

        cmd_vel_topic = str(self.get_parameter("cmd_vel_topic").value)
        request_topic = str(self.get_parameter("request_topic").value)

        self.request_publisher = self.create_publisher(Request, request_topic, 10)
        self.twist_subscription = self.create_subscription(
            Twist,
            cmd_vel_topic,
            self.twist_callback,
            10,
        )

    @staticmethod
    def clamp(value: float, limit: float) -> float:
        """Clamp a value into the closed interval [-limit, limit]."""
        return max(-limit, min(limit, value))

    def apply_linear_deadband_and_clamp(self, value: float) -> float:
        """Zero-out tiny values and cap the remaining linear speed."""
        if abs(value) < self.linear_deadband:
            return 0.0
        return self.clamp(value, self.max_linear_speed)

    def apply_angular_deadband_and_clamp(self, value: float) -> float:
        """Zero-out tiny values and cap the remaining angular speed."""
        if abs(value) < self.angular_deadband:
            return 0.0
        return self.clamp(value, self.max_angular_speed)

    def twist_callback(self, twist: Twist) -> None:
        """Convert cmd_vel into Go2 MOVE or BALANCESTAND requests."""
        request = Request()

        x = self.apply_linear_deadband_and_clamp(float(twist.linear.x))
        y = self.apply_linear_deadband_and_clamp(float(twist.linear.y))
        z = self.apply_angular_deadband_and_clamp(float(twist.angular.z))

        if x == 0.0 and y == 0.0 and z == 0.0:
            request.header.identity.api_id = ROBOT_SPORT_API_IDS["BALANCESTAND"]
        else:
            request.header.identity.api_id = ROBOT_SPORT_API_IDS["MOVE"]
            request.parameter = json.dumps({"x": x, "y": y, "z": z})

        self.request_publisher.publish(request)


def main() -> None:
    rclpy.init()
    node = TwistBridge()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
