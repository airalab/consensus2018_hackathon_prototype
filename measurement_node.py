from model import session, Measurement, City
from std_msgs.msg import String
from std_srvs.srv import Empty
import rospy

if __name__ == '__main__':
    rospy.init_node('measurements_query', anonymous=True)
    pub = rospy.Publisher('measurement', String, queue_size=200)
    finish = rospy.ServiceProxy('liability/finish', Empty)

    def select_city(msg):
        s = session()
        for city_name in msg.data.split(", "):
            try:
                city = s.query(City).filter(City.name == city_name).one()
                for m in s.query(Measurement).filter(Measurement.city_id == city.id):
                    res = String()
                    res.data = '{0} => {1} : {2} {3}'.format(city_name, m.stamp, m.value, m.unit)
                    pub.publish(res)
            except:
                pass
        rospy.wait_for_service('liability/finish')
        try:
            finish()
        except rospy.ServiceException as e:
            print("Service call failed: {}".format(e))

    rospy.Subscriber('select_city', String, select_city)

    rospy.spin()
