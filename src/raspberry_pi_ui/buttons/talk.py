import json
import logging
import logging.config
import os

import yaml

from src.raspberry_pi_ui.buttons.button import Button
from src.raspberry_pi_ui.utility import set_button_property, wait_msg


class TalkButton(Button):
    """A wrapper class representing the talk button widget on UI.

    Inherit from parent class Button
    """

    def __init__(self, button, pub, msg_q):
        """Constructor of the class, which inherit from Button class"""
        super().__init__(button, pub, msg_q)

        # unique functionality flags
        self.rpi_in_intercom_on = False
        self.rpi_out_intercom_on = False

        # set up logger
        with open(
            f"{os.path.dirname(__file__)}/../../../logger_config.yaml", "r"
        ) as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
        self.logger = logging.getLogger("TalkButton")

    def on_clicked(self, widget):
        # Always turn button to yellow whenever button is clicked
        set_button_property(self, "yellow", "Configuring...")
        # user wants to turn on intercom for both rpi_in and rpi_out
        if not self.rpi_in_intercom_on and not self.rpi_out_intercom_on:
            # turn on barnard in rpi_in
            self.logger.info("Turning on barnard Mumble CLI client...")
            # code to turn on barnard
            #########################
            #   Missing code        #
            #########################
            self.rpi_in_intercom_on = True

            # Only signal to rpi_out if rpi_in's Mumble client is on
            if self.rpi_in_intercom_on:
                self.logger.info("Sending intercom ON message to rpi_out...")
                self.pub.publish(json.dumps(["intercom", True]))
                try:  # wait for rpi_out to send msg back
                    self.rpi_out_intercom_on = wait_msg(
                        "intercom", self.logger, self.msg_q
                    )[1]
                except IndexError:  # no message received
                    self.rpi_out_intercom_on = False

            if self.rpi_out_intercom_on and self.rpi_in_intercom_on:
                # intercom is on for both sides, turn button to red
                self.logger.info("Intercom ON on both devices")
                set_button_property(self, "red", "End Talk")
            else:  # at least one of the intercom is not on
                self.logger.error(
                    f"Intercom status: rpi_in = {self.rpi_in_intercom_on}, rpi_out = {self.rpi_out_intercom_on}"
                )
                # display message box with error
                #########################
                #   Missing code        #
                #########################
                set_button_property(self, "blue", "Talk")
                self.rpi_in_intercom_on = False
                self.rpi_out_intercom_on = False

        # intercom active for both devices. Turn off both
        elif self.rpi_in_intercom_on and self.rpi_out_intercom_on:
            self.logger.info("Turning off rpi_in barnard Mumble CLI client...")
            # code to turn off barnard
            #########################
            #   Missing code        #
            #########################
            self.rpi_in_intercom_on = False

            # Only signal to rpi_out if rpi_in's Mumble client is off
            if not self.rpi_in_intercom_on:
                self.logger.info("Sending intercom OFF message to rpi_out...")
                self.pub.publish(json.dumps(["intercom", False]))
                try:  # wait for rpi_out to send msg back
                    self.rpi_out_intercom_on = wait_msg(
                        "intercom", self.logger, self.msg_q
                    )[1]
                except IndexError:  # no message received
                    self.rpi_out_intercom_on = False

            if not self.rpi_out_intercom_on and not self.rpi_in_intercom_on:
                # intercom is off for both sides, turn button to red
                self.logger.info("Intercom OFF on both devices")
            set_button_property(self, "blue", "Talk")
            self.rpi_in_intercom_on = False
            self.rpi_out_intercom_on = False
