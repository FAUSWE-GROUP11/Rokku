# import json
import logging
import logging.config
import os

import yaml

from src.raspberry_pi_ui import embedded_yt, message_box
from src.raspberry_pi_ui.buttons.button import Button

# from src.raspberry_pi_ui.utility import set_button_property, wait_msg


class VideoButton(Button):
    """A wrapper class representing the talk button widget on UI.
    Inherit from parent class Button
    """

    def __init__(self, button, pub, msg_q):
        """Constructor of the class, which inherit from Button class"""
        super().__init__(button, pub, msg_q, "Video")

        # unique functionality flags
        self.yt_videos_link = None

        # set up logger
        with open(
            f"{os.path.dirname(__file__)}/../../../logger_config.yaml", "r"
        ) as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
        self.logger = logging.getLogger("VideoButton")

    def on_clicked(self, widget):
        """Callback when `Videos` button is clicked.


        """
        #########################
        #   Missing code        #
        #########################

        # display message box with error
        message = message_box.MessageBox("title", "message")
        message.run()

        # Pass YT Video Playlist Link
        yt_window = embedded_yt.EmbeddedYT(self.yt_videos_link, "Videos")
        yt_window.run()
        pass
