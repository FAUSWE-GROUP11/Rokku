[![Build Status](https://travis-ci.com/FAUSWE-GROUP11/Rokku.svg?branch=master)](https://travis-ci.com/FAUSWE-GROUP11/Rokku) [![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/) [![Raspberry Pi 3B](https://img.shields.io/badge/raspberrypi-3B+-red)](https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/) ![Contributor Count](https://img.shields.io/github/contributors/FAUSWE-GROUP11/Rokku) ![Last Commit](https://img.shields.io/github/last-commit/FAUSWE-GROUP11/Rokku) ![License](https://img.shields.io/github/license/FAUSWE-GROUP11/Rokku)


# Rokku
## Introduction
`Rokku` is a simple home security system built on two Raspberry Pi (model 3B+ or 4) running Raspbian Buster (kernel version 4.19), along with camera, microphone, speaker, motion sensor, etc. When installed, one of the Raspberry Pi is stationed outside the residence (`rpi_out`), whereas the other inside the house or wherever easily accessible by the user (`rpi_in`). `Rokku` provides a few basic functionalities for home security use case:

* **Motion detection**: `rpi_out` is equipped with PIR motion sensor (see [here](https://learn.adafruit.com/pir-passive-infrared-proximity-motion-sensor/overview) for a brief description of the sensor), which can send alert to `rpi_in` once it is triggered.
* **Livestream**: `rpi_out` is equipped with a Raspberry Pi camera module that allows user to livestream events that are occurring outside the residence.
* **Record video**: The same camera module can also be used to record a short video clip (e.g. 30 seconds long) in case user wants a permanent record of the scene.
* **Intercom**: When both `rpi_in` and `rpi_out` are connected to microphone and speaker/headphone, `Rokku` can serve an intercom system and allow user to verbally communicate with someone outside.
* **Alarm**: `rpi_out` is equipped with a buzzer that allows user to play sharp alarming sound to scare away potential lurker.
* **User Interface**: `rpi_in` runs a simple user interface with various buttons to control `Rokku`, such as initiating the functionalities mentioned above, turning `Rokku` on or off, etc.

## System Architecture
`rpi_in_driver.py` and `rpi_out_driver.py` are the entry points for `rpi_in` and `rpi_out`, respectively. They both rely on the various components in the `src` directory:

* **`src/pi_to_pi`**: Communication between `rpi_in` and `rpi_out`. The service used is MQTT broker, hosted freely by [mosqitto](test.mosquitto.org), and realized by Python [paho-mqtt]((https://pypi.org/project/paho-mqtt/)) package.
* **`src/raspberry_pi_alarm`**: Buzzer interface to send alarming.
* **`src/raspberry_pi_camera`**: Camera interface for livestream and record. Youtube API v3 is used for livestream (each frame recorded by the camera is uploaded to Youtube immediately for livestream), and uploading a recorded video to a pre-configured Youtube playlist to permanently keep the video.
* **`src/raspberry_pi_driver`**: This component contains utility functions for both `rpi_in` and `rpi_out` drivers. Furthermore, it includes various behavior logics such that `rpi_out` can react properly according to user's intention, such as sending alarm, record a video, start livestream, etc.
* **`src/raspberry_pi_intercom`**: This component contains heavy documentation about how to set up intercom between the two Raspberry Pis using a free VoIP service called Mumble, freely hosted by [CleanVoice](https://cleanvoice.ru/free/mumble/en.html). The documentation also contains helpful information regarding the set up of microphone and speaker on Raspberry Pi. 
* **`src/raspberry_pi_motion_sensor`**: Motion sensor interface to properly detect a true motion and send out a trigger.
* **`src/raspberry_pi_ui`**: Component for user interface, relying on `Gtk` library for processing button clicks and `glade` framework to draw out the UI. 

When both `rpi_in` and `rpi_out` drivers are initiated, the two Raspberry Pis will share two MQTT channels, one for `rpi_in` to send messages to `rpi_out`, and the other `rpi_out` to `rpi_in`. `rpi_in` starts the UI, through which user can send commands to `rpi_out` via button click. Meanwhile, `rpi_out` is actively waiting for commands to arrive so that it can react accordingly. For a general example of how the two Raspberry Pis coordinate actions, we can take a closer look at how the intercom system works. After user presses the button to initiate intercom from `rpi_in`, `rpi_in` spins up its own Mumble client and sends a command (a json-encoded message) via the "in-to-out" MQTT channel to `rpi_out`. `rpi_out`, upon receiving the command, turns on its own Mumble client. It then sends a message back to `rpi_in` via the "out-to-in" MQTT channel, reporting whether the Mumble client has been successfully started. After `rpi_in` receives this report, based on whether Mumble clients have been successfully started on both ends, `rpi_in` will indicate user to start using the intercom service or display error message. This work flow applies to most of the other functionalities that require communication between the two Raspberry Pis.

## Usage
### Clone This Repo
`git clone https://github.com/FAUSWE-GROUP11/Rokku.git`

### System Dependencies
```
sudo apt-get install -y libcairo2-dev \
libgirepository1.0-dev \
gir1.2-gtk-3.0 \
gir1.2-webkit-3.0
```
### Python Dependencies
If `Rokku` is to be run directly on top of Raspbian (**NOT recommended**), all Python dependencies are in `requirements.txt`. Simply install the packages in that file and the system should be good to go.

However, we **recommend** using a virtual environment to run `Rokku`. Refer to [this doc](https://docs.python.org/3.7/tutorial/venv.html) about how (and why) to create a virtual environment using Python's `venv` command.

Once virtual environment is created for the `Rokku` directory and activated, run the following commands. Note that although `picamera` and `RPI.GPIO` are available in Raspbian as system-site package, they are not included in a virtual environment. If you don't want to install them separately, you can use `--system-site-packages` option to include system-site package upon creating the virtual environment.

```
pip3 install -r requirements.txt
pip3 install picamera RPi.GPIO
```

### Check Hardware
As described earlier, `Rokku`uses quite a few hardware components. In order to enjoy full functionalities of `Rokku`, we recommend you check whether you have all hardware set up. By "set up", we mean the hardware has been connected to the appropriate PINs (see below) on the Raspberry Pi and individually tested for usability. Below is a checklist for core hardware.

* Motion sensor: [example](https://www.adafruit.com/product/189). Connect to **GPIO23** on `rpi_out`.
* Motion sensor LED: [example](https://www.adafruit.com/product/4204). Connect to **GPIO12** on `rpi_out`.
* Buzzer: [example](https://www.amazon.com/ARCELI-3-3-5V-Passive-Trigger-Arduino/dp/B07MPYWVGD/ref=sr_1_3?keywords=buzzer+module&qid=1574466115&s=electronics&sr=1-3). Connect to **GPIO6** on `rpi_out`.
* Microphone and Speaker: Refer to [intercom doc](https://github.com/FAUSWE-GROUP11/Rokku/blob/master/src/raspberry_pi_intercom/readme.md). Set this up for both `rpi_in` and `rpi_out`
* Intercom mute toggle button: [example](https://www.adafruit.com/product/367). Connect to **GPIO16** on `rpi_out`.
* Intercom unmute indicator LED: [example](https://www.adafruit.com/product/4204). Connect to **GPIO26** on `rpi_out`.
* Camera: [example](https://www.raspberrypi.org/products/camera-module-v2/). Connect to the camera slot on `rpi_out`.
* Screen (optional): [example](https://www.amazon.com/kuman-inch-Resistive-Touch-Screen/dp/B07L9XM11M/ref=pd_sbs_147_7?_encoding=UTF8&pd_rd_i=B07L9XM11M&pd_rd_r=b326fe07-408c-4590-801f-c26b6a4b1e66&pd_rd_w=5uwNZ&pd_rd_wg=lv3I7&pf_rd_p=5873ae95-9063-4a23-9b7e-eafa738c2269&pf_rd_r=HT66W6YNJYG7ZD3WYQP2&psc=1&refRID=HT66W6YNJYG7ZD3WYQP2). Connec to `rpi_in`. A portable screen is not necessary if `rpi_in` is connected to a monitor or VNC viewer.

### Set up Youtube Account for Livestream and Playlist
(To be completed...)

### Run Driver
With virtual environment activated:

For `rpi_in`: `python3 rpi_in_driver.py -p <unique_string>`

For `rpi_out`: `python3 rpi_out_driver.py -p <unique_string>`

The `<unique_string>` is used as a prefix for the MQTT channel where the two Raspebrry Pis will be communicating. It can be any string, but for security reasons, it should be sufficiently unique to the user. This string MUST be the same for both `rpi_in` and `rpi_out`.

Once both drivers are actively running, user can use `Rokku` via the UI on `rpi_in`.


## Security
### Livestream and Video Upload
Both livestream and video upload must be authenticated by Google via oauth2. The youtube account should also be set up private and youtube playlist set to "unlisted" to ensure no third party can get access to the footage.

### MQTT Broker
Since the server used for MQTT is free to the public (test.mosquitto.org), security is built into the channel name such that it is almost impossible for any third party to eavesdrop on the communication between the two Raspberry Pis. User is **strongly recommended** to change the `SALT` value in the `hash_prefix` function in `src/raspberry_pi_driver/utility.py` before using `Rokku`. The `SALT` value should be a random string. Once changed, it can remain as is, unless it is exposed to a third party. 

Upon starting the driver, user must provide a string to generate a prefix for the MQTT channel (along with the `SALT`). This string does not have to be random, but should be sufficiently unique to the user.

With both a sufficiently unique string and a never-exposed random `SALT`, we can generate a very secure channel name.

### Mumble
In order to prevent third party from eavesdropping on the intercom conversation, user is **strongly recommended** to set up access-control list (ACL) on a specific `Rokku` channel for ONLY `rpi_in` and `rpi_out`. This way, no other party is able to join the `Rokku` channel. Please refer to the [intercom doc on mumble](https://github.com/FAUSWE-GROUP11/Rokku/blob/master/src/raspberry_pi_intercom/readme.md#benefits-of-mumble) for how to set up ACL for a specific Mumble channel.


## Known Issues
### `numpy` Failure
During installation of `numpy` on Raspberry Pi, if problems such as "Importing the numpy c-extensions failed" occurs, install this dependency `sudo apt-get install libatlas-base-dev` and try again. 

## To Do
* Avoid hardcoding Youtube URLs in camera interface.