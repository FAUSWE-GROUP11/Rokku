import json
from time import sleep

from src.pi_to_pi import publisher
from src.raspberry_pi_ui import message_box
from src.raspberry_pi_ui.utility import play_notification_sound, retrieve_msg


def alert(topic, msg_q, logger) -> None:
    """Alert user when motion sensor is really triggered.

    An alerting sound will be played for 30 seconds and a pop-up window will
    appear. User must acknowledges the alert in order to get back to the
    regular UI.

    :param topic:       MQTT publisher topic (note this is not publisher
                        object itself).
    :param msg_q:       Main queue to communicate between rpi_in and rpi_out
    :param logger:      For logging purpose
    """
    # Inheriting pub object from rokku.py fails to publish messages. This
    # probably has something to with deadlock between UI's threading and paho
    # MQTT's threading. Once a new publisher object is established here, publish
    # is normal again.
    pub = publisher.Publisher(topic=topic)
    while True:
        # receive msg with "motion_detected" identifier
        if not msg_q.empty() and retrieve_msg("motion_detected", msg_q):
            logger.info("Message for 'motion_detected' received from rpi_out.")

            # once "motion_detected" message is received, we do the following

            # play alert sound
            duration = 30
            play_notification_sound(duration, logger)

            # show pop-up window
            message = message_box.MessageBox(
                "Motion Detected", "Motion is detected outside!"
            )
            message.run()

            # for testing purpose only
            sleep(5)
            pub.publish(json.dumps(["motion_ackd", True]))

        sleep(1)
