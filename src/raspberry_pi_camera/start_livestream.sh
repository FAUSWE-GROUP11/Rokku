#!/bin/bash

tmux new -s livestream -d
tmux send-keys -t livestream "raspivid -o - -t 0 -vf -hf -fps 24 -w 640 -h 480 -b 5000000 | ffmpeg -re -ar 44100 -ac 2 -acodec pcm_s16le -f s16le -ac 2 -i /dev/zero -f h264 -i - -vcodec copy -acodec aac -ab 128k -g 50 -strict experimental -f flv rtmp://a.rtmp.youtube.com/live2/6a8u-vpvr-er4h-e22h" Enter
