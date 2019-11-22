import configparser
import os
from multiprocessing import Queue
import sys

import pytest
import fake_rpi

sys.modules["RPi"] = fake_rpi.RPi
sys.modules["RPi.GPIO"] = fake_rpi.RPi.GPIO


from src.raspberry_pi_motion_sensor.motion_interface import MotionPir


@pytest.fixture(scope="package")
def motion_sensor():
    """Set up motion sensor."""
    app_config = configparser.ConfigParser()
    app_config.read(
        f"{os.path.dirname(__file__)}/fixtures/test_app_config.ini"
    )
    motion_sensor_config = app_config["motion_sensor"]
    motion_queue = Queue()
    motion_pin = 23
    yield MotionPir(motion_queue, motion_pin, motion_sensor_config)
