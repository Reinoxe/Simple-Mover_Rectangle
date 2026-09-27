import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time
import math

class MoverNode(Node):
    def __init__(self):
        super().__init__('mover_node')
        
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.start_time = time.time()

        # Faktor Koreksi Rotasi
        # - Jika putaran kurang dari 90 derajat: ubah ke 1.05, 1.1, dst.
        # - Jika putaran lebih dari 90 derajat: ubah ke 0.95, 0.9, dst.
        self.koreksi_rotasi = 1.23
        self.angular_speed = ((math.pi / 2) / 3.0) * self.koreksi_rotasi

    def timer_callback(self):
        msg = Twist()
        current_time = time.time()
        elapsed_time = current_time - self.start_time

        # 1. Maju 5m -> Kecepatan 1.0 m/s, Butuh 5 detik (0.0 s/d 5.0)
        if elapsed_time < 5.0:
            msg.linear.x = 1.0
            msg.angular.z = 0.0
            self.get_logger().info('1. Maju 5m')
            
        # 2. Putar 90 derajat -> Butuh 3 detik (5.0 s/d 8.0)
        elif elapsed_time < 8.0:
            msg.linear.x = 0.0
            msg.angular.z = self.angular_speed
            self.get_logger().info('2. Putar 90 derajat')
            
        # 3. Maju 10m -> Kecepatan 1.0 m/s, Butuh 10 detik (8.0 s/d 18.0)
        elif elapsed_time < 18.0:
            msg.linear.x = 1.0
            msg.angular.z = 0.0  
            self.get_logger().info('3. Maju 10m')
            
        # 4. Putar 90 derajat -> Butuh 3 detik (18.0 s/d 21.0)
        elif elapsed_time < 21.0:
            msg.linear.x = 0.0
            msg.angular.z = self.angular_speed
            self.get_logger().info('4. Putar 90 derajat')
            
        # 5. Maju 5m -> Kecepatan 1.0 m/s, Butuh 5 detik (21.0 s/d 26.0)
        elif elapsed_time < 26.0:
            msg.linear.x = 1.0
            msg.angular.z = 0.0  
            self.get_logger().info('5. Maju 5m')
            
        # 6. Putar 90 derajat -> Butuh 3 detik (26.0 s/d 29.0)
        elif elapsed_time < 29.0:
            msg.linear.x = 0.0
            msg.angular.z = self.angular_speed
            self.get_logger().info('6. Putar 90 derajat')
            
        # 7. Maju 10m -> Kecepatan 1.0 m/s, Butuh 10 detik (29.0 s/d 39.0)
        elif elapsed_time < 39.0:
            msg.linear.x = 1.0
            msg.angular.z = 0.0  
            self.get_logger().info('7. Maju 10m')
            
        # 8. Berhenti -> Setelah detik ke-39
        else:
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.get_logger().info('8. Berhenti.')
            self.publisher_.publish(msg)
            
            self.timer.cancel()
            rclpy.shutdown()
            return

        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = MoverNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            node.destroy_node()
            rclpy.shutdown()

if __name__ == '__main__':
    main()
