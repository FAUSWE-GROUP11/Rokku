import sys

sys.path.append("/home/pi/github-repos/Rokku/raspberry_pi_motion_sensor")
from motion_interface import MotionPir
from queue import Queue

queue = Queue()
motion = MotionPir(queue, 23)


class TestMotionPir:
    def test_init(self):
        assert motion.channel_num == 23

    def test_init_2(self):
        assert isinstance(motion.queue, Queue) is True

    def test_init_3(self):
        assert motion.armed is False

    def test_set_armed(self):
        motion.set_armed()
        assert motion.armed is True

    # TODO - def test_callback(self):

    # TODO - def test_monitor(self):
