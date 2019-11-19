import logging
import shlex
import subprocess
import time

import RPi.GPIO as GPIO


def togglemute(logger: logging.Logger) -> None:
    """A physical button to toggle mumble client mute and unmute states

    Mumble client unmute when button is pressed and held down (LED light also
    on).
    Mumble client mute when button is released (LED light also off).
    """
    GPIO.setmode(GPIO.BCM)

    # input pin connected to button. Button is pull up, meaning button press
    # sends logic low, while button release high
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # Output pin connected to LED. High leads to LED on, while low off.
    GPIO.setup(12, GPIO.OUT)
    mute: bool = True  # flag

    try:
        while True:
            input_state = GPIO.input(16)
            if input_state:  # input high, button released
                GPIO.output(12, GPIO.LOW)  # turn off LED
                if not mute:
                    subprocess.run(shlex.split("mumble rpc mute"))  # mute
                    mute = True
                    logger.debug("Mumble client MUTE")
            else:  # input low, button pressed
                GPIO.output(12, GPIO.HIGH)  # turn on LED
                if mute:
                    subprocess.run(shlex.split("mumble rpc unmute"))  # unmute
                    mute = False
                    logger.debug("Mumble client UNMUTE")
            time.sleep(0.1)
    except KeyboardInterrupt:
        logger.info("keyboard interruption.")
    finally:
        GPIO.cleanup()
