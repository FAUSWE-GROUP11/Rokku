from src.raspberry_pi_ui import rokku
from src.pi_to_pi import publisher, subscriber
from multiprocessing import Process, Queue
import logging
import logging.config
import yaml
from time import sleep


# set up logger
with open("logger_config.yaml", "r") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)
logger = logging.getLogger("RPI_IN")


logger.info("Setting up publisher and subscriber")
# publisher from rpi_in to rpi_out
pub = publisher.Publisher(topic="Rokku/in_to_out")
msg_q = Queue()
# subscriber listening messages from rpi_out to rpi_in
sub = subscriber.Subscriber(msg_q, topic="Rokku/out_to_in")
# listen in a separate process
listen_proc = Process(target=sub.start_listen, args=())
listen_proc.start()
logger.info("Publisher and subscriber set up successfully!")

try:
    logger.info("Spinning up UI...")
    main = rokku.Main(pub, msg_q)
    main.run()
    logger.info("UI terminated.")
except (KeyboardInterrupt, SystemExit):
    pass  # do nothing here because the code below completes the cleanup

logger.info("Terminate listening process of subscriber")
listen_proc.terminate()
while listen_proc.is_alive():
    logger.debug("Waiting for termination...")
    sleep(1)
listen_proc.join()
logger.info("Listening process of subscriber terminated successfully!")
logger.info("\n******* rpi_in_driver ends *******\n")
