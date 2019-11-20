import configparser
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
from src.raspberry_pi_intercom.togglemute_button import start_togglemute_proc

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

    # parse configuration file
    app_config = configparser.ConfigParser()
    app_config.read("./app_config.ini")
    intercom_config = app_config["mumble"]
    motion_sensor_config = app_config["motion_sensor"]

    # set up pub sub
    logger.info("Setting up publisher and subscriber")
    pub, msg_q, listen_proc = set_up_pub_sub(prefix, "out_to_in", "in_to_out")
    logger.info("Publisher and subscriber set up successfully!")

    motion_queue = Queue()  # set up queue for motion sensor

    # set up flag for camera
    camera_flags = {"livestream_on": False, "recording_on": False}
    cam = CameraInterface()  # Create camera object

    # Run mute button in separate process
    togglemute_proc = start_togglemute_proc(logger)

    try:
        # forever listening on topic "{prefix}/in_to_out"
        while True:
            if not msg_q.empty():
                msg: str = msg_q.get()
                identifier, flag = json.loads(msg)
                if identifier == "alarm":
                    alarm.alarm(pub, flag)
                elif identifier == "intercom":
                    intercom.intercom(pub, flag, intercom_config, logger)
                elif identifier == "motion":
                    motion.motion(
                        pub, flag, motion_queue, motion_sensor_config
                    )
                elif identifier == "record":
                    record.record(pub, cam, camera_flags)
                elif identifier == "livestream":
                    livestream.livestream(pub, cam, camera_flags)
            sleep(1)
    except (KeyboardInterrupt, SystemExit):
        logger.warning("Termination signal sensed.")
        clean_up(logger, processes=[listen_proc, togglemute_proc], cmds=[])
    logger.info("\n******* rpi_out_driver ends *******\n")
    GPIO.cleanup()


if __name__ == "__main__":
    main()
