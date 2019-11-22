import json
from time import sleep


def livestream(pub, cam, camera_flags) -> None:
    """Behavior that will livestream to YouTube,
    and publish an URL to rpi_in.
    """
    if (not camera_flags["livestream_on"]) and (
        not camera_flags["recording_on"]
    ):
        # Prevent other livestreams
        camera_flags["livestream_on"] = True
        # Will change button color, assuming livestream is running.
        pub.publish(json.dumps(["livestream", True]))
        # Start livestreaming and capture link
        yt_livestream_link = cam.start_yt_stream()
        # Sleep thread for 2 seconds
        sleep(2)
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
