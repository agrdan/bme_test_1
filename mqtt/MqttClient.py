import paho.mqtt.client as mqtt
from threading import Thread
from time import sleep as delay
import datetime as dt
from collections import deque

_server = "infrastruktura.com.hr"
_port = 1883


class Mqtt(Thread):
    def __init__(self, topic):
        Thread.__init__(self)
        self.topic = topic
        self.queue = deque()
        self.mqttc = mqtt.Client()
        print("MQTT initialized!")

    def run(self):
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_disconnect = self.on_disconnect
        self.mqttc.on_message = self.on_message
        self.mqttc.on_subscribe = self.on_subscribe
        self.mqttc.on_unsubscribe = self.on_unsubscribe
        self.mqttc.connect(host=_server, port=_port)
        self.mqttc.loop_forever()
        delay(0.3)

    def on_connect(self, mqttc, userdata, flags, rc):
        print('Connected... -> rc = ' + str(rc))
        mqttc.subscribe(topic=self.topic, qos=0)

    def on_disconnect(self, mqttc, userdata, rc):
        print('Disconnected... -> rc = ' + str(rc))

    def on_message(self, mqttc, userdata, msg):
        mqttMsg = msg.topic + ";" + str(msg.payload.decode('utf-8'))
        self.queue.append(mqttMsg)

    def on_subscribe(self, mqttc, userdata, mid, granted_qos):
        print('Subscribed (qos = ' + str(granted_qos) + ')')

    def on_unsubscribe(self, mqttc, userdata, mid, granted_qos):
        print('Unsubscribed (qos = ' + str(granted_qos) + ')')

    def getFromQueue(self):
        if len(self.queue) is not 0:
            return self.queue.popleft()
        else:
            return None

    def publish(self, msg):
        print("Publishing: {}\nTopic: {}".format(msg, _topic))
        self.mqttc.publish(_topic, msg, 0, False)
