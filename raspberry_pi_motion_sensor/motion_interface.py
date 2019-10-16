import RPi.GPIO as GPIO


class MotionPir:
    """Class implemented to interact with a PIR motion sensor.

    Object will act as a 'mini-alarm system' where it can be 'armed' and 'disarmed'.
    Functions set_armed() and set_disarmed() should be used to modify object and motion_callback() will allow
    for object to communicate to other objects.
    when armed.
    """

    def __init__(self):
        """ When MotionPir is created it will be inactive, self.armed set to false"""

        self.armed = False

    def motion_callback(self, channel):
        """channel argument is for receiving GPIO input.

        Function runs on different thread than main.
        When object is 'armed' / True, this function will be called anytime the Pir sensor is activated.
        """

        # Here, alternatively, an application / command can be started
        print("Movement Detected")

    def set_armed(self):
        """Sets Object state to True 'armed' and calls monitor() to initialize GPIO input"""

        self.armed = True
        self.monitor()

    def set_disarmed(self):
        """Sets Object state to False 'disarmed' and calls stop_monitor() to stop event detection"""

        self.armed = False
        self.stop_monitor()

    def show_state(self):
        """Prints the state of armed / 'alarm system' """

        if self.armed:
            print("System Armed")
        else:
            print("System Disarmed")

    def monitor(self):
        """GPIO is set up to manage callback on second thread to run motion_callback() in response to a rising edge"""

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(23, GPIO.IN)
        GPIO.add_event_detect(23, GPIO.RISING, callback=self.motion_callback)

    def stop_monitor(self):
        """Will stop callbacks from motion_pir"""

        GPIO.remove_event_detect(23)


# TODO - make functions to set up GPIO pin settings and possibly initialize within __init__
