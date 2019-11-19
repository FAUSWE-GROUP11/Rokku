import json

from src.raspberry_pi_alarm.buzzer_interface import Buzzer


def alarm(pub, flag) -> None:
    """Behavior that will set off alarm on rpi_out."""
    alarm = Buzzer(24)
    if flag:
        alarm.sound()
    else:
        alarm.silence()
    pub.publish(json.dumps(["alarm", alarm.get_state()]))
