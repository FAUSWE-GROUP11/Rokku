# Introduction
This guide is intended for setting up a mumble client on Raspberry Pi 3B+ (Raspbian Buster, kernel-version 4.19), such that the RPi can be used as part of an audio-only intercom system. 

**mumble** is an open source software providing voice over ip (VOIP) service for free. Generally, it works like this: set up a mumble server, set up a few mumble clients, let the clients connect to the mumble server, the clients can talk to each other. For more details, refer to mumble's [official website](https://www.mumble.com/).

If we have two clients set up on two RPi, one outside the door, and the other by your desk, and if both clients are connected to the same mumble client, the two RPis essentially form an audio-only intercom system, where people by the desk and outside the door can verbally communicate with each other.

# Set up Mumble Server
## Recommended
You can refer to [this site](https://wiki.mumble.info/wiki/Hosters) for a wide range of external mumble servers. We recommend that you apply for a server via [Free Mumble Server](https://cleanvoice.ru/free/mumble/en.html) by providing your email address. This server is persistent and free forever. Although there is no guarantee that the server will always work, it does grant you SuperUser permission, which allows you to set up channel, create groups, add and drop registered users, and configure access-control list (ACL) for the channel.

## Alternative
For a quick and dirty set up of mumble server for limited use or testing purpose, you can choose [GuildBit](https://guildbit.com/) to spin up a temporary server. However, being temporary, GuildBit server won't allow you to configure channel or users. Another long-term and advanced use case option is to set up your own server (aka "murmur") on a device (follow [this guide](https://wiki.mumble.info/wiki/Murmurguide))


# Set up Mumble Client
## Recommended: `mumble`
`mumble` is the official mumble client (available for download [here](https://www.mumble.com/)). For Raspbian Buster, it can also be installed via `sudo apt-get install mumble`. Upon installation, use the following command to connect to a channel on a mumble server:
```
mumble mumble://[client_name]@[server_address]:[port]/[channel]
```
If it is the first time `mumble` is used, a configuration wizard will appear to guide you through audio input/output and other setup. Once this wizard step is done, any future use of the `mumble` command will only open up the client interface while automatically connecting to the server.

### Command line control of `mumble`
Since `mumble` spins up a UI interface, it is not native to be controlled directly from command line. But with the help of the following tools, one can open, close, minimize, and togglemute the mumble client completely via command line.

* Prerequisite: `tmux`. `tmux` allows one to run any commands in a detached shell session such that the logic in the main shell will not be affected. For example, if the device is actively running Rokku UI interface, we can use `tmux` to open `mumble` in a separate shell session such that the main Rokku UI will continue to function normally. To install, use command `sudo apt-get install tmux`. Here is a [cheatsheet of `tmux` command](https://tmuxcheatsheet.com/?q=&hPP=100&idx=tmux_cheats&p=0&is_v=1)
* Use `tmux` to open `mumble` (replace `client_name`, `server_address`, `port`, and `channel` with appropriate values)

```bash
tmux new -s intercom -d
tmux send-keys "mumble mumble://[client_name]@[server_address]:[port]/[channel]" Enter
```
* Use `tmux` to close `mumble`: `tmux kill-sess -t intercom`
* Minimize `mumble` UI window: since opening `mumble` always ends up with its UI window being on top of everything else, it is necessary to minimize its window such that it won't interfere with other UI, such as Rokku UI. [`xdotool`](http://manpages.ubuntu.com/manpages/trusty/man1/xdotool.1.html) is a good way to achieve this goal. You can install it via `sudo apt-get install xdotool`, and minimize `mumble` UI window via `xdotool search "Mumble" windowminimize --sync %@`


### Benefits of `mumble`
1. If you have SuperUser privilege on the mumble server, you can easily set up channel and configure which user can have access to a certain channel using `mumble` client. For details, please refer to this [tutorial video](https://www.youtube.com/watch?v=VOeMsMjQRoM). When a channel is configured such that only `rpi_in` and `rpi_out` are allowed to enter, we can essentially guarantee that no third party can eavesdrop the content of intercom conversation.
2. User registration. `mumble` client allows regular user to register, which enables the user to get access to certain channels, if appropriate ACL has been configured prior. To ensure intercom security (as described in point one), user registration is a must.
3. No password protection needed. If SuperUser has properly configured a channel such that only authorized registered user can enter, there is no need to use password for mumble server connection.
4. Easy installation.

### Downsides for `mumble`
1. `mumble` requires an interface UI. That means it wouldn't work via SSH


## Alternative: `barnard`
[`barnard`](https://github.com/layeh/barnard), an open source CLI mumcle client written in Go. It has been used in other mumble-related projects for RPi, such as [talkiepi](https://github.com/dchote/talkiepi) and [talkkonnect](https://github.com/talkkonnect/talkkonnect). Being a CLI client, `barnard` is easy to control via command line

### Install `barnard`
The following steps are expansion based on the installation guides provided on `barnard` repo [document](https://github.com/layeh/barnard).
#### Install Golang on Raspbian
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

#### Install `opus` development headers
`sudo apt-get install libopus-dev`

#### Install `openAL` development headers
`sudo apt-get install libopenal1 libopenal-dev`

#### Fetch and Build `barnard`
`go get -u layeh.com/barnard`

This takes a while and requires decent internet connection as far as I am concerned, so I would recommend patience if nothing seems to be happening for a while after running the command above.

### Connect `barnard` to Mumble Server
The syntax to use `barnard` without using certificate is this:

`barnard -server=<serveraddress:port> -username=<some_name> -password=<some_passwd> -insecure=true`

For example, using the mumble server parameters mentioned earlier, we can connect a CLI mumble client named "rpi-client" to the mumble server with the following command:

`barnard -server=sf.guildbit.com:50008 -username=rpi-client -password=RichBatman -insecure=true`

Once connected, `barnard` draws a CLI client on the console.

### Use `barnard` on The Front
In general, follow the guides on `barnard` repo for the usage of the client. For the use case of audio-only intercom in particular, `barnard` is always listening to the sound transmitted from the server. It, however, by default disables transmitting sound from microphone. To toggle sound transmission from microphone, press `F1`. Press `F10` to turn the client off.

### Use `barnard` in The Background
Use `tmux`.

```bash
tmux new -s intercom -d
tmux send-keys -t intercom "barnard -server=sf.guildbit.com:50008 -username=rpi-client -password= RichBatman -insecure=true" Enter
# Turn on voice transmission from microphone:
tmux send-keys -t intercom F1

# using barnard...

# Terminate the CLI client:
tmux send-keys -t intercom F10
tmux kill-ses -t intercom
```

### Issues
`barnard` works pretty well at the beginning of this project, but for reasons unbeknown to us, it stops working later when the RPi is connected via SSH or VNC. To be specific, if `barnard` is initiated when the RPi is connected via SSH or VNC, the RPi connection would drop. After connection is dropped, `barnard` seems to be able to still connect to mumbler server, but it would only last for a few seconds before it disconnects from the server. This strange behavior exists even if `barnard` is initiated without SSH or VNC connection to the RPi (schedule a job on the RPi to turn on `barnard` without the RPi connecting to any other devices, yet it still fails). We suspect the problem could be related to unstable internet connection, but currently we have no proof. We would like to test whether this issue of `barnard` can be replicated if the RPi is controlled directly via keyboard and display. Any update on this issue will be documented below.


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
![RPi I2S Product](https://github.com/FAUSWE-GROUP11/Rokku/blob/master/src/raspberry_pi_intercom/static/rpi_I2S_product.jpg)


### Prepare the I2S mic and amp
In general, follow [this tutorial](https://learn.adafruit.com/adafruit-i2s-mems-microphone-breakout/overview) to solder I2S mic and wire it to RPi. Similarly, follow [this tutorial](https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/overview) for I2S amp solder and wiring. However, since we are going to configure both the mic and amp, the eventual wiring and configuration are slightly modified (see below for details).

### Wiring diagram
![RPi I2S Wiring](https://github.com/FAUSWE-GROUP11/Rokku/blob/master/src/raspberry_pi_intercom/static/rpi_I2S_wiring.png)

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
* If you have a USB speaker, identify that it uses sound card 2 (after running `aplay -l`), change the `~/.asoundrc` like this

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
