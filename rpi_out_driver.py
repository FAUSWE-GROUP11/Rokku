from src.pi_to_pi import publisher, subscriber
from multiprocessing import Process, Queue
import logging
import logging.config
import yaml
from time import sleep
import json


# set up logger
with open("logger_config.yaml", "r") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)
logger = logging.getLogger("RPI_OUT")


def set_up_pub_sub():
    """
    Utility function to set up pub and sub

    Args:
        None
    Return:
        publihser object, message queue, and a listening process for subscriber
    Raises:
        None
    """
    logger.info("Setting up publisher and subscriber")
    # publisher from rpi_in to rpi_out
    pub = publisher.Publisher(topic="Rokku/out_to_in")
    msg_q = Queue()
    # subscriber listening messages from rpi_out to rpi_in
    sub = subscriber.Subscriber(msg_q, topic="Rokku/in_to_out")
    # listen in a separate process
    listen_proc = Process(target=sub.start_listen, args=())
    listen_proc.start()
    logger.info("Publisher and subscriber set up successfully!")
    return pub, msg_q, listen_proc


def sample_behavior(msg_q, pub) -> None:
    """
    A sample behavior upon getting message form msg_q. This function can ONLY
    be called if there is something in the msg_q already. Sample behavior
    prints out the received message, and send back a message containing the
    same content.

    Args:
        msg_q:      The queue connecting this process to listen_proc
        pub:        Publisher for publishing MQTT message
    Returns:
        None
    Raises:
        None
    """
    msg: str = msg_q.get()
    print(f"Sample behavior received: {msg}")
    identifier, flag = json.loads(msg)
    sleep(1)
    pub.publish(json.dumps([identifier, flag]))


def main():
    pub, msg_q, listen_proc = set_up_pub_sub()
    try:
        # forever listening on topic "Rokku/in_to_out"
        while True:
            if not msg_q.empty():
                # code behaviors
                sample_behavior(msg_q, pub)
            sleep(1)
    except (KeyboardInterrupt, SystemExit):
        logger.warning("Termination signal sensed.")
        logger.info("Terminate listening process of subscriber")
        listen_proc.terminate()
        while listen_proc.is_alive():
            logger.debug("Waiting for termination...")
            sleep(1)
        listen_proc.join()
        logger.info("Listening process of subscriber terminated successfully!")
    logger.info("\n******* rpi_out_driver ends *******\n")


if __name__ == "__main__":
    main()
