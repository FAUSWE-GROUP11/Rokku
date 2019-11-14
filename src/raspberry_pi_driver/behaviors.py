import json
from time import sleep

from src.raspberry_pi_motion_sensor.motion_interface import MotionPir


def motion(pub, flag, queue) -> None:
    """Behavior that will arm or disarm the motion sensor."""
    sensor = MotionPir(queue, 23)
    if flag:
        sensor.set_armed()
    else:
        sensor.set_disarmed()
    pub.publish(json.dumps(["motion", sensor.get_state()]))


def intercom(pub, flag) -> None:
    """Behavior that will connect or disconnect rpi_out with mumble client."""
    if flag:
        pass  # set up intercom for rpi_out
        pub.publish(json.dumps(["intercom", True]))
    else:
        pass  # disconnect intercom
        pub.publish(json.dumps(["intercom", False]))


def record(pub, flag) -> None:
    """Behavior that will record a video, upload it to YouTube, and publish an URL to rpi_in."""
    if flag:
        # Start recording.
        # Will change button color, assuming video is being recorded.
        pub.publish(json.dumps(["record", True]))

        # Record video
        #########################
        #   Missing code        #
        #########################

        # simulate recording for now. Delete this code once the real code is
        # available above
        sleep(5)
        yt_playlist_link = ""

        # Once recording is over and YouTube gives link to playlist
        pub.publish(json.dumps(["yt_playlist_link", yt_playlist_link]))
    else:
        pub.publish(json.dumps(["record", False]))  # Something went wrong


def alarm(pub, flag) -> None:
    """Behavior that will set off alarm on rpi_out."""
    if flag:
        pass  # A noise worse than death itself
    else:
        pass  # Tranquility
