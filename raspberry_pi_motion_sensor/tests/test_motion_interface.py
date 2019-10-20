import sys
from pathlib import Path

sys.path.append("/home/pi/github-repos/Rokku/raspberry_pi_motion_sensor")
sys.path.append(str(Path.cwd().resolve().parent))
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

    def test_set_disarmed(self):
        motion.set_armed()
        motion.set_disarmed()
        assert motion.armed is False

    def test_set_armed(self):
        motion.set_disarmed()
        motion.set_armed()
        assert motion.armed is True

    def test_motion_callback(self):
        motion.motion_callback(23)
        result = motion.queue.get()
        assert result is True

    def test_get_state(self):
        motion.set_disarmed()
        motion.set_armed()
        result = motion.get_state()
        assert result is True

    def test_get_state2(self):
        result = motion.get_state()
        assert result is True
