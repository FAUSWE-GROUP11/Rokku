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

    def __init__(self, pub, msg_q):
        """Adds the .glade file to draw out the application.

        Also set up css, logger, button, and activate window.
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

<<<<<<< HEAD
        # All functionality flags
        self.armed = False
        self.armed_out = False
        self.alarm_sounding = False
        self.alarm_sounding_out = False
        self.recording = False
        self.rpi_in_intercom_on = False
        self.rpi_out_intercom_on = False

        # connecting all buttons to python to allow for the changing of
        # text/colors
        self.livestreamButton = self.builder.get_object("livestreamButton")
        self.videoButton = self.builder.get_object("videoButton")
        self.talkButton = self.builder.get_object("talkButton")
        self.soundAlarmButton = self.builder.get_object("soundAlarmButton")
        self.recordButton = self.builder.get_object("recordButton")
        self.armButton = self.builder.get_object("armButton")

        # Button background color, set to empty string initially
        self.button_color = {
            self.livestreamButton.get_name(): "",
            self.videoButton.get_name(): "",
            self.talkButton.get_name(): "",
            self.soundAlarmButton.get_name(): "",
            self.recordButton.get_name(): "",
            self.armButton.get_name(): "",
        }

        # set default background color and label for all buttons
        self._set_button_property(self.livestreamButton, "blue", "Livestream")
        self._set_button_property(self.videoButton, "blue", "Videos")
        self._set_button_property(self.soundAlarmButton, "blue", "Sound Alarm")
        self._set_button_property(self.recordButton, "blue", "Record")
        self._set_button_property(self.armButton, "blue", "Arm")
        self._set_button_property(self.talkButton, "blue", "Talk")

        # set up connections between .py file and glade signals
        self.livestreamButton.connect(
            "clicked", self.on_livestreamButton_clicked
        )
        self.videoButton.connect("clicked", self.on_videoButton_clicked)
        self.talkButton.connect("clicked", self.on_talkButton_clicked)
        self.soundAlarmButton.connect(
            "clicked", self.on_soundAlarmButton_clicked
        )
        self.recordButton.connect("clicked", self.on_recordButton_clicked)
        self.armButton.connect("clicked", self.on_armButton_clicked)

        # activate window
        window = self.builder.get_object("Main")
        window.connect("delete-event", self.close_application)
        window.show_all()

        # set up publisher and message queue
        self.pub = pub
        self.msg_q = msg_q

        # variables to catch youtube links sent back (Strings)
        self.yt_playlist_link = None
        self.yt_livestream_link = None

=======
>>>>>>> f7f67e498e37ec299e4907694ebee08a9512401f
        # set up logger
        with open(
            f"{os.path.dirname(__file__)}/../../logger_config.yaml", "r"
        ) as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
        self.logger = logging.getLogger("UI")

<<<<<<< HEAD
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
    This will be called on whenever the Talk button is clicked
    First will communicate with rpi_out to see if intercom is active on both
    parties and will set the self.intercom flag accordingly
    If intercom is active, turn off intercom and set color to blue with 'Talk'
    text for button
    If intercom is not active, send signal to activate intercom and set self.intercom_active accordingly
    Intercom will reset if error message is recieved when trying to active intercom
    """

    def on_talkButton_clicked(self, widget):
        # Always turn button to yellow whenever button is clicked
        self._set_button_property(self.talkButton, "yellow", "Configuring...")
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
                    self.rpi_out_intercom_on = self._wait_msg("intercom")[1]
                except IndexError:  # no message received
                    self.rpi_out_intercom_on = False

            if self.rpi_out_intercom_on and self.rpi_in_intercom_on:
                # intercom is on for both sides, turn button to red
                self.logger.info("Intercom ON on both devices")
                self._set_button_property(self.talkButton, "red", "End Talk")
            else:  # at least one of the intercom is not on
                self.logger.error(
                    f"Intercom status: rpi_in = {self.rpi_in_intercom_on}, rpi_out = {self.rpi_out_intercom_on}"
                )
                # display message box with error
                #########################
                #   Missing code        #
                #########################
                self._set_button_property(self.talkButton, "blue", "Talk")
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
                    self.rpi_out_intercom_on = self._wait_msg("intercom")[1]
                except IndexError:  # no message received
                    self.rpi_out_intercom_on = False

            if not self.rpi_out_intercom_on and not self.rpi_in_intercom_on:
                # intercom is off for both sides, turn button to red
                self.logger.info("Intercom OFF on both devices")
            self._set_button_property(self.talkButton, "blue", "Talk")
            self.rpi_in_intercom_on = False
            self.rpi_out_intercom_on = False



    def on_soundAlarmButton_clicked(self, widget):
        """ This will be called on whenever the Sound Alarm button is clicked

        First will communicate with rpi_out to see if sound is being played and will set the self.alarm_sounding flag accordingly
        If sound alarm is active, do nothing
        If not active, send signal to sound alarm and set self.alarm_sounding accordingly
        """
        # user wants to set off alarm on rpi_out
        if not self.alarm_sounding and not self.alarm_sounding_out:
            # turn button yellow, but with message "Acitvating"
            self._set_button_property(self.soundAlarmButton, "yellow", "Activating...")
            # let rpi_in know intent to sound alarm on rpi_out
            self.logger.info("Activating alarm on rpi_out...")
            self.alarm_sounding = True
            self.logger.info(
                "Sending alarm SOUND message to rpi_out..."
            )
            self.pub.publish(json.dumps(["alarm", True]))
            try:  # wait for rpi_out to send msg back
                self.alarm_sounding_out = self._wait_msg("alarm")[1]
            except IndexError:  # no message received
                # this is assuming rpi_out did not change state
                self.alarm_sounding = False

            # If message from rpi_out was recieved
            if self.alarm_sounding_out:
                # buzzer is playing on rpi_out: turn button to red
                self.logger.info("Alarm SOUNDING on rpi_out")
                self._set_button_property(self.soundAlarmButton, "red", "Silence Alarm")
            else:  # A message from rpi_out was not recieved
                self.logger.error(
                    f"Motion status: rpi_in = {self.alarm_sounding}, rpi_out = {self.alarm_sounding_out}"
                )
                # display message box with error
                #########################
                #   Missing code        #
                #########################
                self._set_button_property(self.soundAlarmButton, "blue", "Sound Alarm")
                self.alarm_sounding = False

        # Alarm is sounding. Silence Alarm.
        elif self.alarm_sounding and self.alarm_sounding_out:
            # turn button yellow, but with message "Silencing"
            self._set_button_property(self.soundAlarmButton, "yellow", "Silencing...")
            self.logger.info("Silencing rpi_out alarm...")
            self.alarm_sounding = False

            # Send silence signal
            self.logger.info("Sending alarm SILENCE message to rpi_out...")
            self.pub.publish(json.dumps(["alarm", False]))
            try:  # wait for rpi_out to send msg back
                self.alarm_sounding_out = self._wait_msg("alarm")[1]
            except IndexError:  # no message received
                # this is assuming rpi_out did not change state
                self.alarm_sounding = True

            if not self.alarm_sounding:
                # rpi_out message recieved, motion detection is off, turn button to blue
                self.logger.info("Alarm is SILENCED on rpi_out")
                self._set_button_property(self.soundAlarmButton, "blue", "Sound Alarm")
                self.alarm_sounding = False
            else:  # A message from rpi_out was not recieved
                self.logger.error(
                    f"Motion status: rpi_in = {self.alarm_sounding}, rpi_out = {self.alarm_sounding_out}"
                )
                # display message box with error
                #########################
                #   Missing code        #
                #########################
                self._set_button_property(self.soundAlarmButton, "red", "Silence")
                self.alarm_sounding = True

    def on_recordButton_clicked(self, widget):
        # Sets button to yellow while rpi_in tries communicating with rpi_out
        self._set_button_property(
            self.recordButton, "yellow", "Spooling up camera..."
=======
        # connecting all buttons to python
        self.talk_button = talk.TalkButton(
            self.builder.get_object("talkButton"), pub, msg_q
        )
        self.arm_button = arm.ArmButton(
            self.builder.get_object("armButton"), pub, msg_q
        )
        self.record_button = record.RecordButton(
            self.builder.get_object("recordButton"), pub, msg_q
        )
        self.livestream_button = livestream.LivestreamButton(
            self.builder.get_object("livestreamButton"), pub, msg_q
        )
        self.video_button = video.VideoButton(
            self.builder.get_object("videoButton"), pub, msg_q
        )
        self.alarm_button = alarm.AlarmButton(
            self.builder.get_object("soundAlarmButton"), pub, msg_q
>>>>>>> f7f67e498e37ec299e4907694ebee08a9512401f
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
