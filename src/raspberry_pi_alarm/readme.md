# Buzzer Module

----

## Installation/Setup

Additional software is not needed to use a buzzer module on the Raspberry Pi 4B. The module itself will use 3 wires for:

1. GND: Ground
2. VCC: 3.3-5V DC
3. I/O: Low level input

The VCC should be set to a pin that always outputs 3.3V. Ground should go to ground. I/O should go to a pin that has a pull up of 3.3V on start up. All pins on the RPI will be set as inputs on startup but when the alarm is initialized the pin will be set as an output on high. Also, in between I/O from the buzzer and the output pin on the RPI, a 4k7 resistor should be used on a breadboard.

<img src="https://github.com/CurtisWoodworth/Rokku/blob/CurtisWoodworth/AlarmReadme/src/raspberry_pi_alarm/images/Resistor.jpg" width="500">

The buzzer module for this project is uses a low-trigger to play sound from the buzzer. An issue came up where the buzzer would sound on startup and continue sounding until a high signal was sent to the I/O of the buzzer. When the Pi boots, some of the GPIO pins have a pull-down to 0V while others pull-up to 3.3V. For more information on the RPI pin states while using your pi, enter `GPIO readall` in the terminal and it will print a list of pins and their states. If the output is an error you may need an update from *WiringPi* ([wiringpi.com](http://wiringpi.com/wiringpi-updated-to-2-52-for-the-raspberry-pi-4b/)).

For more informaiton regarding this solution, please visit this raspberry pi stack exchange fourm:
 [Active Piezo Buzzer Makes Sound On Both Rpi GPIO Low and High Level Signal](https://raspberrypi.stackexchange.com/questions/97980/active-piezo-buzzer-makes-sound-on-both-rpi-gpio-low-and-high-level-signal)
