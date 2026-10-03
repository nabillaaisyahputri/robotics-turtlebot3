import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from std_msgs.msg import Float32


class QosTestPublisher(Node):

    def __init__(self):
        super().__init__('qos_test_publisher')

        self.declare_parameter('reliability', 'reliable')
        self.declare_parameter('depth', 10)
        self.declare_parameter('count', 600)
        self.declare_parameter('rate_hz', 10.0)

        reliability = self.get_parameter('reliability').value
        depth = int(self.get_parameter('depth').value)
        self.target = int(self.get_parameter('count').value)
        rate = float(self.get_parameter('rate_hz').value)

        rel = (
            ReliabilityPolicy.RELIABLE
            if reliability == 'reliable'
            else ReliabilityPolicy.BEST_EFFORT
        )

        qos = QoSProfile(
            depth=depth,
            reliability=rel,
            history=HistoryPolicy.KEEP_LAST
        )

        self.pub = self.create_publisher(
            Float32,
            '/sensor_data',
            qos
        )

        self.sent = 0

        self.timer = self.create_timer(
            1.0 / rate,
            self.publish_message
        )

        self.finish_timer = None

        self.get_logger().info(
            f'publisher started: qos={rel.name}, '
            f'depth={depth}, target={self.target}'
        )

    def publish_message(self):
        if self.sent >= self.target:
            self.timer.cancel()

            self.get_logger().info(
                f'Total messages sent: {self.sent}'
            )

            self.finish_timer = self.create_timer(
                2.0,
                self.finish
            )
            return

        msg = Float32()
        msg.data = float(self.sent + 1)

        self.pub.publish(msg)
        self.sent += 1

    def finish(self):
        self.get_logger().info(
            f'Finished. Total messages sent: {self.sent}'
        )

        if self.finish_timer is not None:
            self.finish_timer.cancel()

        self.destroy_node()


def main():
    rclpy.init()
    node = QosTestPublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    rclpy.shutdown()


if __name__ == '__main__':
    main()
