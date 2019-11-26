import json

from src.raspberry_pi_alarm.buzzer_interface import Buzzer


def alarm(pub, flag) -> None:
    """Behavior that will set off alarm on rpi_out."""
    alarm_pin = 6
    alarm_ = Buzzer(alarm_pin)
    if flag:
        alarm_.sound()
    else:
        alarm_.silence()
    pub.publish(json.dumps(["alarm", alarm_.get_state()]))
