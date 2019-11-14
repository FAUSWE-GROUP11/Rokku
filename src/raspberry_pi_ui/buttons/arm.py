import json
import logging
import logging.config
import os

import yaml

from src.raspberry_pi_ui.buttons.button import Button
from src.raspberry_pi_ui.utility import set_button_property, wait_msg


class ArmButton(Button):
    """A wrapper class representing the talk button widget on UI.

    Inherit from parent class Button
    """

    def __init__(self, button, pub, msg_q):
        """Constructor of the class, which inherit from Button class"""
        super().__init__(button, pub, msg_q, "Arm")

        # unique functionality flags
        self.armed = False
        self.armed_out = False

        # set up logger
        with open(
            f"{os.path.dirname(__file__)}/../../../logger_config.yaml", "r"
        ) as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
        self.logger = logging.getLogger("ArmButton")

    def on_clicked(self, widget):
        """Callback when `Arm` button is clicked.

        Inbetween changing motion detector state, the button will be yellow
        with 'Arming' and 'Disarming' messages to notify that the change has
        not taken place yet.

        If the alarm is not set, sets text to 'Disarm' and color to red along
        with sending a message to rpi_out activing armed flag.

        If the alarm is set, sets text to 'Arm' and color to blue along with
        sending a message to rpi_out disactiving armed flag.
        """
        # user wants to turn on motion_sensor for rpi_out
        if not self.armed and not self.armed_out:
            # turn button yellow, but with message "Arming"
            set_button_property(self, "yellow", "Arming...")
            # let rpi_in know to arm motion detector
            self.logger.info("Arming rpi_out motion sensor...")
            self.armed = True

            self.logger.info(
                "Sending motion detection ON message to rpi_out..."
            )
            self.pub.publish(json.dumps(["motion", True]))
            try:  # wait for rpi_out to send msg back
                self.armed_out = wait_msg("motion", self.logger, self.msg_q)[1]
            except IndexError:  # no message received
                # this is assuming rpi_out did not change state
                self.armed = False

            # If message from rpi_out was recieved
            if self.armed_out:
                # motion_sensor is 'armed' on rpi_out: turn button to red
                self.logger.info("Motion sensor ARMED on rpi_out")
                set_button_property(self, "red", "Disarm")
            else:  # A message from rpi_out was not recieved
                self.logger.error(
                    f"Motion status: rpi_in = {self.armed}, rpi_out = {self.armed_out}"
                )
                # display message box with error
                #########################
                #   Missing code        #
                #########################
                set_button_property(self, "blue", "Arm")
                self.armed = False

        # motion detection active. Turn off sensor.
        elif self.armed and self.armed_out:
            # turn button yellow, but with message "Disarming"
            set_button_property(self, "yellow", "Disarming...")
            self.logger.info("Disarming rpi_out motion sensor...")
            self.armed = False

            # Send disarm signal
            self.logger.info("Sending armed OFF message to rpi_out...")
            self.pub.publish(json.dumps(["motion", False]))
            try:  # wait for rpi_out to send msg back
                self.armed_out = wait_msg("motion", self.logger, self.msg_q)[1]
            except IndexError:  # no message received
                # this is assuming rpi_out did not change state
                self.armed = True

            if not self.armed_out:
                # rpi_out message recieved, motion detection is off, turn button to blue
                self.logger.info("Motion sensor is OFF on rpi_out")
                set_button_property(self, "blue", "Arm")
                self.armed = False
            else:  # A message from rpi_out was not recieved
                self.logger.error(
                    f"Motion status: rpi_in = {self.armed}, rpi_out = ?"
                )
                # display message box with error
                #########################
                #   Missing code        #
                #########################
                set_button_property(self, "red", "Disarm")
                self.armed = True
