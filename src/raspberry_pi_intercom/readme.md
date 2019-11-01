# Introduction
This guide is intended for setting up a mumble client on Raspberry Pi 3B+ (Raspbian Buster, kernel-version 4.19), such that the RPi can be used as part of an audio-only intercom system. 

**mumble** is an open source software providing voice over ip (VOIP) service for free. Generally, it works like this: set up a mumble server, set up a few mumble clients, let the clients connect to the mumble server, the clients can talk to each other. For more details, refer to mumble's [official website](https://www.mumble.com/).

If we have two clients set up on two RPi, one outside the door, and the other by your desk, and if both clients are connected to the same mumble client, the two RPis essentially form an audio-only intercom system, where people by the desk and outside the door can verbally communicate with each other.

# Set up Mumble Server
You can refer to [this site](https://wiki.mumble.info/wiki/Hosters) for a wide range of external mumble servers. For a quick and dirty set up of mumble server for limited use or testing purpose, you can choose [GuildBit](https://guildbit.com/) to spin up a temporary server. If long-term or more advanced use of the server is desired, you can either purchase one at very low cost, or set up your own server (aka "murmur") on a device (follow [this guide](https://wiki.mumble.info/wiki/Murmurguide)). For the purpose of this guide, we will be using a temporary server from GuildBit. The following are the parameters returned after I set up a temporary server from GuildBit (note: your parameters will be different when you set up your server)

* server address: sf.guildbit.com
* port: 50008
* passwd: RichBatman

# Set up Mumble Client
The official mumble client (available for download [here](https://www.mumble.com/)) can be downloaded and installed on Raspbian Buster by running this command: `sudo apt-get install mumble`. Upon installation, usage of this GUI mumble client is self-explanatory.

However, since a GUI mumble client is difficult to control from command line, it is not of much use if one wishes to incorporate VOIP via mumble into his app. Therefore, a CLI mumble client is desired. In our implementation, we choose to use [`barnard`](https://github.com/layeh/barnard), an open source CLI mumcle client written in Go, as it has been used in other mumble-related projects for RPi, such as [talkiepi](https://github.com/dchote/talkiepi) and [talkkonnect](https://github.com/talkkonnect/talkkonnect).

## Install `barnard`
The following steps are expansion based on the installation guides provided on `barnard` repo [document](https://github.com/layeh/barnard).
### Install Golang on Raspbian
Run this command for installation

`sudo apt-get install golang`

Afterwards, check Golang version to ensure it has been successfully installed.

`go version`

Set up proper `GOPATH` and `PATH` by opening `~/.profile` and add the following lines to the end:

```
export GOPATH=$HOME/go
export PATH=/usr/local/go/bin:$PATH:$GOPATH/bin
```
Test `go` installation by following [this guide](https://golang.org/doc/install#testing).

### Install `opus` development headers
`sudo apt-get install libopus-dev`

### Install `openAL` development headers
`sudo apt-get install libopenal1 libopenal-dev`

### Fetch and Build `barnard`
`go get -u layeh.com/barnard`

This takes a while and requires decent internet connection as far as I am concerned, so I would recommend patience if nothing seems to be happening for a while after running the command above.

## Connect `barnard` to Mumble Server
The syntax to use `barnard` without using certificate is this:

`barnard -server=<serveraddress:port> -username=<some_name> -password=<some_passwd> -insecure=true`

For example, using the mumble server parameters mentioned earlier, we can connect a CLI mumble client named "rpi-client" to the mumble server with the following command:

`barnard -server=sf.guildbit.com:50008 -username=rpi-client -password=RichBatman -insecure=true`

Once connected, `barnard` draws a CLI client on the console.

## Use `barnard` on The Front
In general, follow the guides on `barnard` repo for the usage of the client. For the use case of audio-only intercom in particular, `barnard` is always listening to the sound transmitted from the server. It, however, by default disables transmitting sound from microphone. To toggle sound transmission from microphone, press `F1`. Press `F10` to turn the client off.

## Use `barnard` in The Background
Running `barnard` on the front is no different from using the official GUI mumble client. Thus, we must run `barnard` in the background to finely control its behavior. To do so, we will leverage `tmux`.

### Install `tmux`
`sudo apt-get install tmux`

### Cheatsheet
Visit [this site](https://tmuxcheatsheet.com/?q=&hPP=100&idx=tmux_cheats&p=0&is_v=1) for a cheatsheet of `tmux`.

### Run `barnard` in its own session
Start a new detached session called `intercom`:

`tmux new -s intercom -d`

Start up `barnard` by sending the command to `intercom` session via key strokes:

`tmux send-keys -t intercom "barnard -server=sf.guildbit.com:50008 -username=rpi-client -password= RichBatman -insecure=true" Enter`

Turn on voice transmission from microphone:

`tmux send-keys -t intercom F1`

Terminate the CLI client:

`tmux send-keys -t intercom F10`

Kill the `intercom` session:

`tmux kill-ses -t intercom`

# Configure Sound Input/Output on RPi
There are two ways to configure sound input and output. One is via USB mic and 3.5 mm AUX headphone (or speaker), the other I2S microphone (mic), amplifier (amp) and speaker cone. I2S sound card provides much better sound quality, though they require more configuration. In addition, I2S mic and amp need a few GPIO pins, some of which are also needed by the touch screen on `rpi_in`. Therefore, we have decided that the I2S sound card will be set up for `rpi_out`, both because `rpi_out` has more GPIO pins available and this set up provides better sound quality for an open environment. For `rpi_in`, we opt for USB mic and 3.5 mm AUX headphone (speaker), due to lack of GPIO pin availability. Both approaches will be discussed below.

## USB Mic and 3.5 mm AUX Headphone (Speaker)
### Before You Start
The following set up sets sound input from a USB microphone and output via 3.5 mm AUX jack. Plug in the USB microphone and a headphone first.

### Check Sound Card for USB Mic
Run command `arecord -l` to see whether the USB microphone is detected by Raspbian. If it is detected, remember the number of its sound card (typically `card 1`)

### Configure sound file
Run command `nano ~/.asoundrc`

Delete whatever content on `.asoundrc` file, if any, copy and paste the following configuration, and save the file:

```
pcm.!default {
    type asym
    playback.pcm {
        type plug
        slave.pcm "output"
    }
    capture.pcm {
        type plug
        slave.pcm "input"
    }
}

pcm.output {
    type hw
    card 0
}

ctl.!default {
    type hw
    card 0
}

pcm.input {
    type hw
    card 1
}
```

### Adjust Volume
Adjust volume of output and input by using `alsamixer` (run command `alsamixer`, use F6 to choose which sound device to modify, F3 to see sound playback volume, F4 to see sound capture volume, up and down arrow to adjust volume for both output and input). Make sure you change the volume for the microphone to 100%, otherwise the recording volume will be very faint.

### Test Headphone 
Test headphone by running the following command. You shall hear white noise.

`speaker-test`

### Test Microphone
Test microphone by running the following command (still assuming microphone is on card 1). You shall hear your own voice played back after you speak into the microphone. Use this test to estimate roughly the usable range of the microphone.

`arecord --device=hw:1,0 --format S16_LE --rate 48000 -c1 | aplay`

If both headphone and microphone tests are good, your sound input/output configuration is successful. Now you can use `barnard` as a complete audio-only mumble client. You can test it by spinning up another client on your laptop, and see whether sounds spoken into the laptop can be received by RPi via the headphone, and whether sounds spoken into the USB mic can be picked up the speaker of the laptop.

## I2S Mic, Amp, and Speaker Cone
### Finished product
![RPi I2S Product](https://raw.githubusercontent.com/FAUSWE-GROUP11/Rokku/master/raspberry-pi-intercom/static/rpi_I2S_product.jpg)


### Prepare the I2S mic and amp
In general, follow [this tutorial](https://learn.adafruit.com/adafruit-i2s-mems-microphone-breakout/overview) to solder I2S mic and wire it to RPi. Similarly, follow [this tutorial](https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/overview) for I2S amp solder and wiring. However, since we are going to configure both the mic and amp, the eventual wiring and configuration are slightly modified (see below for details).

### Wiring diagram
![RPi I2S Wiring](https://raw.githubusercontent.com/FAUSWE-GROUP11/Rokku/master/raspberry-pi-intercom/static/rpi_I2S_wiring.png)

### I2S mic configuration
Follow exactly the procedures laied out [here](https://learn.adafruit.com/adafruit-i2s-mems-microphone-breakout/raspberry-pi-wiring-and-test). No change needed.

### I2S amp configuration
Follow the instructions in "Detailed Install" (i.e. not running the provided script). In step "Create asound.conf file", we will not create `asound.conf` file, because we already have `.asoundrc` file. Make sure it looks exactly the same as the final content of `.asoundrc` shown below.

### `.asoundrc` file content

```
#This section makes a reference to your I2S hardware, adjust the card name
# to what is shown in arecord -l after card x: before the name in []
#You may have to adjust channel count also but stick with default first
pcm.dmic_hw {
    type hw
    card sndrpisimplecar
    channels 2
    format S32_LE
}

#This is the software volume control, it links to the hardware above and after
# saving the .asoundrc file you can type alsamixer, press F6 to select
# your I2S mic then F4 to set the recording volume and arrow up and down
# to adjust the volume
# After adjusting the volume - go for 50 percent at first, you can do
# something like
# arecord -D dmic_sv -c2 -r 48000 -f S32_LE -t wav -V mono -v myfile.wav
pcm.dmic_sv {
    type softvol
    slave.pcm dmic_hw
    control {
        name "Boost Capture Volume"
        card sndrpisimplecar
    }
    min_dB -3.0
    max_dB 30.0
}

pcm.speakerbonnet {
   type hw card 0
}

pcm.dmixer {
   type dmix
   ipc_key 1024
   ipc_perm 0666
   slave {
     pcm "speakerbonnet"
     period_time 0
     period_size 1024
     buffer_size 8192
     rate 44100
     channels 2
   }
}

ctl.dmixer {
    type hw card 0
}

pcm.softvol {
    type softvol
    slave.pcm "dmixer"
    control.name "PCM"
    control.card 0
}

ctl.softvol {
    type hw card 0
}

pcm.!default {
    type        asym
    playback.pcm    "plug:softvol"
    capture.pcm        "plug:dmic_sv"
}

ctl.!default {
    type    hw
    card    0
}
```

### Test amp and speaker cone
`speaker-test`

### Test mic

```
arecord -D dmic_sv -c2 -r 48000 -f S32_LE -t wav -V mono -v recording.wav
aplay recording.wav
```




# Troubleshooting
* If you run into this error during downloading and building `barnard`: `fatal: index file smaller than expected git pull`, reinstalling Raspbian can resolve this problem.
* If you have a USB speaker, identify that it uses sound card 2 (after running `aplay -i`), change the `~/.asoundrc` like this

```
pcm.!default {
    type asym
    playback.pcm {
        type plug
        slave.pcm "output"
    }
    capture.pcm {
        type plug
        slave.pcm "input"
    }
}

pcm.output {
    type hw
    card 2
}

ctl.!default {
    type hw
    card 2
}

pcm.input {
    type hw
    card 1
}
```
and pass the sound output and input tests, you might still have terrible sound output quality issue when running `barnard`. Currently, I have no direct solution for this problem. A workround is to use 3.5 mm AUX speaker instead of USB speaker (i.e. we use the default sound card).
