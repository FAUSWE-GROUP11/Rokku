from .. import motion_interface
from queue import Queue

queue = Queue()
motion = motion_interface.MotionPir(queue, 23)


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

    def test_show_state(self):
        motion.set_disarmed()
        motion.set_armed()
        result = motion.show_state()
        assert result is True

    def test_show_state2(self):
        result = motion.show_state()
        assert result is True
