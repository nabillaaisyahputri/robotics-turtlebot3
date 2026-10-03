#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import math

class InteractiveJointPublisher(Node):
    def __init__(self):
        super().__init__('interactive_joint_publisher')
        self.publisher_ = self.create_publisher(JointState, 'joint_states', 10)

        # Sesuaikan dengan nama joint yang ada di file URDF lengan robotmu
        self.joint_names = ['joint1', 'joint2', 'joint3', 'joint4'] # Ganti sesuai URDF-mu
        self.num_joints = len(self.joint_names)

        # Nilai sudut awal (dalam radian)
        self.joint_values = [0.0] * self.num_joints

        self.get_logger().info("=== Node Pengendali Interaktif Lengan Robot Aktif ===")
        self.get_logger().info(f"Joint yang terdeteksi: {self.joint_names}")

    def publish_states(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = self.joint_names
        msg.position = self.joint_values
        self.publisher_.publish(msg)

    def run_interactive(self):
        while rclpy.ok():
            try:
                print("\n--- Masukkan Nilai Sudut Baru (dalam Derajat) ---")
                input_str = input(f"Masukkan {self.num_joints} nilai sudut dipisah spasi (contoh: 30 45 -15 90): ")

                if not input_str.strip():
                    continue

                # Konversi input string ke float, lalu ubah derajat ke radian
                values_deg = [float(x) for x in input_str.split()]

                if len(values_deg) != self.num_joints:
                    print(f"[PERINGATAN] Harap masukkan tepat {self.num_joints} nilai!")
                    continue

                # Konversi derajat ke radian
                self.joint_values = [math.radians(deg) for deg in values_deg]

                # Publikasikan nilai ke ROS 2
                self.publish_states()
                print(f"[BERHASIL] Posisi joint diperbarui ke sudut: {values_deg} derajat.")

            except ValueError:
                print("[ERROR] Masukkan angka yang valid!")
            except KeyboardInterrupt:
                print("\nKeluar dari program interaktif.")
                break

def main(args=None):
    rclpy.init(args=args)
    node = InteractiveJointPublisher()

    # Jalankan fungsi input di loop terpisah atau langsung
    try:
        node.run_interactive()
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
