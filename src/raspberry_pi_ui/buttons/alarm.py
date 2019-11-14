# import json
import logging
import logging.config
import os

import yaml

from src.raspberry_pi_ui.buttons.button import Button

# from src.raspberry_pi_ui.utility import set_button_property, wait_msg


class AlarmButton(Button):
    """A wrapper class representing the talk button widget on UI.

    Inherit from parent class Button
    """

    def __init__(self, button, pub, msg_q):
        """Constructor of the class, which inherit from Button class"""
        super().__init__(button, pub, msg_q, "Alarm")

        # unique functionality flags

        # set up logger
        with open(
            f"{os.path.dirname(__file__)}/../../../logger_config.yaml", "r"
        ) as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
        self.logger = logging.getLogger("AlarmButton")

    def on_clicked(self, widget):
        """Callback when `Alarm` button is clicked.


        """
        #########################
        #   Missing code        #
        #########################
        pass
