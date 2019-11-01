#!/bin/bash

if pgrep mjpg_streamer
then
  echo "mjpg_streamer running"
else
  echo "mjpg_streamer not running"
fi