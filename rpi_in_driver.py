import logging
import logging.config

import yaml

from src.pi_to_pi.utility import set_up_pub_sub
from src.raspberry_pi_driver.utility import (
    command_line_parser,
    hash_prefix,
    terminate_proc,
)
from src.raspberry_pi_ui import rokku

# set up logger
with open("logger_config.yaml", "r") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)
logger = logging.getLogger("RPI_IN")


def main():
    # parse command line argument
    args = command_line_parser("RPI_IN_DRIVER")
    prefix: str = hash_prefix(args.public_id)
    # set up pub sub
    logger.info("Setting up publisher and subscriber")
    pub, msg_q, listen_proc = set_up_pub_sub(prefix, "in_to_out", "out_to_in")
    logger.info("Publisher and subscriber set up successfully!")
    try:
        logger.info("Spinning up UI...")
        rokku_ui = rokku.Main(pub, msg_q)
        rokku_ui.run()
        logger.info("UI terminated.")
    except (KeyboardInterrupt, SystemExit):
        pass  # do nothing here because the code below completes the cleanup

    logger.info(f"Terminating {listen_proc.name}...")
    terminate_proc(listen_proc)
    logger.info(f"{listen_proc.name} terminated successfully!")
    logger.info("\n******* rpi_in_driver ends *******\n")


if __name__ == "__main__":
    main()
