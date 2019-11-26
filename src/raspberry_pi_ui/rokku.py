import logging
import logging.config
import os

import gi
import yaml

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")

from gi.repository import Gdk as gdk
from gi.repository import Gtk as gtk

from src.raspberry_pi_ui.buttons import (
    talk,
    arm,
    record,
    alarm,
    livestream,
    video,
)


class Main:
    """Class implemented to create the GUI."""

    def __init__(self, pub, msg_q, intercom_config, video_config):
        """Adds the .glade file to draw out the application.
        Also set up css, logger, button, and activate window.

        :param pub:             MQTT publisher object
        :param msg_q:           A queue on MQTT subscriber object to listen to
                                msg sent from rpi_out.
        :param intercom_config: Config to connect to a mumble client.
        :param video_config:    Config for recording video and livestream.
        """
        self.builder = gtk.Builder()
        self.builder.add_from_file(f"{os.path.dirname(__file__)}/rokku.glade")
        self.builder.connect_signals(self)

        # set up css
        cssProvider = gtk.CssProvider()
        cssProvider.load_from_path(
            f"{os.path.dirname(__file__)}/static/style.css"
        )
        screen = gdk.Screen.get_default()
        styleContext = gtk.StyleContext()
        styleContext.add_provider_for_screen(
            screen, cssProvider, gtk.STYLE_PROVIDER_PRIORITY_USER
        )

        # set up logger
        with open(
            f"{os.path.dirname(__file__)}/../../logger_config.yaml", "r"
        ) as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
        self.logger = logging.getLogger("UI")

        # set up flag for camera
        camera_flags = {"livestream_on": False, "recording_on": False}

        # connecting all buttons to python
        self.talk_button = talk.TalkButton(
            self.builder.get_object("talkButton"), pub, msg_q, intercom_config
        )
        self.arm_button = arm.ArmButton(
            self.builder.get_object("armButton"), pub, msg_q
        )
        self.record_button = record.RecordButton(
            self.builder.get_object("recordButton"), pub, msg_q, camera_flags
        )
        self.livestream_button = livestream.LivestreamButton(
            self.builder.get_object("livestreamButton"),
            pub,
            msg_q,
            camera_flags,
        )
        self.video_button = video.VideoButton(
            self.builder.get_object("videoButton"),
            pub,
            msg_q,
            video_config["yt_playlist_link"],
        )
        self.alarm_button = alarm.AlarmButton(
            self.builder.get_object("soundAlarmButton"), pub, msg_q
        )

        # activate window
        window = self.builder.get_object("Main")
        window.connect("delete-event", self.close_application)
        window.show_all()

    def close_application(self, widget, something):
        """Turn off UI.
        This will be called on closing the Rokku application
        Should close up any processes that have been started when first loading Rokku
        """
        gtk.main_quit()

    def run(self):
        """Run the UI"""
        gtk.main()
