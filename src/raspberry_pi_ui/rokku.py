import logging
import logging.config
import os

import gi
import yaml

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")

from gi.repository import Gdk as gdk
from gi.repository import Gtk as gtk

from src.raspberry_pi_ui.buttons import talk, arm, record


class Main:
    """
    Class implemented to create the GUI
    Contains __init__ which adds the .glade file to draw out the application.
    This also is wear any object in the .glade (buttons, labels, etc.) are
    connected to self
    """

    def __init__(self, pub, msg_q):
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

        # connecting all buttons to python to allow for the changing of
        # text/colors
        # self.livestreamButton = self.builder.get_object("livestreamButton")
        # self.videoButton = self.builder.get_object("videoButton")
        self.talk_button = talk.TalkButton(
            self.builder.get_object("talkButton"), pub, msg_q
        )
        self.arm_button = arm.ArmButton(
            self.builder.get_object("armButton"), pub, msg_q
        )
        self.record_button = record.RecordButton(
            self.builder.get_object("recordButton"), pub, msg_q
        )
        # self.soundAlarmButton = self.builder.get_object("soundAlarmButton")

        # activate window
        window = self.builder.get_object("Main")
        window.connect("delete-event", self.close_application)
        window.show_all()

        # variables to catch youtube links sent back (Strings)

        self.yt_livestream_link = None

    """
    This will be called on whenever the Sound Alarm button is clicked
    """

    def on_livestreamButton_clicked(self, widget):
        # Figure out how to give url passed on button clicked
        os.system("python embedded_yt.py")
        self.livestreamButton.set_label("Need code")

    """
    This will be called on whenever the Videos button is clicked
    """

    def on_videoButton_clicked(self, widget):
        # Figure out how to give url passed on button clicked
        # os.system("python embedded_yt.py")
        self.videoButton.set_label("Need code")

    """
    This will be called on whenever the Sound Alarm button is clicked
    First will communicate with rpi_out to see if sound is being played and will set the self.recording flag accordingly
    If sound alarm is active, do nothing
    If not active, send signal to sound alarm and set self.sound_alarm accordingly
    """

    def on_soundAlarmButton_clicked(self, widget):
        # add code to check if sound alarm is active and set self.sound_alarm accordingly

        if not self.sound_alarm:
            # code to send message to sound alarm

            self.sound_alarm = True

    """
    This will be called on closing the Rokku application
    Should close up any processes that have been started when first loading Rokku
    """

    def close_application(self, widget, something):
        # anything to do before closing (stop livestream)

        # closes window with .py file
        gtk.main_quit()

    def run(self):
        gtk.main()
