# from gpiozero import MotionSensor
from time import sleep

from picamera import PiCamera

# class to hold everything goes here...

"""Just takes a simple picture. Future iterations
will pass a variable to determine resolution and
return file location."""










def take_picture():
    # set dir '/home/pi/Desktop/image.jpg'
    # filename = "{0:%Y}-{0:%m}-{0:%d}".format(datetime.now)
    filename="test.jpg"
    camera = PiCamera()
    camera.resolution = (1024, 768)
    camera.start_preview()
    # Camera warm-up time
    sleep(2)
    camera.capture(filename)
    camera.stop_preview()


"""Records a h264 formetted video. It will return
the file path in future iterations."""






def record_video(length=10):
    camera = PiCamera()
    camera.resolution=(640,480)
    camera.start_recording("test.h264")
    camera.wait_recording(length)
    camera.stop_recording()


def start_mjpg_streamer():
    pass


def stop_mjpg_streamer():
    pass


def main():
    # take_picture()
    # Test to check if file was made goes here
    sleep(5)
    record_video()
    # Test to check if file was made goes here
main()
