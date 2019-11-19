import json
import logging
from logging import config
from multiprocessing import Queue
from time import sleep

import RPi.GPIO as GPIO
import yaml

from src.pi_to_pi.utility import set_up_pub_sub
from src.raspberry_pi_camera.camera_interface import CameraInterface
from src.raspberry_pi_driver.behaviors import (
    alarm,
    intercom,
    livestream,
    motion,
    record,
)
from src.raspberry_pi_driver.utility import (
    clean_up,
    command_line_parser,
    hash_prefix,
)

# set up logger
with open("logger_config.yaml", "r") as f:
    log_config = yaml.safe_load(f.read())
    config.dictConfig(log_config)
logger = logging.getLogger("RPI_OUT")

# set up RPi board
GPIO.setmode(GPIO.BCM)  # use GPIO.setmode(GPIO.board) for using pin numbers


def main():
    # parse command line argument
    args = command_line_parser("RPI_OUT_DRIVER")
    prefix: str = hash_prefix(args.public_id)
    # set up pub sub
    logger.info("Setting up publisher and subscriber")
    pub, msg_q, listen_proc = set_up_pub_sub(prefix, "out_to_in", "in_to_out")
    logger.info("Publisher and subscriber set up successfully!")
    motion_queue = Queue()
    camera_flags = {"livestream_on": False, "recording_on": False}
    # Create camera object
    cam = CameraInterface()
    try:
        # forever listening on topic "Rokku/in_to_out"
        while True:
            if not msg_q.empty():
                msg: str = msg_q.get()
                print(f"Sample behavior received: {msg}")
                identifier, flag = json.loads(msg)
                if identifier == "alarm":
                    alarm.alarm(pub, flag)
                if identifier == "intercom":
                    intercom.intercom(pub, flag)
                if identifier == "motion":
                    motion.motion(pub, flag, motion_queue)
                if identifier == "record":
                    record.record(pub, cam, camera_flags)
                if identifier == "livestream":
                    livestream.livestream(pub, cam, camera_flags)
            sleep(1)
    except (KeyboardInterrupt, SystemExit):
        logger.warning("Termination signal sensed.")
        clean_up(logger, processes=[listen_proc], cmds=[])
    logger.info("\n******* rpi_out_driver ends *******\n")
    GPIO.cleanup()


if __name__ == "__main__":
    main()
