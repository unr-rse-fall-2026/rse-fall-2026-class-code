#!/usr/bin/python

import rclpy
from rclpy.node import Node

import numpy as np
from geometry_msgs.msg import Twist
from rse_msgs.msg import Flbr

class AutoController(Node):

    def __init__(self):
        super().__init__('auto_controller')
        # parameters declaration
        # declare publisher and subscriber
        self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.stop_distance = 0.75

        # subscribe to laser scan
        self.subscription = self.create_subscription(
            Flbr,
            'flbr',
            self.flbr_callback,
            10)
        self.subscription  # prevent unused variable warning
        
    def flbr_callback(self, msg):
        #self.get_logger().info('I heard: "%s"' % msg.header.stamp)

        twist = Twist()
        twist.linear.x = 1.0
        twist.angular.z = 0.0

        if msg.front < self.stop_distance:
        	twist.linear.x = 0.0
        else:
            twist.linear.x = 1.0
        if msg.left > msg.right:
        	twist.angular.z = 0.5
        else:
        	twist.angular.z = -0.5

        self.publisher.publish(twist)

def main(args=None):
    rclpy.init(args=args)

    sp = AutoController()

    rclpy.spin(sp)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    sp.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()