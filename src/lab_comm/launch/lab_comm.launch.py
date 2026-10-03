from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(package='lab_comm', executable='sensor_publisher', name='sensor_publisher'),
        Node(package='lab_comm', executable='processing_node', name='processing_node'),
        Node(package='lab_comm', executable='reset_service', name='reset_service'),
        Node(package='lab_comm', executable='motion_action_server', name='motion_action_server'),
    ])
