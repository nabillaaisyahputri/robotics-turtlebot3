import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from std_msgs.msg import Float32


class QosTestSubscriber(Node):

    def __init__(self):
        super().__init__('qos_test_subscriber')

        self.declare_parameter('reliability', 'reliable')
        self.declare_parameter('depth', 10)

        reliability = self.get_parameter('reliability').value
        depth = self.get_parameter('depth').value

        rel = (
            ReliabilityPolicy.RELIABLE
            if reliability == 'reliable'
            else ReliabilityPolicy.BEST_EFFORT
        )

        qos = QoSProfile(
            depth=int(depth),
            reliability=rel,
            history=HistoryPolicy.KEEP_LAST
        )

        self.count = 0

        self.sub = self.create_subscription(
            Float32,
            '/sensor_data',
            self.callback,
            qos
        )

        self.get_logger().info(
            f'subscriber started: qos={rel.name}, depth={depth}'
        )

    def callback(self, msg):
        self.count += 1

        if self.count % 10 == 0:
            self.get_logger().info(
                f'Messages received: {self.count}'
            )


def main():
    rclpy.init()
    node = QosTestSubscriber()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        print(f'\nTotal messages received: {node.count}')

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
