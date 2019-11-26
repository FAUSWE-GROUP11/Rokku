import configparser
import os
import sys

import pytest
import fake_rpi

sys.modules["picamera"] = fake_rpi.picamera  # Fake picamera

from src.raspberry_pi_camera import camera_interface


@pytest.fixture(scope="package")
def camera():
    """Camera interface object"""
    app_config = configparser.ConfigParser()
    app_config.read(
        f"{os.path.dirname(__file__)}/fixtures/test_app_config.ini"
    )
    video_config = app_config["video"]
    yield camera_interface.CameraInterface(video_config)
