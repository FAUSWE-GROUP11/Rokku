import json


def motion(pub, flag, sensor) -> None:
    """Behavior that will arm or disarm the motion sensor.

    :param pub:     MQTT publisher object.
    :param flag:    True to turn on motion sensor, False to turn off
    :param sensor:  MotionPIR sensor object.
    """
    if flag:  # turn on motion sensor
        sensor.set_armed()
    else:  # turn off motion sensor
        sensor.set_disarmed()
    pub.publish(json.dumps(["motion", sensor.get_state()]))
