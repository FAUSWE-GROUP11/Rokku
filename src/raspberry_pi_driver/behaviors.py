import json
from time import sleep

from src.raspberry_pi_alarm.buzzer_interface import Buzzer
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


def record(pub, flag, cam, camera_flags) -> None:
    """Behavior that will record a video, upload it to YouTube, and publish an URL to rpi_in."""
    if (not camera_flags["livestream_on"]) and (
        not camera_flags["recording_on"]
    ):
        # Prevent other recordings
        camera_flags["recording_on"] = True
        # Will change button color, assuming video is being recorded.
        pub.publish(json.dumps(["record", True]))
        # Start recording and capture string to file
        filepath = cam.record_video()
        # Upload to YouTube
        cam.upload_to_yt(filepath)
        # Sleep thread for 5 seconds
        sleep(5)
        # Once recording is over and static url to playlist is given
        pub.publish(
            json.dumps(["yt_playlist_link", cam.get_yt_playlist_link()])
        )
    else:
        pub.publish(json.dumps(["record", False]))  # Something went wrong
    # Free up camera resource
    camera_flags["recording_on"] = False


def livestream(pub, flag, cam, camera_flags) -> None:
    """Behavior that will livestream to YouTube, and publish an URL to rpi_in."""
    if (not camera_flags["livestream_on"]) and (
        not camera_flags["recording_on"]
    ):
        # Prevent other livestreams
        camera_flags["livestream_on"] = True
        # Will change button color, assuming livestream is running.
        pub.publish(json.dumps(["livestream", True]))
        # Start livestreaming and capture link
        yt_livestream_link = cam.start_yt_stream(
            "a1be-2axc-fkwq-8t2u or 6a8u-vpvr-er4h-e22h"
        )
        # Sleep thread for 5 seconds
        sleep(5)
        # Once recording is over and static url to link is given
        pub.publish(json.dumps(["yt_livestream_link", yt_livestream_link]))
    elif camera_flags["recording_on"]:
        # Send None telling rpi_in to display an error message
        pub.publish(json.dumps(["livestream", None]))
    else:
        # Turn livestream off
        pub.publish(json.dumps(["livestream", False]))  # Turn livestream off
        # Free up camera resource
        camera_flags["livestream_on"] = False
        # Turn off stream
        cam.stop_yt_stream()


def alarm(pub, flag) -> None:
    """Behavior that will set off alarm on rpi_out."""
    alarm = Buzzer(24)
    if flag:
        alarm.sound()
    else:
        alarm.silence()
    pub.publish(json.dumps(["alarm", alarm.get_state()]))
