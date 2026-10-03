import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import math

class DynamicJointPublisher(Node):
    def __init__(self):
        super().__init__('dynamic_joint_publisher')
        self.publisher_ = self.create_publisher(JointState, 'joint_states', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.i = 0.0

    def timer_callback(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = ['joint_base_to_bawah', 'joint_bawah_to_atas']

        # Simulasi gerak harmonis (ayunan sendi)
        msg.position = [
            math.sin(self.i) * 1.0,
            math.cos(self.i) * 0.7
        ]

        self.publisher_.publish(msg)
        self.i += 0.05

def main(args=None):
    rclpy.init(args=args)
    node = DynamicJointPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
