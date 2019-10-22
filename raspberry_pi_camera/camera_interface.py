from picamera import PiCamera
import datetime
import subprocess
from time import sleep

"""class to hold everything goes here..."""


class CameraInterface(object):
    """Constructor takes the length of the videos in seconds (int/float),
    resolution mode (int), and the save location in a string. I recommend
    using resolution mode 2 or 1 as 0 puts strain on the cameraand reduces
    FPS considerbly."""

    def __init__(
        self, video_length=30, resolution=2, save_location="/home/pi/Videos/"
    ):

        if isinstance(video_length, float) or isinstance(video_length, int):
            self.video_length = video_length
        else:
            # __name__ refers to the caller (main)
            raise ValueError(
                __name__ + " ERROR: video_length argument is invalid."
            )

        if isinstance(resolution, int):
            self.resolution = resolution
        else:
            # __name__ refers to the caller (main)
            raise ValueError(
                __name__ + " ERROR: resolution argument is invalid."
            )

        if isinstance(save_location, str):
            self.save_location = save_location
        else:
            # __name__ refers to the caller (main)
            raise ValueError(
                __name__ + " ERROR: save_location argument is invalid."
            )

        self.modes = [(1920, 1080), (1296, 730), (640, 480)]

    """Just takes a simple picture. Future iterations will pass a
    variable to determine resolution and return file location.
    Since the project doesn't really need it I recommend not using
    it or using it seperate from other functions as it causes resource
    issues."""

    def take_picture(self):
        # filename = "{0:%Y}-{0:%m}-{0:%d}".format(datetime.now)
        filename = (
            self.save_location
            + datetime.datetime.now().strftime("%I:%M:%S%p on %B %d, %Y")
            + ".jpg"
        )
        camera = PiCamera()
        camera.resolution = self.modes[self.resolution]
        camera.start_preview()
        # Camera warm-up time
        sleep(2)
        camera.capture(filename)
        camera.stop_preview()
        return filename

    """Records a h264 formetted video. It will return the file
    path in future iterations."""

    def record_video(self):
        filename = (
            self.save_location
            + datetime.datetime.now().strftime("%I:%M:%S%p on %B %d, %Y")
            + ".h264"
        )
        camera = PiCamera()
        camera.resolution = self.modes[self.resolution]
        camera.start_recording(filename)
        camera.wait_recording(self.video_length)
        camera.stop_recording()
        return filename

    """This starts the mjpg streamer program using a shell script.
    https://www.geeksforgeeks.org/python-execute-and-parse-linux-commands/"""

    def start_mjpg_streamer(self):
        # String of start stream shell script
        cmd = "./start_stream.sh"

        # Object to start and capture the shell command
        temp = subprocess.Popen([cmd], stdout=subprocess.PIPE)

        # Where the IP stream is
        print(
            "View the stream at http://<your-raspberry-pi-ip-address>:9000/"
            + "?action=stream or http://127.0.0.1:9000/?action=stream"
        )

        # Catches and prints all the output from the shell script
        output = str(temp.communicate())
        output = output.split("\\n")
        for i in range(1, len(output) - 1, 1):
            print(output[i])

    """This stops the mjpg streamer program using a shell script.
    https://www.geeksforgeeks.org/python-execute-and-parse-linux-commands/"""

    def stop_mjpg_streamer(self):
        # String of start stream shell script
        cmd = "./stop_stream.sh"

        # Object to start and capture the shell command
        temp = subprocess.Popen([cmd], stdout=subprocess.PIPE)

        # The stream should be stopped; the link to make sure
        # print("mjpg_streamer was stopped")

        # Catches and prints all the output from the shell script
        output = str(temp.communicate())
        output = output.split("\\n")
        for i in range(1, len(output) - 1, 1):
            print(output[i])

    def check_mjpg_streamer(self):
        # Used for return
        catch = False

        # String of start stream shell script
        cmd = "./check_stream.sh"

        # Object to start and capture the shell command
        temp = subprocess.Popen([cmd], stdout=subprocess.PIPE)

        # The stream should be stopped; the link to make sure
        # print("mjpg_streamer was stopped")

        # Catches and prints all the output from the shell script
        output = str(temp.communicate())
        output = output.split("\\n")
        for i in range(1, len(output) - 1, 1):
            if output[i] == "mjpg_streamer running":
                catch = True

        return catch

    # Getters and setters
    def get_video_length(self):
        return self.video_length

    def get_resolution(self):
        return str(self.modes[self.resolution])

    def get_save_location(self):
        return self.save_location

    def set_video_length(self, value):
        self.video_length = value

    def set_resolution(self, value):
        self.resolution = value

    def set_save_location(self, value):
        self.save_location = value

    # "Private" classes go here
    """Returns string representation of camera_interface"""

    def __str__(self):
        return str(
            "Video Length: "
            + str(self.video_length)
            + ", Resolution: "
            + str(self.modes[self.resolution])
            + ", Save Location: "
            + str(self.save_location)
        )
