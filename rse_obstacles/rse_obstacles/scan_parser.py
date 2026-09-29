#!/usr/bin/python3

import rclpy
from rclpy.node import Node

import numpy as np

from sensor_msgs.msg import LaserScan
#from geometry_msgs.msg import Twist
from rse_msgs.msg import Flbr


def angular_difference(a, b):
    return np.arctan2(
        np.sin(a - b),
        np.cos(a - b)
    )

def sector_distance( ranges, angles, valid, center, half_width ):
    offset = angular_difference( angles, center )

    covered = ( np.abs(offset) < half_width )

    usable = covered & valid

    if not np.any(usable):
        return float('nan')

    return float( np.min(ranges[usable])
    )



class ScanParser(Node):

    def __init__(self):
        super().__init__('scan_parser')
        self.i = 0

        # parameters declaration

        # declare publisher and subscriber
        self.publisher = self.create_publisher(Flbr, 'flbr', 10)
        
        # subscribe to laser scan
        self.subscription = self.create_subscription(
            LaserScan,
            'scan',
            self.scan_callback,
            10)
        self.subscription  # prevent unused variable warning
        
    def scan_callback(self, msg):
        #self.get_logger().info('I heard: "%s"' % msg.header.stamp)

        ranges = np.asarray( msg.ranges, dtype=float )
        ranges[np.isposinf(ranges)] = msg.range_max
        valid = ( np.isfinite(ranges) & (ranges >= msg.range_min) & (ranges <= msg.range_max) )
        angles = ( msg.angle_min + np.arange(ranges.size) * msg.angle_increment )
        #print ( "ranges: " , (ranges) )
        #print ( "angles: " , (angles) )
        half_width = np.deg2rad(45.0)

        clearances = {
            'front': sector_distance(
                ranges, angles, valid,
                0.0, half_width
            ),
            'left': sector_distance(
                ranges, angles, valid,
                np.pi / 2.0, half_width
            ),
            'back': sector_distance(
                ranges, angles, valid,
                np.pi, half_width
            ),
            'right': sector_distance(
                ranges, angles, valid,
                -np.pi / 2.0, half_width
            ),
        }

        #print(clearances)
        flbr = Flbr()
        flbr.header = msg.header
        flbr.front = clearances['front']
        flbr.left = clearances['left']
        flbr.back = clearances['back']
        flbr.right = clearances['right']
        self.publisher.publish(flbr)

def main(args=None):
    rclpy.init(args=args)

    sp = ScanParser()

    rclpy.spin(sp)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    sp.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()