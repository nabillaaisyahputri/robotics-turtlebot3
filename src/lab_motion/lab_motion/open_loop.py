import math, time
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class OpenLoopSquare(Node):
	def __init__(self):
		 super().__init__('open_loop_square')
		 self.pub = self.create_publisher(Twist, 'cmd_vel', 10)
		 self.declare_parameter('side', 1.0)
		 self.declare_parameter('v', 0.10)
		 self.declare_parameter('w', 0.5)

	def send(self, v, w, duration):
		msg = Twist()
		msg.linear.x, msg.angular.z = v, w
		end = time.time() + duration
		while time.time() < end:
			self.pub.publish(msg)
			time.sleep(0.05)
		self.pub.publish(Twist()) # stop
		time.sleep(0.5)

	def run(self):
		side = self.get_parameter('side').value
		v = self.get_parameter('v').value
		w = self.get_parameter('w').value
		for _ in range(4):
			self.send(v, 0.0, side / v)
			self.send(0.0, w, (math.pi / 2) / w)

def main(args=None):
	rclpy.init(args=args)
	node = OpenLoopSquare()
	rclpy.spin(node)
	node.destroynode()
	rclpy.shutdown()

if __name__ == '__main__':
	main()
