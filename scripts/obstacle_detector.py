#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from easy_filter.msg import Obstacle
import numpy as np

class ObstacleDetector():

    def __init__(self):
        self.sub = rospy.Subscriber('/scan', LaserScan, self.scan, queue_size=1)
        self.pub = rospy.Publisher('obstacle', Obstacle, self.scan, queue_size =10)
        self.bumper()

    def scan(self, scan):
        dist = scan.ranges[0]
        if (dist >= scan.range_min and dist < scan.range_max):
            print(dist)
            if (dist < 0.3):
                self.report_obstacle(scan.ranges[0])

    def bumper(self):
        while not rospy.is_shutdown():
            rospy.spin()

    def report_obstacle(self, dist):
        print ("Measured obstacle at" , dist)
        obstacle = Obstacle()
        obstacle.distance = dist
        self.pub.publish(obstacle)


def main():
    rospy.init_node('obstacle_detector')
    try:
        obdetect = ObstacleDetector()
    except rospy.ROSInterruptException:
        print("Exception")

if __name__ == '__main__':
    main()
    print("clean exit")