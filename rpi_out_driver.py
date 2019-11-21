import configparser
import json
import logging
from logging import config
from multiprocessing import Process, Queue
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
    led_on,
    terminate_proc,
)
from src.raspberry_pi_intercom.togglemute_button import start_togglemute_proc
from src.raspberry_pi_motion_sensor.motion_interface import MotionPir

# set up logger
with open("logger_config.yaml", "r") as f:
    log_config = yaml.safe_load(f.read())
    config.dictConfig(log_config)
logger = logging.getLogger("RPI_OUT")


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

    # set up flag for camera
    camera_flags = {"livestream_on": False, "recording_on": False}
    cam = CameraInterface()  # Create camera object

    # set up motion sensor
    motion_queue = Queue()  # set up queue for motion sensor
    motion_pin = 23  # channel 23 (GPIO23) is connected to motion sensor
    sensor = MotionPir(motion_queue, motion_pin, motion_sensor_config)
    led_proc = None  # placeholder for process lighting up LED.

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
                    motion.motion(pub, flag, sensor)
                elif identifier == "record":
                    record.record(pub, cam, camera_flags)
                elif identifier == "livestream":
                    livestream.livestream(pub, cam, camera_flags)
                elif identifier == "motion_ackd":
                    # User acknowledged motion has been detected.
                    # Resume motion sensor
                    sensor.set_armed()
                    terminate_proc(led_proc, logger)

            if not motion_queue.empty():  # motion detected
                motion_queue.get()
                pub.publish(
                    json.dumps(["motion_detected", True])
                )  # alert user
                # Halt motion sensor as user deals with alert without explicitly
                # change rpi_in's UI (use should NOT be able to interact with
                # UI when the alert is on)
                sensor.set_disarmed()
                led_proc = Process(target=led_on, name="LED proc", args=(12,))
                led_proc.start()
            sleep(1)
    except (KeyboardInterrupt, SystemExit):
        logger.warning("Termination signal sensed.")
        clean_up(logger, processes=[listen_proc, togglemute_proc], cmds=[])
    logger.info("\n******* rpi_out_driver ends *******\n")
    GPIO.cleanup()


if __name__ == "__main__":
    main()
