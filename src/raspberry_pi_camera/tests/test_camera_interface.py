import sys

import fake_rpi

sys.modules["picamera"] = fake_rpi.picamera  # Fake picamera

from .. import camera_interface  # from .. import camera_interface


"""import os"""

sample = camera_interface.CameraInterface()


class TestClass:
    def test_one(self):
        assert "sample" in globals() or "sample" in locals()

    """def test_two(self):
        sample.start_mjpg_streamer()
        assert sample.check_mjpg_streamer()"""

    """def test_three(self):
        sample.stop_mjpg_streamer()
        assert not sample.check_mjpg_streamer()"""

    """def test_four(self):
        fname = sample.record_video()
        assert os.path.isfile(fname)"""

    def test_five(self):
        capture = str(sample)
        assert (
            capture
            == "Video Length: 30, Resolution: (640, 480), Save Location: /home/pi/Videos/"
        )

    def test_six(self):
        sample.set_video_length(10)
        assert sample.get_video_length() == 10

    def test_seven(self):
        sample.set_resolution(1)
        assert sample.get_resolution() == "(1296, 730)"

    def test_eight(self):
        sample.set_save_location("/home/pi/Pictures/")
        assert sample.get_save_location() == "/home/pi/Pictures/"
