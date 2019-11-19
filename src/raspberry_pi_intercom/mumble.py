import os
import subprocess

import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk as gtk


def turn_on(config, name: str, logger):
    """Turn on mumble client via command line

    The channel to connect to is configured in app_config.ini. Only registered
    users approved by Mumble server's SuperUser can connect to the channel.

    :param name:    Name to display on the mumble client. If the user has
                    has already registered on the server, their registered name
                    will be displayed instead of the name here.
    :param config:  Config to connect to a mumble client.
    :param logger:  For logging purpose

    :return: Popen object after running the command to turn on mumble client
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
    mum_proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, shell=True, encoding="utf-8"
    )
    try:
        outs, errs = mum_proc.communicate(timeout=10)
    except subprocess.TimeoutExpired:
        mum_proc.kill()
        outs, errs = mum_proc.communicate()
        mum_proc = None
    while gtk.events_pending():
        gtk.main_iteration()

    if mum_proc is None or outs != "2":
        logger.exception("ERROR: unable to turn on Mumble client")
    else:
        logger.info("Mumble client ON.")
    return mum_proc is not None


def turn_off(logger) -> bool:
    """Turn off mumble client via command line

    :param logger:  For logging purpose

    :return: True if mumble client successfully turned off, else False
    """
    kill_intercom = "tmux kill-sess -t intercom"
    logger.info("Turning off rpi_in Mumble CLI client...")
    try:
        mum_proc = subprocess.run(kill_intercom, shell=True)
    except Exception:
        logger.exception("ERROR: unable to turn off Mumble client")
        mum_proc = None
    if mum_proc is not None:
        logger.info("Mumble client OFF.")
    return mum_proc is not None
