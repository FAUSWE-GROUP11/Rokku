# raspberry-pi-camera-interface
This takes Pi Camera functionility and wraps them in premade class functions. It also utilizes mjpg-streamer to stream live video from the Raspberry Pi to an IP address.

## Before you start
Make sure you download all the requirements from requirements.txt, have a camera hooked up to your pi and install mjpg-streamer to your pi. 

Also, be sure to look through the code to understand the class and its methods.

Once you start mjpg-streamer the link will be at http://<your-raspberry-pi-ip-address>:9000/

### Installing mjpg-streamer
```
# Install dev version of libjpeg
sudo apt-get install libjpeg62-dev

# Install cmake
sudo apt-get install cmake

# Download mjpg-streamer with raspicam plugin
git clone https://github.com/jacksonliam/mjpg-streamer.git ~/mjpg-streamer

# Change directory
cd ~/mjpg-streamer/mjpg-streamer-experimental

# Compile
make clean all

# Replace old mjpg-streamer
sudo rm -rf /opt/mjpg-streamer
sudo mv ~/mjpg-streamer/mjpg-streamer-experimental /opt/mjpg-streamer
sudo rm -rf ~/mjpg-streamer

```

