import json
from time import time
from typing import Any, List

import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk as gtk


def set_button_property(button, color: str, label: str):
    """
    Set background color and label of a given button

    :param button:      A button wrapper class.
    :param color:       Name of the color (choose from 'blue', 'red', and
                        'yellow')
    :param label:       The label to be displayed on the button

    :returns:   None
    """
    ctx = button.get_style_context()
    if button.get_color():
        ctx.remove_class(button.get_color())
    ctx.add_class(color)
    button.set_color(color)
    button.set_label(label)


def wait_msg(identifier: str, logger, msg_q, timeout: int = 10) -> List[Any]:
    """
    Wait for a message containing the given identifier. Note that all
    messages are in the format of '[identifier, boolean]'. Thus, we only
    need to check the first element for identifier in the received, json-
    loaded, list.

    :param identifier:      A unique string to differentiate the recipient of
                            the received message.
    :param logger:          Logging from the caller.
    :param msg_q:           A queue to receive msg from rpi_out
    :param timeout:         Timeout duration. If function hangs for more than
                            the amount of time specified by timeout, end the
                            function. Default timeout set to 10 seconds
    :return:
        A json-loaded object (a list) from the received message. If timeout
        is triggered, return an empty list.
    """
    start = time()
    msg_list = []
    while True:
        if time() - start >= timeout:
            logger.error("Wait for rpi_out message timeout.")
            break
        if not msg_q.empty():
            msg = msg_q.get()
            msg_list = json.loads(msg)
            if msg_list[0] == identifier:
                logger.info(f"Message for {identifier} received from rpi_out.")
                break
            else:  # if the received message is not for intercom
                msg_q.put(msg)  # put the message back
                msg_list = []  # reset msg_list
        while gtk.events_pending():
            gtk.main_iteration()
    return msg_list
