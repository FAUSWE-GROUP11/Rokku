import paho.mqtt.client as mqtt
from time import sleep


class Subscriber:
    """
    A wrapper class to create an instance of client to subscribe to a topic and
    handle related functionalities.
    """

    def __init__(
        self,
        name: str,
        queue,
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

    def start_listen(self):
        """
        This function must be run in a child process, as it is blocking.
        """
        self.client.loop_forever()

    # Call backs
    def on_connect(self, client, userdata, flags, rc):
        """
        This function is called upon the client gets connected to the broker
        """
        if rc == 0:
            print("Connection successful")
            # subscribe to the given topic upon connection is established
            self.client.subscribe(self.topic)
        else:
            print("Connection fails, reconnect in 1 second")
            sleep(2)
            self.client.reconnect()

    def on_message(self, client, userdata, message):
        """
        This function is called upon the client receives message from the topic
        it subscribes to. It proceeds to push the message to the queue such
        that the parent process can get the message.
        """
        self.queue.put(str(message.payload.decode("utf-8")))

    def on_subscribe(self, client, userdata, mid, granted_qos):
        """
        This function is called upon the client successfully subscribes to a
        topic.
        """
        print("Subscribed!")

    def close(self):
        """
        End the life of the client instance
        """
        self.client.loop_stop()
        self.client.disconnect()
