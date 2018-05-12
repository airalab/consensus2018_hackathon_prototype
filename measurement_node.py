from model import session, Measurement, City
from std_msgs.msg import String
import rospy

if __name__ == '__main__':
    rospy.init_node('measurements_query', anonymous=True)
    pub = rospy.Publisher('measurement', String, queue_size=200)

    def select_city(msg):
        s = session()
        city = s.query(City).filter(City.name == msg.data).one()
        for m in s.query(Measurement).filter(Measurement.city_id == city.id):
            res = String()
            res.data = '{0}: {1} {2}'.format(m.stamp, m.value, m.unit)
            pub.publish(res)
    rospy.Subscriber('select_city', String, select_city)

    rospy.spin()
