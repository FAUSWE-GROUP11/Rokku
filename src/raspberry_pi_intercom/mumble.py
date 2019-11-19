import os
from subprocess import Popen, check_output, run
from time import sleep

import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk as gtk


def turn_on(config, name: str, logger) -> None:
    """Turn on mumble client via command line

    The channel to connect to is configured in app_config.ini. Only registered
    users approved by Mumble server's SuperUser can connect to the channel.

    :param name:    Name to display on the mumble client. If the user has
                    has already registered on the server, their registered name
                    will be displayed instead of the name here.
    :param config:  Config to connect to a mumble client.
    :param logger:  For logging purpose
    """
    host: str = config["HOST"]
    port: str = config["PORT"]
    channel: str = config["CHANNEL"]
    logger.info("Turning on Mumble client...")
    cmd: str = (
        f"{os.path.dirname(__file__)}/start_mumble.sh "
        f"-n {name} "
        f"-h {host} "
        f"-p {port} "
        f"-c {channel}"
    )
    Popen(cmd, shell=True)


def is_on(timeout: int = 10) -> bool:
    """Check whether mumble client has been turned on

    :return: True if mumble client is on, else False
    """
    mumble_on: bool = False
    timer: int = 0
    while timer <= timeout:
        if check_output("ps -ef | grep -c mumble", shell=True) == "2":
            mumble_on = True
            break
        while gtk.events_pending():
            gtk.main_iteration()
        sleep(1)
        timer += 1
    return mumble_on


def turn_off(logger) -> bool:
    """Turn off mumble client via command line

    :param logger:  For logging purpose

    :return: True if mumble client successfully turned off, else False
    """
    kill_intercom = "tmux kill-sess -t intercom"
    logger.info("Turning off rpi_in Mumble CLI client...")
    try:
        mum_proc = run(kill_intercom, shell=True)
    except Exception:
        logger.exception("ERROR: unable to turn off Mumble client")
        mum_proc = None
    if mum_proc is not None:
        logger.info("Mumble client OFF.")
    return mum_proc is not None
