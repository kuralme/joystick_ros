import rospy
from sensor_msgs.msg import Joy, LaserScan, Range
from geometry_msgs.msg import Twist

mylist = [0.]*5
sonar = 0

def range_callback(msg):
  global sonar
  sonar = msg.range

def joy_callback(msg):
  global mylist
  mylist = [ msg.axes[0], msg.axes[1], msg.axes[4], msg.buttons[0], msg.buttons[1]]

def scan_callback(msg):
  #print(msg.ranges)
  pass


if __name__ == "__main__":
  rospy.init_node('hector_quad')
  pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
  rospy.Subscriber('/joy', Joy, joy_callback)
  rospy.Subscriber("/scan", LaserScan, scan_callback)
  rospy.Subscriber("/sonar_height", Range, range_callback)
  r = rospy.Rate(10) # 10hz
  count = 0
  fly = 0
  landing = 0
  altitude = 0
  while not rospy.is_shutdown():
    a=Twist()

    if mylist[3] or fly:
        fly = 1
        count +=1
        # 5 seconds count
        if count <= 50:
          a.linear.z = 0.5
          pub.publish(a)
        else:
          fly =0
          count=0

    if (mylist[4] or landing) and not fly:
        landing = 1
        # Total inputted altitude as count
        if 0.5< sonar <= 3.:
          a.linear.z = -0.5
          pub.publish(a)
        elif 0.2 <= sonar <= 0.5:
          a.linear.z = -0.2
          pub.publish(a)
        else:
          landing =0

    if fly == 0 and landing == 0:
      a.angular.z= mylist[0]/2.
      a.linear.x= mylist[1]/2.
      a.linear.z = mylist[2]/2.
      pub.publish(a)

    r.sleep()