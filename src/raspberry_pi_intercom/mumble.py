import subprocess


def turn_on(config, name: str, logger) -> bool:
    """Turn on mumble client via command line

    :param name:    Name to display on the mumble client. If the user has
                    has already registered on the server, their registered name
                    will be displayed instead of the name here.
    :param config:  Config to connect to a mumble client.
    :param logger:  For logging purpose

    :return: True if mumble client successfully turned on, else False
    """
    new_tmux = "tmux new -s intercom -d"
    host: str = config["HOST"]
    port: str = config["PORT"]
    open_mumble = (
        "tmux send-keys -t intercom "
        f'"mumble -n mumble://{name}@{host}:{port}"'
        "Enter"
    )
    try:
        mum_proc = subprocess.run(new_tmux + " && " + open_mumble, shell=True)
    except Exception:
        logger.exception("ERROR: unable to turn on Mumble client")
        mum_proc = None
    return mum_proc is not None
