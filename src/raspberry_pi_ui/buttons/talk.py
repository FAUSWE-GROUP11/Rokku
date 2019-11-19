import json
import logging
import logging.config
import os

import yaml

from src.raspberry_pi_intercom import mumble
from src.raspberry_pi_ui.buttons.button import Button
from src.raspberry_pi_ui.utility import set_button_property, wait_msg


class TalkButton(Button):
    """A wrapper class representing the talk button widget on UI.

    Inherit from parent class Button
    """

    def __init__(self, button, pub, msg_q, intercom_config):
        """Constructor of the class, which inherit from Button class

        :param button:          The real button widget from UI.
        :param pub:             MQTT publisher object
        :param msg_q:           A queue in MQTT subscriber object to listen to
                                msg sent from rpi_in
        :param intercom_config: Config to connect to a mumble client.
        """
        super().__init__(button, pub, msg_q, "Talk")

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

        self.intercom_config = intercom_config

    def on_clicked(self, widget) -> None:
        """Callback when `Talk` button is clicked.

        This will be called on whenever the Talk button is clicked
        First will communicate with rpi_out to see if intercom is active on
        both parties and will set the self.intercom flag accordingly.

        If intercom is active, turn off intercom and set color to blue with
        'Talk' text for button.

        If intercom is not active, send signal to activate intercom and set
        self.intercom_active accordingly

        Intercom will reset if error message is received when trying to active
        intercom.

        :param widget:      Pointing to this button. Not used in the function.

        :return:    None
        """
        # Always turn button to yellow whenever button is clicked
        set_button_property(self, "yellow", "Configuring...")
        # user wants to turn on intercom for both rpi_in and rpi_out
        if not self.rpi_in_intercom_on and not self.rpi_out_intercom_on:
            # Turn on Mumble for rpi_in
            mumble.turn_on(self.intercom_config, "rpi_in", self.logger)
            self.rpi_in_intercom_on = mumble.is_on(self.logger)

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
                self.rpi_in_intercom_on = not mumble.turn_off(self.logger)
                self.rpi_out_intercom_on = False
                set_button_property(self, "blue", "Talk")

        # intercom active for both devices. Turn off both
        elif self.rpi_in_intercom_on and self.rpi_out_intercom_on:
            self.rpi_in_intercom_on = not mumble.turn_off(self.logger)  # OFF
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
