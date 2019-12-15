# raspberry-pi-camera-interface
This takes Pi Camera functionility and wraps them in premade class functions. 

## Before you start
Make sure you download all the requirements from requirements.txt, and have a camera hooked up to your pi. 

Also, be sure to look through the code to understand the class and its methods.

Install the Google APIs Client Library for Python (google-api-python-client) if you haven't already.

You're going to have to register a YouTube account to use with this project at https://developers.google.com/youtube/registering_an_application

Make sure you get a an api that supports OAuth 2.0 and has youtube as the scope. The youtube scope allows uploading of videos and insertion of videos into a playlist.

After you get all the credentials for the registered application you're gonna have to comb through the camera src folder and replace things. (e.g. playlist urls, client_secrets.json, start_livestream.sh, playlist id in upload_video.py etc.)

Make sure you signed into your YouTube account and have setup a current livestream as well.

Delete upload_video.py-oauth2.json, so it gets regenerated with the right info from client_secrets.json.

Also, when you first run the application make sure your browser can be opened as Google will ask if our application can have access to your YouTube account.

Everything should just work know, if not check the links below.

### Helpful Links
https://developers.google.com/youtube/v3/guides/uploading_a_video
https://developers.google.com/youtube/v3/docs/playlistItems/insert
https://developers.google.com/youtube/registering_an_application
https://developers.google.com/youtube/v3/docs/videos/insert#auth
https://github.com/googleapis/google-api-python-client
https://github.com/alokmahor/add_to_youtube_playlist/blob/master/playlist.py
https://developers.google.com/youtube/v3/docs/videos/insert#auth

### Installing mjpg-streamer (Optional)
The functionaility was not used in the final build because it could only be used on a local connection. 
However it is here if you want it. 

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

