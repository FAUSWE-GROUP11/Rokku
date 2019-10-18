import paho.mqtt.client as mqtt
from time import sleep
import logging
import logging.config
import yaml
import os


class Publisher:
    """
    A wrapper class to create an instance of client to publish message and
    handle related functionalities.
    """

    def __init__(
        self,
        name: str = "",
        topic: str = "Rokku",  # default topic
        broker_address: str = "test.mosquitto.org",  # default broker
        port: int = 1883,
    ):
        self.topic = topic
        # create a client instance
        self.client = mqtt.Client(name)
        # set up callbacks
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        # connect client
        self.client.connect(broker_address, port=port)
        self.client.loop_start()

        # set up logger
        fname: str = f"{os.path.dirname(__file__)}/../logger_config.yaml"
        with open(fname, "r") as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
        self.logger = logging.getLogger("Publisher")

    def publish(self, msg: str) -> None:
        """
        Have the client publish a message to a topic

        Args:
            msg:    The message to be published. Must be a string
        Return:
            None
        Raises:
            None
        """
        msg_info = self.client.publish(self.topic, msg, qos=1)
        # This call will block until the message is published.
        msg_info.wait_for_publish()
        self.logger.debug(f"Published content: {msg}")

    def close(self):
        """
        End the life of the client instance
        """
        self.client.loop_stop()
        self.client.disconnect()
        self.logger.debug("Connection to broker closed.")

    # Call backs
    def on_connect(self, client, userdata, flags, rc):
        """
        This function is called upon the client gets connected to the broker
        """
        if rc == 0:
            self.logger.debug("Connection to broker successful.")
        else:
            self.logger.error("Connection fails, reconnect in 1 second.")
            sleep(1)
            self.client.reconnect()

    def on_publish(self, client, userdata, mid):
        """
        This function is called upon the client successfully publish a message.
        """
        self.logger.debug(f"Messge published to topic: {self.topic}.")
