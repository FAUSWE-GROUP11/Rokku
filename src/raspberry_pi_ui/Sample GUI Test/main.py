import os
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk

gladeFile = "main.glade"


class Main:
    """
    Class implemented to create the GUI
    Contains __init__ which adds the .glade file to draw out the application.
    This also is wear any object in the .glade (buttons, labels, etc.) are connected to self
    """

    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file(gladeFile)
        self.builder.connect_signals(self)

        self.label1 = self.builder.get_object("label1")

        window = self.builder.get_object("Main")
        window.connect("delete-event", gtk.main_quit)
        window.show()

    """
    This function is connected to the .glade which is called whenever button1 is pressed.
    Prints out to terminal as well as setting a label with some text
    """

    def printText(self, widget):
        print("Hello World")
        self.label1.set_text("I'm a label")

    """
    This function is connected to the .glade which is called whenever button2 is pressed.
    Grabs the python file (similar to this one) and then runs the .py to draw the window(Test)
    above the current window (Main).
    These two windows will act independently of each other
    """

    def on_button2_clicked(self, widget):
        os.system("python test.py")


if __name__ == "__main__":
    main = Main()
    gtk.main()
