import paho.mqtt.client as mqtt
from time import sleep


class CallBacks:
    def __init__(self):
        self.connect_success = False

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connection successful")
            self.connect_success = True
        else:
            print("Connection fails")
            self.connect_success = False


class Publisher:
    def __init__(
        self,
        name: str,
        topic: str = "Rokku",
        broker_address: str = "test.mosquitto.org",
        port: int = 1883,
    ):
        self.topic = topic
        self.callbacks = CallBacks()
        # create a client instance
        self.client = mqtt.Client(name)
        # set up callbacks
        self.client.on_connect = self.callbacks.on_connect
        # connect client
        while not self.callbacks.connect_success:
            self.client.connect(broker_address, port=port)
            sleep(1)
        self.client.loop_start()

    def publish(self, msg: str):
        while not self.client.publish(self.topic, msg).is_published:
            sleep(1)  # publish fail, re-publish in 1 second

    def close(self):
        self.client.loop_end()
        self.client.disconnect()
