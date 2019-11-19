import os
import subprocess


def turn_on(config, name: str, logger) -> bool:
    """Turn on mumble client via command line

    The channel to connect to is configured in app_config.ini. Only registered
    users approved by Mumble server's SuperUser can connect to the channel.

    :param name:    Name to display on the mumble client. If the user has
                    has already registered on the server, their registered name
                    will be displayed instead of the name here.
    :param config:  Config to connect to a mumble client.
    :param logger:  For logging purpose

    :return: True if mumble client successfully turned on, else False
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
    try:
        mum_proc = subprocess.run(cmd, shell=True)
    except Exception:
        logger.exception("ERROR: unable to turn on Mumble client")
        mum_proc = None
    if mum_proc is not None:
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