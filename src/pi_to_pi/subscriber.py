import logging
import logging.config
import os
from time import sleep

import paho.mqtt.client as mqtt
import yaml


class Subscriber:
    """
    A wrapper class to create an instance of client to subscribe to a topic and
    handle related functionalities.
    """

    def __init__(
        self,
        queue,
        name: str = "",
        topic: str = "Rokku",  # default topic
        broker_address: str = "test.mosquitto.org",  # default broker
        port: int = 1883,
    ):
        self.topic = topic
        self.queue = queue  # for use of communicating with parent process
        # create a client instance
        self.client = mqtt.Client(name)
        # set up callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_subscribe = self.on_subscribe
        # connect client
        self.client.connect(broker_address, port=port)

        # set up logger
        fname: str = f"{os.path.dirname(__file__)}/../../logger_config.yaml"
        with open(fname, "r") as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
        self.logger = logging.getLogger("Subscriber")

    def start_listen(self):
        """
        This function must be run in a child process, as it is blocking.
        """
        self.client.loop_forever()
        self.logger.debug(f"Start listening on topic {self.topic}")

    # Call backs
    def on_connect(self, client, userdata, flags, rc):
        """
        This function is called upon the client gets connected to the broker
        """
        if rc == 0:
            self.logger.debug("Connection to broker successful.")
            # subscribe to the given topic upon connection is established
            self.client.subscribe(self.topic)
        else:
            self.logger.error("Connection fails, reconnect in 1 second.")
            sleep(2)
            self.client.reconnect()

    def on_message(self, client, userdata, message):
        """
        This function is called upon the client receives message from the topic
        it subscribes to. It proceeds to push the message to the queue such
        that the parent process can get the message.
        """
        msg: str = str(message.payload.decode("utf-8"))
        self.queue.put(msg)
        self.logger.debug(f"Message received: {msg}")

    def on_subscribe(self, client, userdata, mid, granted_qos):
        """
        This function is called upon the client successfully subscribes to a
        topic.
        """
        self.logger.debug(f"Subscribed to topic: {self.topic}")

    def close(self):
        """
        End the life of the client instance
        """
        self.client.loop_stop()
        self.client.disconnect()
        self.logger.debug("Connection to broker closed.")
