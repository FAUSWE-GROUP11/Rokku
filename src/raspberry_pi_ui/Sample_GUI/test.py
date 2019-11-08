import gi
from gi.repository import Gtk as gtk

gi.require_version("Gtk", "3.0")


class Main:
    """
    Class implemented to create the GUI
    Contains __init__ which adds the .glade file to draw out the application.
    This also is wear any object in the .glade (buttons, labels, etc.) are connected to self
    """

    def __init__(self):
        gladeFile = "test.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(gladeFile)
        self.builder.connect_signals(self)

        window = self.builder.get_object("Main")
        window.connect("delete-event", gtk.main_quit)
        window.show()


if __name__ == "__main__":
    main = Main()
    gtk.main()
