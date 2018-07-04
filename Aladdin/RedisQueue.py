from django.conf import settings
redis_ip = settings.REDIS_IP
redis_password = settings.REDIS_PASSWORD

from redis import Redis

class Redis_Queue(object):
    def __init__(self,channel):
        self.__conn = Redis(host=redis_ip,password=redis_password)
        self.chan_sub = channel
        self.chan_pub = channel

    #发送消息
    def publish(self,msg):
        self.__conn.publish(self.chan_pub,msg)
        return True

    #订阅消息
    def subscribe(self):
        #建立连接
        pub = self.__conn.pubsub()
        #调频道
        pub.subscribe(self.chan_sub)
        #准备接收
        pub.parse_response()
        return pub