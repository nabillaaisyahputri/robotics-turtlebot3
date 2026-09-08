import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import SetParametersResult
from std_msgs.msg import Float32

class ProcessingNode(Node):
    def __init__(self):
        super().__init__('processing_node')
        
        self.declare_parameter('threshold', 0.5)
        self.threshold = self.get_parameter('threshold').value
        
        self.add_on_set_parameters_callback(self.parameter_callback)
        
        self.subscription = self.create_subscription(
            Float32,
            'sensor_data',
            self.listener_callback,
            10
        )
        self.publisher = self.create_publisher(Float32, 'filtered_data', 10)
        self.get_logger().info('Processing Node successfully started.')

    def parameter_callback(self, params):
        for param in params:
            if param.name == 'threshold':
                if param.value < 0.0:
                    self.get_logger().warn('Threshold cannot be negative!')
                    return SetParametersResult(successful=False, reason='Threshold must be >= 0')
                
                self.threshold = param.value
                self.get_logger().info(f'Threshold updated to: {self.threshold}')
        return SetParametersResult(successful=True)

    def listener_callback(self, msg):
        if msg.data > self.threshold:
            filtered_msg = Float32()
            filtered_msg.data = msg.data
            self.publisher.publish(filtered_msg)
            self.get_logger().info(f'Published filtered data: {msg.data:.2f}')

def main(args=None):
    rclpy.init(args=args)
    node = ProcessingNode()
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
