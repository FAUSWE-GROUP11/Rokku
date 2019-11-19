#!/bin/bash

main() {
  if [[ $NAME == "" ]]; then
    echo "ERROR: Please specify your mumble client user name."
    print_usage
    exit 1
  fi
  if [[ $HOST == "" ]]; then
    echo "ERROR: Please specify your mumble server host address."
    print_usage
    exit 1
  fi
  if [[ $PORT == "" ]]; then
    echo "ERROR: Please specify your mumble server port value."
    print_usage
    exit 1
  fi
  if [[ $CHANNEL == "" ]]; then
    echo "ERROR: Please specify the mumble channel you want to connect to."
    print_usage
    exit 1
  fi

  tmux new -s intercom -d
  tmux send-keys -t intercom "mumble mumble://$NAME@$HOST:$PORT/$CHANNEL" Enter
  sleep 5
  xdotool search "Mumble" windowminimize --sync %@
  echo $(ps -ef | grep -c mumble)
}


# DEFAULTS
NAME=""
HOST=""
PORT=""
CHANNEL=""


print_usage() {
  printf "%s\n" "Usage: start_mumble.sh [-n name] [-h host] [-p port] [-c channel]"
  printf "%s\t\t%s\n" "-n" "Name of to display on mumble client. Required" \
    "-h" "Mumble server host address. Required." \
    "-p" "Mumble server port number. Required" \
    "-c" "Channel to connect to. Required."
}


# Parse options and flags
while [[ "$#" -gt 0 ]]; do
  case "$1" in
    -n)  # mumble client name
      if [[ "$2" != "" ]]; then
        NAME="$2"
        shift 1
      else # -n must be followed by a second argument
        print_usage
        exit 1
      fi
      shift 1
      ;;
    -h)  # mumble server host address
      if [[ "$2" != "" ]]; then
        HOST="$2"
        shift 1
      else # -h must be followed by a second argument
        print_usage
        exit 1
      fi
      shift 1
      ;;
    -p)  # mumble server port number
      if [[ "$2" =~ ^[0-9]+$ ]]; then
        PORT="$2"
        shift 1
      else # -p must be followed by a valid numeric value
        print_usage
        exit 1
      fi
      shift 1
      ;;
    -c)  # channel to connect to
      if [[ "$2" != "" ]]; then
        CHANNEL="$2"
        shift 1
      else # -c must be followed by a valid numeric value
        print_usage
        exit 1
      fi
      shift 1
      ;;
    *) # unsupported flags
      print_usage
      exit 1
      ;;
  esac
done

main