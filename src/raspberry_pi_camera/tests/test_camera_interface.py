def test_one(camera):
    assert "camera" in globals() or "camera" in locals()


"""def test_two(self):
    camera.start_mjpg_streamer()
    assert camera.check_mjpg_streamer()"""

"""def test_three(self):
    camera.stop_mjpg_streamer()
    assert not camera.check_mjpg_streamer()"""

"""def test_four(self):
    fname = camera.record_video()
    assert os.path.isfile(fname)"""


def test_five(camera):
    capture = str(camera)
    assert (
        capture
        == "Video Length: 30, Resolution: (640, 480), Save Location: /home/pi/Videos/, YouTube Livestream Link: https://youtu.be/t48LW4J8b4A, YouTube Playlist Link: https://youtube.com/playlist?list=PLTdMMnsiEwSnKNWdLlAEJNiyHgG02ECXN"
    )


def test_six(camera):
    camera.set_video_length(10)
    assert camera.get_video_length() == 10


def test_seven(camera):
    camera.set_resolution(1)
    assert camera.get_resolution() == "(1296, 730)"


def test_eight(camera):
    camera.set_save_location("/home/pi/Pictures/")
    assert camera.get_save_location() == "/home/pi/Pictures/"
