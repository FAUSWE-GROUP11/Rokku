import os
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk

gi.require_version("WebKit", "3.0")
from gi.repository import WebKit


class EmbeddedYT:
    """
    Constructor for EmbeddedYT class
    Takes a url link to be opened and a title to be given to the application itself

    NOTE: Link needs to be as such: 'http://youtube.com'
    """

    def __init__(self, link, title):
        # set up glade file
        self.builder = gtk.Builder()
        self.builder.add_from_file(
            f"{os.path.dirname(__file__)}/embedded_yt.glade"
        )
        # self.builder.add_from_file("embedded_yt.glade")

        # set up main window with signals
        self.window = self.builder.get_object("Main")
        self.window.connect("delete-event", gtk.main_quit)
        self.window.set_title(title)

        # set up WebView to load YT
        self.webview = WebKit.WebView()

        # adds webview object to scroll window
        self.scrl_window = self.builder.get_object("ScrollWindow")
        self.scrl_window.add(self.webview)

        self.webview.load_uri(link)
        self.webview.show()

        self.window.show_all()

    def run(self):
        gtk.main()
