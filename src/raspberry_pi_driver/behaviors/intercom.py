import json


def intercom(pub, flag) -> None:
    """Behavior that will connect or disconnect rpi_out with mumble client."""
    if flag:
        pass  # set up intercom for rpi_out
        pub.publish(json.dumps(["intercom", True]))
    else:
        pass  # disconnect intercom
        pub.publish(json.dumps(["intercom", False]))
