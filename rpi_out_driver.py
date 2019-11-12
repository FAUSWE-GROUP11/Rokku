import logging
import logging.config
from time import sleep

import yaml

from src.pi_to_pi.utility import set_up_pub_sub
from src.raspberry_pi_driver.behaviors import (motion)
from src.raspberry_pi_driver.utility import (
    command_line_parser,
    hash_prefix,
    terminate_proc,
)

# set up logger
with open("logger_config.yaml", "r") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)
logger = logging.getLogger("RPI_OUT")


def main():
    # parse command line argument
    args = command_line_parser("RPI_OUT_DRIVER")
    prefix: str = hash_prefix(args.public_id)
    # set up pub sub
    logger.info("Setting up publisher and subscriber")
    pub, msg_q, listen_proc = set_up_pub_sub(prefix, "out_to_in", "in_to_out")
    logger.info("Publisher and subscriber set up successfully!")
    try:
        # forever listening on topic "Rokku/in_to_out"
        while True:
            if not msg_q.empty():
                msg: str = msg_q.get()
                print(f"Sample behavior received: {msg}")
                identifier, flag = json.loads(msg)
                if identifier is "motion":
                    motion(pub, flag)              
            sleep(1)
    except (KeyboardInterrupt, SystemExit):
        logger.warning("Termination signal sensed.")
        logger.info(f"Terminating {listen_proc.name}...")
        terminate_proc(listen_proc)
        logger.info(f"{listen_proc.name} terminated successfully!")
    logger.info("\n******* rpi_out_driver ends *******\n")


if __name__ == "__main__":
    main()
