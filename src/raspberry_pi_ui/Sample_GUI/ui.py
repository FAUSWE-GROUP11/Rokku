import os

import gi
from gi.repository import Gdk, Gtk

gi.require_version("Gtk", "3.0")


class Main:
    """
    Class implemented to create the GUI
    Contains __init__ which adds the .glade file to draw out the application.
    This also is wear any object in the .glade (buttons, labels, etc.) are connected to self
    """

    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(f"{os.path.dirname(__file__)}/ui.glade")
        self.builder.connect_signals(self)

        # set up css
        cssProvider = Gtk.CssProvider()
        cssProvider.load_from_path(f"{os.path.dirname(__file__)}/style.css")
        screen = Gdk.Screen.get_default()
        styleContext = Gtk.StyleContext()
        styleContext.add_provider_for_screen(
            screen, cssProvider, Gtk.STYLE_PROVIDER_PRIORITY_USER
        )

        # set up window
        window = self.builder.get_object("Main")
        window.connect("delete-event", Gtk.main_quit)
        window.show_all()

        # intercom button
        self.intercom_button = self.builder.get_object("intercom")
        self.intercom_button.set_name("intercom")

    def intercom_handler(self, widget):
        # upon clicking, change intercom button color and text
        ctx = widget.get_style_context()
        ctx.remove_class("intercom_default")
        ctx.add_class("intercom_connecting")
        widget.set_label("Connecting intercom...")

    """
    This function is connected to the .glade which is called whenever button2 is pressed.
    Grabs the python file (similar to this one) and then runs the .py to draw the window(Test)
    above the current window (Main).
    These two windows will act independently of each other
    """

    def on_button2_clicked(self, widget):
        os.system("python test.py")

    """
    Record button
    """

    def record_btn_clicked(self, widget):
        # upon clicking, change record button color and text
        ctx = widget.get_style_context()
        ctx.remove_class("record_default")
        ctx.add_class("recording")
        widget.set_label("Recording...")

    def run(self):
        Gtk.main()


if __name__ == "__main__":
    main = Main()
    Gtk.main()
