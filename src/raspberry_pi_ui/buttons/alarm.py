import json
import logging
import logging.config
import os

import yaml

from src.raspberry_pi_ui import message_box
from src.raspberry_pi_ui.buttons.button import Button
from src.raspberry_pi_ui.utility import set_button_property, wait_msg


class AlarmButton(Button):
    """A wrapper class representing the talk button widget on UI.

    Inherit from parent class Button
    """

    def __init__(self, button, pub, msg_q):
        """Constructor of the class, which inherit from Button class"""
        super().__init__(button, pub, msg_q, "Alarm")

        # unique functionality flags
        self.alarm_sounding = False
        self.alarm_sounding_out = False
        # set up logger
        with open(
            f"{os.path.dirname(__file__)}/../../../logger_config.yaml", "r"
        ) as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
        self.logger = logging.getLogger("AlarmButton")

    def on_clicked(self, widget):
        """Callback when `Alarm` button is clicked

        First will communicate with rpi_out to see if sound is being played and will set the self.alarm_sounding flag accordingly
        If sound alarm is active, do nothing
        If not active, send signal to sound alarm and set self.alarm_sounding accordingly
        """
        # user wants to set off alarm on rpi_out
        if not self.alarm_sounding and not self.alarm_sounding_out:
            # turn button yellow, but with message "Acitvating"
            set_button_property(self, "yellow", "Activating...")
            # let rpi_in know intent to sound alarm on rpi_out
            self.logger.info("Activating alarm on rpi_out...")
            self.alarm_sounding = True
            self.logger.info("Sending alarm SOUND message to rpi_out...")
            self.pub.publish(json.dumps(["alarm", True]))
            try:  # wait for rpi_out to send msg back
                self.alarm_sounding_out = wait_msg(
                    "alarm", self.logger, self.msg_q
                )[1]
            except IndexError:  # no message received
                # this is assuming rpi_out did not change state
                self.alarm_sounding = False

            # If message from rpi_out was recieved
            if self.alarm_sounding_out:
                # buzzer is playing on rpi_out: turn button to red
                self.logger.info("Alarm SOUNDING on rpi_out")
                set_button_property(self, "red", "Silence Alarm")
            else:  # A message from rpi_out was not recieved
                self.logger.error(
                    f"Alarm status: rpi_in = {self.alarm_sounding}, rpi_out = {self.alarm_sounding_out}"
                )
                # display message box with error
                message = message_box.MessageBox("title", "message")
                message.run()

                set_button_property(self, "blue", "Sound Alarm")
                self.alarm_sounding = False

        # Alarm is sounding. Silence Alarm.
        elif self.alarm_sounding and self.alarm_sounding_out:
            # turn button yellow, but with message "Silencing"
            set_button_property(self, "yellow", "Silencing...")
            self.logger.info("Silencing rpi_out alarm...")
            self.alarm_sounding = False

            # Send silence signal
            self.logger.info("Sending alarm SILENCE message to rpi_out...")
            self.pub.publish(json.dumps(["alarm", False]))
            try:  # wait for rpi_out to send msg back
                self.alarm_sounding_out = wait_msg(
                    "alarm", self.logger, self.msg_q
                )[1]
            except IndexError:  # no message received
                # this is assuming rpi_out did not change state
                self.alarm_sounding = True

            if not self.alarm_sounding:
                # rpi_out message recieved, Alarm sound is off, turn button to blue
                self.logger.info("Alarm is SILENCED on rpi_out")
                set_button_property(self, "blue", "Sound Alarm")
                self.alarm_sounding = False
            else:  # A message from rpi_out was not recieved
                self.logger.error(
                    f"Alarm status: rpi_in = {self.alarm_sounding}, rpi_out = {self.alarm_sounding_out}"
                )
                # display message box with error
                message = message_box.MessageBox("title", "message")
                message.run()

                set_button_property(self, "red", "Silence")
                self.alarm_sounding = True
