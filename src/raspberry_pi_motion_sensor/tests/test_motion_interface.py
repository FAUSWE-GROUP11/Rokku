from collections import deque
from typing import Deque
from time import sleep


def test_init(motion_sensor):
    assert motion_sensor.channel_num == 23


def test_init_2(motion_sensor):
    assert motion_sensor.queue.empty()


def test_init_3(motion_sensor):
    assert motion_sensor.armed is False


def test_set_disarmed(motion_sensor):
    motion_sensor.set_armed()
    motion_sensor.set_disarmed()
    assert motion_sensor.armed is False


def test_set_armed(motion_sensor):
    motion_sensor.set_disarmed()
    motion_sensor.set_armed()
    assert motion_sensor.armed is True


def test_motion_callback_triggered(motion_sensor):
    """Trigger twice within 2 seconds, shall lead to true trigger"""
    motion_sensor.set_armed()
    motion_sensor.motion_callback(23)
    sleep(2)
    motion_sensor.motion_callback(23)
    result = motion_sensor.queue.get()
    assert result is True


def test_motion_callback_not_triggered(motion_sensor):
    """Trigger twice within 3 seconds, shall NOT lead to true trigger"""
    motion_sensor.set_armed()
    motion_sensor.motion_callback(23)
    sleep(3)
    motion_sensor.motion_callback(23)
    assert motion_sensor.queue.empty()


def test_get_state(motion_sensor):
    motion_sensor.set_disarmed()
    motion_sensor.set_armed()
    result = motion_sensor.get_state()
    assert result is True


def test_get_state2(motion_sensor):
    result = motion_sensor.get_state()
    assert result is True


def test_reset_trigger_times(motion_sensor):
    res = motion_sensor._reset_trigger_times()
    assert isinstance(res, Deque) and res == deque([-1])
