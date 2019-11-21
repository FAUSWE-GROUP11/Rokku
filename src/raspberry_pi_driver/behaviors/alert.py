import json
from time import sleep

from src.raspberry_pi_ui.utility import retrieve_msg


def alert(pub, msg_q, logger) -> None:
    """Alert user when motion sensor is really triggered.

    An alerting sound will be played for 30 seconds and a pop-up window will
    appear. User must acknowledges the alert in order to get back to the
    regular UI.

    :param pub:         MQTT publihser object
    :param msg_q:       Main queue to communicate between rpi_in and rpi_out
    :param logger:      For logging purpose
    """
    while True:
        # receive msg with "motion_detected" identifier
        if not msg_q.empty() and retrieve_msg("motion_detected", msg_q):
            logger.info("Message for 'motion_detected' received from rpi_out.")

            # once "motion_detected" message is received, we do the following

            # play alert sound
            #########################
            #   Missing code        #
            #########################

            # show pop-up window
            #########################
            #   Missing code        #
            #########################

            # for testing purpose only
            sleep(10)
            pub.publish(json.dumps(["motion_ackd", True]))
        sleep(1)
