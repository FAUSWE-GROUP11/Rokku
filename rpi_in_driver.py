import configparser
import logging
from logging import config
from multiprocessing import Process

import yaml

from src.pi_to_pi.utility import set_up_pub_sub
from src.raspberry_pi_driver.behaviors import alert
from src.raspberry_pi_driver.utility import (
    clean_up,
    command_line_parser,
    hash_prefix,
)
from src.raspberry_pi_ui import rokku

# set up logger
with open("logger_config.yaml", "r") as f:
    log_config = yaml.safe_load(f.read())
    config.dictConfig(log_config)
logger = logging.getLogger("RPI_IN")


def main():
    # parse command line argument
    args = command_line_parser("RPI_IN_DRIVER")
    prefix: str = hash_prefix(args.public_id)

    # parse configuration file
    app_config = configparser.ConfigParser()
    app_config.read("./app_config.ini")
    intercom_config = app_config["mumble"]

    # set up pub sub
    logger.info("Setting up publisher and subscriber")
    pub, msg_q, listen_proc = set_up_pub_sub(prefix, "in_to_out", "out_to_in")
    logger.info("Publisher and subscriber set up successfully!")
    try:
        # Set up motion sensor alert
        # Must use a separate process to handle alert.alert, because it contains
        # a forever loop, which if directly invoked in UI, would cause failure
        # when UI is closed.
        alert_proc = Process(
            target=alert.alert,
            name="Alert User",
            args=(pub.topic, msg_q, logger),
        )
        alert_proc.start()
        logger.info("Spinning up UI...")
        rokku_ui = rokku.Main(pub, msg_q, intercom_config)
        rokku_ui.run()
        logger.info("UI terminated.")
    except (KeyboardInterrupt, SystemExit):
        pass  # do nothing here because the code below completes the cleanup

    clean_up(logger, processes=[listen_proc, alert_proc], cmds=[])
    logger.info("\n******* rpi_in_driver ends *******\n")


if __name__ == "__main__":
    main()
