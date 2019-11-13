import logging
import logging.config
import os

import gi
import yaml

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")

from gi.repository import Gdk as gdk
from gi.repository import Gtk as gtk

from src.raspberry_pi_ui.buttons import talk, arm


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

        # All functionality flags

        self.sound_playing = False
        self.recording = False

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
        # self.soundAlarmButton = self.builder.get_object("soundAlarmButton")
        # self.recordButton = self.builder.get_object("recordButton")

        # Button background color, set to empty string initially
        # self.button_color = {
        #     self.livestreamButton.get_name(): "",
        #     self.videoButton.get_name(): "",
        #     self.talkButton.get_name(): "",
        #     self.soundAlarmButton.get_name(): "",
        #     self.recordButton.get_name(): "",
        #     self.armButton.get_name(): "",
        # }

        # set default background color and label for all buttons
        # self._set_button_property(self.livestreamButton, "blue", "Livestream")
        # self._set_button_property(self.videoButton, "blue", "Videos")
        # self._set_button_property(self.soundAlarmButton, "blue", "Sound Alarm")
        # self._set_button_property(self.recordButton, "blue", "Record")
        # self._set_button_property(self.armButton, "blue", "Arm")
        # self._set_button_property(self.talkButton, "blue", "Talk")

        # set up connections between .py file and glade signals
        # self.livestreamButton.connect(
        #     "clicked", self.on_livestreamButton_clicked
        # )
        # self.videoButton.connect("clicked", self.on_videoButton_clicked)
        # self.talkButton.connect("clicked", self.on_talkButton_clicked)
        # self.soundAlarmButton.connect(
        #     "clicked", self.on_soundAlarmButton_clicked
        # )
        # self.recordButton.connect("clicked", self.on_recordButton_clicked)
        # self.armButton.connect("clicked", self.on_armButton_clicked)

        # activate window
        window = self.builder.get_object("Main")
        window.connect("delete-event", self.close_application)
        window.show_all()

        # variables to catch youtube links sent back (Strings)
        self.yt_playlist_link = None
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
    This will be called on whenever the Record button is clicked
    First will communicate with rpi_out to see if a clip is being record or not and will set the self.recording flag accordingly
    If recording still, do nothing
    If not record, send signal to record clip and set self.recording accordingly
    """

    # def on_recordButton_clicked(self, widget):
    #     # Sets button to yellow while rpi_in tries communicating with rpi_out
    #     self._set_button_property(
    #         self.recordButton, "yellow", "Spooling up camera..."
    #     )
    #     # Check if not recording
    #     if not self.recording:
    #         self.logger.info("Sending record ON message to rpi_out...")
    #         self.pub.publish(json.dumps(["record", True]))
    #         try:  # wait for rpi_out to send true msg back
    #             self.recording = self._wait_msg("record")[1]
    #         except IndexError:  # no message received
    #             self.recording = False
    #     if self.recording:
    #         # Since rpi_out sent back true it should be recording now
    #         self.logger.info("rpi_out is recording now...")
    #         # turn button to red if not already red
    #         self._set_button_property(self.recordButton, "red", "Recording...")
    #         # waiting for rpi_out to send youtube playlist link
    #         try:  # wait for rpi_out to send msg back
    #             self.yt_playlist_link = self._wait_msg("yt_playlist_link")[1]
    #         except IndexError:  # no message received
    #             self.recording = False
    #     if (
    #         type(self.yt_playlist_link) == str
    #     ) and self.recording:  # Does not catch if junk str was sent back
    #         self.logger.info("rpi_out recorded a video succesfully...")
    #     else:  # Something wrong with mqtt or the recording failed
    #         self.logger.error(
    #             f"Mqtt or the YouTube Api broke, no video was recorded. Recording status: rpi_in = {self.recording}"
    #         )
    #         # display message box with error
    #         #########################
    #         #   Missing code        #
    #         #########################
    #     self._set_button_property(self.recordButton, "blue", "Record")
    #     self.recording = False

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
