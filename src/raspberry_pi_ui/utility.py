import json
import os
from time import time
from typing import Any, List
from time import sleep
import subprocess

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


def retrieve_msg(identifier: str, msg_q) -> List[Any]:
    """Retrieve one msg from msg_q.

    If the msg does not fit identifier, put the msg back in the queue.

    :param identifier:  A unique string to differentiate the recipient of
                        the received message.
    :param msg_q:       A queue to receive msg from rpi_out
    :return: A json-loaded object (or empty list) from the received message.
    """
    msg = msg_q.get()
    msg_list = json.loads(msg)
    # if the received message is not what we want
    if msg_list[0] != identifier:
        msg_q.put(msg)  # put the message back
        msg_list = []  # reset msg_list
    return msg_list


def wait_msg(identifier: str, logger, msg_q, timeout: int = 10) -> List[Any]:
    """Wait for a message containing the given identifier inside UI.

    Note that all messages are in the format of '[identifier, boolean]'. Thus,
    we only need to check the first element for identifier in the received,
    json-loaded, list.

    If timeout or force_end is triggered, return an empty list.

    This function shall be used ONLY in button callback.

    :param identifier:  A unique string to differentiate the recipient of
                        the received message.
    :param logger:      Logging from the caller.
    :param msg_q:       A queue to receive msg from rpi_out
    :param timeout:     Timeout duration. If function hangs for more than
                        the amount of time specified by timeout, end the
                        function. Default timeout set to 10 seconds.
    :return: A json-loaded object (or empty list) from the received message.
    """
    start = time()
    msg_list = []
    while True:
        if time() - start >= timeout:
            logger.error("Wait for rpi_out message timeout.")
            break
        if not msg_q.empty():
            msg_list = retrieve_msg(identifier, msg_q)
            if msg_list:
                logger.info(f"Message for {identifier} received from rpi_out.")
                break
        while gtk.events_pending():  # keep UI alive
            gtk.main_iteration()
        sleep(1)
    return msg_list


def play_notification_sound(duration: int, logger):
    """
    Plays a sound from a .wav file within sounds.

    :param duration: Allows you to shorten a sound from its original length. If it is bigger than
    length of audio time the process will finish when the audio file is done playing.

    :param logger: Logs when an audio message is played.
    """
    audio_dir = os.path.dirname(__file__) + "/static/audio/notify.wav"
    dur_param = "-d" + str(duration)
    play = subprocess.Popen(["aplay", "-q", dur_param, audio_dir])
    logger.info(f"Notification sound: {play}")
