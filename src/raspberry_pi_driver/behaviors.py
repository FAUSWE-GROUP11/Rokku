import json

from ..raspberry_pi_alarm.buzzer_interface import Buzzer
from ..raspberry_pi_motion_sensor.motion_interface import MotionPir


def motion(pub, flag, queue) -> None:
    """Behavior that will arm or disarm the motion sensor."""
    sensor = MotionPir(queue, 23)
    if flag is True:
        sensor.set_armed()
    else:
        sensor.set_disarmed()
    pub.publish(json.dumps(["motion", sensor.get_state()]))


def intercom(pub, flag) -> None:
    """Behavior that will connect or disconnect rpi_out with mumble client."""
    if flag is True:
        pass  # set up intercom for rpi_out
        pub.publish(json.dumps(["intercom", True]))
    else:
        pass  # disconnect intercom
        pub.publish(json.dumps(["intercom", False]))


def record(pub, flag) -> None:
    """Behavior that will record a video, upload it to YouTube, and publish an URL to rpi_in."""
    if flag is True:
        # Start recording.
        pub.publish(
            json.dumps(["record", True])
        )  # Will change button color, assuming video is being recorded.
        # Once recording is over and YouTube gives link to playlist
        pub.publish(json.dumps(["yt_playlist_link", True]))
    else:
        pub.publish(json.dumps(["record", False]))  # Something went wrong


def alarm(pub, flag) -> None:
    """Behavior that will set off alarm on rpi_out."""
    alarm = Buzzer(24)
    if flag is True:
        alarm.sound()
    else:
        alarm.silence()
    pub.publish(json.dumps(["alarm", alarm.get_state()]))