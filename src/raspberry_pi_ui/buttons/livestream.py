import json
import logging
import logging.config
import os

import yaml

from src.raspberry_pi_ui.buttons.button import Button
from src.raspberry_pi_ui.utility import set_button_property, wait_msg


class LivestreamButton(Button):
    """A wrapper class representing the talk button widget on UI.

    Inherit from parent class Button
    """

    def __init__(self, button, pub, msg_q):
        """Constructor of the class, which inherit from Button class"""
        super().__init__(button, pub, msg_q, "Live Stream")

        # unique functionality flags
        self.livestream = False

        # variables to catch youtube links sent back (Strings)
        self.yt_livestream_link = None

        # set up logger
        with open(
            f"{os.path.dirname(__file__)}/../../../logger_config.yaml", "r"
        ) as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
        self.logger = logging.getLogger("LivestreamButton")

    def on_clicked(self, widget):
        """Callback when `Live Stream` button is clicked.

        This will be called on whenever the Live Stream button is clicked
        First will communicate with rpi_out to see if a clip is being
        recorded or the livestream is already on and will set the
        self.livestream flag accordingly.

        If livestreaming still, turn off livestream and close window

        If not livestreaming, send signal to livestream, open window and set self.livestream
        accordingly.
        """
        # Sets button to yellow while rpi_in tries communicating with rpi_out
        set_button_property(self, "yellow", "Spooling up camera...")
        # Check if not recording
        if not self.livestream:
            self.logger.info("Sending livestream ON message to rpi_out...")
            self.pub.publish(json.dumps(["livestream", True]))
            try:  # wait for rpi_out to send true msg back
                self.livestream = wait_msg(
                    "livestream", self.logger, self.msg_q
                )[1]
                # True sent back
                if self.livestream:
                    # Since rpi_out sent back true it should be livestreaming
                    self.logger.info("rpi_out is livestreaming now...")
                    # turn button to red if not already red
                    set_button_property(self, "red", "Livestreaming...")
                    # waiting for rpi_out to send youtube playlist link
                    self.yt_livestream_link = wait_msg(
                        "yt_livestream_link",
                        self.logger,
                        self.msg_q,
                        timeout=30,
                    )[1]
                    # Does not catch if junk str was sent back
                    if type(self.yt_livestream_link) == str:
                        pass
                        # display window with livestream
                        #########################
                        #   Missing code        #
                        #########################
                else:  # Something wrong with mqtt or the recording failed
                    self.logger.error(
                        f"The camera is running, Mqtt broke or the YouTube Api broke. Live Stream status: rpi_in = {self.livestream}"
                    )
                    # display message box with error
                    #########################
                    #   Missing code        #
                    #########################
            except IndexError:  # no message received
                self.livestream = True
        elif self.livestream:
            # Try to turn off livestream
            self.pub.publish(json.dumps(["livestream", False]))
            # Log event
            self.logger.info("Turning off rpi_out livestream...")
            try:  # wait for rpi_out to send msg back.
                self.livestream = wait_msg(
                    "livestream", self.logger, self.msg_q
                )[1]
            except IndexError:  # no message received
                self.livestream = True
            if not self.livestream:
                # Reset button to blue
                set_button_property(self, "blue", "Livestream")
                # Log event
                self.logger.info("Livestream is off...")
                # close livestream window
                #########################
                #   Missing code        #
                #########################
            else:
                self.logger.info("Livestream won't turn off...")
                set_button_property(self, "red", "Livestreaming...")
                # display message saying to try again later
                #########################
                #   Missing code        #
                #########################
