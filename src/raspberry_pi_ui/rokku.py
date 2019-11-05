import os
import json
import gi
import logging
import logging.config
import yaml
from time import time

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk, Gdk as gdk

# Any global variables that should be used throughout file
red = "#eb3434"
blue = "#346eeb"
yellow = "#e5eb34"


class Main:
    """
    Class implemented to create the GUI
    Contains __init__ which adds the .glade file to draw out the application.
    This also is wear any object in the .glade (buttons, labels, etc.) are connected to self
    """

    def __init__(self, pub, msg_q):
        self.builder = gtk.Builder()
        self.builder.add_from_file(f"{os.path.dirname(__file__)}/rokku.glade")
        self.builder.connect_signals(self)

        self.armed = False
        self.sound_playing = False
        self.recording = False
        self.rpi_in_intercom_on = False
        self.rpi_out_intercom_on = False

        # set up colors
        color = gdk.RGBA()
        color.parse(blue)
        color.to_string()

        # connecting all buttons to python to allow for the changing of text/colors
        self.livestreamButton = self.builder.get_object("livestreamButton")
        self.videoButton = self.builder.get_object("videoButton")
        self.talkButton = self.builder.get_object("talkButton")
        self.soundAlarmButton = self.builder.get_object("soundAlarmButton")
        self.recordButton = self.builder.get_object("recordButton")
        self.armButton = self.builder.get_object("armButton")

        # set up buttons with correct background color
        self.livestreamButton.override_background_color(
            gtk.StateFlags.NORMAL, color
        )
        self.videoButton.override_background_color(
            gtk.StateFlags.NORMAL, color
        )
        self._set_button_property(self.talkButton, blue, "Talk")
        self.soundAlarmButton.override_background_color(
            gtk.StateFlags.NORMAL, color
        )
        self.recordButton.override_background_color(
            gtk.StateFlags.NORMAL, color
        )
        self.armButton.override_background_color(gtk.StateFlags.NORMAL, color)

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

        # set livestream

        # activate window
        window = self.builder.get_object("Main")
        window.connect("delete-event", self.close_application)
        window.show_all()

        # set up publisher and message queue
        self.pub = pub
        self.msg_q = msg_q

        # set up logger
        # set up logger
        with open(
            f"{os.path.dirname(__file__)}/../../logger_config.yaml", "r"
        ) as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
        self.logger = logging.getLogger("UI")

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
    First will communicate with rpi_out to see if intercom is active on both parties and will set the self.intercom flag accordingly
    If intercom is active, turn off intercom and set color to blue with 'Talk' text for button
    If intercom is not active, send signal to activate intercom and set self.intercom_active accordingly
    Intercom will reset if error message is recieved when trying to active intercom
    """

    def on_talkButton_clicked(self, widget):
        # Always turn button to yellow whenever button is clicked
        self._set_button_property(self.talkButton, yellow, "Connecting...")
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
                self._set_button_property(self.talkButton, red, "End Talk")
            else:  # at least one of the intercom is not on
                self.logger.error(
                    f"Intercom status: rpi_in = {self.rpi_in_intercom_on}, rpi_out = {self.rpi_out_intercom_on}"
                )
                # display message box with error
                #########################
                #   Missing code        #
                #########################
                self._set_button_property(self.talkButton, blue, "Talk")
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
            self._set_button_property(self.talkButton, blue, "Talk")
            self.rpi_in_intercom_on = False
            self.rpi_out_intercom_on = False

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

    def on_recordButton_clicked(self, widget):
        # add code to check if clip is still recording and set self.recording accordingly

        if not self.recording:
            # code to send message to record clip

            self.recording = True

    """
    This will be called on whenever the Arm button is clicked
    If the alarm is not set, sets text to 'Disarm' and color to red along with sending a message to rpi_out activing armed flag
    If the alarm is set, sets text to 'Arm' and color to blue along with sending a message to rpi_out disactiving armed flag
    """

    def on_armButton_clicked(self, widget):
        if not self.armed:
            # Change text to 'Disarm' and change color of button to red
            color = gdk.RGBA()
            color.parse(red)
            self.armButton.override_background_color(
                gtk.StateFlags.NORMAL, color
            )
            self.armButton.set_label("Disarm")
            self.armed = True

            # actual code to arm alarm

        else:
            # Change text to 'Disarm' and change color of button to red
            color = gdk.RGBA()
            color.parse(blue)
            self.armButton.override_background_color(
                gtk.StateFlags.NORMAL, color
            )
            self.armButton.set_label("Arm")
            self.armed = False

            # actual code to disarm alarm

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

    # Utility functions listed below.
    def _wait_msg(self, identifier: str, timeout: int = 10):
        """
        Wait for a message containing the given identifier. Note that all
        messages are in the format of '[identifier, boolean]'. Thus, we only
        need to check the first element for identifier in the received, json-
        loaded, list.

        Args:
            identifier:     A unique string to differentiate the recipient of
                            the received message.
            timeout:        Timeout duration. If function hangs for more than
                            the amount of time specified by timeout, end the
                            function. Default timeout set to 10 seconds
        Return:
            A json-loaded object (a list) from the received message. If timeout
            is triggered, return an empty list.
        Raises:
            None
        """
        start = time()
        msg_list = []
        while True:
            if time() - start >= timeout:
                self.logger.error("Wait for rpi_out message timeout.")
                break
            if not self.msg_q.empty():
                msg = self.msg_q.get()
                msg_list = json.loads(msg)
                if msg_list[0] == identifier:
                    self.logger.info(
                        f"Message for {identifier} received from rpi_out."
                    )
                    break
                else:  # if the received message is not for intercom
                    self.msg_q.put(msg)  # put the message back
                    msg_list = []  # reset msg_list
            while gtk.events_pending():
                gtk.main_iteration()
        return msg_list

    def _set_button_property(self, button, color_name: str, label: str):
        """
        Set background color and label of a given button

        Args:
            button:     A button widget object.
            color_name: Name of the color (choose from blue, red, and yellow)
            label:      The label to be displayed on the button
        Returns:
            None
        Raises:
            None
        """
        color = gdk.RGBA()
        color.parse(color_name)
        button.override_background_color(gtk.StateFlags.NORMAL, color)
        button.set_label(label)
