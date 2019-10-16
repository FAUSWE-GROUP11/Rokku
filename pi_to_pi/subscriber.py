import paho.mqtt.client as mqtt
from time import sleep
from collections import defaultdict
from typing import Dict, List, Tuple
import json


class CallBacks:
    def __init__(self):
        self.connect_success = False
        self.received_msgs: Dict[str, List[str]] = defaultdict(list)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connection successful")
            self.connect_success = True
        else:
            print("Connection fails")
            self.connect_success = False

    def on_message(self, client, userdata, message):
        msg: Tuple[str, str] = json.loads(message.payload.decode("utf-8"))
        print(f"received: {msg}")
        self.received_msgs[msg[0]].append(msg[1])


class Subscriber:
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
        self.client.on_message = self.callbacks.on_message
        # connect client
        while not self.callbacks.connect_success:
            self.client.connect(broker_address, port=port)
            sleep(1)
        self.client.loop_start()
        # subscribe to the given topic
        while self.client.subscribe(self.topic)[0] != 0:
            sleep(1)  # subscribe fail, wait for 1 second and retry

    def get_msg(self, subtopic: str) -> str:
        return self.callbacks.received_msgs[subtopic].pop()

    def close(self):
        self.client.loop_end()
        self.client.disconnect()
