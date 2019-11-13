import RPi.GPIO as GPIO
from time import sleep

class Buzzer:
    """Buzzer is a class providing definitions to interact with a buzzer module connected through the RPi pins."""

    def __init__(self, channel):
        self.state = False
        GPIO.setup(channel, GPIO.OUT, initial=GPIO.HIGH)

    def get_state(self) -> bool:
        if self.state is True:
            return True
        else:
            return False

    def sound(self):
        self.state = True
        GPIO.output(channel, GPIO.HIGH)

    def scilence(self):
        self.state = False
        GPIO.output(channel, GPIO.LOW)
        





