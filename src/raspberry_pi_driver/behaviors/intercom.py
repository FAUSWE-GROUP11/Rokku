import json

from src.raspberry_pi_intercom import mumble


def intercom(pub, flag, config, logger) -> None:
    """Intercom behavior on rpi_out upon receiving msg from rpi_in.

    If flag is True, that means rpi_in is signaling rpi_out to turn on its
    mumble client.

    If flag is False, that means rpi_in is signaling rpi_out to turn off its
    mumble client.

    If rpi_out turns on mumble client successfully, it response with
    ["intercom", True] to rpi_in; otherwise ["intercom", False]

    :param pub:     MQTT publisher object.
    :param flag:    flag extracted from rpi_in msg
    :param config:  Config to connect to a mumble client.
    :param logger:  For logging purpose
    """
    if flag:
        mumble.turn_on(config, "rpi_out", logger)
        pub.publish(json.dumps(["intercom", mumble.is_on(logger)]))
    else:
        pub.publish(json.dumps(["intercom", not mumble.turn_off(logger)]))
