import os
import gi

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

    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file("rokku.glade")
        self.builder.connect_signals(self)

        self.armed = False
        self.sound_playing = False
        self.recording = False
        self.intercom_active = False

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
        self.talkButton.override_background_color(gtk.StateFlags.NORMAL, color)
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
        # code to check if intercom is active

        if not self.intercom_active:
            # Set color to yellow for set up
            color = gdk.RGBA()
            color.parse(yellow)
            self.talkButton.override_background_color(
                gtk.StateFlags.NORMAL, color
            )

            # code to set up intercom

            # Set color to red to show intercom is active
            # need to grab value that intercom is set up okay before showing as active
            if True:
                color = gdk.RGBA()
                color.parse(red)
                self.talkButton.override_background_color(
                    gtk.StateFlags.NORMAL, color
                )
                self.talkButton.set_label("Talking")
                self.intercom_active = True
            # Set color to blue to show intercom is inactive with error message
            else:
                color = gdk.RGBA()
                color.parse(blue)
                self.talkButton.override_background_color(
                    gtk.StateFlags.NORMAL, color
                )
                self.talkButton.set_label("Talk")
                self.intercom_active = False

                # Figure out code to show messagebox with error

        else:
            # Set color to blue for reactivating intercom
            color = gdk.RGBA()
            color.parse(blue)
            self.talkButton.override_background_color(
                gtk.StateFlags.NORMAL, color
            )
            self.talkButton.set_label("Talk")
            self.intercom_active = False

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

    def close_application(self, widget):
        # anything to do before closing (stop livestream)

        # closes window with .py file
        gtk.main_quit()


if __name__ == "__main__":
    main = Main()
    gtk.main()
