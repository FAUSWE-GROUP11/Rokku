import json
import logging
import logging.config
import os

import yaml

from src.raspberry_pi_ui.buttons.button import Button
from src.raspberry_pi_ui.utility import set_button_property, wait_msg


class RecordButton(Button):
    """A wrapper class representing the talk button widget on UI.

    Inherit from parent class Button
    """

    def __init__(self, button, pub, msg_q):
        """Constructor of the class, which inherit from Button class"""
        super().__init__(button, pub, msg_q, "Record")

        # unique functionality flags
        self.recording = False

        # variables to catch youtube links sent back (Strings)
        self.yt_playlist_link = None

        # set up logger
        with open(
            f"{os.path.dirname(__file__)}/../../../logger_config.yaml", "r"
        ) as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
        self.logger = logging.getLogger("RecordButton")

    def on_clicked(self, widget):
        """Callback when `Record` button is clicked.

        This will be called on whenever the Record button is clicked
        First will communicate with rpi_out to see if a clip is being record
        or not and will set the self.recording flag accordingly

        If recording still, do nothing

        If not record, send signal to record clip and set self.recording
        accordingly.
        """
        # Sets button to yellow while rpi_in tries communicating with rpi_out
        set_button_property(self, "yellow", "Spooling up camera...")
        # Check if not recording
        if not self.recording:
            self.logger.info("Sending record ON message to rpi_out...")
            self.pub.publish(json.dumps(["record", True]))
            try:  # wait for rpi_out to send true msg back
                self.recording = wait_msg("record", self.logger, self.msg_q)[1]
            except IndexError:  # no message received
                self.recording = False
        if self.recording:
            # Since rpi_out sent back true it should be recording now
            self.logger.info("rpi_out is recording now...")
            # turn button to red if not already red
            set_button_property(self, "red", "Recording...")
            # waiting for rpi_out to send youtube playlist link
            try:  # wait for rpi_out to send msg back
                self.yt_playlist_link = wait_msg(
                    "yt_playlist_link", self.logger, self.msg_q
                )[1]
            except IndexError:  # no message received
                self.recording = False
        # Does not catch if junk str was sent back
        if type(self.yt_playlist_link) == str and self.recording:
            self.logger.info("rpi_out recorded a video succesfully...")
        else:  # Something wrong with mqtt or the recording failed
            self.logger.error(
                f"Mqtt or the YouTube Api broke, no video was recorded. Recording status: rpi_in = {self.recording}"
            )
            # display message box with error
            #########################
            #   Missing code        #
            #########################
        set_button_property(self, "blue", "Record")
        self.recording = False
