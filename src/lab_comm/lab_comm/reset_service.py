import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger

class ResetService(Node):
    def __init__(self):
        super().__init__('reset_service')
        self.srv = self.create_service(Trigger, 'reset_system', self.reset_callback)
        self.get_logger().info('Reset Service Ready.')

    def reset_callback(self, request, response):
        response.success = True
        response.message = 'System reset successfully'
        self.get_logger().info('Reset request received and executed.')
        return response

def main(args=None):
    rclpy.init(args=args)
    node = ResetService()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()
