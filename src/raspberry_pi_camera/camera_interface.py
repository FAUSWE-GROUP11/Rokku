import datetime
import socket
import subprocess
from time import sleep

from picamera import PiCamera

"""class to hold everything goes here..."""


class CameraInterface(object):
    """Constructor takes the length of the videos in seconds (int/float),
    resolution mode (int), and the save location in a string. I recommend
    using resolution mode 2 or 1 as 0 puts strain on the cameraand reduces
    FPS considerbly."""

    def __init__(
        self,
        video_length=30,
        resolution=2,
        save_location="/home/pi/Videos/",
        yt_livestream_link="https://youtu.be/t48LW4J8b4A",
        yt_playlist_link="https://www.youtube.com/playlist?list=PLTdMMnsiEwSnKNWdLlAEJNiyHgG02ECXN",
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
        if isinstance(yt_livestream_link, str):
            self.yt_livestream_link = yt_livestream_link
        else:
            # __name__ refers to the caller (main)
            raise ValueError(
                __name__ + " ERROR: save_location argument is invalid."
            )
        if isinstance(yt_playlist_link, str):
            self.yt_playlist_link = yt_playlist_link
        else:
            # __name__ refers to the caller (main)
            raise ValueError(
                __name__ + " ERROR: save_location argument is invalid."
            )

        self.modes = [(1920, 1080), (1296, 730), (640, 480)]
        self.last_recording = ""

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
        self.last_recording = (
            datetime.datetime.now().strftime("%I:%M:%S%p on %B %d, %Y")
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
        # print("View the stream at http://<your-raspberry-pi-ip-address>:9000/" +
        # "?action=stream or http://127.0.0.1:9000/?action=stream")

        # Catches and prints all the output from the shell script
        output = str(temp.communicate())
        output = output.split("\\n")
        for i in range(1, len(output) - 1, 1):
            print(output[i])

        return "http://" + socket.gethostname() + ":9000/?action=stream"

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

    """This returns a boolean after checking if mjpg_streamer is running."""

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

    """This function returns void and starts a livestream from a
    predetermined youtube channel. Handled by raspivid in a shell
    script."""

    def start_yt_stream(self, key):
        # String of start stream shell script
        cmd = (
            "raspivid -o - -t 0 -vf -hf -fps 24 -w 640 -h 480 -b 5000000 | ffmpeg -re -ar 44100 -ac 2 -acodec pcm_s16le -f s16le -ac 2 -i /dev/zero -f h264 -i - -vcodec copy -acodec aac -ab 128k -g 50 -strict experimental -f flv rtmp://a.rtmp.youtube.com/live2/"
            + key
        )

        # Object to start and capture the shell command
        temp = subprocess.Popen(["bash", "-c", cmd], stdout=subprocess.PIPE)

        # Catches and prints all the output from the shell script
        output = str(temp.communicate())
        output = output.split("\\n")
        for i in range(1, len(output) - 1, 1):
            print(output[i])

        return self.yt_livestream_link

    """This function returns void and turns off the youtube livestream
    being hosted at a predetermined youtube channel.Handled by raspivid \
    in a shell script."""

    def stop_yt_stream(self):
        # String of start stream shell script
        cmd = "pkill raspivid"

        # Object to start and capture the shell command
        temp = subprocess.Popen(["bash", "-c", cmd], stdout=subprocess.PIPE)

        # Catches and prints all the output from the shell script
        output = str(temp.communicate())
        output = output.split("\\n")
        for i in range(1, len(output) - 1, 1):
            print(output[i])

    """This function returns void and sends a command line instruction to
    upload a video from the given filepath."""

    def upload_to_yt(self, filepath):
        # Making the command line script
        cmd = (
            'python upload_video.py --file="'
            + filepath
            + '"'
            + ' --title="Date: '
            + self.last_recording
            + '"'
            + ' --description="A recording from raspi_out."'
            + ' --keywords="school,technology"'
            + ' --category="22"'
            + ' --privacyStatus="unlisted"'
        )

        # Passing the command to the shell
        temp = subprocess.Popen(["bash", "-c", cmd], stdout=subprocess.PIPE)

        # Catches and prints all the output from the shell script
        output = str(temp.communicate())
        output = output.split("\\n")
        for i in range(1, len(output) - 1, 1):
            print(output[i])

    # Getters and setters
    """Returns int of the object's video length."""

    def get_video_length(self):
        return self.video_length

    """Returns a tuple of the object's current resolution."""

    def get_resolution(self):
        return str(self.modes[self.resolution])

    """Returns a string of the object's save location."""

    def get_save_location(self):
        return self.save_location

    """Returns a string of the object's YouTube livestream link"""

    def get_yt_livestream_link(self):
        return self.yt_livestream_link

    """Returns a string of the object's YouTube playlist link"""

    def get_yt_playlist_link(self):
        return self.yt_playlist_link

    """Returns void, and accepts an integer to replace the object's
    video length in seconds."""

    def set_video_length(self, value):
        self.video_length = value

    """Returns void, and accepts an integer (0, 1, 2) to change the
    object's resolution"""

    def set_resolution(self, value):
        self.resolution = value

    """Returns void, and accepts a string to replace the object's
    save location."""

    def set_save_location(self, value):
        self.save_location = value

    """Returns void, and accepts a string to replace the object's
    YouTube livestream link."""

    def set_yt_livestream_link(self, value):
        self.yt_livestream_link = value

    """Returns void, and accepts a string to replace the object's
    YouTube playlist link."""

    def set_yt_playlist_link(self, value):
        self.yt_playlist_link = value

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
            + ", YouTube Livestream Link: "
            + str(self.yt_livestream_link)
            + ", YouTube Playlist Link: "
            + str(self.yt_playlist_link)
        )
