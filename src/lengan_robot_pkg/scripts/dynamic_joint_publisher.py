import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import math


class DynamicJointPublisher(Node):

    def __init__(self):
        super().__init__('dynamic_joint_publisher')

        self.publisher = self.create_publisher(
            JointState,
            '/joint_states',
            10
        )

        self.timer = self.create_timer(
            0.1,
            self.move_robot
        )

        self.time = 0.0

    def move_robot(self):

        msg = JointState()

        msg.header.stamp = self.get_clock().now().to_msg()

        msg.name = [
            'joint_1_base',
            'joint_2_elbow',
            'joint_3_wrist',
            'gripper_left_joint',
            'gripper_right_joint'
        ]

        # =========================
        # GERAKAN 3 JOINT LENGAN
        # =========================

        joint_1 = 0.7 * math.sin(self.time)

        joint_2 = 0.5 * math.sin(
            self.time * 0.7
        )

        joint_3 = 0.3 * math.sin(
            self.time * 1.2
        )


        # =========================
        # GERAKAN GRIPPER
        # =========================

        # Nilai 0 = tertutup
        # Nilai 0.12 = terbuka

        gripper = (
            0.10
            + 0.10 * math.sin(self.time * 0.3)
        )


        # =========================
        # KIRIM POSISI
        # =========================

        msg.position = [
            joint_1,
            joint_2,
            joint_3,
            gripper,
            gripper
        ]

        self.publisher.publish(msg)

        # Kecepatan gerakan
        self.time += 0.05


def main(args=None):

    rclpy.init(args=args)

    node = DynamicJointPublisher()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
