from src.raspberry_pi_ui.utility import set_button_property


class Button(object):
    """A wrapper class representing the button widget on UI

    This is the parent class.
    """

    def __init__(self, button, pub, msg_q, label: str):
        """Constructor of the class.

        :param button:      The actual button widget from UI
        :param pub:         pub object for publishing msg via MQTT
        :param msg_q:       A queue to receive msg from rpi_out
        """
        self._button = button
        self._color = ""  # initialize color with empty string
        self._button.connect("clicked", self.on_clicked)
        set_button_property(self, "blue", label)  # initial button property

        # set up publisher and message queue
        self.pub = pub
        self.msg_q = msg_q

    def get_style_context(self):
        """Wrapper function for get_style_context() in the real widget"""
        return self._button.get_style_context()

    def get_color(self) -> str:
        """Getter function to retrieve button color"""
        return self._color

    def set_color(self, color: str) -> None:
        """Setter function to set button color"""
        self._color = color

    def get_label(self) -> str:
        """Getter function to retrieve button label"""
        return self._button.get_label()

    def set_label(self, label: str) -> None:
        """Setter function to set button label"""
        self._button.set_label(label)

    def on_clicked(self, widget):
        """Placeholder.

        Each button will redefine their own on_clicked callback.
        """
        pass
