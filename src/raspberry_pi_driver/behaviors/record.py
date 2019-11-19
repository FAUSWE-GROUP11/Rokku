import json
from time import sleep


def record(pub, cam, camera_flags) -> None:
    """Behavior that will record a video, upload it to YouTube,
    and publish an URL to rpi_in.
    """
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
