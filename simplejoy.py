import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist

mylist = [0.]*2

def joy_callback(msg):
    global mylist
    mylist = [ msg.axes[0], msg.axes[1]]


if __name__ == "__main__":
    rospy.init_node('joynode')
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.Subscriber('/joy', Joy, joy_callback)
    r = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        a=Twist()
        a.angular.z= mylist[0]/2.
        a.linear.x= mylist[1]/2.
        pub.publish(a)
        r.sleep()