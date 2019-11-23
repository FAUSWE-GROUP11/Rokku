import os
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk


class MessageBox:
    """
    Class implemented to create the GUI

    Takes a Title along with a Message to set up in the MessageBox object
    MessageBox object will hold main UI from input until closed
    """

    def __init__(self, title, message):
        self.builder = gtk.Builder()
        self.builder.add_from_file(
            f"{os.path.dirname(__file__)}/message_box.glade"
        )

        # Grab window object
        self.window = self.builder.get_object("Main")
        self.window.connect("destroy", gtk.main_quit)

        # Grab children
        self.label1 = self.builder.get_object("Label1")
        self.button1 = self.builder.get_object("Button1")
        self.button1.connect("clicked", self.on_button_clicked)

        # Set title and message
        self.window.set_title(title)
        self.label1.set_label(message)

        self.window.show_all()

    # Called when the 'OK' button is clicked
    def on_button_clicked(self, *args):
        self.window.destroy()

    # Called to show the MessageBox object
    def run(self):
        gtk.main()
