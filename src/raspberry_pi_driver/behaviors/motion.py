import json

from src.raspberry_pi_motion_sensor.motion_interface import MotionPir


def motion(pub, flag, queue, config) -> None:
    """Behavior that will arm or disarm the motion sensor."""
    sensor = MotionPir(queue, 23, config)  # channel 23 is GPIO23 is PIN16
    if flag:
        sensor.set_armed()
    else:
        sensor.set_disarmed()
    pub.publish(json.dumps(["motion", sensor.get_state()]))
